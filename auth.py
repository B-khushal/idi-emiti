"""
Authentication module for Cultural Corpus Collection Platform
Handles user registration, login, session management, and profile operations
Uses CSV-based storage instead of MySQL database
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

# Import CSV-based user management
from csv_user_manager import (
    get_user_by_email, get_user_by_id, create_user, update_user_login,
    update_user_profile, deactivate_user, create_session, validate_session,
    logout_user, get_user_statistics, change_user_password, delete_user,
    hash_password, verify_password
)

def ensure_auth_directories():
    """Ensure authentication data directories exist"""
    Path(DATA_FOLDER).mkdir(exist_ok=True)

# Password functions are now imported from csv_user_manager
# User and session loading/saving is handled by csv_user_manager

def register_user(email: str, password: str, name: str, profile_data: Dict = None) -> Tuple[bool, Any]:
    """Create a new user account using CSV storage"""
    try:
        # Check if email already exists
        existing_user = get_user_by_email(email)
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
        
        # Create user using CSV manager
        user_id = create_user(
            username=email.split('@')[0],  # Use email prefix as username
            email=email.lower(),
            password_hash=password_hash,
            full_name=name,
            cultural_background=cultural_background,
            profession=profession,
            location=location
        )
        
        if user_id:
            return True, user_id
        else:
            return False, "Failed to create user account"
            
    except Exception as e:
        return False, f"Failed to create user: {str(e)}"

def authenticate_user(email: str, password: str) -> Tuple[bool, Any]:
    """Authenticate user with email and password using CSV storage"""
    try:
        # Get user by email
        user = get_user_by_email(email.lower())
        if not user:
            return False, "Invalid email or password"
        
        # Check if account is active
        if not user.get('is_active', True):
            return False, "Account is deactivated"
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return False, "Invalid email or password"
        
        # Update last login
        update_user_login(user['user_id'])
        
        # Return user data
        user_data = {
            'user_id': user['user_id'],
            'email': user['email'],
            'name': user['full_name'] or user['username'],
            'created_at': user['created_at'],
            'last_login': user['last_login'],
            'profile_data': {
                'cultural_background': user.get('cultural_background', ''),
                'profession': user.get('profession', ''),
                'location': user.get('location', '')
            },
            'is_active': user.get('is_active', True),
            'role': user.get('role', 'contributor')
        }
        
        return True, user_data
        
    except Exception as e:
        return False, f"Authentication failed: {str(e)}"


def create_user_session(user_id) -> str:
    """Create a new session for user using CSV storage"""
    try:
        return create_session(user_id)
    except Exception as e:
        print(f"Error creating session: {e}")
        return None

def validate_user_session(session_token: str) -> Optional[Dict]:
    """Validate session token and return user data using CSV storage"""
    try:
        user = validate_session(session_token)
        if not user:
            return None
        
        # Format user data to match the expected structure
        return {
            'user_id': user['user_id'],
            'email': user['email'],
            'name': user['full_name'] or user['username'],
            'created_at': user['created_at'],
            'last_login': user['last_login'],
            'profile_data': {
                'cultural_background': user.get('cultural_background', ''),
                'profession': user.get('profession', ''),
                'location': user.get('location', '')
            },
            'is_active': user.get('is_active', True),
            'role': user.get('role', 'contributor')
        }
    except Exception as e:
        print(f"Error validating session: {e}")
        return None

def logout_user_session(session_token: str) -> bool:
    """Logout user by deactivating session using CSV storage"""
    try:
        return logout_user(session_token)
    except Exception as e:
        print(f"Error logging out user: {e}")
        return False

def get_user_by_id_wrapper(user_id) -> Optional[Dict]:
    """Get user data by user ID using CSV storage"""
    try:
        user = get_user_by_id(user_id)
        if not user:
            return None
        
        return {
            'user_id': user['user_id'],
            'email': user['email'],
            'name': user['full_name'] or user['username'],
            'created_at': user['created_at'],
            'last_login': user['last_login'],
            'profile_data': {
                'cultural_background': user.get('cultural_background', ''),
                'profession': user.get('profession', ''),
                'location': user.get('location', '')
            },
            'is_active': user.get('is_active', True),
            'role': user.get('role', 'contributor')
        }
        
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None

def update_user_profile_wrapper(user_id, profile_data: Dict) -> Tuple[bool, str]:
    """Update user profile data using CSV storage"""
    try:
        # Extract profile fields
        updates = {}
        if 'full_name' in profile_data:
            updates['full_name'] = profile_data['full_name']
        if 'cultural_background' in profile_data:
            updates['cultural_background'] = profile_data['cultural_background']
        if 'profession' in profile_data:
            updates['profession'] = profile_data['profession']
        if 'location' in profile_data:
            updates['location'] = profile_data['location']
        
        if updates:
            success = update_user_profile(user_id, **updates)
            if success:
                return True, "Profile updated successfully"
            else:
                return False, "Failed to update profile"
        else:
            return False, "No valid profile data provided"
            
    except Exception as e:
        return False, f"Profile update error: {str(e)}"

def change_password(user_id, current_password: str, new_password: str) -> Tuple[bool, str]:
    """Change user password using CSV storage"""
    try:
        user = get_user_by_id(user_id)
        
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
        success = change_user_password(user_id, new_password_hash)
        
        if success:
            return True, "Password changed successfully"
        else:
            return False, "Failed to change password"
            
    except Exception as e:
        return False, f"Password change error: {str(e)}"

def delete_user_account(user_id, password: str) -> Tuple[bool, str]:
    """Delete user account using CSV storage"""
    try:
        user = get_user_by_id(user_id)
        
        if not user:
            return False, "User not found"
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return False, "Password is incorrect"
        
        # Deactivate account
        success = deactivate_user(user_id)
        
        if success:
            return True, "Account deactivated successfully"
        else:
            return False, "Failed to deactivate account"
            
    except Exception as e:
        return False, f"Account deletion error: {str(e)}"

def get_user_statistics_wrapper(user_id) -> Dict:
    """Get user contribution statistics using CSV storage"""
    try:
        return get_user_statistics(user_id)
    except Exception as e:
        print(f"Error getting user statistics: {e}")
        return {
            'total_contributions': 0,
            'media_types': {},
            'languages': {},
            'categories': {},
            'last_contribution': None,
            'account_created': None,
            'last_login': None
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
                session_token = create_user_session(user['user_id'])
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
    
    # Show storage status
    st.success("✅ Using CSV-based storage system")
    
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
            
            success, result = register_user(email, password, name, profile_data)
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
    stats = get_user_statistics_wrapper(user['user_id'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Contributions", stats['total_contributions'])
    with col2:
        st.metric("Images Uploaded", stats.get('media_types', {}).get('image', 0))
    with col3:
        st.metric("Audio Uploaded", stats.get('media_types', {}).get('audio', 0))
    with col4:
        st.metric("Video Uploaded", stats.get('media_types', {}).get('video', 0))
    
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
            
            success, message = update_user_profile_wrapper(user['user_id'], profile_data)
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
                    logout_user_session(st.session_state['user_session'])
                st.session_state.clear()
                st.rerun()
            else:
                st.error(message)

def check_user_authentication():
    """Check if user is authenticated"""
    session_token = st.session_state.get('user_session')
    if not session_token:
        return None
    
    user = validate_user_session(session_token)
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