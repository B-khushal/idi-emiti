"""
Database configuration for Cultural Corpus Platform
"""

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

# Alternative: Use environment variables
import os

DB_CONFIG_ENV = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'khushal893'),  # MySQL root password
    'database': os.getenv('MYSQL_DATABASE', 'cultural_corpus_platform'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True
} 