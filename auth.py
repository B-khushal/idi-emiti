"""
Authentication module for Cultural Corpus Collection Platform
Handles user registration, login, session management, and profile operations
"""

import streamlit as st
import secrets
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
from pathlib import Path
from config import DATA_FOLDER

# User data file
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
SESSIONS_FILE = os.path.join(DATA_FOLDER, "sessions.json")

def ensure_auth_directories():
    """Ensure authentication data directories exist"""
    Path(DATA_FOLDER).mkdir(exist_ok=True)

def get_auth_db():
    """Get database instance for authentication - returns None if MySQL not available"""
    try:
        from database import get_database
        return get_database()
    except Exception as e:
        print(f"MySQL not available, using JSON fallback: {e}")
        return None

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def load_users():
    """Load users from JSON file"""
    ensure_auth_directories()
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    ensure_auth_directories()
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def load_sessions():
    """Load active sessions from JSON file"""
    ensure_auth_directories()
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_sessions(sessions):
    """Save active sessions to JSON file"""
    ensure_auth_directories()
    with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

def create_user(email: str, password: str, name: str, profile_data: Dict = None) -> Tuple[bool, Any]:
    """Create a new user account - tries MySQL first, falls back to JSON"""
    # Try MySQL first
    db = get_auth_db()
    if db:
        try:
            # Check if email already exists
            existing_user = db.get_user_by_email(email)
            if existing_user:
                return False, "Email already registered"
            
            # Validate email format
            if '@' not in email or '.' not in email:
                return False, "Invalid email format"
            
            # Validate password strength
            if len(password) < 8:
                return False, "Password must be at least 8 characters long"
            
            # Hash password
            password_hash = hash_password(password)
            
            # Extract profile data
            cultural_background = profile_data.get('cultural_background', '') if profile_data else ''
            profession = profile_data.get('profession', '') if profile_data else ''
            location = profile_data.get('location', '') if profile_data else ''
            
            # Create user in database
            user_id = db.create_user(
                username=email.split('@')[0],  # Use email prefix as username
                email=email.lower(),
                password_hash=password_hash,
                full_name=name,
                bio=f"Cultural Background: {cultural_background}, Profession: {profession}, Location: {location}"
            )
            
            if user_id:
                return True, user_id
            else:
                return False, "Failed to create user account"
                
        except Exception as e:
            print(f"MySQL user creation failed, falling back to JSON: {e}")
    
    # Fallback to JSON storage
    try:
        users = load_users()
        
        # Check if email already exists
        if email.lower() in [user['email'].lower() for user in users.values()]:
            return False, "Email already registered"
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return False, "Invalid email format"
        
        # Validate password strength
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # Create user object
        user_id = secrets.token_hex(16)
        user = {
            'user_id': user_id,
            'email': email.lower(),
            'name': name,
            'password_hash': hash_password(password),
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'profile_data': profile_data or {},
            'is_active': True,
            'role': 'contributor'
        }
        
        users[user_id] = user
        save_users(users)
        
        return True, user_id
        
    except Exception as e:
        return False, f"Failed to create user: {str(e)}"

def authenticate_user(email: str, password: str) -> Tuple[bool, Any]:
    """Authenticate user with email and password - tries MySQL first, falls back to JSON"""
    # Try MySQL first
    db = get_auth_db()
    if db:
        try:
            # Get user by email
            user = db.get_user_by_email(email.lower())
            if not user:
                return False, "Invalid email or password"
            
            # Check if account is active
            if not user.get('is_active', True):
                return False, "Account is deactivated"
            
            # Verify password
            if not verify_password(password, user['password_hash']):
                return False, "Invalid email or password"
            
            # Update last login
            db.update_user_login(user['user_id'])
            
            # Return user data
            user_data = {
                'user_id': user['user_id'],
                'email': user['email'],
                'name': user['full_name'] or user['username'],
                'created_at': user['join_date'].isoformat() if user['join_date'] else datetime.now().isoformat(),
                'last_login': user['last_login'].isoformat() if user['last_login'] else None,
                'profile_data': {
                    'cultural_background': '',
                    'profession': '',
                    'location': ''
                },
                'is_active': user.get('is_active', True),
                'role': 'contributor'
            }
            
            return True, user_data
            
        except Exception as e:
            print(f"MySQL authentication failed, falling back to JSON: {e}")
    
    # Fallback to JSON storage
    try:
        users = load_users()
        
        # Find user by email
        user = None
        for user_data in users.values():
            if user_data['email'].lower() == email.lower():
                user = user_data
                break
        
        if not user:
            return False, "Invalid email or password"
        
        if not user['is_active']:
            return False, "Account is deactivated"
        
        if not verify_password(password, user['password_hash']):
            return False, "Invalid email or password"
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        users[user['user_id']] = user
        save_users(users)
        
        return True, user
        
    except Exception as e:
        return False, f"Authentication error: {str(e)}"

