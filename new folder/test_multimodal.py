#!/usr/bin/env python3
"""
Test script for the Cultural Corpus Collection Platform
Tests multimodal functionality and data handling
"""

import os
import sys
import pandas as pd
from datetime import datetime
from utils import (
    ensure_directories,
    get_available_media,
    get_media_type,
    validate_media_file,
    save_user_response,
    get_submission_count,
    get_comprehensive_analytics
)
from config import (
    ASSETS_FOLDER, DATA_FOLDER, CSV_FILE, UPLOADS_FOLDER,
    IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS,
    MAX_IMAGE_SIZE, MAX_AUDIO_SIZE, MAX_VIDEO_SIZE,
    CATEGORIES, LANGUAGES
)

def test_directory_creation():
    """Test directory creation functionality"""
    print("🧪 Testing directory creation...")
    
    ensure_directories()
    
    # Check if directories exist
    directories = [ASSETS_FOLDER, DATA_FOLDER, UPLOADS_FOLDER]
    subdirectories = [
        os.path.join(UPLOADS_FOLDER, "images"),
        os.path.join(UPLOADS_FOLDER, "audio"),
        os.path.join(UPLOADS_FOLDER, "video")
    ]
    
    all_dirs = directories + subdirectories
    
    for directory in all_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory} - Created successfully")
        else:
            print(f"❌ {directory} - Failed to create")
            return False
    
    return True

def test_media_type_detection():
    """Test media type detection functionality"""
    print("\n🧪 Testing media type detection...")
    
    test_files = [
        ("image.jpg", "image"),
        ("photo.png", "image"),
        ("audio.mp3", "audio"),
        ("music.wav", "audio"),
        ("video.mp4", "video"),
        ("movie.avi", "video"),
        ("document.pdf", "unknown"),
        ("text.txt", "unknown")
    ]
    
    for filename, expected_type in test_files:
        detected_type = get_media_type(filename)
        if detected_type == expected_type:
            print(f"✅ {filename} -> {detected_type}")
        else:
            print(f"❌ {filename} -> Expected: {expected_type}, Got: {detected_type}")
            return False
    
    return True

def test_file_validation():
    """Test file validation functionality"""
    print("\n🧪 Testing file validation...")
    
    # Test valid files
    valid_tests = [
        ("test.jpg", MAX_IMAGE_SIZE - 1000, True),
        ("test.mp3", MAX_AUDIO_SIZE - 1000, True),
        ("test.mp4", MAX_VIDEO_SIZE - 1000, True)
    ]
    
    for filename, size, expected in valid_tests:
        is_valid, message = validate_media_file(filename, size)
        if is_valid == expected:
            print(f"✅ {filename} ({size} bytes) - {message}")
        else:
            print(f"❌ {filename} ({size} bytes) - Expected: {expected}, Got: {is_valid}")
            return False
    
    # Test invalid files
    invalid_tests = [
        ("test.jpg", MAX_IMAGE_SIZE + 1000, False),
        ("test.mp3", MAX_AUDIO_SIZE + 1000, False),
        ("test.mp4", MAX_VIDEO_SIZE + 1000, False),
        ("test.pdf", 1000, False)
    ]
    
    for filename, size, expected in invalid_tests:
        is_valid, message = validate_media_file(filename, size)
        if is_valid == expected:
            print(f"✅ {filename} ({size} bytes) - {message}")
        else:
            print(f"❌ {filename} ({size} bytes) - Expected: {expected}, Got: {is_valid}")
            return False
    
    return True

def test_data_saving():
    """Test data saving functionality"""
    print("\n🧪 Testing data saving...")
    
    # Create test data
    test_data = {
        'media_filename': 'test_image.jpg',
        'media_type': 'image',
        'title': 'Test Cultural Object',
        'description': 'This is a test description for a cultural object',
        'language': 'English',
        'contributor_name': 'Test User',
        'contributor_email': 'test@example.com',
        'contributor_details': 'Test contributor details',
        'category': 'Other',
        'session_id': 'test-session-123',
        'latitude': 17.3850,
        'longitude': 78.4867,
        'file_size': 1024000,
        'file_path': 'uploads/images/test_image.jpg'
    }
    
    try:
        # Save test data
        save_user_response(**test_data)
        
        # Check if data was saved
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            if len(df) > 0:
                latest_row = df.iloc[-1]
                if latest_row['title'] == test_data['title']:
                    print("✅ Data saved successfully")
                    return True
                else:
                    print("❌ Data saved but content doesn't match")
                    return False
            else:
                print("❌ CSV file exists but is empty")
                return False
        else:
            print("❌ CSV file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error saving data: {str(e)}")
        return False

def test_analytics():
    """Test analytics functionality"""
    print("\n🧪 Testing analytics...")
    
    try:
        # Get comprehensive analytics
        analytics = get_comprehensive_analytics()
        
        # Check if analytics structure is correct
        required_keys = ['time_based', 'user_engagement', 'content_analysis', 
                        'popular_media', 'growth_metrics', 'quality_metrics']
        
        for key in required_keys:
            if key in analytics:
                print(f"✅ {key} analytics available")
            else:
                print(f"❌ {key} analytics missing")
                return False
        
        # Check submission count
        count = get_submission_count()
        print(f"✅ Total submissions: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in analytics: {str(e)}")
        return False

def test_configuration():
    """Test configuration constants"""
    print("\n🧪 Testing configuration...")
    
    # Test required constants
    required_constants = [
        'APP_TITLE', 'APP_ICON', 'ASSETS_FOLDER', 'DATA_FOLDER',
        'IMAGE_EXTENSIONS', 'AUDIO_EXTENSIONS', 'VIDEO_EXTENSIONS',
        'CATEGORIES', 'LANGUAGES', 'MAX_IMAGE_SIZE', 'MAX_AUDIO_SIZE', 'MAX_VIDEO_SIZE'
    ]
    
    for constant in required_constants:
        try:
            value = getattr(sys.modules['config'], constant)
            print(f"✅ {constant}: {value}")
        except AttributeError:
            print(f"❌ {constant} not found in config")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🏛️ Cultural Corpus Collection Platform - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Directory Creation", test_directory_creation),
        ("Media Type Detection", test_media_type_detection),
        ("File Validation", test_file_validation),
        ("Configuration", test_configuration),
        ("Data Saving", test_data_saving),
        ("Analytics", test_analytics)
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
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Platform is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 