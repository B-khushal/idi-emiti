"""
Database module for Cultural Corpus Collection Platform
Handles MySQL database operations and connection management
"""

import mysql.connector
from mysql.connector import Error
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages MySQL database connections and operations"""
    
    def __init__(self, host='localhost', user='root', password='khushal893', database='cultural_corpus_platform'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                autocommit=True
            )
            logger.info("Database connection established successfully")
            return True
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """Execute a SELECT query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logger.error(f"Error executing query: {e}")
            return None
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute an INSERT, UPDATE, or DELETE query"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            cursor.close()
            return True
        except Error as e:
            logger.error(f"Error executing update: {e}")
            return False
    
    def get_last_insert_id(self) -> Optional[int]:
        """Get the last inserted ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Error as e:
            logger.error(f"Error getting last insert ID: {e}")
            return None

class CulturalCorpusDB:
    """High-level database operations for cultural corpus platform"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    # User Management
    def create_user(self, username: str, email: str, password_hash: str, 
                   full_name: str = None, bio: str = None, country: str = None,
                   region: str = None, city: str = None) -> Optional[int]:
        """Create a new user account"""
        query = """
        INSERT INTO users (username, email, password_hash, full_name, bio, country, region, city)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (username, email, password_hash, full_name, bio, country, region, city)
        
        if self.db.execute_update(query, params):
            return self.db.get_last_insert_id()
        return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email address"""
        query = "SELECT * FROM users WHERE email = %s"
        results = self.db.execute_query(query, (email,))
        return results[0] if results else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by user ID"""
        query = "SELECT * FROM users WHERE user_id = %s"
        results = self.db.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def update_user_login(self, user_id: int) -> bool:
        """Update user's last login timestamp"""
        query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = %s"
        return self.db.execute_update(query, (user_id,))
    
    def update_user_profile(self, user_id: int, **kwargs) -> bool:
        """Update user profile information"""
        allowed_fields = ['full_name', 'bio', 'country', 'region', 'city', 'display_publicly']
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                updates.append(f"{field} = %s")
                params.append(value)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        return self.db.execute_update(query, tuple(params))
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account"""
        query = "UPDATE users SET is_active = FALSE WHERE user_id = %s"
        return self.db.execute_update(query, (user_id,))
    
    # Category Management
    def get_categories(self, parent_id: int = None) -> List[Dict]:
        """Get categories, optionally filtered by parent"""
        if parent_id is None:
            query = "SELECT * FROM corpus_categories ORDER BY category_name"
            return self.db.execute_query(query) or []
        else:
            query = "SELECT * FROM corpus_categories WHERE parent_category_id = %s ORDER BY category_name"
            return self.db.execute_query(query, (parent_id,)) or []
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict]:
        """Get category by ID"""
        query = "SELECT * FROM corpus_categories WHERE category_id = %s"
        results = self.db.execute_query(query, (category_id,))
        return results[0] if results else None
    
    def create_category(self, name: str, description: str = None, parent_id: int = None) -> Optional[int]:
        """Create a new category"""
        query = """
        INSERT INTO corpus_categories (category_name, description, parent_category_id)
        VALUES (%s, %s, %s)
        """
        params = (name, description, parent_id)
        
        if self.db.execute_update(query, params):
            return self.db.get_last_insert_id()
        return None
    
    # Cultural Items Management
    def create_cultural_item(self, title: str, contributor_id: int, category_id: int,
                           description_en: str = None, description_te: str = None,
                           latitude: float = None, longitude: float = None,
                           location_name: str = None) -> Optional[int]:
        """Create a new cultural item"""
        query = """
        INSERT INTO cultural_items (title, description_en, description_te, contributor_id, 
                                   category_id, latitude, longitude, location_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (title, description_en, description_te, contributor_id, category_id,
                 latitude, longitude, location_name)
        
        if self.db.execute_update(query, params):
            return self.db.get_last_insert_id()
        return None
    
    def get_cultural_item(self, item_id: int) -> Optional[Dict]:
        """Get cultural item by ID with related data"""
        query = """
        SELECT ci.*, u.username, u.full_name, cc.category_name
        FROM cultural_items ci
        JOIN users u ON ci.contributor_id = u.user_id
        JOIN corpus_categories cc ON ci.category_id = cc.category_id
        WHERE ci.item_id = %s
        """
        results = self.db.execute_query(query, (item_id,))
        return results[0] if results else None
    
    def get_cultural_items(self, limit: int = 50, offset: int = 0, 
                          approved_only: bool = True) -> List[Dict]:
        """Get cultural items with pagination"""
        if approved_only:
            query = """
            SELECT ci.*, u.username, u.full_name, cc.category_name
            FROM cultural_items ci
            JOIN users u ON ci.contributor_id = u.user_id
            JOIN corpus_categories cc ON ci.category_id = cc.category_id
            WHERE ci.is_approved = TRUE
            ORDER BY ci.submission_date DESC
            LIMIT %s OFFSET %s
            """
        else:
            query = """
            SELECT ci.*, u.username, u.full_name, cc.category_name
            FROM cultural_items ci
            JOIN users u ON ci.contributor_id = u.user_id
            JOIN corpus_categories cc ON ci.category_id = cc.category_id
            ORDER BY ci.submission_date DESC
            LIMIT %s OFFSET %s
            """
        
        return self.db.execute_query(query, (limit, offset)) or []
    
    def get_items_by_contributor(self, contributor_id: int) -> List[Dict]:
        """Get all items by a specific contributor"""
        query = """
        SELECT ci.*, cc.category_name
        FROM cultural_items ci
        JOIN corpus_categories cc ON ci.category_id = cc.category_id
        WHERE ci.contributor_id = %s
        ORDER BY ci.submission_date DESC
        """
        return self.db.execute_query(query, (contributor_id,)) or []
    
    def approve_item(self, item_id: int, reviewer_id: int) -> bool:
        """Approve a cultural item"""
        query = """
        UPDATE cultural_items 
        SET is_approved = TRUE, reviewer_id = %s, review_date = CURRENT_TIMESTAMP
        WHERE item_id = %s
        """
        return self.db.execute_update(query, (reviewer_id, item_id))
    
    def reject_item(self, item_id: int, reviewer_id: int, reason: str) -> bool:
        """Reject a cultural item with reason"""
        query = """
        UPDATE cultural_items 
        SET is_approved = FALSE, reviewer_id = %s, review_date = CURRENT_TIMESTAMP, 
            rejection_reason = %s
        WHERE item_id = %s
        """
        return self.db.execute_update(query, (reviewer_id, reason, item_id))
    
    # Media Management
    def add_item_media(self, item_id: int, media_type: str, file_path: str,
                      thumbnail_path: str = None, description: str = None,
                      file_size_kb: int = None, duration_seconds: int = None,
                      dimensions: str = None) -> Optional[int]:
        """Add media file to a cultural item"""
        query = """
        INSERT INTO item_media (item_id, media_type, file_path, thumbnail_path, 
                               description, file_size_kb, duration_seconds, dimensions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (item_id, media_type, file_path, thumbnail_path, description,
                 file_size_kb, duration_seconds, dimensions)
        
        if self.db.execute_update(query, params):
            return self.db.get_last_insert_id()
        return None
    
    def get_item_media(self, item_id: int) -> List[Dict]:
        """Get all media files for a cultural item"""
        query = "SELECT * FROM item_media WHERE item_id = %s ORDER BY upload_date"
        return self.db.execute_query(query, (item_id,)) or []
    
    def delete_item_media(self, media_id: int) -> bool:
        """Delete a media file"""
        query = "DELETE FROM item_media WHERE media_id = %s"
        return self.db.execute_update(query, (media_id,))
    
    # Tags Management
    def create_tag(self, tag_name: str) -> Optional[int]:
        """Create a new tag"""
        query = "INSERT INTO tags (tag_name) VALUES (%s)"
        if self.db.execute_update(query, (tag_name,)):
            return self.db.get_last_insert_id()
        return None
    
    def get_or_create_tag(self, tag_name: str) -> int:
        """Get existing tag or create new one"""
        # Try to get existing tag
        query = "SELECT tag_id FROM tags WHERE tag_name = %s"
        results = self.db.execute_query(query, (tag_name,))
        if results:
            return results[0]['tag_id']
        
        # Create new tag
        return self.create_tag(tag_name)
    
    def add_item_tags(self, item_id: int, tag_names: List[str]) -> bool:
        """Add tags to a cultural item"""
        for tag_name in tag_names:
            tag_id = self.get_or_create_tag(tag_name)
            if tag_id:
                query = "INSERT IGNORE INTO item_tags (item_id, tag_id) VALUES (%s, %s)"
                self.db.execute_update(query, (item_id, tag_id))
        return True
    
    def get_item_tags(self, item_id: int) -> List[Dict]:
        """Get all tags for a cultural item"""
        query = """
        SELECT t.* FROM tags t
        JOIN item_tags it ON t.tag_id = it.tag_id
        WHERE it.item_id = %s
        ORDER BY t.tag_name
        """
        return self.db.execute_query(query, (item_id,)) or []
    
    # Comments Management
    def add_comment(self, item_id: int, user_id: int, comment_text: str) -> Optional[int]:
        """Add a comment to a cultural item"""
        query = """
        INSERT INTO comments (item_id, user_id, comment_text)
        VALUES (%s, %s, %s)
        """
        params = (item_id, user_id, comment_text)
        
        if self.db.execute_update(query, params):
            return self.db.get_last_insert_id()
        return None
    
    def get_item_comments(self, item_id: int) -> List[Dict]:
        """Get all comments for a cultural item"""
        query = """
        SELECT c.*, u.username, u.full_name
        FROM comments c
        JOIN users u ON c.user_id = u.user_id
        WHERE c.item_id = %s AND c.is_moderated = FALSE
        ORDER BY c.comment_date DESC
        """
        return self.db.execute_query(query, (item_id,)) or []
    
    # Analytics and Statistics
    def get_submission_stats(self) -> Dict:
        """Get submission statistics"""
        stats = {}
        
        # Total items
        query = "SELECT COUNT(*) as total FROM cultural_items"
        results = self.db.execute_query(query)
        stats['total_items'] = results[0]['total'] if results else 0
        
        # Approved items
        query = "SELECT COUNT(*) as approved FROM cultural_items WHERE is_approved = TRUE"
        results = self.db.execute_query(query)
        stats['approved_items'] = results[0]['approved'] if results else 0
        
        # Pending items
        query = "SELECT COUNT(*) as pending FROM cultural_items WHERE is_approved = FALSE"
        results = self.db.execute_query(query)
        stats['pending_items'] = results[0]['pending'] if results else 0
        
        # Total users
        query = "SELECT COUNT(*) as users FROM users WHERE is_active = TRUE"
        results = self.db.execute_query(query)
        stats['total_users'] = results[0]['users'] if results else 0
        
        # Media counts
        query = "SELECT media_type, COUNT(*) as count FROM item_media GROUP BY media_type"
        results = self.db.execute_query(query)
        stats['media_counts'] = {row['media_type']: row['count'] for row in results} if results else {}
        
        return stats
    
    def get_category_stats(self) -> List[Dict]:
        """Get statistics by category"""
        query = """
        SELECT cc.category_name, COUNT(ci.item_id) as item_count
        FROM corpus_categories cc
        LEFT JOIN cultural_items ci ON cc.category_id = ci.category_id AND ci.is_approved = TRUE
        GROUP BY cc.category_id, cc.category_name
        ORDER BY item_count DESC
        """
        return self.db.execute_query(query) or []
    
    def get_recent_submissions(self, limit: int = 10) -> List[Dict]:
        """Get recent cultural item submissions"""
        query = """
        SELECT ci.*, u.username, u.full_name, cc.category_name
        FROM cultural_items ci
        JOIN users u ON ci.contributor_id = u.user_id
        JOIN corpus_categories cc ON ci.category_id = cc.category_id
        ORDER BY ci.submission_date DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,)) or []

# Database initialization
def initialize_database(db_manager: DatabaseManager) -> bool:
    """Initialize database with schema and initial data"""
    try:
        # Read and execute the SQL schema
        schema_file = "database_schema.sql"
        if os.path.exists(schema_file):
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Split by semicolon and execute each statement
            statements = schema_sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    db_manager.execute_update(statement)
            
            logger.info("Database schema initialized successfully")
            return True
        else:
            logger.error("Database schema file not found")
            return False
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

# Global database instance
_db_manager = None
_db = None

def get_database() -> CulturalCorpusDB:
    """Get global database instance"""
    global _db_manager, _db
    
    if _db is None:
        # Initialize database connection
        _db_manager = DatabaseManager()
        if _db_manager.connect():
            _db = CulturalCorpusDB(_db_manager)
        else:
            raise Exception("Failed to connect to database")
    
    return _db

def close_database():
    """Close global database connection"""
    global _db_manager
    if _db_manager:
        _db_manager.disconnect() 