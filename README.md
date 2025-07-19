# 🏛️ Cultural Corpus Collection Platform

A comprehensive web-based platform for collecting structured, high-quality multimodal cultural corpus data with rich metadata for advanced AI and linguistic research, especially for regional Indian languages.

## 🌟 Features

### 📁 Multimodal Data Collection
- **Images**: Support for JPG, PNG, GIF, WebP formats
- **Audio**: Support for MP3, WAV, OGG, M4A, FLAC formats  
- **Video**: Support for MP4, AVI, MOV, MKV, WebM formats
- **File Validation**: Automatic format and size validation
- **Secure Storage**: Organized file storage with unique naming

### 📊 Rich Metadata Collection
- **Geolocation**: Automatic GPS detection with manual override
- **Contributor Details**: Name, email, cultural background
- **Cultural Context**: Title, description, category classification
- **Multilingual Support**: 13+ Indian languages including Telugu, Hindi, Tamil, etc.
- **Session Tracking**: Unique session management for analytics

### 🎯 Cultural Categories
Comprehensive categorization system covering:
- Cooking Utensils & Agricultural Tools
- Religious Items & Ritual Objects
- Traditional Clothing & Textiles
- Musical Instruments & Folk Art
- Storage Containers & Pottery
- Traditional Medicine & Festival Items
- And many more...

### 📈 Advanced Analytics
- **Real-time Metrics**: Submission counts, user engagement
- **Content Analysis**: Language distribution, media type trends
- **Quality Metrics**: Data completeness, validation status
- **Growth Tracking**: Daily, weekly, monthly trends
- **Geographic Analysis**: Regional distribution insights

### 🔧 Admin Panel
- **Data Management**: View, export, and curate submissions
- **Analytics Dashboard**: Comprehensive insights and reports
- **User Management**: Contributor tracking and engagement
- **Quality Control**: Validation status management

### 🔐 User Authentication System ✅ **NEW**
- **User Registration**: Secure email-based account creation with profile data
- **User Login**: Secure authentication with session management
- **User Profiles**: Personal profile management with cultural background
- **Account Settings**: Password change and account deletion
- **Session Management**: Secure token-based sessions with 7-day timeout
- **Guest Mode**: Anonymous contributions without registration
- **Profile Integration**: Automatic form pre-filling for registered users

### 🗄️ CSV-Based Storage System ✅ **NEW**
- **Simple Storage**: CSV files for easy data management
- **No Database Setup**: No complex database configuration required
- **Data Integrity**: Secure user authentication and session management
- **Performance**: Fast read/write operations for local storage
- **Portable**: Easy to backup, restore, and migrate
- **Reliable**: No database connection issues or dependencies
- **Multi-user Support**: Concurrent user access with session management

### 🌍 Multilingual Support ✅ **NEW**
- **Dynamic Language Switching**: Real-time language changes
- **Multiple Languages**: English, Hindi, Telugu support
- **Cultural Translations**: Context-aware translations
- **RTL Support**: Right-to-left language support
- **Localized UI**: All interface elements translated

### 🎮 Idi-Emiti Cultural Game ✅ **NEW**
- **Interactive Identification**: Cultural object identification game
- **Local Language Preservation**: Vocabulary preservation through gameplay
- **Audio Recording**: Pronunciation recording features
- **Cultural Context**: Regional dialect documentation
- **Engagement Analytics**: Game participation tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit 1.28.0+
- Required packages (see requirements.txt)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cultural-corpus-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **No Database Setup Required** ✅
   ```bash
   # The application uses CSV-based storage
   # CSV files are automatically created on first run
   # No additional setup needed!
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the platform**
   - Open your browser to `http://localhost:8501`
   - Start contributing cultural data!

## 📁 Project Structure

```
cultural-corpus-platform/
├── app.py                 # Main Streamlit application
├── auth.py               # Authentication system
├── csv_user_manager.py   # CSV-based user management system
├── config.py             # Configuration and constants
├── utils.py              # Core utility functions
├── admin_dashboard.py    # Admin analytics dashboard
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── SETUP_GUIDE.md       # Detailed setup instructions
├── CSV_MIGRATION_SUMMARY.md # CSV migration documentation
├── SYSTEM_OVERVIEW.md   # Technical architecture
├── PROJECT_ROADMAP.md   # Development roadmap
├── test_auth.py         # Authentication system tests
├── test_multimodal.py   # Core functionality tests
├── test_csv_system.py   # CSV system tests
├── assets/              # Sample media files
├── data/                # Data storage (CSV files)
│   ├── users.csv        # User accounts and profiles
│   ├── sessions.csv     # Active user sessions
│   └── user_responses.csv # Cultural data submissions
├── uploads/             # User uploaded files
│   ├── images/          # Image uploads
│   ├── audio/           # Audio uploads
│   └── video/           # Video uploads
└── .streamlit/          # Streamlit configuration
```

