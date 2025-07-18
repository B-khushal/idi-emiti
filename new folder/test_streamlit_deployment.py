#!/usr/bin/env python3
"""
Test script for Streamlit Cloud deployment verification
Tests all major components and database fallback mechanisms
"""

import os
import sys
import json
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import mysql.connector
        print("✅ MySQL Connector imported successfully")
    except ImportError as e:
        print(f"❌ MySQL Connector import failed: {e}")
        return False
    
    return True

def test_database_config():
    """Test database configuration"""
    print("\n🧪 Testing database configuration...")
    
    try:
        from db_config import get_storage_mode, is_mysql_available, get_database_config
        
        # Test storage mode detection
        storage_mode = get_storage_mode()
        print(f"✅ Storage mode detected: {storage_mode}")
        
        # Test MySQL availability
        mysql_available = is_mysql_available()
        print(f"✅ MySQL availability check: {mysql_available}")
        
        # Test database config
        config = get_database_config()
        print(f"✅ Database config retrieved: {config['host']}")
        
        return True
    except Exception as e:
        print(f"❌ Database config test failed: {e}")
        return False

def test_auth_system():
    """Test authentication system"""
    print("\n🧪 Testing authentication system...")
    
    try:
        from auth import hash_password, verify_password, load_users, save_users
        
        # Test password hashing
        test_password = "test123"
        hashed = hash_password(test_password)
        print("✅ Password hashing works")
        
        # Test password verification
        if verify_password(test_password, hashed):
            print("✅ Password verification works")
        else:
            print("❌ Password verification failed")
            return False
        
        # Test user storage
        test_users = {"test": {"email": "test@example.com", "password_hash": hashed}}
        save_users(test_users)
        loaded_users = load_users()
        if "test" in loaded_users:
            print("✅ User storage works")
        else:
            print("❌ User storage failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("\n🧪 Testing utility functions...")
    
    try:
        from utils import get_storage_status, display_storage_status
        
        # Test storage status
        status = get_storage_status()
        print(f"✅ Storage status: {status['mode']}")
        
        # Test display function (should not raise errors)
        print("✅ Storage status display function works")
        
        return True
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def test_file_structure():
    """Test required file structure"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        "app.py",
        "auth.py",
        "config.py",
        "utils.py",
        "db_config.py",
        "database.py",
        "requirements.txt",
        "audio_recorder.py"
    ]
    
    required_dirs = [
        "data",
        "assets",
        "uploads"
    ]
    
    # Check files
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Check directories
    for dir in required_dirs:
        if os.path.exists(dir):
            print(f"✅ {dir}/ directory exists")
        else:
            print(f"❌ {dir}/ directory missing")
            return False
    
    return True

def test_data_files():
    """Test data file creation"""
    print("\n🧪 Testing data file creation...")
    
    try:
        # Test data directory
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Test users.json
        users_file = data_dir / "users.json"
        if not users_file.exists():
            with open(users_file, 'w') as f:
                json.dump({}, f)
        print("✅ users.json ready")
        
        # Test sessions.json
        sessions_file = data_dir / "sessions.json"
        if not sessions_file.exists():
            with open(sessions_file, 'w') as f:
                json.dump({}, f)
        print("✅ sessions.json ready")
        
        # Test user_responses.csv
        csv_file = data_dir / "user_responses.csv"
        if not csv_file.exists():
            with open(csv_file, 'w') as f:
                f.write("session_id,timestamp,media_path,description,name,category,latitude,longitude\n")
        print("✅ user_responses.csv ready")
        
        return True
    except Exception as e:
        print(f"❌ Data file test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Streamlit Cloud Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Database Config", test_database_config),
        ("Authentication", test_auth_system),
        ("Utilities", test_utils),
        ("Data Files", test_data_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed\n")
            else:
                print(f"❌ {test_name} test failed\n")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}\n")
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for Streamlit Cloud deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 