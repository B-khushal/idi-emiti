#!/usr/bin/env python3
"""
Simple database connection test
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    """Test database connection"""
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Enter your MySQL root password here
            database='cultural_corpus_platform',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database!")
            
            # Get database info
            db_info = connection.get_server_info()
            print(f"📊 MySQL Server version: {db_info}")
            
            # Create cursor
            cursor = connection.cursor()
            
            # Test query - get categories count
            cursor.execute("SELECT COUNT(*) FROM corpus_categories")
            categories_count = cursor.fetchone()[0]
            print(f"📁 Categories in database: {categories_count}")
            
            # Test query - get users count
            cursor.execute("SELECT COUNT(*) FROM users")
            users_count = cursor.fetchone()[0]
            print(f"👥 Users in database: {users_count}")
            
            # Test query - get tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"🗂️ Tables in database: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            
            cursor.close()
            connection.close()
            print("✅ Database connection test completed successfully!")
            return True
            
    except Error as e:
        print(f"❌ Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing MySQL Database Connection")
    print("=" * 50)
    test_connection() 