def create_session(user_id) -> str:
    """Create a new session for user"""
    try:
        # For now, we'll use a simple session token
        # In a production system, you'd want to store sessions in the database
        session_token = secrets.token_hex(32)
        
        # Store session in Streamlit session state for now
        if 'sessions' not in st.session_state:
            st.session_state.sessions = {}
        
        session = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat(),
        }
        
        st.session_state.sessions[session_token] = session
        return session_token
        
    except Exception as e:
        return None

def validate_session(session_token: str) -> Optional[Dict]:
    """Validate session token and return user data"""
    try:
        if 'sessions' not in st.session_state:
            return None
        
        if session_token not in st.session_state.sessions:
            return None
        
        session = st.session_state.sessions[session_token]
        
        # Check if session is expired
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires_at:
            # Remove expired session
            del st.session_state.sessions[session_token]
            return None
        
        # Get user data
        db = get_auth_db()
        if db:
            try:
                user = db.get_user_by_id(session['user_id'])
                
                if not user or not user.get('is_active', True):
                    return None
                
                # Return user data
                user_data = {
                    'user_id': user['user_id'],
                    'email': user['email'],
                    'name': user['full_name'] or user['username'],
                    'created_at': user['join_date'].isoformat() if user['join_date'] else datetime.now().isoformat(),
                    'last_login': user['last_login'].isoformat() if user['last_login'] else None,
                    'profile_data': {
                        'cultural_background': '',
                        'profession': '',
                        'location': ''
                    },
                    'is_active': user.get('is_active', True),
                    'role': 'contributor'
                }
                
                return user_data
            except Exception as e:
                print(f"MySQL session validation failed, falling back to JSON: {e}")
        
        # Fallback to JSON storage
        users = load_users()
        user_id = session['user_id']
        if user_id not in users:
            return None
        
        user = users[user_id]
        if not user['is_active']:
            return None
        
        return user
        
    except Exception as e:
        return None

def logout_user(session_token: str) -> bool:
    """Logout user by removing session"""
    try:
        if 'sessions' in st.session_state and session_token in st.session_state.sessions:
            del st.session_state.sessions[session_token]
        return True
    except Exception as e:
        return False

def get_user_by_id(user_id) -> Optional[Dict]:
    """Get user data by user ID"""
    try:
        db = get_auth_db()
        if db:
            try:
                user = db.get_user_by_id(user_id)
                
                if not user:
                    return None
                
                return {
                    'user_id': user['user_id'],
                    'email': user['email'],
                    'name': user['full_name'] or user['username'],
                    'created_at': user['join_date'].isoformat() if user['join_date'] else datetime.now().isoformat(),
                    'last_login': user['last_login'].isoformat() if user['last_login'] else None,
                    'profile_data': {
                        'cultural_background': '',
                        'profession': '',
                        'location': ''
                    },
                    'is_active': user.get('is_active', True),
                    'role': 'contributor'
                }
            except Exception as e:
                print(f"MySQL user lookup failed, falling back to JSON: {e}")
        
        # Fallback to JSON storage
        users = load_users()
        return users.get(user_id)
        
    except Exception as e:
        return None

