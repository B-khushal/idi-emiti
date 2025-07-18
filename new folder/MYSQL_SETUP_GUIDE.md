# 🗄️ MySQL Database Setup Guide

This guide will help you set up MySQL database for the Cultural Corpus Collection Platform.

## 📋 Prerequisites

- **MySQL Server** (version 8.0 or higher recommended)
- **Python 3.8+** with pip
- **MySQL Connector for Python**

## 🚀 Installation Steps

### 1. Install MySQL Server

#### Windows
1. Download MySQL Installer from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
2. Run the installer and follow the setup wizard
3. Choose "Developer Default" or "Server only" installation
4. Set root password (remember this!)
5. Complete the installation

#### macOS
```bash
# Using Homebrew
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation
mysql_secure_installation
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install MySQL
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 2. Create Database

1. **Connect to MySQL**:
   ```bash
   mysql -u root -p
   ```

2. **Create database**:
   ```sql
   CREATE DATABASE cultural_corpus_platform 
   CHARACTER SET utf8mb4 
   COLLATE utf8mb4_unicode_ci;
   ```

3. **Create user** (optional but recommended):
   ```sql
   CREATE USER 'cultural_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON cultural_corpus_platform.* TO 'cultural_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Exit MySQL**:
   ```sql
   EXIT;
   ```

### 3. Install Python Dependencies

```bash
# Install MySQL connector
pip install mysql-connector-python>=8.0.0

# Or install all requirements
pip install -r requirements.txt
```

### 4. Configure Database Connection

Edit the database connection settings in `database.py`:

```python
# Default settings (modify as needed)
db_manager = DatabaseManager(
    host='localhost',           # MySQL server host
    user='root',               # MySQL username
    password='your_password',   # MySQL password
    database='cultural_corpus_platform'  # Database name
)
```

If you created a separate user:
```python
db_manager = DatabaseManager(
    host='localhost',
    user='cultural_user',
    password='your_password',
    database='cultural_corpus_platform'
)
```

## 🔧 Database Initialization

### Option 1: Automatic Initialization (Recommended)

Run the migration script to set up the database schema and migrate existing data:

```bash
python migrate_to_mysql.py
```

This will:
- Create all necessary tables
- Insert initial categories
- Create default admin user
- Migrate existing CSV data (if any)
- Migrate existing user accounts (if any)

### Option 2: Manual Schema Creation

If you prefer to create the schema manually:

1. **Connect to MySQL**:
   ```bash
   mysql -u root -p cultural_corpus_platform
   ```

2. **Run the schema file**:
   ```sql
   SOURCE database_schema.sql;
   ```

3. **Verify tables**:
   ```sql
   SHOW TABLES;
   ```

## 🧪 Testing the Setup

Run the MySQL database tests to verify everything is working:

```bash
python test_mysql.py
```

Expected output:
```
🗄️ MySQL Database Integration - Test Suite
============================================================

==================== Database Connection ====================
🧪 Testing database connection...
✅ Database connection successful
✅ Database Connection - PASSED

==================== Database Schema ====================
🧪 Testing database schema initialization...
✅ Database schema initialized successfully
✅ Database Schema - PASSED

... (more tests)

📊 Test Results: 8/8 tests passed
🎉 All MySQL database tests passed! Database integration is ready.
```

## 🔐 Default Admin Credentials

After running the migration script, you'll have a default admin user:

- **Email**: `admin@cultural.corpus`
- **Password**: `admin123`

⚠️ **Important**: Change the admin password after first login!

## 📊 Database Schema Overview

The database includes the following tables:

### Core Tables
- **`users`** - User accounts and profiles
- **`corpus_categories`** - Cultural item categories
- **`cultural_items`** - Main cultural item data
- **`item_media`** - Media files (images, audio, video)

### Supporting Tables
- **`tags`** - Flexible tagging system
- **`item_tags`** - Many-to-many relationship between items and tags
- **`comments`** - User comments on cultural items

### Features
- **Multilingual Support**: UTF8MB4 encoding for all Indian scripts
- **Geolocation**: Latitude/longitude fields for spatial queries
- **Moderation**: Approval workflow for cultural items
- **Media Management**: Support for multiple media files per item
- **User Management**: Complete user profile system

## 🔧 Configuration Options

### Database Connection Settings

You can modify database settings in `database.py`:

```python
class DatabaseManager:
    def __init__(self, 
                 host='localhost',           # Database host
                 user='root',               # Database user
                 password='',               # Database password
                 database='cultural_corpus_platform'):  # Database name
```

### Environment Variables (Optional)

You can use environment variables for database configuration:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=cultural_corpus_platform
```

Then modify `database.py` to use them:

```python
import os

class DatabaseManager:
    def __init__(self, 
                 host=os.getenv('MYSQL_HOST', 'localhost'),
                 user=os.getenv('MYSQL_USER', 'root'),
                 password=os.getenv('MYSQL_PASSWORD', ''),
                 database=os.getenv('MYSQL_DATABASE', 'cultural_corpus_platform')):
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Connection Refused
```
Error connecting to database: 2003 (HY000): Can't connect to MySQL server
```

**Solution**:
- Ensure MySQL service is running
- Check if MySQL is listening on the correct port (default: 3306)
- Verify firewall settings

#### 2. Access Denied
```
Error connecting to database: 1045 (28000): Access denied for user
```

**Solution**:
- Verify username and password
- Check user privileges
- Ensure user can connect from your host

#### 3. Database Not Found
```
Error connecting to database: 1049 (42000): Unknown database
```

**Solution**:
- Create the database first
- Check database name spelling
- Verify user has access to the database

#### 4. Character Set Issues
```
Error: Incorrect string value
```

**Solution**:
- Ensure database uses UTF8MB4 character set
- Check table collation settings
- Verify MySQL configuration

### Performance Optimization

#### 1. Indexes
The schema includes optimized indexes for common queries:
- User email and username lookups
- Cultural item searches and filtering
- Geographic queries
- Media type filtering

#### 2. Connection Pooling
For production use, consider implementing connection pooling:

```python
import mysql.connector.pooling

config = {
    'pool_name': 'cultural_pool',
    'pool_size': 5,
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'cultural_corpus_platform'
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(**config)
```

#### 3. Backup Strategy
Regular backups are essential:

```bash
# Create backup
mysqldump -u root -p cultural_corpus_platform > backup_$(date +%Y%m%d).sql

# Restore backup
mysql -u root -p cultural_corpus_platform < backup_20240101.sql
```

## 📈 Migration from CSV

If you have existing CSV data, the migration script will:

1. **Preserve all data** from CSV files
2. **Create user accounts** for contributors
3. **Link media files** to database records
4. **Maintain relationships** between data
5. **Auto-approve** existing submissions

### Migration Process

```bash
# Run migration
python migrate_to_mysql.py

# Verify migration
python test_mysql.py
```

### Post-Migration

After successful migration:

1. **Test the application** with new database
2. **Verify all data** is accessible
3. **Update any hardcoded paths** if needed
4. **Backup the database** for safety

## 🎉 Next Steps

Once MySQL is set up and tested:

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Login as admin** and change default password

3. **Test all features**:
   - User registration and login
   - Cultural item submission
   - Media upload
   - Admin panel

4. **Monitor performance** and adjust settings as needed

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Run the test suite** to identify specific problems
3. **Review MySQL error logs** for detailed information
4. **Check the project documentation** for additional help

---

**🎯 Your Cultural Corpus Platform is now ready with a robust MySQL database!** 