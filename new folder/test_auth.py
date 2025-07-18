#!/usr/bin/env python3
"""
Test script for the Authentication System
Tests user registration, login, and session management
"""

import os
import sys
import json
from auth import (
    ensure_auth_directories,
    create_user,
    authenticate_user,
    create_session,
    validate_session,
    logout_user,
    change_password,
    delete_user_account,
    load_users,
    load_sessions
)

def test_directory_creation():
    """Test authentication directory creation"""
    print("🧪 Testing authentication directory creation...")
    
    ensure_auth_directories()
    
    if os.path.exists("data"):
        print("✅ data/ directory created successfully")
        return True
    else:
        print("❌ data/ directory creation failed")
        return False

def test_user_creation():
    """Test user account creation"""
    print("\n🧪 Testing user account creation...")
    
    # Test valid user creation
    success, result = create_user(
        email="test@example.com",
        password="testpassword123",
        name="Test User",
        profile_data={
            'cultural_background': 'Telugu',
            'profession': 'Student',
            'location': 'Hyderabad'
        }
    )
    
    if success:
        print(f"✅ User created successfully with ID: {result}")
        return result
    else:
        print(f"❌ User creation failed: {result}")
        return None

def test_user_authentication():
    """Test user authentication"""
    print("\n🧪 Testing user authentication...")
    
    # Test valid login
    success, result = authenticate_user("test@example.com", "testpassword123")
    if success:
        print(f"✅ User authenticated successfully: {result['name']}")
        return result
    else:
        print(f"❌ User authentication failed: {result}")
        return None

def test_session_management():
    """Test session creation and validation"""
    print("\n🧪 Testing session management...")
    
    # Create a test user first
    success, user_id = create_user(
        email="session@example.com",
        password="sessionpass123",
        name="Session User"
    )
    
    if not success:
        print(f"❌ Failed to create test user: {user_id}")
        return None
    
    # Create session
    session_token = create_session(user_id)
    print(f"✅ Session created: {session_token[:16]}...")
    
    # Validate session
    user = validate_session(session_token)
    if user:
        print(f"✅ Session validated for user: {user['name']}")
        return session_token, user
    else:
        print("❌ Session validation failed")
        return None

def test_password_change():
    """Test password change functionality"""
    print("\n🧪 Testing password change...")
    
    # Create a test user
    success, user_id = create_user(
        email="password@example.com",
        password="oldpassword123",
        name="Password User"
    )
    
    if not success:
        print(f"❌ Failed to create test user: {user_id}")
        return False
    
    # Change password
    success, message = change_password(user_id, "oldpassword123", "newpassword123")
    if success:
        print("✅ Password changed successfully")
        
        # Verify new password works
        auth_success, user = authenticate_user("password@example.com", "newpassword123")
        if auth_success:
            print("✅ New password authentication successful")
            return True
        else:
            print("❌ New password authentication failed")
            return False
    else:
        print(f"❌ Password change failed: {message}")
        return False

def test_duplicate_email():
    """Test duplicate email prevention"""
    print("\n🧪 Testing duplicate email prevention...")
    
    # Create first user
    success1, result1 = create_user(
        email="duplicate@example.com",
        password="password123",
        name="First User"
    )
    
    if not success1:
        print(f"❌ Failed to create first user: {result1}")
        return False
    
    # Try to create second user with same email
    success2, result2 = create_user(
        email="duplicate@example.com",
        password="password456",
        name="Second User"
    )
    
    if not success2:
        print("✅ Duplicate email correctly prevented")
        return True
    else:
        print("❌ Duplicate email was allowed")
        return False

def test_invalid_credentials():
    """Test invalid credential handling"""
    print("\n🧪 Testing invalid credential handling...")
    
    # Test invalid email
    success, result = authenticate_user("nonexistent@example.com", "password123")
    if not success:
        print("✅ Invalid email correctly rejected")
    else:
        print("❌ Invalid email was accepted")
        return False
    
    # Test invalid password
    success, result = authenticate_user("test@example.com", "wrongpassword")
    if not success:
        print("✅ Invalid password correctly rejected")
        return True
    else:
        print("❌ Invalid password was accepted")
        return False

def test_account_deletion():
    """Test account deletion functionality"""
    print("\n🧪 Testing account deletion...")
    
    # Create a test user
    success, user_id = create_user(
        email="delete@example.com",
        password="deletepass123",
        name="Delete User"
    )
    
    if not success:
        print(f"❌ Failed to create test user: {user_id}")
        return False
    
    # Delete account
    success, message = delete_user_account(user_id, "deletepass123")
    if success:
        print("✅ Account deleted successfully")
        
        # Verify account is deactivated
        users = load_users()
        if user_id in users and not users[user_id]['is_active']:
            print("✅ Account correctly deactivated")
            return True
        else:
            print("❌ Account not properly deactivated")
            return False
    else:
        print(f"❌ Account deletion failed: {message}")
        return False

def test_data_persistence():
    """Test data persistence across sessions"""
    print("\n🧪 Testing data persistence...")
    
    # Create user
    success, user_id = create_user(
        email="persist@example.com",
        password="persistpass123",
        name="Persist User"
    )
    
    if not success:
        print(f"❌ Failed to create test user: {user_id}")
        return False
    
    # Load users and verify persistence
    users = load_users()
    if user_id in users:
        print("✅ User data persisted correctly")
        
        # Test session persistence
        session_token = create_session(user_id)
        sessions = load_sessions()
        if session_token in sessions:
            print("✅ Session data persisted correctly")
            return True
        else:
            print("❌ Session data not persisted")
            return False
    else:
        print("❌ User data not persisted")
        return False

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    # Remove test users
    users = load_users()
    test_emails = [
        "test@example.com",
        "session@example.com", 
        "password@example.com",
        "duplicate@example.com",
        "delete@example.com",
        "persist@example.com"
    ]
    
    users_to_remove = []
    for user_id, user in users.items():
        if user['email'] in test_emails:
            users_to_remove.append(user_id)
    
    for user_id in users_to_remove:
        del users[user_id]
    
    # Save cleaned users
    from auth import save_users
    save_users(users)
    
    print(f"✅ Cleaned up {len(users_to_remove)} test users")

def main():
    """Run all authentication tests"""
    print("🔐 Authentication System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Directory Creation", test_directory_creation),
        ("User Creation", test_user_creation),
        ("User Authentication", test_user_authentication),
        ("Session Management", test_session_management),
        ("Password Change", test_password_change),
        ("Duplicate Email Prevention", test_duplicate_email),
        ("Invalid Credentials", test_invalid_credentials),
        ("Account Deletion", test_account_deletion),
        ("Data Persistence", test_data_persistence)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
    
    # Cleanup
    cleanup_test_data()
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All authentication tests passed! System is ready.")
        return True
    else:
        print("⚠️ Some authentication tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 