#!/usr/bin/env python3
"""
Migration utility to migrate from CSV storage to MySQL database
"""

import pandas as pd
import os
import sys
from datetime import datetime
from database import DatabaseManager, CulturalCorpusDB, initialize_database
from auth import load_users, load_sessions
import hashlib
import secrets

def migrate_users_from_json(db: CulturalCorpusDB):
    """Migrate users from JSON file to MySQL database"""
    print("🔄 Migrating users from JSON to MySQL...")
    
    users = load_users()
    migrated_count = 0
    
    for user_id, user_data in users.items():
        try:
            # Create user in MySQL
            mysql_user_id = db.create_user(
                username=user_data.get('email', '').split('@')[0],  # Use email prefix as username
                email=user_data.get('email', ''),
                password_hash=user_data.get('password_hash', ''),
                full_name=user_data.get('name', ''),
                bio=user_data.get('profile_data', {}).get('cultural_background', ''),
                country='India',  # Default for cultural corpus
                region=user_data.get('profile_data', {}).get('location', ''),
                city=user_data.get('profile_data', {}).get('location', '')
            )
            
            if mysql_user_id:
                migrated_count += 1
                print(f"✅ Migrated user: {user_data.get('name', 'Unknown')}")
            else:
                print(f"❌ Failed to migrate user: {user_data.get('name', 'Unknown')}")
                
        except Exception as e:
            print(f"❌ Error migrating user {user_data.get('name', 'Unknown')}: {e}")
    
    print(f"📊 Users migration completed: {migrated_count}/{len(users)} users migrated")
    return migrated_count

def migrate_cultural_data_from_csv(db: CulturalCorpusDB):
    """Migrate cultural data from CSV to MySQL database"""
    print("🔄 Migrating cultural data from CSV to MySQL...")
    
    csv_file = "data/user_responses.csv"
    if not os.path.exists(csv_file):
        print("❌ CSV file not found")
        return 0
    
    try:
        df = pd.read_csv(csv_file)
        migrated_count = 0
        
        for index, row in df.iterrows():
            try:
                # Get or create user (for anonymous submissions, create a guest user)
                contributor_email = row.get('contributor_email', '')
                if contributor_email:
                    user = db.get_user_by_email(contributor_email)
                    if user:
                        contributor_id = user['user_id']
                    else:
                        # Create guest user
                        contributor_id = db.create_user(
                            username=f"guest_{index}",
                            email=f"guest_{index}@cultural.corpus",
                            password_hash=hashlib.sha256(secrets.token_hex(16).encode()).hexdigest(),
                            full_name=row.get('contributor_name', 'Anonymous Contributor')
                        )
                else:
                    # Create anonymous user
                    contributor_id = db.create_user(
                        username=f"anonymous_{index}",
                        email=f"anonymous_{index}@cultural.corpus",
                        password_hash=hashlib.sha256(secrets.token_hex(16).encode()).hexdigest(),
                        full_name=row.get('contributor_name', 'Anonymous Contributor')
                    )
                
                if not contributor_id:
                    print(f"❌ Failed to create contributor for row {index}")
                    continue
                
                # Get or create category
                category_name = row.get('category', 'Other')
                categories = db.get_categories()
                category_id = None
                
                for cat in categories:
                    if cat['category_name'].lower() == category_name.lower():
                        category_id = cat['category_id']
                        break
                
                if not category_id:
                    # Create new category
                    category_id = db.create_category(category_name, f"Category for {category_name}")
                
                if not category_id:
                    print(f"❌ Failed to create category for row {index}")
                    continue
                
                # Create cultural item
                item_id = db.create_cultural_item(
                    title=row.get('title', f'Cultural Item {index}'),
                    contributor_id=contributor_id,
                    category_id=category_id,
                    description_en=row.get('description', ''),
                    description_te=row.get('description', ''),  # Same as English for now
                    latitude=float(row.get('latitude', 0)) if row.get('latitude') else None,
                    longitude=float(row.get('longitude', 0)) if row.get('longitude') else None,
                    location_name=row.get('location_name', '')
                )
                
                if not item_id:
                    print(f"❌ Failed to create cultural item for row {index}")
                    continue
                
                # Add media if exists
                media_filename = row.get('media_filename', '')
                if media_filename and media_filename != 'nan':
                    media_type = row.get('media_type', 'image')
                    file_path = f"uploads/{media_type}s/{media_filename}"
                    
                    # Check if file exists
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path) // 1024  # Convert to KB
                        
                        db.add_item_media(
                            item_id=item_id,
                            media_type=media_type,
                            file_path=file_path,
                            file_size_kb=file_size
                        )
                
                # Auto-approve existing submissions
                db.approve_item(item_id, 1)  # Approve with admin user ID 1
                
                migrated_count += 1
                print(f"✅ Migrated item {index + 1}: {row.get('title', 'Untitled')}")
                
            except Exception as e:
                print(f"❌ Error migrating row {index}: {e}")
        
        print(f"📊 Cultural data migration completed: {migrated_count}/{len(df)} items migrated")
        return migrated_count
        
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return 0

