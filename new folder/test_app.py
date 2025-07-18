#!/usr/bin/env python3
"""
Test script for the "ఇది ఏమిటి? (What's This?)" application
"""

import os
import sys
from utils import (
    ensure_directories,
    get_available_images,
    get_random_image,
    create_sample_data,
    get_submission_count,
    get_language_stats
)

def test_basic_functionality():
    """Test basic functionality of the application"""
    print("🧪 Testing Basic Functionality...")
    
    # Test directory creation
    print("1. Testing directory creation...")
    ensure_directories()
    assert os.path.exists("assets"), "Assets directory not created"
    assert os.path.exists("data"), "Data directory not created"
    print("✅ Directories created successfully")
    
    # Test image handling
    print("2. Testing image handling...")
    images = get_available_images()
    print(f"   Found {len(images)} images in assets folder")
    
    if len(images) == 0:
        print("   ⚠️  No images found. Please add some images to the assets folder.")
        print("   Supported formats: .jpg, .jpeg, .png")
    
    # Test random image selection
    random_image = get_random_image()
    if random_image:
        print(f"   ✅ Random image selected: {os.path.basename(random_image)}")
    else:
        print("   ⚠️  No random image available (no images in assets folder)")
    
    # Test sample data creation
    print("3. Testing data storage...")
    create_sample_data()
    count = get_submission_count()
    print(f"   ✅ Sample data created. Total submissions: {count}")
    
    # Test language statistics
    print("4. Testing statistics...")
    lang_stats = get_language_stats()
    print(f"   ✅ Language statistics: {lang_stats}")
    
    print("\n🎉 All basic tests completed!")

def create_sample_images_info():
    """Create information about sample images"""
    print("\n📷 Sample Images Information:")
    print("To test the application, add some images to the 'assets' folder:")
    print("   - traditional_utensil_1.jpg")
    print("   - rural_tool_1.jpg") 
    print("   - craft_item_1.jpg")
    print("   - cooking_implement_1.jpg")
    print("   - agricultural_tool_1.jpg")
    print("\nYou can use any .jpg, .jpeg, or .png files.")

def main():
    """Main test function"""
    print("🎯 Testing 'ఇది ఏమిటి? (What's This?)' Application")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        create_sample_images_info()
        
        print("\n🚀 To run the application:")
        print("   streamlit run app.py")
        
        print("\n📁 Current project structure:")
        for root, dirs, files in os.walk("."):
            level = root.replace(".", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files:
                if not file.startswith("."):
                    print(f"{subindent}{file}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 