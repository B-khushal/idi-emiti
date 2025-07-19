# 🌐 Enable Remote MySQL Access - Simple Steps

## Current Status ✅
- **Your App**: Working perfectly at `http://192.168.1.6:8501`
- **Database**: MySQL working locally
- **Goal**: Access from any device

## 🎯 To Enable Remote Access (3 Simple Steps)

### Step 1: Create Remote MySQL User
**Open Command Prompt as Administrator and run:**
```cmd
mysql -u root -p
```
Enter password: `khushal893`

Then run these commands:
```sql
CREATE USER 'cultural_user'@'%' IDENTIFIED BY 'CulturalCorpus2024!';
GRANT ALL PRIVILEGES ON cultural_corpus_platform.* TO 'cultural_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

### Step 2: Allow MySQL Port in Firewall
**In the same Administrator Command Prompt:**
```cmd
netsh advfirewall firewall add rule name="MySQL Remote Access" dir=in action=allow protocol=TCP localport=3306
```

### Step 3: Switch to Remote Configuration
**Edit `db_config.py` and change:**
```python
DB_CONFIG = {
    'host': '10.39.96.219',  # Change from 'localhost' to your IP
    'user': 'cultural_user',  # Change from 'root' to 'cultural_user'
    'password': 'CulturalCorpus2024!',  # Change to new password
    # ... rest stays the same
}
```

## 🎉 After These Steps

### Access from Any Device:
- **Mobile/Tablet**: Open browser → `http://192.168.1.6:8501`
- **Laptop/Desktop**: Same URL
- **Admin Login**: 
  - Email: `admin@cultural.corpus`
  - Password: `admin123`

### Database Management:
- **MySQL Workbench**: Connect to `192.168.1.6:3306`
- **Username**: `cultural_user`
- **Password**: `CulturalCorpus2024!`

## 🔧 Quick Test
After completing the steps, run:
```cmd
python test_remote_access.py
```

## ⚠️ Important Notes
- Your app is already accessible remotely at `http://192.168.1.6:8501`
- Only the database needs remote configuration
- Change default passwords after setup
- Keep your network secure

## 🚀 Ready to Start?
Your Cultural Corpus Platform is already working! Follow the steps above when you want to enable remote database access. 