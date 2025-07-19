"""
Configuration file for Cultural Corpus Collection Platform
Contains all app settings, constants, and language configurations
"""

import os
from pathlib import Path

# App Configuration
APP_TITLE = "Cultural Corpus Collection Platform"
APP_ICON = "🏛️"
APP_DESCRIPTION = "Preserving Cultural Heritage Through Multimodal Data Collection"

# Admin Configuration
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_SESSION_KEY = "admin_authenticated"

# File Paths
ASSETS_FOLDER = "assets"
DATA_FOLDER = "data"
CSV_FILE = os.path.join(DATA_FOLDER, "user_responses.csv")
UPLOADS_FOLDER = "uploads"

# File Extensions
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
AUDIO_EXTENSIONS = ('.mp3', '.wav', '.ogg', '.m4a', '.flac')
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm')

# All supported media extensions (for filtering)
MEDIA_EXTENSIONS = tuple(IMAGE_EXTENSIONS + AUDIO_EXTENSIONS + VIDEO_EXTENSIONS)

# Form Configuration
MAX_FORM_WIDTH = 800
IMAGE_CAPTION = "Upload an image of the cultural object"
TEXT_AREA_HEIGHT = 150

# Placeholders
NAME_PLACEHOLDER = "Enter your name"
DESCRIPTION_PLACEHOLDER = "Describe the cultural object, its significance, and usage..."
USER_DETAILS_PLACEHOLDER = "Share your cultural background, profession, and location..."
LATITUDE_PLACEHOLDER = "Enter latitude (optional)"
LONGITUDE_PLACEHOLDER = "Enter longitude (optional)"
TITLE_PLACEHOLDER = "Enter a title for this cultural object"
CATEGORY_PLACEHOLDER = "Select a category"

# Categories
CATEGORIES = [
    "Traditional Clothing & Textiles",
    "Musical Instruments",
    "Cooking Utensils & Tools",
    "Religious & Ceremonial Items",
    "Agricultural Tools",
    "Art & Crafts",
    "Jewelry & Accessories",
    "Games & Toys",
    "Architecture & Structures",
    "Food & Beverages",
    "Other"
]

# Languages
LANGUAGES = [
    "English",
    "Hindi",
    "Telugu",
    "Tamil",
    "Bengali",
    "Marathi",
    "Gujarati",
    "Kannada",
    "Malayalam",
    "Punjabi",
    "Odia",
    "Assamese",
    "Sanskrit",
    "Urdu"
]

# Language Configuration
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'हिंदी',
    'te': 'తెలుగు',
    'ta': 'தமிழ்',
    'bn': 'বাংলা',
    'mr': 'मराठी',
    'gu': 'ગુજરાતી',
    'kn': 'ಕನ್ನಡ',
    'ml': 'മലയാളം',
    'pa': 'ਪੰਜਾਬੀ',
    'or': 'ଓଡ଼ିଆ',
    'as': 'অসমীয়া',
    'sa': 'संस्कृतम्',
    'ur': 'اردو'
}

