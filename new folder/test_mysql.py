#!/usr/bin/env python3
"""
Test script for MySQL Database Integration
Tests database operations and functionality
"""

import os
import sys
import tempfile
from database import DatabaseManager, CulturalCorpusDB, initialize_database
import hashlib
import secrets

def test_database_connection():
    """Test database connection"""
    print("🧪 Testing database connection...")
    
    db_manager = DatabaseManager()
    if db_manager.connect():
        print("✅ Database connection successful")
        db_manager.disconnect()
        return True
    else:
        print("❌ Database connection failed")
        return False

def test_database_schema():
    """Test database schema initialization"""
    print("\n🧪 Testing database schema initialization...")
    
    db_manager = DatabaseManager()
    if db_manager.connect():
        if initialize_database(db_manager):
            print("✅ Database schema initialized successfully")
            db_manager.disconnect()
            return True
        else:
            print("❌ Database schema initialization failed")
            db_manager.disconnect()
            return False
    else:
        print("❌ Cannot test schema - database connection failed")
        return False

def test_user_operations():
    """Test user management operations"""
    print("\n🧪 Testing user operations...")
    
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Cannot test user operations - database connection failed")
        return False
    
    db = CulturalCorpusDB(db_manager)
    
    # Test user creation
    test_email = f"test_{secrets.token_hex(8)}@example.com"
    test_username = f"testuser_{secrets.token_hex(4)}"
    password_hash = hashlib.sha256("testpassword123".encode()).hexdigest()
    
    user_id = db.create_user(
        username=test_username,
        email=test_email,
        password_hash=password_hash,
        full_name="Test User",
        bio="Test bio",
        country="India",
        region="Telangana",
        city="Hyderabad"
    )
    
    if user_id:
        print("✅ User creation successful")
        
        # Test user retrieval
        user = db.get_user_by_email(test_email)
        if user and user['user_id'] == user_id:
            print("✅ User retrieval by email successful")
        else:
            print("❌ User retrieval by email failed")
            return False
        
        user = db.get_user_by_id(user_id)
        if user and user['email'] == test_email:
            print("✅ User retrieval by ID successful")
        else:
            print("❌ User retrieval by ID failed")
            return False
        
        # Test user update
        if db.update_user_profile(user_id, bio="Updated bio", city="Mumbai"):
            print("✅ User profile update successful")
        else:
            print("❌ User profile update failed")
            return False
        
        # Test user deactivation
        if db.deactivate_user(user_id):
            print("✅ User deactivation successful")
        else:
            print("❌ User deactivation failed")
            return False
        
        db_manager.disconnect()
        return True
    else:
        print("❌ User creation failed")
        db_manager.disconnect()
        return False

def test_category_operations():
    """Test category management operations"""
    print("\n🧪 Testing category operations...")
    
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Cannot test category operations - database connection failed")
        return False
    
    db = CulturalCorpusDB(db_manager)
    
    # Test category creation
    category_name = f"Test Category {secrets.token_hex(4)}"
    category_id = db.create_category(category_name, "Test category description")
    
    if category_id:
        print("✅ Category creation successful")
        
        # Test category retrieval
        category = db.get_category_by_id(category_id)
        if category and category['category_name'] == category_name:
            print("✅ Category retrieval successful")
        else:
            print("❌ Category retrieval failed")
            return False
        
        # Test category listing
        categories = db.get_categories()
        if categories and len(categories) > 0:
            print("✅ Category listing successful")
        else:
            print("❌ Category listing failed")
            return False
        
        db_manager.disconnect()
        return True
    else:
        print("❌ Category creation failed")
        db_manager.disconnect()
        return False

def test_cultural_item_operations():
    """Test cultural item operations"""
    print("\n🧪 Testing cultural item operations...")
    
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Cannot test cultural item operations - database connection failed")
        return False
    
    db = CulturalCorpusDB(db_manager)
    
    # Create test user
    test_email = f"contributor_{secrets.token_hex(8)}@example.com"
    password_hash = hashlib.sha256("testpassword123".encode()).hexdigest()
    
    user_id = db.create_user(
        username=f"contributor_{secrets.token_hex(4)}",
        email=test_email,
        password_hash=password_hash,
        full_name="Test Contributor"
    )
    
    if not user_id:
        print("❌ Cannot test cultural items - user creation failed")
        db_manager.disconnect()
        return False
    
    # Get or create category
    categories = db.get_categories()
    category_id = categories[0]['category_id'] if categories else None
    
    if not category_id:
        category_id = db.create_category("Test Category", "Test category")
    
    if not category_id:
        print("❌ Cannot test cultural items - category creation failed")
        db_manager.disconnect()
        return False
    
    # Test cultural item creation
    item_id = db.create_cultural_item(
        title="Test Cultural Item",
        contributor_id=user_id,
        category_id=category_id,
        description_en="Test English description",
        description_te="Test Telugu description",
        latitude=17.3850,
        longitude=78.4867,
        location_name="Hyderabad, Telangana, India"
    )
    
    if item_id:
        print("✅ Cultural item creation successful")
        
        # Test item retrieval
        item = db.get_cultural_item(item_id)
        if item and item['title'] == "Test Cultural Item":
            print("✅ Cultural item retrieval successful")
        else:
            print("❌ Cultural item retrieval failed")
            return False
        
        # Test item approval
        if db.approve_item(item_id, user_id):
            print("✅ Cultural item approval successful")
        else:
            print("❌ Cultural item approval failed")
            return False
        
        # Test item listing
        items = db.get_cultural_items(limit=10)
        if items and len(items) > 0:
            print("✅ Cultural item listing successful")
        else:
            print("❌ Cultural item listing failed")
            return False
        
        # Test contributor items
        contributor_items = db.get_items_by_contributor(user_id)
        if contributor_items and len(contributor_items) > 0:
            print("✅ Contributor items retrieval successful")
        else:
            print("❌ Contributor items retrieval failed")
            return False
        
        db_manager.disconnect()
        return True
    else:
        print("❌ Cultural item creation failed")
        db_manager.disconnect()
        return False