def update_user_profile(user_id, profile_data: Dict) -> Tuple[bool, str]:
    """Update user profile data"""
    try:
        db = get_auth_db()
        if db:
            try:
                # Extract profile fields
                updates = {}
                if 'full_name' in profile_data:
                    updates['full_name'] = profile_data['full_name']
                if 'cultural_background' in profile_data or 'profession' in profile_data or 'location' in profile_data:
                    bio_parts = []
                    if profile_data.get('cultural_background'):
                        bio_parts.append(f"Cultural Background: {profile_data['cultural_background']}")
                    if profile_data.get('profession'):
                        bio_parts.append(f"Profession: {profile_data['profession']}")
                    if profile_data.get('location'):
                        bio_parts.append(f"Location: {profile_data['location']}")
                    updates['bio'] = ', '.join(bio_parts)
                
                if updates:
                    success = db.update_user_profile(user_id, **updates)
                    if success:
                        return True, "Profile updated successfully"
                    else:
                        return False, "Failed to update profile"
                else:
                    return False, "No valid profile data provided"
            except Exception as e:
                print(f"MySQL profile update failed, falling back to JSON: {e}")
        
        # Fallback to JSON storage
        users = load_users()
        
        if user_id not in users:
            return False, "User not found"
        
        users[user_id]['profile_data'].update(profile_data)
        save_users(users)
        
        return True, "Profile updated successfully"
            
    except Exception as e:
        return False, f"Profile update error: {str(e)}"

def change_password(user_id, current_password: str, new_password: str) -> Tuple[bool, str]:
    """Change user password"""
    try:
        db = get_auth_db()
        if db:
            try:
                user = db.get_user_by_id(user_id)
                
                if not user:
                    return False, "User not found"
                
                # Verify current password
                if not verify_password(current_password, user['password_hash']):
                    return False, "Current password is incorrect"
                
                # Validate new password
                if len(new_password) < 8:
                    return False, "New password must be at least 8 characters long"
                
                # Update password
                new_password_hash = hash_password(new_password)
                success = db.update_user_profile(user_id, password_hash=new_password_hash)
                
                if success:
                    return True, "Password changed successfully"
                else:
                    return False, "Failed to change password"
            except Exception as e:
                print(f"MySQL password change failed, falling back to JSON: {e}")
        
        # Fallback to JSON storage
        users = load_users()
        
        if user_id not in users:
            return False, "User not found"
        
        user = users[user_id]
        
        # Verify current password
        if not verify_password(current_password, user['password_hash']):
            return False, "Current password is incorrect"
        
        # Validate new password
        if len(new_password) < 8:
            return False, "New password must be at least 8 characters long"
        
        # Update password
        user['password_hash'] = hash_password(new_password)
        save_users(users)
        
        return True, "Password changed successfully"
            
    except Exception as e:
        return False, f"Password change error: {str(e)}"

def delete_user_account(user_id, password: str) -> Tuple[bool, str]:
    """Delete user account"""
    try:
        db = get_auth_db()
        if db:
            try:
                user = db.get_user_by_id(user_id)
                
                if not user:
                    return False, "User not found"
                
                # Verify password
                if not verify_password(password, user['password_hash']):
                    return False, "Password is incorrect"
                
                # Deactivate account
                success = db.deactivate_user(user_id)
                
                if success:
                    return True, "Account deactivated successfully"
                else:
                    return False, "Failed to deactivate account"
            except Exception as e:
                print(f"MySQL account deletion failed, falling back to JSON: {e}")
        
        # Fallback to JSON storage
        users = load_users()
        
        if user_id not in users:
            return False, "User not found"
        
        user = users[user_id]
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return False, "Password is incorrect"
        
        # Deactivate account instead of deleting
        user['is_active'] = False
        user['deactivated_at'] = datetime.now().isoformat()
        save_users(users)
        
        # Remove all sessions for this user
        sessions = load_sessions()
        sessions_to_remove = [token for token, session in sessions.items() 
                             if session['user_id'] == user_id]
        
        for token in sessions_to_remove:
            del sessions[token]
        save_sessions(sessions)
        
        return True, "Account deactivated successfully"
            
    except Exception as e:
        return False, f"Account deletion error: {str(e)}"