# Language Translations
TRANSLATIONS = {
    'en': {
        'app_title': 'Cultural Corpus Collection Platform',
        'app_description': 'Preserving Cultural Heritage Through Multimodal Data Collection',
        'welcome': 'Welcome',
        'sign_in': 'Sign In',
        'sign_up': 'Sign Up',
        'logout': 'Logout',
        'my_profile': 'My Profile',
        'start_contributing': 'Start Contributing',
        'cultural_corpus': 'Cultural Corpus Collection',
        'idi_emiti': 'Idi-Emiti (What is this?)',
        'analytics': 'Analytics Dashboard',
        'admin_panel': 'Admin Panel',
        'system_status': 'System Status',
        'using_local_storage': 'Using Local JSON Storage',
        'connected_to_csv': 'Connected to CSV Storage System',
'csv_setup_guide': 'Using CSV-based storage system',
'csv_setup_instructions': '''**CSV-based storage system:**

The application uses CSV files for data storage:
- User data stored in `data/users.csv`
- Session data stored in `data/sessions.csv`
- User responses stored in `data/user_responses.csv`

No additional setup required.''',
        'about_platform': 'About Our Platform',
        'platform_description': '''The Cultural Corpus Collection Platform is a comprehensive digital repository designed to preserve and document 
cultural heritage through multimodal data collection. Our platform enables communities to share, document, and 
preserve their cultural traditions, languages, and artifacts for future generations.''',
        'platform_impact': 'Platform Impact',
        'cultural_submissions': 'Cultural Submissions',
        'active_contributors': 'Active Contributors',
        'languages_documented': 'Languages Documented',
        'cultural_identifications': 'Cultural Identifications',
        'platform_features': 'Platform Features',
        'multimodal_upload': 'Multimodal media upload (images, audio, video)',
        'local_language': 'Local language and dialect documentation',
        'cultural_context': 'Cultural context and usage information',
        'geographic_tracking': 'Geographic location tracking',
        'start_collection': 'Start Collection',
        'cultural_identification': 'Cultural object identification',
        'vocabulary_preservation': 'Local language vocabulary preservation',
        'audio_pronunciation': 'Audio pronunciation recordings',
        'dialect_documentation': 'Regional dialect documentation',
        'try_idi_emiti': 'Try Idi-Emiti',
        'real_time_stats': 'Real-time platform statistics',
        'language_analytics': 'Language and dialect analytics',
        'user_engagement': 'User engagement metrics',
        'data_quality': 'Data quality assessment',
        'view_analytics': 'View Analytics',
        'secure_login': 'Secure login and registration',
        'profile_management': 'User profile management',
        'contribution_tracking': 'Contribution history tracking',
        'csv_storage': 'CSV-based storage system',
        'technology_stack': 'Technology Stack',
        'get_started': 'Get Started',
        'explore_features': 'Explore Features',
        'ready_to_start': 'Ready to Start?',
        'join_thousands': 'Join thousands of contributors preserving cultural heritage worldwide',
        'create_account': 'Create Account',
        'continue_journey': 'Continue your cultural preservation journey',
        'upload_content': 'Upload Content',
        'play_idi_emiti': 'Play Idi-Emiti',
        'language_selector': 'Select Language',
        'change_language': 'Change Language',
        # Form fields and buttons
        'title': 'Title',
        'description': 'Description',
        'name': 'Name',
        'email': 'Email',
        'category': 'Category',
        'language': 'Language',
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'submit': 'Submit',
        'upload': 'Upload',
        'choose_file': 'Choose File',
        'select_category': 'Select Category',
        'select_language': 'Select Language',
        'optional': 'Optional',
        'required': 'Required',
        # Page titles and headers
        'upload_cultural_media': 'Upload Cultural Media',
        'cultural_information': 'Cultural Information',
        'media_preview': 'Media Preview',
        'idi_emiti_game': 'Idi-Emiti Game',
        'analytics_dashboard': 'Analytics Dashboard',
        'admin_panel': 'Admin Panel',
        'user_profile': 'User Profile',
        'login_page': 'Login Page',
        'signup_page': 'Sign Up Page',
        # Messages and notifications
        'upload_success': 'Upload successful!',
        'upload_error': 'Upload error',
        'file_too_large': 'File too large',
        'invalid_file_type': 'Invalid file type',
        'please_login': 'Please log in',
        'access_denied': 'Access denied',
        'authentication_required': 'Authentication required',
        'please_fill_all_fields': 'Please fill all fields',
        'thank_you_contribution': 'Thank you for your contribution!',
        # Idi-Emiti specific
        'what_is_this': 'What is this?',
        'record_pronunciation': 'Record Pronunciation',
        'skip_object': 'Skip Object',
        'new_object': 'New Object',
        'reset_recording': 'Reset Recording',
        're_record': 'Re-record',
        'submit_identification': 'Submit Identification',
        'local_name': 'Local Name',
        'pronunciation_guide': 'Pronunciation Guide',
        'cultural_context': 'Cultural Context',
        'dialect_variation': 'Dialect Variation',
        # Analytics specific
        'total_submissions': 'Total Submissions',
        'total_contributors': 'Total Contributors',
        'total_languages': 'Total Languages',
        'recent_activity': 'Recent Activity',
        'language_distribution': 'Language Distribution',
        'media_type_distribution': 'Media Type Distribution',
        'category_distribution': 'Category Distribution',
        'growth_trends': 'Growth Trends',
        'quality_metrics': 'Quality Metrics',
        'user_engagement': 'User Engagement',
        # Admin specific
        'admin_login': 'Admin Login',
        'username': 'Username',
        'password': 'Password',
        'login': 'Login',
        'admin_dashboard': 'Admin Dashboard',
        'manage_submissions': 'Manage Submissions',
        'approve_submission': 'Approve Submission',
        'reject_submission': 'Reject Submission',
        'curator_notes': 'Curator Notes',
        'validation_status': 'Validation Status',
        'pending': 'Pending',
        'approved': 'Approved',
        'rejected': 'Rejected',
        # Profile specific
        'edit_profile': 'Edit Profile',
        'change_password': 'Change Password',
        'delete_account': 'Delete Account',
        'account_settings': 'Account Settings',
        'contribution_history': 'Contribution History',
        'personal_info': 'Personal Information',
        'cultural_background': 'Cultural Background',
        'profession': 'Profession',
        'location': 'Location',
        'save_changes': 'Save Changes',
        'cancel': 'Cancel',
        'confirm': 'Confirm',
        'delete': 'Delete',
        # Navigation
        'home': 'Home',
        'navigation': 'Navigation',
        'choose_page': 'Choose a page',
        'back_to_home': 'Back to Home',
        'next': 'Next',
        'previous': 'Previous',
        # Common actions
        'view': 'View',
        'edit': 'Edit',
        'delete': 'Delete',
        'download': 'Download',
        'share': 'Share',
        'search': 'Search',
        'filter': 'Filter',
        'sort': 'Sort',
        'refresh': 'Refresh',
        'export': 'Export',
        'import': 'Import',
        # Status messages
        'loading': 'Loading...',
        'saving': 'Saving...',
        'processing': 'Processing...',
        'success': 'Success!',
        'error': 'Error',
        'warning': 'Warning',
        'info': 'Info',
        'no_data': 'No data',
        'no_results': 'No results',
        'try_again': 'Try again',
        'contact_support': 'Contact support'
    },
    'hi': {
        'app_title': 'सांस्कृतिक कोष संग्रहण मंच',
        'app_description': 'बहु-माध्यम डेटा संग्रहण के माध्यम से सांस्कृतिक विरासत का संरक्षण',
        'welcome': 'स्वागत है',
        'sign_in': 'साइन इन करें',
        'sign_up': 'साइन अप करें',
        'logout': 'लॉगआउट',
        'my_profile': 'मेरा प्रोफाइल',
        'start_contributing': 'योगदान शुरू करें',
        'cultural_corpus': 'सांस्कृतिक कोष संग्रहण',
        'idi_emiti': 'इदि-एमिति (यह क्या है?)',
        'analytics': 'विश्लेषण डैशबोर्ड',
        'admin_panel': 'प्रशासक पैनल',
        'system_status': 'सिस्टम स्थिति',
        'using_local_storage': 'स्थानीय JSON भंडारण का उपयोग कर रहे हैं',
        'connected_to_csv': 'CSV स्टोरेज सिस्टम से जुड़ा हुआ',
        'csv_setup_guide': 'CSV-आधारित स्टोरेज सिस्टम का उपयोग कर रहे हैं',
        'csv_setup_instructions': '''**CSV-आधारित स्टोरेज सिस्टम:**

एप्लिकेशन डेटा स्टोरेज के लिए CSV फाइलों का उपयोग करती है:
- उपयोगकर्ता डेटा `data/users.csv` में संग्रहित
- सेशन डेटा `data/sessions.csv` में संग्रहित
- उपयोगकर्ता प्रतिक्रियाएं `data/user_responses.csv` में संग्रहित

कोई अतिरिक्त सेटअप आवश्यक नहीं।''',
        'about_platform': 'हमारे मंच के बारे में',
        'platform_description': '''सांस्कृतिक कोष संग्रहण मंच एक व्यापक डिजिटल भंडार है जो बहु-माध्यम डेटा संग्रहण के माध्यम से 
सांस्कृतिक विरासत को संरक्षित और दस्तावेज करने के लिए डिज़ाइन किया गया है। हमारा मंच समुदायों को साझा करने, दस्तावेज करने और 
भविष्य की पीढ़ियों के लिए उनकी सांस्कृतिक परंपराओं, भाषाओं और कलाकृतियों को संरक्षित करने में सक्षम बनाता है।''',
        'platform_impact': 'मंच का प्रभाव',
        'cultural_submissions': 'सांस्कृतिक प्रस्तुतियां',
        'active_contributors': 'सक्रिय योगदानकर्ता',
        'languages_documented': 'दस्तावेजीकृत भाषाएं',
        'cultural_identifications': 'सांस्कृतिक पहचान',
        'platform_features': 'मंच की विशेषताएं',
        'multimodal_upload': 'बहु-माध्यम मीडिया अपलोड (छवियां, ऑडियो, वीडियो)',
        'local_language': 'स्थानीय भाषा और बोली दस्तावेजीकरण',
        'cultural_context': 'सांस्कृतिक संदर्भ और उपयोग की जानकारी',
        'geographic_tracking': 'भौगोलिक स्थान ट्रैकिंग',
        'start_collection': 'संग्रहण शुरू करें',
        'cultural_identification': 'सांस्कृतिक वस्तु पहचान',
        'vocabulary_preservation': 'स्थानीय भाषा शब्दावली संरक्षण',
        'audio_pronunciation': 'ऑडियो उच्चारण रिकॉर्डिंग',
        'dialect_documentation': 'क्षेत्रीय बोली दस्तावेजीकरण',
        'try_idi_emiti': 'इदि-एमिति आज़माएं',
        'real_time_stats': 'रीयल-टाइम मंच आंकड़े',
        'language_analytics': 'भाषा और बोली विश्लेषण',
        'user_engagement': 'उपयोगकर्ता जुड़ाव मेट्रिक्स',
        'data_quality': 'डेटा गुणवत्ता मूल्यांकन',
        'view_analytics': 'विश्लेषण देखें',
        'secure_login': 'सुरक्षित लॉगिन और पंजीकरण',
        'profile_management': 'उपयोगकर्ता प्रोफाइल प्रबंधन',
        'contribution_tracking': 'योगदान इतिहास ट्रैकिंग',
        'csv_storage': 'CSV-आधारित भंडारण प्रणाली',
        'technology_stack': 'तकनीकी स्टैक',
        'get_started': 'शुरू करें',
        'explore_features': 'विशेषताएं देखें',
        'ready_to_start': 'शुरू करने के लिए तैयार?',
        'join_thousands': 'दुनिया भर में सांस्कृतिक विरासत को संरक्षित करने वाले हजारों योगदानकर्ताओं में शामिल हों',
        'create_account': 'खाता बनाएं',
        'continue_journey': 'अपनी सांस्कृतिक संरक्षण यात्रा जारी रखें',
        'upload_content': 'सामग्री अपलोड करें',
        'play_idi_emiti': 'इदि-एमिति खेलें',
        'language_selector': 'भाषा चुनें',
        'change_language': 'भाषा बदलें',
        # Form fields and buttons
        'title': 'शीर्षक',
        'description': 'विवरण',
        'name': 'नाम',
        'email': 'ईमेल',
        'category': 'वर्ग',
        'language': 'भाषा',
        'latitude': 'अक्षांश',
        'longitude': 'रेखांश',
        'submit': 'जमा करें',
        'upload': 'अपलोड करें',
        'choose_file': 'फाइल चुनें',
        'select_category': 'वर्ग चुनें',
        'select_language': 'भाषा चुनें',
        'optional': 'वैकल्पिक',
        'required': 'आवश्यक',
        # Page titles and headers
        'upload_cultural_media': 'सांस्कृतिक मीडिया अपलोड करें',
        'cultural_information': 'सांस्कृतिक जानकारी',
        'media_preview': 'मीडिया पूर्वावलोकन',
        'idi_emiti_game': 'इदि-एमिति खेल',
        'analytics_dashboard': 'विश्लेषण डैशबोर्ड',
        'admin_panel': 'प्रशासक पैनल',
        'user_profile': 'उपयोगकर्ता प्रोफ़ाइल',
        'login_page': 'लॉगिन पेज',
        'signup_page': 'साइनअप पेज',
        # Messages and notifications
        'upload_success': 'अपलोड सफल!',
        'upload_error': 'अपलोड त्रुटि',
        'file_too_large': 'फाइल बहुत बड़ी है',
        'invalid_file_type': 'अमान्य फाइल प्रकार',
        'please_login': 'कृपया लॉगिन करें',
        'access_denied': 'प्रवेश अस्वीकृत',
        'authentication_required': 'प्रमाणन आवश्यक',
        'please_fill_all_fields': 'कृपया सभी फ़ील्ड भरें',
        'thank_you_contribution': 'आपके योगदान के लिए धन्यवाद!',
        # Idi-Emiti specific
        'what_is_this': 'यह क्या है?',
        'record_pronunciation': 'उच्चारण रिकॉर्ड करें',
        'skip_object': 'वस्तु को छोड़ें',
        'new_object': 'नया वस्तु',
        'reset_recording': 'रिकॉर्डिंग रीसेट करें',
        're_record': 'पुनः रिकॉर्ड करें',
        'submit_identification': 'पहचान जमा करें',
        'local_name': 'स्थानीय नाम',
        'pronunciation_guide': 'उच्चारण गाइड',
        'cultural_context': 'सांस्कृतिक संदर्भ',
        'dialect_variation': 'भाषा विविधता',
        # Analytics specific
        'total_submissions': 'कुल जमा',
        'total_contributors': 'कुल योगदानकर्ता',
        'total_languages': 'कुल भाषाएं',
        'recent_activity': 'आज़माने वाली गतिविधि',
        'language_distribution': 'भाषा वितरण',
        'media_type_distribution': 'मीडिया प्रकार वितरण',
        'category_distribution': 'वर्ग वितरण',
        'growth_trends': 'वृद्धि धोखाधड़ी',
        'quality_metrics': 'गुणवत्ता मीट्रिक्स',
        'user_engagement': 'उपयोगकर्ता जुड़ाव',
        # Admin specific
        'admin_login': 'अडमिन लॉगिन',
        'username': 'उपयोगकर्ता नाम',
        'password': 'पासवर्ड',
        'login': 'लॉगिन',
        'admin_dashboard': 'अडमिन डैशबोर्ड',
        'manage_submissions': 'जमा करें',
        'approve_submission': 'जमा करें',
        'reject_submission': 'जमा करें',
        'curator_notes': 'क्यूरेटर टिप्पणियां',
        'validation_status': 'सत्यापन स्थिति',
        'pending': 'संग्रहीत',
        'approved': 'अनुमोदित',
        'rejected': 'अस्वीकृत',
        # Profile specific
        'edit_profile': 'प्रोफ़ाइल संपादित करें',
        'change_password': 'पासवर्ड बदलें',
        'delete_account': 'खाता हटाएं',
        'account_settings': 'खाता सेटिंग्स',
        'contribution_history': 'योगदान इतिहास',
        'personal_info': 'व्यक्तिगत जानकारी',
        'cultural_background': 'सांस्कृतिक पृष्ठभूमि',
        'profession': 'व्यवसाय',
        'location': 'स्थान',
        'save_changes': 'परिवर्तन सहेजें',
        'cancel': 'रद्द करें',
        'confirm': 'पुष्टि करें',
        'delete': 'हटाएं',
        # Navigation
        'home': 'होम',
        'navigation': 'नेविगेशन',
        'choose_page': 'पेज चुनें',
        'back_to_home': 'होम पर वापस जाएं',
        'next': 'अगला',
        'previous': 'पिछला',
        # Common actions
        'view': 'देखें',
        'edit': 'संपादित करें',
        'delete': 'हटाएं',
        'download': 'डाउनलोड करें',
        'share': 'साझा करें',
        'search': 'खोजें',
        'filter': 'फ़िल्टर',
        'sort': 'क्रमबद्ध करें',
        'refresh': 'अपडेट करें',
        'export': 'निर्यात करें',
        'import': 'आयात करें',
        # Status messages
        'loading': 'लोडिंग...',
        'saving': 'सहेजते हैं...',
        'processing': 'प्रोसेसिंग...',
        'success': 'सफलता!',
        'error': 'त्रुटि',
        'warning': 'चेतावनी',
        'info': 'जानकारी',
        'no_data': 'डेटा नहीं',
        'no_results': 'परिणाम नहीं',
        'try_again': 'पुनः प्रयास करें',
        'contact_support': 'सहायता से संपर्क करें'
    },
    'te': {
        'app_title': 'సాంస్కృతిక కోర్పస్ సేకరణ వేదిక',
        'app_description': 'బహుళ-మాధ్యమ డేటా సేకరణ ద్వారా సాంస్కృతిక వారసత్వాన్ని పరిరక్షించడం',
        'welcome': 'స్వాగతం',
        'sign_in': 'సైన్ ఇన్',
        'sign_up': 'సైన్ అప్',
        'logout': 'లాగ్అవుట్',
        'my_profile': 'నా ప్రొఫైల్',
        'start_contributing': 'సహకారం ప్రారంభించండి',
        'cultural_corpus': 'సాంస్కృతిక కోర్పస్ సేకరణ',
        'idi_emiti': 'ఇది-ఎమితి (ఇది ఏమిటి?)',
        'analytics': 'విశ్లేషణ డాష్‌బోర్డ్',
        'admin_panel': 'అడ్మిన్ పానెల్',
        'system_status': 'సిస్టమ్ స్థితి',
        'using_local_storage': 'స్థానిక JSON నిల్వను ఉపయోగిస్తున్నారు',
        'connected_to_csv': 'CSV నిల్వ వ్యవస్థతో కనెక్ట్ చేయబడింది',
        'csv_setup_guide': 'CSV-ఆధారిత నిల్వ వ్యవస్థను ఉపయోగిస్తున్నారు',
        'csv_setup_instructions': '''**CSV-ఆధారిత నిల్వ వ్యవస్థ:**

అప్లికేషన్ డేటా నిల్వ కోసం CSV ఫైల్‌లను ఉపయోగిస్తుంది:
- వినియోగదారు డేటా `data/users.csv` లో నిల్వ చేయబడుతుంది
- సెషన్ డేటా `data/sessions.csv` లో నిల్వ చేయబడుతుంది
- వినియోగదారు ప్రతిస్పందనలు `data/user_responses.csv` లో నిల్వ చేయబడతాయి

అదనపు సెటప్ అవసరం లేదు.''',
        'about_platform': 'మా వేదిక గురించి',
        'platform_description': '''సాంస్కృతిక కోర్పస్ సేకరణ వేదిక అనేది బహుళ-మాధ్యమ డేటా సేకరణ ద్వారా 
సాంస్కృతిక వారసత్వాన్ని పరిరక్షించడానికి మరియు డాక్యుమెంట్ చేయడానికి రూపొందించబడిన సమగ్ర డిజిటల్ రిపోజిటరీ. మా వేదిక సమాజాలను పంచుకోవడానికి, డాక్యుమెంట్ చేయడానికి మరియు 
భవిష్యత్ తరాల కోసం వారి సాంస్కృతిక సంప్రదాయాలు, భాషలు మరియు కళా వస్తువులను పరిరక్షించడానికి అనుమతిస్తుంది.''',
        'platform_impact': 'వేదిక ప్రభావం',
        'cultural_submissions': 'సాంస్కృతిక సమర్పణలు',
        'active_contributors': 'క్రియాశీల సహకారులు',
        'languages_documented': 'డాక్యుమెంట్ చేయబడిన భాషలు',
        'cultural_identifications': 'సాంస్కృతిక గుర్తింపులు',
        'platform_features': 'వేదిక లక్షణాలు',
        'multimodal_upload': 'బహుళ-మాధ్యమ మీడియా అప్‌లోడ్ (చిత్రాలు, ఆడియో, వీడియో)',
        'local_language': 'స్థానిక భాష మరియు మాండలిక డాక్యుమెంటేషన్',
        'cultural_context': 'సాంస్కృతిక సందర్భం మరియు ఉపయోగ సమాచారం',
        'geographic_tracking': 'భౌగోళిక స్థాన ట్రాకింగ్',
        'start_collection': 'సేకరణ ప్రారంభించండి',
        'cultural_identification': 'సాంస్కృతిక వస్తువు గుర్తింపు',
        'vocabulary_preservation': 'స్థానిక భాష పదజాల పరిరక్షణ',
        'audio_pronunciation': 'ఆడియో ఉచ్చారణ రికార్డింగ్‌లు',
        'dialect_documentation': 'ప్రాంతీయ మాండలిక డాక్యుమెంటేషన్',
        'try_idi_emiti': 'ఇది-ఎమితి ప్రయత్నించండి',
        'real_time_stats': 'రియల్-టైమ్ వేదిక గణాంకాలు',
        'language_analytics': 'భాష మరియు మాండలిక విశ్లేషణ',
        'user_engagement': 'వినియోగదారు నిశ్చితార్థ మెట్రిక్స్',
        'data_quality': 'డేటా నాణ్యత అంచనా',
        'view_analytics': 'విశ్లేషణ చూడండి',
        'secure_login': 'సురక్షిత లాగిన్ మరియు నమోదు',
        'profile_management': 'వినియోగదారు ప్రొఫైల్ నిర్వహణ',
        'contribution_tracking': 'సహకార చరిత్ర ట్రాకింగ్',
        'csv_storage': 'CSV-ఆధారిత నిల్వ వ్యవస్థ',
        'technology_stack': 'టెక్నాలజీ స్టాక్',
        'get_started': 'ప్రారంభించండి',
        'explore_features': 'లక్షణాలను అన్వేషించండి',
        'ready_to_start': 'ప్రారంభించడానికి సిద్ధంగా ఉన్నారా?',
        'join_thousands': 'ప్రపంచవ్యాప్తంగా సాంస్కృతిక వారసత్వాన్ని పరిరక్షించే వేలమంది సహకారులలో చేరండి',
        'create_account': 'ఖాతా సృష్టించండి',
        'continue_journey': 'మీ సాంస్కృతిక పరిరక్షణ ప్రయాణాన్ని కొనసాగించండి',
        'upload_content': 'విషయాన్ని అప్‌లోడ్ చేయండి',
        'play_idi_emiti': 'ఇది-ఎమితి ఆడండి',
        'language_selector': 'భాషను ఎంచుకోండి',
        'change_language': 'భాషను మార్చండి',
        # Form fields and buttons
        'title': 'శీర్షిక',
        'description': 'వివరణ',
        'name': 'పేరు',
        'email': 'ఇమెయిల్',
        'category': 'వర్గం',
        'language': 'భాష',
        'latitude': 'అక్షాంశం',
        'longitude': 'రేఖాంశం',
        'submit': 'సమర్పించండి',
        'upload': 'అప్‌లోడ్ చేయండి',
        'choose_file': 'ఫైల్‌ని ఎంచుకోండి',
        'select_category': 'వర్గాన్ని ఎంచుకోండి',
        'select_language': 'భాషను ఎంచుకోండి',
        'optional': 'ఐచ్ఛికం',
        'required': 'అవసరం',
        # Page titles and headers
        'upload_cultural_media': 'సాంస్కృతిక మీడియా అప్‌లోడ్ చేయండి',
        'cultural_information': 'సాంస్కృతిక సమాచారం',
        'media_preview': 'మీడియా మునుజూపు',
        'idi_emiti_game': 'ఇది-ఎమితి ఆట',
        'analytics_dashboard': 'విశ్లేషణ డాష్‌బోర్డ్',
        'admin_panel': 'అడ్మిన్ పానెల్',
        'user_profile': 'వినియోగదారు ప్రొఫైల్',
        'login_page': 'లాగిన్ పేజీ',
        'signup_page': 'సైన్‌అప్ పేజీ',
        # Messages and notifications
        'upload_success': 'అప్‌లోడ్ విజయవంతంగా జరిగింది!',
        'upload_error': 'అప్‌లోడ్ లోపం',
        'file_too_large': 'ఫైల్ చాలా పెద్దది',
        'invalid_file_type': 'చెల్లని ఫైల్ రకం',
        'please_login': 'దయచేసి లాగిన్ చేయండి',
        'access_denied': 'ప్రవేశం నిరాకరించబడింది',
        'authentication_required': 'అధికారీకరణ అవసరం',
        'please_fill_all_fields': 'దయచేసి అన్ని ఫీల్డ్‌లను నింపండి',
        'thank_you_contribution': 'మీ సహకారానికి ధన్యవాదాలు!',
        # Idi-Emiti specific
        'what_is_this': 'ఇది ఏమిటి?',
        'record_pronunciation': 'ఉచ్చారణను రికార్డ్ చేయండి',
        'skip_object': 'వస్తువును దాటవేయండి',
        'new_object': 'కొత్త వస్తువు',
        'reset_recording': 'రికార్డింగ్‌ని రీసెట్ చేయండి',
        're_record': 'మళ్లీ రికార్డ్ చేయండి',
        'submit_identification': 'గుర్తింపును సమర్పించండి',
        'local_name': 'స్థానిక పేరు',
        'pronunciation_guide': 'ఉచ్చారణ మార్గదర్శకం',
        'cultural_context': 'సాంస్కృతిక సందర్భం',
        'dialect_variation': 'మాండలిక వ్యత్యాసం',
        # Analytics specific
        'total_submissions': 'మొత్తం సమర్పణలు',
        'total_contributors': 'మొత్తం సహకారులు',
        'total_languages': 'మొత్తం భాషలు',
        'recent_activity': 'ఇటీవలి కార్యకలాపం',
        'language_distribution': 'భాషా పంపిణీ',
        'media_type_distribution': 'మీడియా రకం పంపిణీ',
        'category_distribution': 'వర్గం పంపిణీ',
        'growth_trends': 'పెరుగుదల ధోరణులు',
        'quality_metrics': 'నాణ్యత మెట్రిక్స్',
        'user_engagement': 'వినియోగదారు నిశ్చితార్థం',
        # Admin specific
        'admin_login': 'అడ్మిన్ లాగిన్',
        'username': 'వినియోగదారు పేరు',
        'password': 'పాస్‌వర్డ్',
        'login': 'లాగిన్',
        'admin_dashboard': 'అడ్మిన్ డాష్‌బోర్డ్',
        'manage_submissions': 'సమర్పణలను నిర్వహించండి',
        'approve_submission': 'సమర్పణను ఆమోదించండి',
        'reject_submission': 'సమర్పణను తిరస్కరించండి',
        'curator_notes': 'క్యూరేటర్ గమనికలు',
        'validation_status': 'ధృవీకరణ స్థితి',
        'pending': 'పెండింగ్',
        'approved': 'ఆమోదించబడింది',
        'rejected': 'తిరస్కరించబడింది',
        # Profile specific
        'edit_profile': 'ప్రొఫైల్‌ని సవరించండి',
        'change_password': 'పాస్‌వర్డ్‌ని మార్చండి',
        'delete_account': 'ఖాతాను తొలగించండి',
        'account_settings': 'ఖాతా సెట్టింగ్‌లు',
        'contribution_history': 'సహకార చరిత్ర',
        'personal_info': 'వ్యక్తిగత సమాచారం',
        'cultural_background': 'సాంస్కృతిక నేపథ్యం',
        'profession': 'వృత్తి',
        'location': 'స్థానం',
        'save_changes': 'మార్పులను సేవ్ చేయండి',
        'cancel': 'రద్దు చేయండి',
        'confirm': 'నిర్ధారించండి',
        'delete': 'తొలగించండి',
        # Navigation
        'home': 'హోమ్',
        'navigation': 'నావిగేషన్',
        'choose_page': 'పేజీని ఎంచుకోండి',
        'back_to_home': 'హోమ్‌కి తిరిగి వెళ్లండి',
        'next': 'తదుపరి',
        'previous': 'మునుపటి',
        # Common actions
        'view': 'చూడండి',
        'edit': 'సవరించండి',
        'delete': 'తొలగించండి',
        'download': 'డౌన్‌లోడ్ చేయండి',
        'share': 'షేర్ చేయండి',
        'search': 'వెతకండి',
        'filter': 'ఫిల్టర్',
        'sort': 'క్రమబద్ధం చేయండి',
        'refresh': 'రిఫ్రెష్ చేయండి',
        'export': 'ఎగుమతి చేయండి',
        'import': 'దిగుమతి చేయండి',
        # Status messages
        'loading': 'లోడ్ అవుతోంది...',
        'saving': 'సేవ్ చేస్తోంది...',
        'processing': 'ప్రాసెస్ చేస్తోంది...',
        'success': 'విజయవంతం!',
        'error': 'లోపం',
        'warning': 'హెచ్చరిక',
        'info': 'సమాచారం',
        'no_data': 'డేటా లేదు',
        'no_results': 'ఫలితాలు లేవు',
        'try_again': 'మళ్లీ ప్రయత్నించండి',
        'contact_support': 'మద్దతుతో సంప్రదించండి'
    }
}

# Messages
SUCCESS_MESSAGE = "✅ Submission saved successfully!"
INFO_MESSAGE = "ℹ️ Using CSV-based storage system"
ERROR_NO_DESCRIPTION = "❌ Please provide a description"
ERROR_NO_MEDIA = "❌ Please upload at least one media file"
ERROR_INVALID_FILE = "❌ Invalid file type. Please upload an image, audio, or video file"
ERROR_FILE_TOO_LARGE = "❌ File too large. Please upload a smaller file"
ERROR_NO_TITLE = "❌ Please provide a title"
ERROR_NO_CATEGORY = "❌ Please select a category"
ADMIN_LOGIN_ERROR = "❌ Invalid admin credentials"
ADMIN_ACCESS_DENIED = "❌ Access denied. Admin privileges required"

# Recent responses limit
RECENT_RESPONSES_LIMIT = 10

# Media types
MEDIA_TYPES = {
    'image': 'Image',
    'audio': 'Audio',
    'video': 'Video'
}

# File size limits (in bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB

# Custom CSS
CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    .main {
        background: transparent;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #f093fb);
        transform: translateY(-2px);
    }
</style>
"""

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