def test_media_operations():
    """Test media file operations"""
    print("\n🧪 Testing media operations...")
    
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Cannot test media operations - database connection failed")
        return False
    
    db = CulturalCorpusDB(db_manager)
    
    # Create test item first
    test_email = f"media_test_{secrets.token_hex(8)}@example.com"
    password_hash = hashlib.sha256("testpassword123".encode()).hexdigest()
    
    user_id = db.create_user(
        username=f"media_test_{secrets.token_hex(4)}",
        email=test_email,
        password_hash=password_hash,
        full_name="Media Test User"
    )
    
    categories = db.get_categories()
    category_id = categories[0]['category_id'] if categories else db.create_category("Test Category", "Test")
    
    item_id = db.create_cultural_item(
        title="Media Test Item",
        contributor_id=user_id,
        category_id=category_id,
        description_en="Test item for media operations"
    )
    
    if not item_id:
        print("❌ Cannot test media operations - item creation failed")
        db_manager.disconnect()
        return False
    
    # Test media addition
    media_id = db.add_item_media(
        item_id=item_id,
        media_type="image",
        file_path="uploads/images/test_image.jpg",
        file_size_kb=1024,
        dimensions="1920x1080"
    )
    
    if media_id:
        print("✅ Media addition successful")
        
        # Test media retrieval
        media_files = db.get_item_media(item_id)
        if media_files and len(media_files) > 0:
            print("✅ Media retrieval successful")
        else:
            print("❌ Media retrieval failed")
            return False
        
        # Test media deletion
        if db.delete_item_media(media_id):
            print("✅ Media deletion successful")
        else:
            print("❌ Media deletion failed")
            return False
        
        db_manager.disconnect()
        return True
    else:
        print("❌ Media addition failed")
        db_manager.disconnect()
        return False

def test_tag_operations():
    """Test tag operations"""
    print("\n🧪 Testing tag operations...")
    
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Cannot test tag operations - database connection failed")
        return False
    
    db = CulturalCorpusDB(db_manager)
    
    # Create test item
    test_email = f"tag_test_{secrets.token_hex(8)}@example.com"
    password_hash = hashlib.sha256("testpassword123".encode()).hexdigest()
    
    user_id = db.create_user(
        username=f"tag_test_{secrets.token_hex(4)}",
        email=test_email,
        password_hash=password_hash,
        full_name="Tag Test User"
    )
    
    categories = db.get_categories()
    category_id = categories[0]['category_id'] if categories else db.create_category("Test Category", "Test")
    
    item_id = db.create_cultural_item(
        title="Tag Test Item",
        contributor_id=user_id,
        category_id=category_id,
        description_en="Test item for tag operations"
    )
    
    if not item_id:
        print("❌ Cannot test tag operations - item creation failed")
        db_manager.disconnect()
        return False
    
    # Test tag creation and assignment
    tag_names = ["ancient", "folk art", "traditional"]
    if db.add_item_tags(item_id, tag_names):
        print("✅ Tag assignment successful")
        
        # Test tag retrieval
        tags = db.get_item_tags(item_id)
        if tags and len(tags) == len(tag_names):
            print("✅ Tag retrieval successful")
        else:
            print("❌ Tag retrieval failed")
            return False
        
        db_manager.disconnect()
        return True
    else:
        print("❌ Tag assignment failed")
        db_manager.disconnect()
        return False

def test_analytics_operations():
    """Test analytics operations"""
    print("\n🧪 Testing analytics operations...")
    
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Cannot test analytics operations - database connection failed")
        return False
    
    db = CulturalCorpusDB(db_manager)
    
    # Test submission stats
    stats = db.get_submission_stats()
    if isinstance(stats, dict) and 'total_items' in stats:
        print("✅ Submission stats retrieval successful")
    else:
        print("❌ Submission stats retrieval failed")
        return False
    
    # Test category stats
    category_stats = db.get_category_stats()
    if isinstance(category_stats, list):
        print("✅ Category stats retrieval successful")
    else:
        print("❌ Category stats retrieval failed")
        return False
    
    # Test recent submissions
    recent_submissions = db.get_recent_submissions(limit=5)
    if isinstance(recent_submissions, list):
        print("✅ Recent submissions retrieval successful")
    else:
        print("❌ Recent submissions retrieval failed")
        return False
    
    db_manager.disconnect()
    return True

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    db_manager = DatabaseManager()
    if not db_manager.connect():
        print("❌ Cannot cleanup - database connection failed")
        return
    
    # Delete test users (this will cascade to their items)
    db_manager.execute_update(
        "DELETE FROM users WHERE email LIKE '%test%' OR email LIKE '%example.com'"
    )
    
    # Delete test categories
    db_manager.execute_update(
        "DELETE FROM corpus_categories WHERE category_name LIKE '%Test%'"
    )
    
    print("✅ Test data cleanup completed")
    db_manager.disconnect()

def main():
    """Run all MySQL database tests"""
    print("🗄️ MySQL Database Integration - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Database Schema", test_database_schema),
        ("User Operations", test_user_operations),
        ("Category Operations", test_category_operations),
        ("Cultural Item Operations", test_cultural_item_operations),
        ("Media Operations", test_media_operations),
        ("Tag Operations", test_tag_operations),
        ("Analytics Operations", test_analytics_operations)
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
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All MySQL database tests passed! Database integration is ready.")
        return True
    else:
        print("⚠️ Some MySQL database tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 