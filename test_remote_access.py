#!/usr/bin/env python3
"""
Remote MySQL Access Test Script
Tests if MySQL can be accessed from remote devices
"""

import sys
import os
import socket
from db_config import DB_CONFIG, test_connection

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def test_mysql_remote_access():
    """Test MySQL remote access configuration"""
    print("🌐 Testing MySQL Remote Access Configuration")
    print("=" * 50)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"📋 Your Local IP Address: {local_ip}")
    print(f"📋 MySQL Port: 3306")
    print(f"📋 Database: {DB_CONFIG['database']}")
    print(f"📋 User: {DB_CONFIG['user']}")
    print()
    
    # Test connection
    print("🔍 Testing MySQL Connection...")
    result = test_connection()
    
    if result['status'] == 'success':
        print("✅ MySQL Connection Successful!")
        print(f"   Message: {result['message']}")
        print(f"   Connection Type: {result.get('connection_type', 'unknown')}")
        print()
        
        # Test database operations
        test_remote_operations()
        
    else:
        print("❌ MySQL Connection Failed!")
        print(f"   Error: {result['message']}")
        print()
        
        # Provide troubleshooting steps
        provide_remote_troubleshooting(local_ip)
    
    return result['status'] == 'success'

def test_remote_operations():
    """Test basic remote database operations"""
    print("🔧 Testing Remote Database Operations...")
    print("-" * 40)
    
    try:
        import mysql.connector
        from db_config import get_database_config
        
        config = get_database_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Test 1: Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables in database")
        
        # Test 2: Check user permissions
        cursor.execute("SHOW GRANTS")
        grants = cursor.fetchall()
        print(f"✅ User has {len(grants)} permissions")
        
        # Test 3: Test a simple query
        cursor.execute("SELECT COUNT(*) as user_count FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Database contains {user_count} users")
        
        cursor.close()
        connection.close()
        
        print("\n✅ All remote operations successful!")
        
    except Exception as e:
        print(f"❌ Remote operation error: {e}")

def provide_remote_troubleshooting(local_ip):
    """Provide troubleshooting steps for remote access"""
    print("🔧 Remote Access Troubleshooting Steps:")
    print("-" * 40)
    
    print("1. 🔥 Configure Windows Firewall (Run as Administrator):")
    print(f"   netsh advfirewall firewall add rule name=\"MySQL\" dir=in action=allow protocol=TCP localport=3306")
    print()
    
    print("2. 🗄️ Configure MySQL for Remote Access:")
    print("   a. Open MySQL Command Line Client")
    print("   b. Login as root")
    print("   c. Run these commands:")
    print("      CREATE USER 'cultural_user'@'%' IDENTIFIED BY 'CulturalCorpus2024!';")
    print("      GRANT ALL PRIVILEGES ON cultural_corpus_platform.* TO 'cultural_user'@'%';")
    print("      FLUSH PRIVILEGES;")
    print()
    
    print("3. 🌐 Test Remote Connection:")
    print(f"   From another device, try connecting to: {local_ip}:3306")
    print("   Username: cultural_user")
    print("   Password: CulturalCorpus2024!")
    print()
    
    print("4. 📱 Access Your Application:")
    print(f"   Streamlit App: http://{local_ip}:8501")
    print("   (Already working based on your setup)")
    print()
    
    print("5. 🔍 Verify Network Connectivity:")
    print(f"   ping {local_ip}")
    print("   telnet {local_ip} 3306")

def generate_connection_strings(local_ip):
    """Generate connection strings for different tools"""
    print("\n🔗 Connection Information for Remote Access:")
    print("=" * 50)
    
    print("📊 MySQL Connection Details:")
    print(f"   Host: {local_ip}")
    print(f"   Port: 3306")
    print(f"   Database: cultural_corpus_platform")
    print(f"   Username: cultural_user")
    print(f"   Password: CulturalCorpus2024!")
    print()
    
    print("🌐 Application URLs:")
    print(f"   Streamlit App: http://{local_ip}:8501")
    print(f"   MySQL Port: {local_ip}:3306")
    print()
    
    print("📱 Mobile/Tablet Access:")
    print(f"   Open browser and go to: http://{local_ip}:8501")
    print("   Login with admin credentials:")
    print("   Email: admin@cultural.corpus")
    print("   Password: admin123")
    print()
    
    print("💻 Database Management Tools:")
    print("   MySQL Workbench:")
    print(f"   Host: {local_ip}")
    print("   Port: 3306")
    print("   Username: cultural_user")
    print()
    
    print("🔐 Security Notes:")
    print("   ⚠️ Change default passwords after setup")
    print("   ⚠️ Use strong passwords for production")
    print("   ⚠️ Consider VPN for secure remote access")
    print("   ⚠️ Monitor access logs regularly")

def main():
    """Main function"""
    print("🚀 MySQL Remote Access Test")
    print("=" * 30)
    print()
    
    # Test remote access
    success = test_mysql_remote_access()
    
    # Get local IP for connection info
    local_ip = get_local_ip()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Remote MySQL Access is Ready!")
        print("   You can now access your database from any device.")
    else:
        print("⚠️ Remote MySQL Access needs configuration.")
        print("   Follow the troubleshooting steps above.")
    
    # Generate connection information
    generate_connection_strings(local_ip)
    
    print("\n📋 Next Steps:")
    print("   1. Configure Windows Firewall (as Administrator)")
    print("   2. Test connection from another device")
    print("   3. Access your app at the provided URL")
    print("   4. Change default passwords for security")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 