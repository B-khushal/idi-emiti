@echo off
echo ========================================
echo    MySQL Remote Access Setup Script
echo ========================================
echo.

echo This script will help you configure MySQL for remote access.
echo Please run this as Administrator.
echo.

pause

echo.
echo Step 1: Creating MySQL remote user...
echo.

REM Create the remote user
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'cultural_user'@'%%' IDENTIFIED BY 'CulturalCorpus2024!'; GRANT ALL PRIVILEGES ON cultural_corpus_platform.* TO 'cultural_user'@'%%'; FLUSH PRIVILEGES;"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create MySQL user.
    echo Please run MySQL commands manually:
    echo.
    echo mysql -u root -p
    echo CREATE USER 'cultural_user'@'%%' IDENTIFIED BY 'CulturalCorpus2024!';
    echo GRANT ALL PRIVILEGES ON cultural_corpus_platform.* TO 'cultural_user'@'%%';
    echo FLUSH PRIVILEGES;
    echo EXIT;
    echo.
    pause
    goto :end
)

echo.
echo Step 2: Configuring Windows Firewall...
echo.

REM Add firewall rule for MySQL
netsh advfirewall firewall add rule name="MySQL Remote Access" dir=in action=allow protocol=TCP localport=3306

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Failed to configure firewall automatically.
    echo Please run this command manually as Administrator:
    echo netsh advfirewall firewall add rule name="MySQL Remote Access" dir=in action=allow protocol=TCP localport=3306
    echo.
) else (
    echo Firewall rule added successfully.
)

echo.
echo Step 3: Testing remote access...
echo.

REM Test the connection
python test_remote_access.py

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Your MySQL database should now be accessible remotely.
echo.
echo Connection Details:
echo - Host: 10.39.96.219
echo - Port: 3306
echo - Database: cultural_corpus_platform
echo - Username: cultural_user
echo - Password: CulturalCorpus2024!
echo.
echo Application URL: http://10.39.96.219:8501
echo.
echo IMPORTANT: Change default passwords for security!
echo.

:end
pause 