## 🎯 Usage Guide

### For Contributors

#### Guest Users (No Registration Required)
1. **Upload Media**: Choose images, audio, or video files of cultural objects
2. **Provide Context**: Fill in title, description, and cultural details
3. **Select Category**: Choose the most appropriate cultural category
4. **Add Location**: Allow GPS detection or enter coordinates manually
5. **Submit**: Your contribution is saved to the cultural corpus

#### Registered Users
1. **Create Account**: Sign up with email and profile information
2. **Login**: Access your personalized dashboard
3. **Upload Media**: Choose images, audio, or video files of cultural objects
4. **Provide Context**: Forms are pre-filled with your profile data
5. **Track Contributions**: View your submission history and statistics
6. **Manage Profile**: Update your information and preferences

### For Administrators

1. **Access Admin Panel**: Use admin credentials to access management tools
2. **Review Submissions**: View and curate incoming cultural data
3. **Generate Reports**: Access comprehensive analytics and insights
4. **Export Data**: Download curated datasets for research

## 🔧 Configuration

### Environment Variables
- `ADMIN_USERNAME`: Admin login username (default: "admin")
- `ADMIN_PASSWORD`: Admin login password (default: "cultural2024")

### File Size Limits
- **Images**: 10MB maximum
- **Audio**: 50MB maximum  
- **Video**: 100MB maximum

### Supported Languages
- Telugu, Hindi, Tamil, Kannada, Bengali
- Malayalam, Marathi, Gujarati, Punjabi
- Odia, Assamese, English, Other

## 📊 Data Schema

The platform collects structured data with the following schema:

```csv
timestamp,media_filename,media_type,title,description,language,
contributor_name,contributor_email,contributor_details,category,
latitude,longitude,session_id,file_size,file_path,
validation_status,curator_notes
```

## 🔒 Security & Privacy

- **Secure File Uploads**: Validated file types and sizes
- **User Authentication**: Secure password hashing with salt
- **Session Management**: Token-based sessions with timeout
- **Admin Authentication**: Secure admin access
- **Data Privacy**: Optional contributor information
- **Geolocation**: User-controlled location sharing
- **Account Security**: Password change and account deletion
- **Session Security**: Automatic cleanup of expired sessions

## 🛠️ Development

### Adding New Features
1. Update `config.py` for new constants
2. Extend `utils.py` for new functionality
3. Modify `app.py` for UI changes
4. Update analytics in `admin_dashboard.py`

### Database Schema Changes
1. Update `DATABASE_SCHEMA` in `config.py`
2. Modify `save_user_response()` in `utils.py`
3. Update analytics functions for new fields

### Styling Customization
- Modify CSS in `app.py` for UI changes
- Update color schemes and layouts
- Add responsive design elements

## 📈 Analytics & Insights

The platform provides comprehensive analytics:

### User Engagement
- Unique contributors and sessions
- Submission patterns and trends
- Session duration analysis

### Content Analysis
- Language distribution and diversity
- Media type popularity
- Category distribution

### Quality Metrics
- Data completeness rates
- Validation status tracking
- Geographic coverage

### Growth Trends
- Daily, weekly, monthly submissions
- Platform adoption rates
- Regional engagement patterns

## 🌍 Cultural Impact

This platform serves as a vital tool for:

- **Cultural Preservation**: Documenting traditional practices and objects
- **Linguistic Research**: Supporting regional language documentation
- **AI Development**: Providing training data for cultural AI models
- **Academic Research**: Enabling cultural studies and analysis

## 🚀 Deployment

### Streamlit Cloud Deployment
1. **Connect Repository**: Link your Git repository to Streamlit Cloud
2. **Configure Environment**: Set up environment variables
3. **Deploy**: Automatic deployment with each push
4. **Monitor**: Track performance and usage analytics

### Local Deployment
1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Configure Database**: Set up MySQL or use local storage
3. **Run Application**: `streamlit run app.py`
4. **Access Platform**: Open browser to localhost:8501

## 🤝 Contributing

We welcome contributions to improve the platform:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Swecha**: For supporting cultural preservation initiatives
- **SOAI Hackathon**: For providing the platform to showcase this project
- **Contributors**: All users who contribute cultural data
- **Open Source Community**: For the amazing tools and libraries used

---

**🏛️ Cultural Corpus Collection Platform** - Preserving cultural heritage through technology and community collaboration.