def create_admin_user(db: CulturalCorpusDB):
    """Create default admin user"""
    print("🔄 Creating default admin user...")
    
    # Check if admin already exists
    admin = db.get_user_by_email('admin@cultural.corpus')
    if admin:
        print("✅ Admin user already exists")
        return admin['user_id']
    
    # Create admin user
    admin_id = db.create_user(
        username='admin',
        email='admin@cultural.corpus',
        password_hash=hashlib.sha256('admin123'.encode()).hexdigest(),
        full_name='System Administrator',
        bio='Default system administrator',
        country='India',
        region='Telangana',
        city='Hyderabad'
    )
    
    if admin_id:
        # Set as admin
        db.db.execute_update(
            "UPDATE users SET is_admin = TRUE WHERE user_id = %s",
            (admin_id,)
        )
        print("✅ Admin user created successfully")
        return admin_id
    else:
        print("❌ Failed to create admin user")
        return None

def verify_migration(db: CulturalCorpusDB):
    """Verify migration results"""
    print("🔍 Verifying migration results...")
    
    # Check users
    users = db.db.execute_query("SELECT COUNT(*) as count FROM users")
    user_count = users[0]['count'] if users else 0
    print(f"📊 Users in database: {user_count}")
    
    # Check cultural items
    items = db.db.execute_query("SELECT COUNT(*) as count FROM cultural_items")
    item_count = items[0]['count'] if items else 0
    print(f"📊 Cultural items in database: {item_count}")
    
    # Check categories
    categories = db.db.execute_query("SELECT COUNT(*) as count FROM corpus_categories")
    category_count = categories[0]['count'] if categories else 0
    print(f"📊 Categories in database: {category_count}")
    
    # Check media files
    media = db.db.execute_query("SELECT COUNT(*) as count FROM item_media")
    media_count = media[0]['count'] if media else 0
    print(f"📊 Media files in database: {media_count}")
    
    return {
        'users': user_count,
        'items': item_count,
        'categories': category_count,
        'media': media_count
    }

def main():
    """Main migration function"""
    print("🚀 Cultural Corpus Platform - MySQL Migration Tool")
    print("=" * 60)
    
    # Initialize database connection with correct credentials
    from db_config import DB_CONFIG_ENV
    db_manager = DatabaseManager(
        host=DB_CONFIG_ENV['host'],
        user=DB_CONFIG_ENV['user'],
        password=DB_CONFIG_ENV['password'],
        database=DB_CONFIG_ENV['database']
    )
    if not db_manager.connect():
        print("❌ Failed to connect to MySQL database")
        print("Please ensure MySQL is running and the database 'cultural_corpus_platform' exists")
        return False
    
    # Initialize database schema
    print("🔄 Initializing database schema...")
    if not initialize_database(db_manager):
        print("❌ Failed to initialize database schema")
        return False
    
    db = CulturalCorpusDB(db_manager)
    
    # Create admin user
    admin_id = create_admin_user(db)
    
    # Migrate users
    user_count = migrate_users_from_json(db)
    
    # Migrate cultural data
    item_count = migrate_cultural_data_from_csv(db)
    
    # Verify migration
    stats = verify_migration(db)
    
    # Close database connection
    db_manager.disconnect()
    
    print("\n" + "=" * 60)
    print("🎉 Migration completed successfully!")
    print(f"📊 Migration Summary:")
    print(f"   - Users migrated: {stats['users']}")
    print(f"   - Cultural items migrated: {stats['items']}")
    print(f"   - Categories created: {stats['categories']}")
    print(f"   - Media files linked: {stats['media']}")
    print("\n🔑 Default admin credentials:")
    print("   - Email: admin@cultural.corpus")
    print("   - Password: admin123")
    print("\n⚠️  Please change the admin password after first login!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 