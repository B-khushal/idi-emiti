"""
Configuration file for the Cultural Corpus Collection Platform
"""

# Application Settings
APP_TITLE = "Cultural Corpus Collection Platform"
APP_ICON = "🏛️"
APP_DESCRIPTION = "Interactive platform for collecting structured, high-quality multimodal cultural corpus data"

# Admin Authentication Settings
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "cultural2024"  # Change this to a secure password
ADMIN_SESSION_KEY = "admin_authenticated"

# File Paths
ASSETS_FOLDER = "assets"
DATA_FOLDER = "data"
CSV_FILE = "data/user_responses.csv"
UPLOADS_FOLDER = "uploads"

# Supported Media Formats
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG', '.gif', '.GIF', '.webp', '.WEBP')
AUDIO_EXTENSIONS = ('.mp3', '.MP3', '.wav', '.WAV', '.ogg', '.OGG', '.m4a', '.M4A', '.flac', '.FLAC')
VIDEO_EXTENSIONS = ('.mp4', '.MP4', '.avi', '.AVI', '.mov', '.MOV', '.mkv', '.MKV', '.webm', '.WEBM')

# Combined media extensions for validation
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS + AUDIO_EXTENSIONS + VIDEO_EXTENSIONS

# File size limits (in bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB

# Supported Languages
LANGUAGES = [
    "Telugu",
    "Hindi", 
    "Tamil",
    "Kannada",
    "Bengali",
    "Malayalam",
    "Marathi",
    "Gujarati",
    "Punjabi",
    "Odia",
    "Assamese",
    "English",
    "Other"
]

# UI Configuration
MAX_FORM_WIDTH = 800
IMAGE_CAPTION = "Cultural Object"
TEXT_AREA_HEIGHT = 150

# Form Placeholders
NAME_PLACEHOLDER = "Enter your name (required)"
DESCRIPTION_PLACEHOLDER = "Describe this cultural object, its significance, usage, and cultural context"
USER_DETAILS_PLACEHOLDER = "Tell us about yourself (age, profession, cultural background, etc.) - optional"
LATITUDE_PLACEHOLDER = "Automatically detected or manually enter"
LONGITUDE_PLACEHOLDER = "Automatically detected or manually enter"
TITLE_PLACEHOLDER = "Enter a descriptive title for this cultural object"
CATEGORY_PLACEHOLDER = "Select the most appropriate category"

# Enhanced Category Options for Cultural Corpus
CATEGORIES = [
    "Cooking Utensils",
    "Agricultural Tools", 
    "Religious Items",
    "Traditional Clothing",
    "Musical Instruments",
    "Storage Containers",
    "Decorative Items",
    "Ritual Objects",
    "Transportation",
    "Weaving & Textiles",
    "Pottery & Ceramics",
    "Metalwork",
    "Woodwork",
    "Basketry",
    "Traditional Medicine",
    "Festival Items",
    "Wedding Items",
    "Folk Art",
    "Traditional Games",
    "Architecture Elements",
    "Other"
]

# Media Type Categories
MEDIA_TYPES = {
    "image": "Image",
    "audio": "Audio Recording", 
    "video": "Video Recording"
}

# Messages
SUCCESS_MESSAGE = "🎉 Thank you for your contribution to our cultural corpus!"
INFO_MESSAGE = "Your cultural knowledge helps preserve our traditions for future generations."
ERROR_NO_DESCRIPTION = "Please provide a description before submitting."
ERROR_NO_MEDIA = "No media files found. Please add some files to get started."
ERROR_INVALID_FILE = "Invalid file format. Please check supported formats."
ERROR_FILE_TOO_LARGE = "File size exceeds the maximum limit."
ERROR_NO_TITLE = "Please provide a title for this cultural object."
ERROR_NO_CATEGORY = "Please select a category for this cultural object."

# Admin Messages
ADMIN_LOGIN_ERROR = "Invalid username or password. Please try again."
ADMIN_ACCESS_DENIED = "Access denied. Admin privileges required."

# CSS Styles
CUSTOM_CSS = """
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .image-container {
        text-align: center;
        margin: 2rem 0;
    }
    .form-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    .submit-button {
        margin-top: 1rem;
    }
    .stats-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .media-upload-container {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        background-color: rgba(255, 255, 255, 0.1);
    }
    .media-upload-container:hover {
        border-color: #1f77b4;
        background-color: rgba(31, 119, 180, 0.1);
    }
    @media (max-width: 768px) {
        .form-container {
            padding: 0.5rem;
        }
    }
</style>
"""

# Analytics Settings
RECENT_RESPONSES_LIMIT = 10

# Database Schema Configuration
DATABASE_SCHEMA = {
    'timestamp': 'datetime',
    'media_filename': 'string',
    'media_type': 'string',  # image, audio, video
    'title': 'string',
    'description': 'string',
    'language': 'string',
    'contributor_name': 'string',
    'contributor_email': 'string',
    'contributor_details': 'string',
    'category': 'string',
    'latitude': 'float',
    'longitude': 'float',
    'session_id': 'string',
    'file_size': 'integer',
    'file_path': 'string',
    'validation_status': 'string',  # pending, approved, rejected
    'curator_notes': 'string'
} 