def get_user_statistics(user_id) -> Dict:
    """Get user contribution statistics"""
    try:
        db = get_auth_db()
        if db:
            # This would need to be implemented based on your data structure
            # For now, return basic structure
            return {
                'total_contributions': 0,
                'images_uploaded': 0,
                'audio_uploaded': 0,
                'video_uploaded': 0,
            }
    except Exception as e:
        pass
    
    # Fallback to basic structure
    return {
        'total_contributions': 0,
        'images_uploaded': 0,
        'audio_uploaded': 0,
        'video_uploaded': 0,
    }

# Streamlit UI Components

def render_login_form():
    """Render login form"""
    st.markdown("### 🔐 Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Login", use_container_width=True)
        with col2:
            if st.form_submit_button("Forgot Password?", use_container_width=True):
                st.info("Password reset functionality will be implemented in Phase 3")
        
        if submit_button:
            if not email or not password:
                st.error("Please fill in all fields")
                return None
            
            success, result = authenticate_user(email, password)
            if success:
                user = result
                session_token = create_session(user['user_id'])
                st.session_state['user_session'] = session_token
                st.session_state['user_data'] = user
                st.success(f"Welcome back, {user['name']}!")
                # Redirect to main page
                st.session_state['current_page'] = 'main'
                st.rerun()
            else:
                st.error(result)
    
    st.markdown("---")
    st.markdown("Don't have an account? [Sign up here](#signup)")

def render_signup_form():
    """Render signup form"""
    st.markdown("### 📝 Create Your Account")
    
    # Show database status
    db = get_auth_db()
    if db:
        st.success("✅ Connected to MySQL database")
    else:
        st.info("ℹ️ Using local JSON storage (MySQL not available)")
        st.markdown("""
        **To enable MySQL database storage:**
        1. Install MySQL Server
        2. Create database: `cultural_corpus_platform`
        3. Update `db_config.py` with your MySQL credentials
        4. Run: `python migrate_to_mysql.py`
        """)
    
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Create a password (min 8 characters)")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        # Profile data
        st.markdown("#### Profile Information (Optional)")
        cultural_background = st.text_input("Cultural Background", placeholder="e.g., Telugu, Bengali, etc.")
        profession = st.text_input("Profession", placeholder="e.g., Student, Researcher, etc.")
        location = st.text_input("Location", placeholder="e.g., Hyderabad, India")
        
        # Voice Introduction Section
        st.markdown("#### 🎤 Voice Introduction (Optional)")
        st.markdown("Record a brief introduction about yourself and your cultural background.")
        
        # Web Audio Recording for Signup
        from audio_recorder import audio_recorder_component
        audio_recorder_component(key="signup")
        
        # File upload as fallback for voice introduction
        st.markdown("**Or upload an audio file for your voice introduction:**")
        voice_intro_audio = st.file_uploader(
            "🎵 Upload Voice Introduction",
            type=['mp3', 'wav', 'ogg', 'm4a'],
            help="Upload a brief audio introduction about yourself"
        )
        
        if voice_intro_audio:
            st.audio(voice_intro_audio, caption="Your voice introduction")
        
        submit_button = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit_button:
            # Validation
            if not name or not email or not password:
                st.error("Please fill in all required fields")
                return None
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return None
            
            if len(password) < 8:
                st.error("Password must be at least 8 characters long")
                return None
            
            # Create profile data
            profile_data = {
                'cultural_background': cultural_background,
                'profession': profession,
                'location': location
            }
            
            success, result = create_user(email, password, name, profile_data)
            if success:
                user_id = result
                st.success("Account created successfully! You can now log in.")
                # Redirect to login page
                st.session_state['current_page'] = 'login'
                st.rerun()
            else:
                st.error(result)
    
    st.markdown("---")
    st.markdown("Already have an account? [Login here](#login)")

