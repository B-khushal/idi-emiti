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

### 🗄️ MySQL Database Integration ✅ **NEW**
- **Robust Database**: MySQL database with comprehensive schema
- **Scalable Storage**: Professional database management system
- **Data Integrity**: Foreign key constraints and data validation
- **Performance**: Optimized indexes for fast queries
- **Migration Tools**: Easy migration from CSV to MySQL
- **Backup Support**: Database backup and restore capabilities
- **Multi-user Support**: Concurrent user access and transactions

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

3. **Set up MySQL Database** (Recommended)
   ```bash
   # Follow the MySQL setup guide
   # See MYSQL_SETUP_GUIDE.md for detailed instructions
   
   # Quick setup:
   # 1. Install MySQL Server
   # 2. Create database: cultural_corpus_platform
   # 3. Run migration script
   python migrate_to_mysql.py
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
├── database.py           # MySQL database operations
├── config.py             # Configuration and constants
├── utils.py              # Core utility functions
├── admin_dashboard.py    # Admin analytics dashboard
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── SETUP_GUIDE.md       # Detailed setup instructions
├── MYSQL_SETUP_GUIDE.md # MySQL database setup guide
├── SYSTEM_OVERVIEW.md   # Technical architecture
├── PROJECT_ROADMAP.md   # Development roadmap
├── database_schema.sql  # MySQL database schema
├── migrate_to_mysql.py  # CSV to MySQL migration tool
├── test_auth.py         # Authentication system tests
├── test_multimodal.py   # Core functionality tests
├── test_mysql.py        # MySQL database tests
├── assets/              # Sample media files
├── data/                # Data storage (CSV + JSON)
│   ├── users.json       # User accounts and profiles (legacy)
│   ├── sessions.json    # Active user sessions (legacy)
│   └── user_responses.csv # Cultural data submissions (legacy)
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
- **Community Engagement**: Connecting cultural communities globally

## 🤝 Contributing

We welcome contributions to enhance the platform:

1. **Bug Reports**: Report issues and suggest improvements
2. **Feature Requests**: Propose new functionality
3. **Code Contributions**: Submit pull requests for enhancements
4. **Cultural Data**: Contribute cultural objects and knowledge
5. **Documentation**: Help improve guides and documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Cultural communities and contributors
- Regional language experts and researchers
- Open source community and tools
- Academic institutions supporting cultural preservation

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation and guides

---

**🏛️ Preserving Cultural Heritage, One Contribution at a Time** 