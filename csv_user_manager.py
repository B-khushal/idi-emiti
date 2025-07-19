"""
CSV-based User Management System for Cultural Corpus Collection Platform
Replaces MySQL database with simple CSV file storage for user data
"""

import csv
import os
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple, Any
from pathlib import Path
import pandas as pd

# File paths
DATA_FOLDER = "data"
USERS_CSV_FILE = os.path.join(DATA_FOLDER, "users.csv")
SESSIONS_CSV_FILE = os.path.join(DATA_FOLDER, "sessions.csv")

def ensure_data_directories():
    """Ensure data directories exist"""
    Path(DATA_FOLDER).mkdir(exist_ok=True)

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def initialize_users_csv():
    """Initialize users CSV file with headers if it doesn't exist"""
    ensure_data_directories()
    
    if not os.path.exists(USERS_CSV_FILE):
        headers = [
            'user_id', 'username', 'email', 'password_hash', 'full_name', 
            'bio', 'country', 'region', 'city', 'cultural_background',
            'profession', 'location', 'created_at', 'last_login', 
            'is_active', 'role', 'display_publicly'
        ]
        
        with open(USERS_CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def initialize_sessions_csv():
    """Initialize sessions CSV file with headers if it doesn't exist"""
    ensure_data_directories()
    
    if not os.path.exists(SESSIONS_CSV_FILE):
        headers = ['session_token', 'user_id', 'created_at', 'expires_at', 'is_active']
        
        with open(SESSIONS_CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def load_users() -> List[Dict]:
    """Load all users from CSV file"""
    initialize_users_csv()
    
    users = []
    try:
        df = pd.read_csv(USERS_CSV_FILE)
        for _, row in df.iterrows():
            user = row.to_dict()
            users.append(user)
    except Exception as e:
        print(f"Error loading users: {e}")
    
    return users

def save_users(users: List[Dict]):
    """Save users to CSV file"""
    ensure_data_directories()
    
    if not users:
        return
    
    df = pd.DataFrame(users)
    df.to_csv(USERS_CSV_FILE, index=False)

def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email address"""
    users = load_users()
    
    for user in users:
        if user.get('email', '').lower() == email.lower():
            return user
    
    return None

def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Get user by user ID"""
    users = load_users()
    
    for user in users:
        if user.get('user_id') == user_id:
            return user
    
    return None

def create_user(username: str, email: str, password_hash: str, 
               full_name: str = None, bio: str = None, country: str = None,
               region: str = None, city: str = None, cultural_background: str = None,
               profession: str = None, location: str = None) -> Optional[str]:
    """Create a new user account"""
    # Check if email already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return None
    
    # Generate unique user ID
    user_id = secrets.token_hex(16)
    
    # Create user object
    user = {
        'user_id': user_id,
        'username': username,
        'email': email.lower(),
        'password_hash': password_hash,
        'full_name': full_name or '',
        'bio': bio or '',
        'country': country or '',
        'region': region or '',
        'city': city or '',
        'cultural_background': cultural_background or '',
        'profession': profession or '',
        'location': location or '',
        'created_at': datetime.now().isoformat(),
        'last_login': '',
        'is_active': True,
        'role': 'contributor',
        'display_publicly': True
    }
    
    # Load existing users and add new user
    users = load_users()
    users.append(user)
    save_users(users)
    
    return user_id

def update_user_login(user_id: str) -> bool:
    """Update user's last login timestamp"""
    users = load_users()
    
    for user in users:
        if user.get('user_id') == user_id:
            user['last_login'] = datetime.now().isoformat()
            save_users(users)
            return True
    
    return False

def update_user_profile(user_id: str, **kwargs) -> bool:
    """Update user profile information"""
    allowed_fields = [
        'full_name', 'bio', 'country', 'region', 'city', 
        'cultural_background', 'profession', 'location', 'display_publicly'
    ]
    
    users = load_users()
    
    for user in users:
        if user.get('user_id') == user_id:
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    user[field] = value
            
            save_users(users)
            return True
    
    return False

def deactivate_user(user_id: str) -> bool:
    """Deactivate a user account"""
    users = load_users()
    
    for user in users:
        if user.get('user_id') == user_id:
            user['is_active'] = False
            save_users(users)
            return True
    
    return False

def load_sessions() -> List[Dict]:
    """Load all sessions from CSV file"""
    initialize_sessions_csv()
    
    sessions = []
    try:
        df = pd.read_csv(SESSIONS_CSV_FILE)
        for _, row in df.iterrows():
            session = row.to_dict()
            sessions.append(session)
    except Exception as e:
        print(f"Error loading sessions: {e}")
    
    return sessions

def save_sessions(sessions: List[Dict]):
    """Save sessions to CSV file"""
    ensure_data_directories()
    
    if not sessions:
        return
    
    df = pd.DataFrame(sessions)
    df.to_csv(SESSIONS_CSV_FILE, index=False)

def create_session(user_id: str, expires_in_hours: int = 24) -> str:
    """Create a new session for a user"""
    session_token = secrets.token_hex(32)
    created_at = datetime.now()
    expires_at = created_at + timedelta(hours=expires_in_hours)
    
    session = {
        'session_token': session_token,
        'user_id': user_id,
        'created_at': created_at.isoformat(),
        'expires_at': expires_at.isoformat(),
        'is_active': True
    }
    
    # Load existing sessions and add new session
    sessions = load_sessions()
    sessions.append(session)
    save_sessions(sessions)
    
    return session_token

def validate_session(session_token: str) -> Optional[Dict]:
    """Validate session token and return user data if valid"""
    sessions = load_sessions()
    current_time = datetime.now()
    
    for session in sessions:
        if (session.get('session_token') == session_token and 
            session.get('is_active', False)):
            
            # Check if session has expired
            try:
                expires_at = datetime.fromisoformat(session['expires_at'])
                if current_time > expires_at:
                    # Session expired, deactivate it
                    session['is_active'] = False
                    save_sessions(sessions)
                    return None
                
                # Session is valid, get user data
                user = get_user_by_id(session['user_id'])
                if user and user.get('is_active', True):
                    return user
                    
            except Exception as e:
                print(f"Error parsing session expiry: {e}")
                continue
    
    return None

def logout_user(session_token: str) -> bool:
    """Logout user by deactivating session"""
    sessions = load_sessions()
    
    for session in sessions:
        if session.get('session_token') == session_token:
            session['is_active'] = False
            save_sessions(sessions)
            return True
    
    return False

def cleanup_expired_sessions():
    """Remove expired sessions from the CSV file"""
    sessions = load_sessions()
    current_time = datetime.now()
    active_sessions = []
    
    for session in sessions:
        try:
            expires_at = datetime.fromisoformat(session['expires_at'])
            if current_time <= expires_at and session.get('is_active', False):
                active_sessions.append(session)
        except Exception as e:
            print(f"Error parsing session expiry: {e}")
            continue
    
    save_sessions(active_sessions)

def get_user_statistics(user_id: str) -> Dict:
    """Get user statistics"""
    user = get_user_by_id(user_id)
    if not user:
        return {}
    
    # Load user responses to get contribution stats
    try:
        from utils import CSV_FILE
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            user_contributions = df[df['contributor_email'] == user.get('email', '')]
            
            return {
                'total_contributions': len(user_contributions),
                'media_types': user_contributions['media_type'].value_counts().to_dict() if len(user_contributions) > 0 else {},
                'languages': user_contributions['language'].value_counts().to_dict() if len(user_contributions) > 0 else {},
                'categories': user_contributions['category'].value_counts().to_dict() if len(user_contributions) > 0 else {},
                'last_contribution': user_contributions['timestamp'].iloc[-1] if len(user_contributions) > 0 else None,
                'account_created': user.get('created_at'),
                'last_login': user.get('last_login')
            }
    except Exception as e:
        print(f"Error getting user statistics: {e}")
    
    return {
        'total_contributions': 0,
        'media_types': {},
        'languages': {},
        'categories': {},
        'last_contribution': None,
        'account_created': user.get('created_at'),
        'last_login': user.get('last_login')
    }

def get_all_users() -> List[Dict]:
    """Get all users (for admin purposes)"""
    return load_users()

def delete_user(user_id: str) -> bool:
    """Delete a user account completely"""
    users = load_users()
    original_count = len(users)
    
    users = [user for user in users if user.get('user_id') != user_id]
    
    if len(users) < original_count:
        save_users(users)
        return True
    
    return False

def change_user_password(user_id: str, new_password_hash: str) -> bool:
    """Change user password"""
    users = load_users()
    
    for user in users:
        if user.get('user_id') == user_id:
            user['password_hash'] = new_password_hash
            save_users(users)
            return True
    
    return False

# Initialize CSV files on import
initialize_users_csv()
initialize_sessions_csv() 