def render_user_profile():
    """Render user profile page"""
    user = st.session_state.get('user_data')
    if not user:
        st.error("Please log in to view your profile")
        return
    
    st.markdown("### 👤 Your Profile")
    
    # User information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Name:** {user['name']}")
        st.markdown(f"**Email:** {user['email']}")
        st.markdown(f"**Member Since:** {user['created_at'][:10]}")
        st.markdown(f"**Last Login:** {user['last_login'][:19] if user['last_login'] else 'Never'}")
    
    with col2:
        # Profile data
        profile = user.get('profile_data', {})
        if profile:
            st.markdown("**Profile Information:**")
            for key, value in profile.items():
                if value:
                    st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
    
    # Statistics
    st.markdown("### 📊 Your Contributions")
    stats = get_user_statistics(user['user_id'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Contributions", stats['total_contributions'])
    with col2:
        st.metric("Images Uploaded", stats['images_uploaded'])
    with col3:
        st.metric("Audio Uploaded", stats['audio_uploaded'])
    with col4:
        st.metric("Video Uploaded", stats['video_uploaded'])
    
    # Account actions
    st.markdown("### ⚙️ Account Settings")
    
    tab1, tab2, tab3 = st.tabs(["Edit Profile", "Change Password", "Delete Account"])
    
    with tab1:
        render_edit_profile_form(user)
    
    with tab2:
        render_change_password_form(user)
    
    with tab3:
        render_delete_account_form(user)

def render_edit_profile_form(user):
    """Render edit profile form"""
    profile = user.get('profile_data', {})
    
    with st.form("edit_profile_form"):
        new_name = st.text_input("Full Name", value=user['name'])
        cultural_background = st.text_input("Cultural Background", value=profile.get('cultural_background', ''))
        profession = st.text_input("Profession", value=profile.get('profession', ''))
        location = st.text_input("Location", value=profile.get('location', ''))
        
        # Voice Introduction Section
        st.markdown("#### 🎤 Voice Introduction (Optional)")
        st.markdown("Record a brief introduction about yourself and your cultural background.")
        
        # Web Audio Recording for Profile
        from audio_recorder import audio_recorder_component
        audio_recorder_component(key="profile")
        
        # File upload as fallback for voice introduction
        st.markdown("**Or upload an audio file for your voice introduction:**")
        voice_intro_audio = st.file_uploader(
            "🎵 Upload Voice Introduction",
            type=['mp3', 'wav', 'ogg', 'm4a'],
            help="Upload a brief audio introduction about yourself"
        )
        
        if voice_intro_audio:
            st.audio(voice_intro_audio, caption="Your voice introduction")
        
        if st.form_submit_button("Update Profile"):
            # Update user data
            profile_data = {
                'full_name': new_name,
                'cultural_background': cultural_background,
                'profession': profession,
                'location': location
            }
            
            success, message = update_user_profile(user['user_id'], profile_data)
            if success:
                # Update session state
                user['name'] = new_name
                user['profile_data'] = {
                    'cultural_background': cultural_background,
                    'profession': profession,
                    'location': location
                }
                st.session_state['user_data'] = user
                st.success("Profile updated successfully!")
                st.rerun()
            else:
                st.error(message)

def render_change_password_form(user):
    """Render change password form"""
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Change Password"):
            if new_password != confirm_password:
                st.error("New passwords do not match")
                return
            
            success, message = change_password(user['user_id'], current_password, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

def render_delete_account_form(user):
    """Render delete account form"""
    st.warning("⚠️ This action cannot be undone. Your account will be permanently deactivated.")
    
    with st.form("delete_account_form"):
        password = st.text_input("Enter your password to confirm", type="password")
        
        if st.form_submit_button("Delete Account", type="secondary"):
            success, message = delete_user_account(user['user_id'], password)
            if success:
                st.success(message)
                # Clear session
                if 'user_session' in st.session_state:
                    logout_user(st.session_state['user_session'])
                st.session_state.clear()
                st.rerun()
            else:
                st.error(message)

def check_user_authentication():
    """Check if user is authenticated"""
    session_token = st.session_state.get('user_session')
    if not session_token:
        return None
    
    user = validate_session(session_token)
    if user:
        st.session_state['user_data'] = user
        return user
    
    # Session is invalid, clear it
    st.session_state.pop('user_session', None)
    st.session_state.pop('user_data', None)
    return None

def require_authentication():
    """Decorator to require authentication for certain pages"""
    user = check_user_authentication()
    if not user:
        st.error("Please log in to access this page")
        st.session_state['current_page'] = 'login'
        st.rerun()
    return user 