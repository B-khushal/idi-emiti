"""
Database configuration for Cultural Corpus Platform
Optimized for Streamlit Cloud deployment
"""

import os

# Check if we're running on Streamlit Cloud
IS_STREAMLIT_CLOUD = os.getenv('STREAMLIT_SERVER_PORT') is not None

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'khushal893',  # MySQL root password
    'database': 'cultural_corpus_platform',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True
}

# Environment-based configuration (preferred for deployment)
DB_CONFIG_ENV = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'khushal893'),
    'database': os.getenv('MYSQL_DATABASE', 'cultural_corpus_platform'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True
}

# Streamlit Cloud specific configuration
if IS_STREAMLIT_CLOUD:
    # On Streamlit Cloud, we'll use environment variables or fall back to local storage
    DB_CONFIG_ENV.update({
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'cultural_corpus_platform'),
    })

def get_database_config():
    """Get the appropriate database configuration based on environment"""
    if IS_STREAMLIT_CLOUD:
        # On Streamlit Cloud, prefer environment variables
        return DB_CONFIG_ENV
    else:
        # Local development - use local config
        return DB_CONFIG

def is_mysql_available():
    """Check if MySQL is available and configured"""
    try:
        import mysql.connector
        config = get_database_config()
        
        # Try to connect to MySQL
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset'],
            collation=config['collation'],
            autocommit=config['autocommit']
        )
        connection.close()
        return True
    except Exception:
        return False

def get_storage_mode():
    """Determine the storage mode to use"""
    if is_mysql_available():
        return "mysql"
    else:
        return "json" 