# 🚀 Quick Setup Guide - ఇది ఏమిటి? (What's This?)

## ⚡ Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Images
Place traditional Indian object images in the `assets/` folder:
- Supported: `.jpg`, `.jpeg`, `.png`
- Recommended: 800x600 pixels
- Examples: cooking utensils, rural tools, crafts, agricultural implements

### 3. Run the Application
```bash
streamlit run app.py
```

**OR** on Windows, simply double-click `run_app.bat`

---

## 📁 What's Included

### Core Files
- `app.py` - Main Streamlit application
- `utils.py` - Helper functions
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies

### Additional Features
- `admin_dashboard.py` - Analytics dashboard (run with `streamlit run admin_dashboard.py`)
- `test_app.py` - Test script to verify setup
- `run_app.bat` - Windows startup script

### Folders
- `assets/` - Place your images here
- `data/` - User responses are stored here automatically

---

## 🎯 How It Works

1. **User sees** a random traditional object image
2. **User describes** what they think it is in their language
3. **Data is saved** to `data/user_responses.csv`
4. **User can continue** with another object or skip

---

## 📊 Features

✅ **Multi-language support** (Telugu, Hindi, Tamil, etc.)  
✅ **Mobile-responsive design**  
✅ **Offline functionality**  
✅ **Session tracking**  
✅ **Data export**  
✅ **Admin dashboard**  
✅ **Skip functionality**  

---

## 🔧 Customization

Edit `config.py` to:
- Change supported languages
- Modify UI messages
- Adjust styling
- Update image formats

---

## 📞 Need Help?

1. Run `python test_app.py` to check setup
2. Check the main `README.md` for detailed documentation
3. Ensure images are in the `assets/` folder
4. Verify Python and pip are installed

---

**Ready to preserve cultural knowledge! 🎉** 