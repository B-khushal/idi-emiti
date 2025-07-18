import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime
from utils import (
    get_random_media,
    save_user_response,
    get_available_media,
    get_session_id,
    get_submission_count,
    get_comprehensive_analytics,
    get_time_based_analytics,
    get_user_engagement_metrics,
    get_content_analysis,
    get_popular_media_analysis,
    get_growth_metrics,
    get_quality_metrics,
    get_media_type,
    validate_media_file,
    save_uploaded_file,
    get_idi_emiti_count,
    get_idi_emiti_languages,
    get_user_idi_emiti_count,
    get_idi_emiti_analytics
)
from audio_recorder import audio_recorder_component, reset_audio_recorder
from config import (
    APP_TITLE, APP_ICON, APP_DESCRIPTION, ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_SESSION_KEY,
    ASSETS_FOLDER, DATA_FOLDER, CSV_FILE, UPLOADS_FOLDER, IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS,
    MAX_FORM_WIDTH, IMAGE_CAPTION, TEXT_AREA_HEIGHT, NAME_PLACEHOLDER,
    DESCRIPTION_PLACEHOLDER, USER_DETAILS_PLACEHOLDER, LATITUDE_PLACEHOLDER,
    LONGITUDE_PLACEHOLDER, TITLE_PLACEHOLDER, CATEGORY_PLACEHOLDER, CATEGORIES, LANGUAGES,
    SUCCESS_MESSAGE, INFO_MESSAGE, ERROR_NO_DESCRIPTION, ERROR_NO_MEDIA,
    ERROR_INVALID_FILE, ERROR_FILE_TOO_LARGE, ERROR_NO_TITLE, ERROR_NO_CATEGORY,
    ADMIN_LOGIN_ERROR, ADMIN_ACCESS_DENIED, CUSTOM_CSS, RECENT_RESPONSES_LIMIT,
    MEDIA_TYPES, MAX_IMAGE_SIZE, MAX_AUDIO_SIZE, MAX_VIDEO_SIZE
)
from auth import (
    check_user_authentication,
    render_login_form,
    render_signup_form,
    render_user_profile,
    logout_user
)
import hashlib
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Professional UI/UX Design System
st.markdown("""
<style>
    /* Modern Design System - Cultural Heritage Theme */
    
    /* Global Reset & Typography */
    * {
        font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        box-sizing: border-box;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        min-height: 100vh;
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.05)"/><circle cx="10" cy="60" r="0.5" fill="rgba(255,255,255,0.05)"/><circle cx="90" cy="40" r="0.5" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
        z-index: 0;
    }
    
    .main {
        background: transparent;
        padding: 0;
        position: relative;
        z-index: 1;
    }
    
    /* Hero Section */
    .hero-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0 0 40px 40px;
        padding: 4rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.15);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        color: #FFFFFF !important;
        margin: 0 0 1.5rem 0;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 30px rgba(255, 255, 255, 0.3);
        animation: fadeInUp 1s ease-out;
        background: none;
        -webkit-background-clip: initial;
        -webkit-text-fill-color: initial;
        background-clip: initial;
    }
    
    .hero-title {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 30px rgba(255, 255, 255, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.6rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 400;
        margin: 0;
        opacity: 0.9;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Content Container */
    .content-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Glass Card for Analytics */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.2);
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 24px 24px 0 0;
    }
    
    /* Media Showcase */
    .media-showcase {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 32px;
        padding: 3rem;
        margin: 3rem 0;
        text-align: center;
        position: relative;
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideInUp 0.8s ease-out;
    }
    
    .media-showcase:hover {
        transform: translateY(-5px);
        box-shadow: 0 40px 120px rgba(0, 0, 0, 0.25);
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Form Styling */
    .stForm {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 16px;
        color: #333333;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 1);
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        color: #333333;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 16px;
        min-height: 120px;
        color: #333333;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        background: rgba(255, 255, 255, 1);
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        color: #333333;
    }
    
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 16px;
        color: #333333;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        background: rgba(255, 255, 255, 1);
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        color: #333333;
    }
    
    /* Placeholder text styling */
    .stTextInput > div > div > input::placeholder {
        color: #666666;
        opacity: 1;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #666666;
        opacity: 1;
    }
    
    .stSelectbox > div > div > select option {
        color: #333333;
        background: #ffffff;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* File Upload Styling */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Media Display */
    .media-display {
        max-width: 100%;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .content-container {
            padding: 0 1rem;
        }
        
        .media-showcase {
            padding: 2rem 1rem;
        }
        
        .stForm {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)



def get_location_js():
    """JavaScript for getting user location"""
    return """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // Send location data to Streamlit
                    const data = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    };
                    
                    // Use Streamlit's component communication
                    if (window.parent && window.parent.postMessage) {
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: JSON.stringify(data)
                        }, '*');
                    }
                },
                function(error) {
                    console.log("Error getting location:", error);
                }
            );
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    }
    
    // Auto-get location when page loads
    window.onload = function() {
        getLocation();
    };
    </script>
    """

def initialize_session_state():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = get_session_id()
    
    if 'current_media' not in st.session_state:
        st.session_state.current_media = None
    
    if 'submission_count' not in st.session_state:
        st.session_state.submission_count = get_submission_count()

def main():
    # Initialize session state
    initialize_session_state()
    
    # Check user authentication
    user = check_user_authentication()
    
    # Handle URL parameters for page navigation
    if 'page' in st.query_params:
        page_param = st.query_params['page']
        # Map URL parameters to actual page names
        page_mapping = {
            'Login': 'Login',
            'Sign_Up': 'Sign Up',
            'Cultural_Corpus_Collection': 'Cultural Corpus Collection',
            'Idi_Emiti': 'Idi-Emiti (What is this?)',
            'My_Profile': 'My Profile',
            'Analytics_Dashboard': 'Analytics Dashboard',
            'Admin_Panel': 'Admin Panel',
            'Home': '🏠 Home'
        }
        if page_param in page_mapping:
            st.session_state['selected_page'] = page_mapping[page_param]
            # Clear the URL parameter
            st.query_params.clear()
    
    # Handle page navigation from authentication
    if 'current_page' in st.session_state:
        target_page = st.session_state['current_page']
        del st.session_state['current_page']  # Clear the navigation flag
        
        # Set the appropriate page based on the target
        if target_page == 'main':
            st.session_state['selected_page'] = "Cultural Corpus Collection"
        elif target_page == 'login':
            st.session_state['selected_page'] = "Login"
        elif target_page == 'signup':
            st.session_state['selected_page'] = "Sign Up"
        elif target_page == 'profile':
            st.session_state['selected_page'] = "My Profile"
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("🏛️ Navigation")
        
        # Show user info if logged in
        if user:
            st.markdown(f"**👤 Welcome, {user['name']}**")
            if st.button("🚪 Logout", use_container_width=True):
                logout_user(st.session_state['user_session'])
                st.session_state.clear()
                st.rerun()
            st.markdown("---")
        else:
            # Show login prompt for guests
            st.warning("🔐 Please log in to access the platform")
            st.markdown("---")
        
        # Navigation options
        if user:
            # Logged in users
            page = st.radio(
                "Choose a page:",
                ["🏠 Home", "Cultural Corpus Collection", "Idi-Emiti (What is this?)", "My Profile", "Analytics Dashboard", "Admin Panel"],
                key="page_selector",
                index=0 if 'selected_page' not in st.session_state else 
                      ["🏠 Home", "Cultural Corpus Collection", "Idi-Emiti (What is this?)", "My Profile", "Analytics Dashboard", "Admin Panel"].index(st.session_state['selected_page'])
            )
        else:
            # Guest users - only show authentication pages
            page = st.radio(
                "Choose a page:",
                ["🏠 Home", "Login", "Sign Up", "Analytics Dashboard", "Admin Panel"],
                key="page_selector",
                index=0 if 'selected_page' not in st.session_state else 
                      ["🏠 Home", "Login", "Sign Up", "Analytics Dashboard", "Admin Panel"].index(st.session_state['selected_page'])
            )
        
        # Store the selected page
        st.session_state['selected_page'] = page
    
    # Main content area
    if page == "🏠 Home":
        landing_page()
    elif page == "Cultural Corpus Collection":
        if user:
            cultural_corpus_page(user)
        else:
            st.error("🔐 Please log in to access the Cultural Corpus Collection page")
            st.info("Use the sidebar to navigate to the Login or Sign Up page")
    elif page == "Idi-Emiti (What is this?)":
        if user:
            idi_emiti_page(user)
        else:
            st.error("🔐 Please log in to access the Idi-Emiti page")
            st.info("Use the sidebar to navigate to the Login or Sign Up page")
    elif page == "Login":
        authentication_page("login")
    elif page == "Sign Up":
        authentication_page("signup")
    elif page == "My Profile":
        if user:
            render_user_profile()
        else:
            st.error("Please log in to view your profile")
    elif page == "Analytics Dashboard":
        analytics_dashboard_page()
    elif page == "Admin Panel":
        admin_panel_page()

def admin_login_form():
    """Admin login form"""
    st.markdown("### 🔐 Admin Authentication")
    
    with st.form("admin_login"):
        username = st.text_input("Username", key="admin_username")
        password = st.text_input("Password", type="password", key="admin_password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if authenticate_admin(username, password):
                st.session_state[ADMIN_SESSION_KEY] = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(ADMIN_LOGIN_ERROR)

def authenticate_admin(username, password):
    """Authenticate admin credentials"""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def cultural_corpus_page(user=None):
    """Main cultural corpus collection page"""
    # Require authentication
    if not user:
        st.error("🔐 Authentication Required")
        st.warning("You must be logged in to access this page.")
        st.info("Please use the sidebar to navigate to the Login or Sign Up page.")
        return
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🏛️ Cultural Corpus Collection Platform</h1>
        <p class="hero-subtitle">Preserving cultural heritage through multimodal data collection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content container
    with st.container():
        st.markdown("""
        <div class="content-container">
        """, unsafe_allow_html=True)
        
        # Media Upload Section
        st.markdown("### 📁 Upload Cultural Media")
        st.markdown("Share images, audio recordings, or videos of cultural objects, traditions, or practices.")
        
        # Media type selection
        media_type_options = {
            "All Media Types": ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp3', 'wav', 'ogg', 'm4a', 'flac', 'mp4', 'avi', 'mov', 'mkv', 'webm'],
            "Images Only": ['jpg', 'jpeg', 'png', 'gif', 'webp'],
            "Audio Only": ['mp3', 'wav', 'ogg', 'm4a', 'flac'],
            "Video Only": ['mp4', 'avi', 'mov', 'mkv', 'webm']
        }
        
        # Media type icons
        media_type_icons = {
            "All Media Types": "📁",
            "Images Only": "🖼️",
            "Audio Only": "🎵",
            "Video Only": "🎬"
        }
        
        col1, col2 = st.columns([1, 2])
        with col1:
            selected_media_type = st.selectbox(
                f"{media_type_icons.get('All Media Types', '📁')} Select Media Type",
                options=list(media_type_options.keys()),
                help="Choose the type of media you want to upload"
            )
        
        with col2:
            # Show selected media type info
            icon = media_type_icons.get(selected_media_type, "📁")
            st.markdown(f"**{icon} {selected_media_type}**")
            if selected_media_type != "All Media Types":
                formats = ", ".join(media_type_options[selected_media_type]).upper()
                st.caption(f"Supported formats: {formats}")
        
        # File upload with filtered types
        icon = media_type_icons.get(selected_media_type, "📁")
        uploaded_file = st.file_uploader(
            f"{icon} Choose a {selected_media_type.lower()} file",
            type=media_type_options[selected_media_type],
            help=f"Supported formats: {selected_media_type}"
        )
        
        if uploaded_file is not None:
            # Validate file
            file_size = len(uploaded_file.getbuffer())
            is_valid, validation_message = validate_media_file(uploaded_file.name, file_size)
            
            if not is_valid:
                st.error(validation_message)
                return
            
            # Display media preview
            media_type = get_media_type(uploaded_file.name)
            st.markdown(f"### 📺 {MEDIA_TYPES.get(media_type, 'Media')} Preview")
            
            if media_type == "image":
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            elif media_type == "audio":
                st.audio(uploaded_file)
            elif media_type == "video":
                st.video(uploaded_file)
            
            # Collection Form
            st.markdown("### 📝 Cultural Information")
            
            with st.form("cultural_data_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    title = st.text_input("Title", placeholder=TITLE_PLACEHOLDER, help="Give your cultural object a descriptive title")
                    
                    # Pre-fill user data if logged in
                    if user:
                        contributor_name = st.text_input("Your Name", value=user['name'], help="Your name for attribution")
                        contributor_email = st.text_input("Email", value=user['email'], help="For follow-up questions or acknowledgments")
                    else:
                        contributor_name = st.text_input("Your Name", placeholder=NAME_PLACEHOLDER, help="Your name for attribution")
                        contributor_email = st.text_input("Email (Optional)", placeholder="your.email@example.com", help="For follow-up questions or acknowledgments")
                    
                    language = st.selectbox("Language", ["Select Language"] + LANGUAGES, help="Language of your description")
                
                with col2:
                    category = st.selectbox("Category", ["Select Category"] + CATEGORIES, help="Choose the most appropriate category")
                    latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=None, placeholder="Auto-detected", help="Geographic latitude")
                    longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=None, placeholder="Auto-detected", help="Geographic longitude")
                
                description = st.text_area(
                    "Description",
                    placeholder=DESCRIPTION_PLACEHOLDER,
                    height=TEXT_AREA_HEIGHT,
                    help="Describe the cultural significance, usage, and context of this object or practice"
                )
                
                # Initialize local language variables
                local_language_name = None
                dialect = None
                pronunciation_guide = None
                cultural_context = None
                audio_recording = None
                
                # Local Language and Dialect Section (for images)
                if media_type == "image":
                    st.markdown("---")
                    st.markdown("### 🌍 Local Language & Dialect Information")
                    st.markdown("Help preserve your local language by providing the name and pronunciation of this cultural object.")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        local_language_name = st.text_input(
                            "Local Language Name",
                            placeholder="What is this called in your local language?",
                            help="Enter the name of this object in your local language or dialect"
                        )
                        
                        dialect = st.text_input(
                            "Dialect/Regional Variation",
                            placeholder="e.g., Telugu (Hyderabad), Bengali (Kolkata)",
                            help="Specify the dialect or regional variation of your language"
                        )
                    
                    with col2:
                        pronunciation_guide = st.text_input(
                            "Pronunciation Guide",
                            placeholder="e.g., 'gulab-jamun' (goo-lahb jah-moon)",
                            help="Provide a pronunciation guide in English letters"
                        )
                        
                        cultural_context = st.text_input(
                            "Cultural Context",
                            placeholder="e.g., Used in weddings, festivals, daily prayers",
                            help="When and how is this object used in your culture?"
                        )
                    
                    # Audio recording for pronunciation
                    st.markdown("#### 🎤 Audio Pronunciation (Optional)")
                    st.markdown("Record yourself saying the name of this object in your local language.")
                    
                    # Web Audio Recording
                    audio_recorder_component(key="cultural_corpus")
                    
                    # File upload as fallback
                    st.markdown("**Or upload an audio file:**")
                    audio_recording = st.file_uploader(
                        "🎵 Upload Audio Recording",
                        type=['mp3', 'wav', 'ogg', 'm4a'],
                        help="Record the pronunciation of the object name in your local language"
                    )
                    
                    if audio_recording:
                        st.audio(audio_recording, caption="Your pronunciation recording")
                
                contributor_details = st.text_area(
                    "About You (Optional)",
                    placeholder=USER_DETAILS_PLACEHOLDER,
                    height=100,
                    help="Tell us about your cultural background, profession, or connection to this cultural object"
                )
                
                # Submit button
                submit_button = st.form_submit_button("🏛️ Submit to Cultural Corpus", use_container_width=True)
                
                if submit_button:
                    # Check authentication first
                    if not user:
                        st.error("🔐 Authentication Required")
                        st.warning("You must be logged in to submit cultural data.")
                        st.info("Please log in or create an account to continue.")
                        return
                    
                    # Validation
                    if not title:
                        st.error(ERROR_NO_TITLE)
                        return
                    
                    if not description:
                        st.error(ERROR_NO_DESCRIPTION)
                        return
                    
                    if category == "Select Category":
                        st.error(ERROR_NO_CATEGORY)
                        return
                    
                    if language == "Select Language":
                        st.error("Please select a language")
                        return
                    
                    try:
                        # Save uploaded file
                        filename, file_path = save_uploaded_file(uploaded_file, media_type)
                        
                        # Save audio recording if provided (for images)
                        audio_filename = None
                        audio_path = None
                        if media_type == "image" and audio_recording is not None:
                            audio_filename, audio_path = save_uploaded_file(audio_recording, "audio")
                        
                        # Save response to database
                        save_user_response(
                            media_filename=filename,
                            media_type=media_type,
                            title=title,
                            description=description,
                            language=language,
                            contributor_name=contributor_name,
                            contributor_email=contributor_email,
                            contributor_details=contributor_details,
                            category=category,
                            session_id=st.session_state.session_id,
                            latitude=latitude,
                            longitude=longitude,
                            file_size=file_size,
                            file_path=file_path,
                            local_language_name=local_language_name if media_type == "image" else None,
                            dialect_regional_variation=dialect if media_type == "image" else None,
                            pronunciation_guide=pronunciation_guide if media_type == "image" else None,
                            cultural_context=cultural_context if media_type == "image" else None,
                            local_language_audio_path=audio_path if media_type == "image" else None
                        )
                        
                        # Success message
                        st.success(SUCCESS_MESSAGE)
                        st.info(INFO_MESSAGE)
                        
                        # Update session state
                        st.session_state.submission_count = get_submission_count()
                        
                        # Clear form
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error saving data: {str(e)}")
        
        # Sample Media Section (if no upload)
        else:
            st.markdown("### 🎯 Sample Cultural Objects")
            st.markdown("Explore existing cultural objects or upload your own media to contribute.")
            
            # Get random media from assets
            random_media = get_random_media()
            if random_media:
                media_type = get_media_type(random_media)
                st.markdown(f"#### 📺 Sample {MEDIA_TYPES.get(media_type, 'Media')}")
                
                if media_type == "image":
                    st.image(random_media, caption="Sample Cultural Object", use_container_width=True)
                elif media_type == "audio":
                    st.audio(random_media)
                elif media_type == "video":
                    st.video(random_media)
                
                st.markdown("**Upload your own cultural media above to contribute to our corpus!**")
            else:
                st.warning("No sample media found. Please upload your own cultural media.")
        
        # Statistics
        st.markdown("### 📊 Platform Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Submissions", st.session_state.submission_count)
        
        with col2:
            st.metric("Your Session", st.session_state.session_id[:8] + "...")
        
        with col3:
            st.metric("Languages Supported", len(LANGUAGES))
        
        # User contribution statistics
        if user:
            st.markdown("---")
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.1); padding: 2rem; border-radius: 16px; text-align: center;">
                <h3>🌟 Welcome to Our Cultural Community!</h3>
                <p>Thank you for contributing to our cultural preservation efforts.</p>
                <p><strong>Your contributions help:</strong></p>
                <ul style="text-align: left; display: inline-block;">
                    <li>Preserve cultural heritage for future generations</li>
                    <li>Share knowledge across communities</li>
                    <li>Build a comprehensive cultural database</li>
                    <li>Connect people through shared traditions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def idi_emiti_page(user=None):
    """Idi-Emiti (What is this?) page - Cultural object identification game"""
    # Require authentication
    if not user:
        st.error("🔐 Authentication Required")
        st.warning("You must be logged in to access this page.")
        st.info("Please use the sidebar to navigate to the Login or Sign Up page.")
        return
    
    # Initialize session state for audio recorder reset
    if 'audio_reset_trigger' not in st.session_state:
        st.session_state.audio_reset_trigger = 0
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🤔 Idi-Emiti (What is this?)</h1>
        <p class="hero-subtitle">Help us preserve cultural vocabulary by identifying traditional objects in your language</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content container
    with st.container():
        st.markdown("""
        <div class="content-container">
        """, unsafe_allow_html=True)
        
        # Game Instructions
        st.markdown("### 🎯 How to Play")
        st.markdown("""
        1. **Look at the image** - A traditional cultural object will be shown
        2. **Think about it** - What is this object called in your local language?
        3. **Share your knowledge** - Tell us the name, dialect, and pronunciation
        4. **Help preserve culture** - Your contribution helps document linguistic diversity
        """)
        
        # Get random image from assets
        random_image = get_random_media()
        
        if random_image and get_media_type(random_image) == "image":
            # Display the image with skip button below
            st.markdown("### 🖼️ What is this object called in your language?")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(random_image, caption="Traditional Cultural Object", use_container_width=True)
                
                # Skip button below the image
                st.markdown("---")
                skip_col1, skip_col2, skip_col3 = st.columns([1, 1, 1])
                with skip_col2:
                    if st.button("⏭️ Skip This Object", use_container_width=True, help="Skip to a different cultural object"):
                        st.rerun()
            
            with col2:
                st.markdown("#### 📝 Object Information")
                st.markdown(f"**File:** {os.path.basename(random_image)}")
                st.markdown("**Type:** Traditional Cultural Object")
                st.markdown("**Region:** Various Indian Cultures")
                
                # Show some hints
                st.markdown("#### 💡 Hints")
                st.markdown("""
                - Look at the shape and material
                - Consider its traditional use
                - Think about your cultural background
                - What would your elders call this?
                """)
            
            # Language identification form
            st.markdown("---")
            st.markdown("### 🌍 Tell us what this is called in your language")
            
            with st.form("idi_emiti_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    local_name = st.text_input(
                        "Local Language Name",
                        placeholder="What is this called in your language?",
                        help="Enter the name of this object in your local language or dialect"
                    )
                    
                    dialect = st.text_input(
                        "Dialect/Regional Variation",
                        placeholder="e.g., Telugu (Hyderabad), Bengali (Kolkata)",
                        help="Specify the dialect or regional variation of your language"
                    )
                    
                    pronunciation = st.text_input(
                        "Pronunciation Guide",
                        placeholder="e.g., 'gulab-jamun' (goo-lahb jah-moon)",
                        help="Provide a pronunciation guide in English letters"
                    )
                
                with col2:
                    cultural_use = st.text_input(
                        "Cultural Use/Context",
                        placeholder="e.g., Used in cooking, festivals, daily life",
                        help="When and how is this object used in your culture?"
                    )
                    
                    confidence_level = st.selectbox(
                        "How confident are you?",
                        ["Select Confidence", "Very Confident", "Somewhat Confident", "Not Sure", "Just Guessing"],
                        help="Indicate your confidence in the identification"
                    )
                    
                    additional_info = st.text_area(
                        "Additional Information (Optional)",
                        placeholder="Any other details about this object...",
                        height=100,
                        help="Share any additional cultural context or memories"
                    )
                
                # Audio recording for pronunciation
                st.markdown("#### 🎤 Audio Pronunciation (Optional)")
                st.markdown("Record yourself saying the name of this object in your local language.")
                
                # Web Audio Recording with reset trigger
                audio_recorder_component(key="idi_emiti", reset_trigger=st.session_state.audio_reset_trigger)
                
                # File upload as fallback
                st.markdown("**Or upload an audio file:**")
                audio_recording = st.file_uploader(
                    "🎵 Upload Audio Recording",
                    type=['mp3', 'wav', 'ogg', 'm4a'],
                    help="Record the pronunciation of the object name in your local language"
                )
                
                if audio_recording:
                    st.audio(audio_recording, caption="Your pronunciation recording")
                
                # Action buttons with reset/re-record features
                st.markdown("---")
                st.markdown("#### 🎮 Action Buttons")
                
                # Button layout
                button_col1, button_col2, button_col3, button_col4 = st.columns([2, 1, 1, 1])
                
                with button_col1:
                    submit_button = st.form_submit_button("🏛️ Submit Identification", use_container_width=True)
                
                with button_col2:
                    reset_button = st.form_submit_button("🔄 Reset Form", use_container_width=True)
                
                with button_col3:
                    rerecord_button = st.form_submit_button("🎤 Re-record Audio", use_container_width=True)
                
                with button_col4:
                    new_object_button = st.form_submit_button("🆕 New Object", use_container_width=True)
                
                # Handle button actions
                if submit_button:
                    # Validation
                    if not local_name:
                        st.error("Please provide the local language name")
                        return
                    
                    if confidence_level == "Select Confidence":
                        st.error("Please select your confidence level")
                        return
                    
                    try:
                        # Save audio recording if provided
                        audio_filename = None
                        audio_path = None
                        if audio_recording is not None:
                            audio_filename, audio_path = save_uploaded_file(audio_recording, "audio")
                        
                        # Save identification to database
                        save_user_response(
                            media_filename=os.path.basename(random_image),
                            media_type="image",
                            title=f"Idi-Emiti: {local_name}",
                            description=f"Cultural object identification game. Local name: {local_name}. Cultural use: {cultural_use}. Additional info: {additional_info}",
                            language="Multiple",
                            contributor_name=user['name'],
                            contributor_email=user['email'],
                            contributor_details=f"Confidence: {confidence_level}. {user.get('profile_data', {}).get('cultural_background', '')}",
                            category="Cultural Identification",
                            session_id=st.session_state.session_id,
                            latitude=None,
                            longitude=None,
                            file_size=None,
                            file_path=random_image,
                            local_language_name=local_name,
                            dialect_regional_variation=dialect,
                            pronunciation_guide=pronunciation,
                            cultural_context=cultural_use,
                            local_language_audio_path=audio_path
                        )
                        
                        # Success message
                        st.success("🎉 Thank you for your contribution!")
                        st.info("Your identification helps preserve cultural vocabulary and linguistic diversity.")
                        
                        # Show next object option
                        if st.button("🔄 Show Another Object"):
                            st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error saving identification: {str(e)}")
                
                elif reset_button:
                    # Clear form data and show success message
                    st.success("✅ Form has been reset! You can start fresh.")
                    st.info("All fields have been cleared. You can now enter new information.")
                    # The form will be cleared on the next render
                
                elif rerecord_button:
                    # Increment reset trigger to force audio recorder reset
                    st.session_state.audio_reset_trigger += 1
                    st.success("🎤 Audio recording cleared! You can record again.")
                    st.info("Please use the audio recorder above to record a new pronunciation.")
                    # Inject reset script
                    st.markdown(reset_audio_recorder("idi_emiti"), unsafe_allow_html=True)
                    st.rerun()
                
                elif new_object_button:
                    # Show new object
                    st.success("🆕 Loading a new cultural object...")
                    st.rerun()
        
        else:
            st.warning("No cultural object images found in the assets folder.")
            st.info("Please add some traditional cultural object images to the assets folder to enable this feature.")
        
        # User contribution message
        st.markdown("---")
        st.markdown("### 🎯 Your Contribution")
        st.info("Thank you for helping preserve cultural vocabulary! Your identification will be reviewed and added to our cultural database.")
        
        # Cultural preservation message
        st.markdown("---")
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); padding: 2rem; border-radius: 16px; text-align: center;">
            <h3>🌍 Preserving Cultural Vocabulary</h3>
            <p>Every identification you make helps preserve the rich linguistic diversity of our cultural heritage.</p>
            <p><strong>Your contributions:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>Document traditional object names in local languages</li>
                <li>Preserve regional dialects and pronunciations</li>
                <li>Create a multilingual cultural dictionary</li>
                <li>Help future generations understand their heritage</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def landing_page():
    """Professional landing page for the Cultural Corpus Collection Platform"""
    
    # Check if user is logged in
    user = check_user_authentication()
    
    # Top Authentication Banner
    if user:
        # Logged in user banner
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); padding: 1rem; text-align: center; color: white; margin: -1rem -1rem 1rem -1rem; border-radius: 0 0 20px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
                <div style="font-weight: bold; font-size: 1.1rem;">🏛️ Cultural Heritage Platform</div>
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <span style="background: rgba(255, 255, 255, 0.2); padding: 0.5rem 1rem; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.3);">👤 Welcome, {user['name']}</span>
                    <a href="?page=My_Profile" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.5rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.3);">My Profile</a>
                    <a href="?page=Cultural_Corpus_Collection" style="background: rgba(255, 255, 255, 0.9); color: #667eea; padding: 0.5rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: bold;">Start Contributing</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Guest user banner
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); padding: 1rem; text-align: center; color: white; margin: -1rem -1rem 1rem -1rem; border-radius: 0 0 20px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;">
                <div style="font-weight: bold; font-size: 1.1rem;">🏛️ Cultural Heritage Platform</div>
                <div style="display: flex; gap: 1rem;">
                    <a href="?page=Login" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.5rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.3);">Sign In</a>
                    <a href="?page=Sign_Up" style="background: rgba(255, 255, 255, 0.9); color: #667eea; padding: 0.5rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: bold;">Sign Up</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); padding: 4rem 2rem; text-align: center; color: white; border-radius: 0 0 40px 40px; margin: -1rem -1rem 3rem -1rem;">
        <h1 style="font-size: 3.5rem; font-weight: 900; margin-bottom: 1rem; text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);">🏛️ Cultural Corpus Collection Platform</h1>
        <p style="font-size: 1.4rem; margin-bottom: 2rem; opacity: 0.95;">Preserving Cultural Heritage Through Multimodal Data Collection</p>
        <div style="margin-top: 2rem;">
            <a href="#features" style="background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem;">Explore Features</a>
            <a href="#get-started" style="background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem;">Get Started</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Action Section
    if user:
        # Logged in user actions
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 2rem 0; text-align: center;">
            <h2 style="margin-bottom: 1rem;">🚀 Welcome back, {user['name']}!</h2>
            <p style="margin-bottom: 2rem; font-size: 1.1rem;">Continue your cultural preservation journey</p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <a href="?page=Cultural_Corpus_Collection" style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem; transition: transform 0.3s ease;">Upload Content</a>
                <a href="?page=Idi_Emiti" style="background: linear-gradient(45deg, #f093fb, #f5576c); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem; transition: transform 0.3s ease;">Play Idi-Emiti</a>
                <a href="?page=My_Profile" style="background: linear-gradient(45deg, #48dbfb, #0abde3); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem; transition: transform 0.3s ease;">My Profile</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Guest user actions
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 2rem 0; text-align: center;">
            <h2 style="margin-bottom: 1rem;">🚀 Ready to Start?</h2>
            <p style="margin-bottom: 2rem; font-size: 1.1rem;">Join thousands of contributors preserving cultural heritage worldwide</p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <a href="?page=Login" style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem; transition: transform 0.3s ease;">Sign In</a>
                <a href="?page=Sign_Up" style="background: linear-gradient(45deg, #f093fb, #f5576c); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem; transition: transform 0.3s ease;">Create Account</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Platform Overview
    st.markdown("## 🌍 About Our Platform")
    st.markdown("""
    The Cultural Corpus Collection Platform is a comprehensive digital repository designed to preserve and document 
    cultural heritage through multimodal data collection. Our platform enables communities to share, document, and 
    preserve their cultural traditions, languages, and artifacts for future generations.
    """)
    
    # Key Statistics
    try:
        analytics = get_comprehensive_analytics()
        total_submissions = analytics.get('growth_metrics', {}).get('total_submissions', 0)
        unique_contributors = analytics.get('user_engagement', {}).get('unique_contributors', 0)
        languages_documented = analytics.get('content_analysis', {}).get('total_languages', 0)
        idi_emiti_stats = get_idi_emiti_analytics()
        cultural_identifications = idi_emiti_stats.get('total_identifications', 0)
    except:
        total_submissions = 0
        unique_contributors = 0
        languages_documented = 0
        cultural_identifications = 0
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 3rem 2rem; border-radius: 20px; margin: 2rem 0; color: white;">
        <h2 style="text-align: center; margin-bottom: 2rem;">📊 Platform Impact</h2>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="text-align: center; margin: 1rem;">
                <h3 style="font-size: 2.5rem; margin: 0;">{}</h3>
                <p>Cultural Submissions</p>
            </div>
            <div style="text-align: center; margin: 1rem;">
                <h3 style="font-size: 2.5rem; margin: 0;">{}</h3>
                <p>Active Contributors</p>
            </div>
            <div style="text-align: center; margin: 1rem;">
                <h3 style="font-size: 2.5rem; margin: 0;">{}</h3>
                <p>Languages Documented</p>
            </div>
            <div style="text-align: center; margin: 1rem;">
                <h3 style="font-size: 2.5rem; margin: 0;">{}</h3>
                <p>Cultural Identifications</p>
            </div>
        </div>
    </div>
    """.format(total_submissions, unique_contributors, languages_documented, cultural_identifications), 
    unsafe_allow_html=True)
    
    # Features Section
    st.markdown("## ✨ Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h3>📁 Cultural Corpus Collection</h3>
            <p>Upload and document cultural objects, traditions, and practices with rich metadata including images, 
            audio recordings, and videos. Support for multiple languages and regional dialects.</p>
            <ul>
                <li>Multimodal media upload (images, audio, video)</li>
                <li>Local language and dialect documentation</li>
                <li>Cultural context and usage information</li>
                <li>Geographic location tracking</li>
            </ul>
            <div style="margin-top: 1rem;">
                <a href="?page=Cultural_Corpus_Collection" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 15px; text-decoration: none; font-size: 0.9rem;">Start Collection</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h3>🤔 Idi-Emiti (What is this?)</h3>
            <p>Interactive cultural object identification game that helps preserve traditional vocabulary and 
            linguistic diversity. Users identify cultural objects in their local languages.</p>
            <ul>
                <li>Cultural object identification</li>
                <li>Local language vocabulary preservation</li>
                <li>Audio pronunciation recordings</li>
                <li>Regional dialect documentation</li>
            </ul>
            <div style="margin-top: 1rem;">
                <a href="?page=Idi_Emiti" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 15px; text-decoration: none; font-size: 0.9rem;">Try Idi-Emiti</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h3>📊 Analytics Dashboard</h3>
            <p>Comprehensive analytics and insights into cultural data collection, user engagement, and 
            platform growth. Monitor linguistic diversity and cultural preservation efforts.</p>
            <ul>
                <li>Real-time platform statistics</li>
                <li>Language and dialect analytics</li>
                <li>User engagement metrics</li>
                <li>Data quality assessment</li>
            </ul>
            <div style="margin-top: 1rem;">
                <a href="?page=Analytics_Dashboard" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.5rem 1rem; border-radius: 15px; text-decoration: none; font-size: 0.9rem;">View Analytics</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h3>🔐 User Authentication</h3>
            <p>Secure user management system with profile management, contribution tracking, and 
            personalized experience. Support for both MySQL and local storage.</p>
            <ul>
                <li>Secure login and registration</li>
                <li>User profile management</li>
                <li>Contribution history tracking</li>
                <li>Hybrid database support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("## 🛠️ Technology Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h4>Frontend</h4>
            <ul>
                <li>Streamlit Web Framework</li>
                <li>Responsive Design</li>
                <li>Interactive Components</li>
                <li>Real-time Updates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h4>Backend</h4>
            <ul>
                <li>Python Data Processing</li>
                <li>Pandas Analytics</li>
                <li>File Management</li>
                <li>Session Management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <h4>Database</h4>
            <ul>
                <li>MySQL Database</li>
                <li>CSV Data Storage</li>
                <li>JSON Configuration</li>
                <li>Data Migration Tools</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Cultural Impact
    st.markdown("## 🌟 Cultural Impact")
    
    st.markdown("""
    Our platform is making a significant impact on cultural preservation:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #feca57; padding: 1.5rem; margin: 1rem 0; border-radius: 10px;">
            <h4>🏛️ Heritage Preservation</h4>
            <p>Documenting traditional objects, practices, and knowledge that might otherwise be lost to time.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #feca57; padding: 1.5rem; margin: 1rem 0; border-radius: 10px;">
            <h4>🗣️ Linguistic Diversity</h4>
            <p>Preserving local languages and dialects through vocabulary documentation and pronunciation recordings.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #feca57; padding: 1.5rem; margin: 1rem 0; border-radius: 10px;">
            <h4>🌍 Community Engagement</h4>
            <p>Engaging communities in the preservation of their own cultural heritage through interactive features.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #feca57; padding: 1.5rem; margin: 1rem 0; border-radius: 10px;">
            <h4>📚 Educational Resource</h4>
            <p>Creating a comprehensive database for researchers, educators, and future generations to learn from.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Get Started Section
    st.markdown("## 🚀 Get Started")
    
    st.markdown("""
    Ready to contribute to cultural preservation? Join our platform and start documenting your cultural heritage today.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3>1️⃣ Create Account</h3>
            <p>Sign up for a free account to start contributing to our cultural database.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3>2️⃣ Upload Content</h3>
            <p>Share images, audio, and video of cultural objects with detailed descriptions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3>3️⃣ Preserve Heritage</h3>
            <p>Help preserve cultural traditions and languages for future generations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to Action
    if user:
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <a href="?page=Cultural_Corpus_Collection" style="background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem;">Continue Contributing</a>
            <a href="?page=Analytics_Dashboard" style="background: linear-gradient(45deg, #48dbfb, #0abde3); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem;">View Analytics</a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <a href="?page=Cultural_Corpus_Collection" style="background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem;">Start Contributing Now</a>
            <a href="?page=Sign_Up" style="background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; padding: 1rem 2rem; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; margin: 0.5rem;">Create Account</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Access Section
    if user:
        # Logged in user quick access
        st.markdown("## 🔐 Quick Access")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0;">
                <h3>📁 Upload Content</h3>
                <p>Share cultural objects, traditions, and practices with rich metadata.</p>
                <a href="?page=Cultural_Corpus_Collection" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.8rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 1rem; border: 2px solid rgba(255, 255, 255, 0.3);">Start Uploading</a>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0;">
                <h3>🤔 Play Idi-Emiti</h3>
                <p>Help preserve cultural vocabulary by identifying traditional objects.</p>
                <a href="?page=Idi_Emiti" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.8rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 1rem; border: 2px solid rgba(255, 255, 255, 0.3);">Start Playing</a>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0;">
                <h3>👤 My Profile</h3>
                <p>View your contributions, update your profile, and track your impact.</p>
                <a href="?page=My_Profile" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.8rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 1rem; border: 2px solid rgba(255, 255, 255, 0.3);">View Profile</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Guest user quick access
        st.markdown("## 🔐 Quick Access")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0;">
                <h3>👋 Welcome Back</h3>
                <p>Already have an account? Sign in to continue your cultural preservation journey.</p>
                <a href="?page=Login" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.8rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 1rem; border: 2px solid rgba(255, 255, 255, 0.3);">Sign In</a>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0;">
                <h3>🌟 Join Our Community</h3>
                <p>Create a free account and start contributing to cultural heritage preservation today.</p>
                <a href="?page=Sign_Up" style="background: rgba(255, 255, 255, 0.2); color: white; padding: 0.8rem 2rem; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 1rem; border: 2px solid rgba(255, 255, 255, 0.3);">Sign Up</a>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="background: #2c3e50; color: white; padding: 2rem; text-align: center; margin-top: 4rem;">
        <h3>🏛️ Cultural Corpus Collection Platform</h3>
        <p>Preserving cultural heritage through technology and community engagement</p>
        <p style="margin-top: 1rem; opacity: 0.8;">
            Built with ❤️ for cultural preservation | 
            <a href="mailto:support@culturalcorpus.org" style="color: #feca57;">Contact Us</a>
        </p>
    </div>
    
    <!-- Floating Action Button for Quick Access -->
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000;">
        <div style="background: linear-gradient(45deg, #ff6b6b, #feca57); border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3); cursor: pointer; transition: transform 0.3s ease;" onclick="window.location.href='?page=Cultural_Corpus_Collection'">
            <span style="color: white; font-size: 24px; font-weight: bold;">+</span>
        </div>
        <div style="position: absolute; bottom: 70px; right: 0; background: white; border-radius: 10px; padding: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.2); display: none;" id="quickAuth">
            <a href="?page=Cultural_Corpus_Collection" style="display: block; color: #333; text-decoration: none; padding: 0.5rem 1rem; border-radius: 5px; margin-bottom: 0.5rem;">Upload Content</a>
            <a href="?page=Idi_Emiti" style="display: block; color: #333; text-decoration: none; padding: 0.5rem 1rem; border-radius: 5px; margin-bottom: 0.5rem;">Play Idi-Emiti</a>
            <a href="?page=My_Profile" style="display: block; color: #333; text-decoration: none; padding: 0.5rem 1rem; border-radius: 5px; background: #feca57;">My Profile</a>
        </div>
    </div>
    
    <script>
        // Toggle quick auth menu
        document.querySelector('.floating-btn').addEventListener('click', function() {
            const menu = document.getElementById('quickAuth');
            menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
        });
    </script>
    """, unsafe_allow_html=True)

def analytics_dashboard_page():
    """Analytics dashboard page"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">📊 Analytics Dashboard</h1>
        <p class="hero-subtitle">Insights into cultural corpus growth and engagement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get analytics data
    analytics = get_comprehensive_analytics()
    
    # Overview metrics
    st.markdown("### 📈 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Submissions", analytics.get('growth_metrics', {}).get('total_submissions', 0))
    
    with col2:
        engagement = analytics.get('user_engagement', {})
        st.metric("Unique Contributors", engagement.get('unique_contributors', 0))
    
    with col3:
        content = analytics.get('content_analysis', {})
        st.metric("Languages Used", content.get('total_languages', 0))
    
    with col4:
        quality = analytics.get('quality_metrics', {})
        st.metric("Data Completeness", f"{quality.get('completeness_rate', 0)}%")
    
    # Detailed analytics sections
    st.markdown("### 📊 Detailed Analytics")
    
    # Media type distribution
    if analytics.get('content_analysis', {}).get('media_type_distribution'):
        st.markdown("#### Media Type Distribution")
        media_dist = analytics['content_analysis']['media_type_distribution']
        st.bar_chart(media_dist)
    
    # Language distribution
    if analytics.get('content_analysis', {}).get('most_common_language'):
        st.markdown("#### Language Distribution")
        # This would need to be implemented with actual language data
        st.info("Language distribution chart would be displayed here")
    
    # Growth trends
    if analytics.get('growth_metrics', {}).get('avg_daily_submissions'):
        st.markdown("#### Growth Trends")
        growth = analytics['growth_metrics']
        st.metric("Average Daily Submissions", f"{growth.get('avg_daily_submissions', 0):.2f}")
        st.metric("First Submission", growth.get('first_submission_date', 'N/A'))
        st.metric("Latest Submission", growth.get('last_submission_date', 'N/A'))

def authentication_page(auth_type):
    """Authentication page for login or signup"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🔐 User Authentication</h1>
        <p class="hero-subtitle">Join our cultural preservation community</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content container
    with st.container():
        st.markdown("""
        <div class="content-container">
        """, unsafe_allow_html=True)
        
        if auth_type == "login":
            render_login_form()
        elif auth_type == "signup":
            render_signup_form()
        
        st.markdown("</div>", unsafe_allow_html=True)

def admin_panel_page():
    """Admin panel page"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🔧 Admin Panel</h1>
        <p class="hero-subtitle">Manage and curate cultural corpus data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if admin is authenticated
    if not st.session_state.get(ADMIN_SESSION_KEY, False):
        admin_login_form()
        return
    
    # Admin is authenticated
    st.success("✅ Admin access granted")
    
    # Admin controls
    st.markdown("### 🔧 Admin Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 View All Submissions"):
            st.session_state.show_submissions = True
        
        if st.button("📈 Generate Analytics Report"):
            st.session_state.generate_report = True
    
    with col2:
        if st.button("🗑️ Clear All Data"):
            if st.button("⚠️ Confirm Clear"):
                # Clear data logic would go here
                st.warning("Data clearing functionality would be implemented here")
        
        if st.button("🚪 Logout"):
            st.session_state[ADMIN_SESSION_KEY] = False
            st.rerun()
    
    # Show submissions if requested
    if st.session_state.get('show_submissions', False):
        st.markdown("### 📋 All Submissions")
        try:
            df = pd.read_csv(CSV_FILE)
            st.dataframe(df, use_container_width=True)
        except:
            st.info("No submissions found")
    
    # Generate report if requested
    if st.session_state.get('generate_report', False):
        st.markdown("### 📈 Analytics Report")
        analytics = get_comprehensive_analytics()
        
        # Display analytics in a more readable format
        tab1, tab2 = st.tabs(["📊 Summary", "📄 Raw JSON"])
        
        with tab1:
            st.markdown("#### 📈 Platform Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Submissions", analytics.get('growth_metrics', {}).get('total_submissions', 0))
            
            with col2:
                st.metric("Unique Contributors", analytics.get('user_engagement', {}).get('unique_contributors', 0))
            
            with col3:
                st.metric("Languages Used", analytics.get('content_analysis', {}).get('total_languages', 0))
            
            with col4:
                st.metric("Data Completeness", f"{analytics.get('quality_metrics', {}).get('completeness_rate', 0)}%")
            
            # Time-based analytics
            st.markdown("#### 📅 Recent Activity")
            time_based = analytics.get('time_based', {})
            if time_based.get('recent_trend'):
                recent_data = time_based['recent_trend']
                if recent_data:
                    st.line_chart(recent_data)
            
            # User engagement
            st.markdown("#### 👥 User Engagement")
            engagement = analytics.get('user_engagement', {})
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Active Contributors:**")
                active_contributors = engagement.get('active_contributors', {})
                for contributor, count in list(active_contributors.items())[:5]:
                    st.markdown(f"- {contributor}: {count} submissions")
            
            with col2:
                st.markdown("**Session Statistics:**")
                st.markdown(f"- Average submissions per session: {engagement.get('avg_submissions_per_session', 0):.2f}")
                st.markdown(f"- Average session duration: {engagement.get('avg_session_duration', 0):.2f} minutes")
            
            # Content analysis
            st.markdown("#### 📝 Content Analysis")
            content = analytics.get('content_analysis', {})
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Language Distribution:**")
                st.markdown(f"- Most common language: {content.get('most_common_language', 'N/A')}")
                st.markdown(f"- Total languages: {content.get('total_languages', 0)}")
            
            with col2:
                st.markdown("**Category Distribution:**")
                st.markdown(f"- Most common category: {content.get('most_common_category', 'N/A')}")
                st.markdown(f"- Total categories: {content.get('total_categories', 0)}")
            
            # Quality metrics
            st.markdown("#### ✅ Data Quality")
            quality = analytics.get('quality_metrics', {})
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Completeness Rate", f"{quality.get('completeness_rate', 0)}%")
            
            with col2:
                st.metric("Language Completeness", f"{quality.get('language_completeness', 0)}%")
            
            with col3:
                st.metric("Geo Completeness", f"{quality.get('geo_completeness', 0)}%")
        
        with tab2:
            # Format the JSON properly for display
            import json
            try:
                formatted_json = json.dumps(analytics, indent=2, ensure_ascii=False)
                st.code(formatted_json, language='json')
            except Exception as e:
                st.error(f"Error formatting analytics report: {e}")
                st.json(analytics)
    
    # Idi-Emiti Statistics (Admin Only)
    st.markdown("---")
    st.markdown("### 🤔 Idi-Emiti Statistics")
    st.markdown("Comprehensive statistics for the cultural object identification game.")
    
    # Get Idi-Emiti analytics
    idi_emiti_stats = get_idi_emiti_analytics()
    
    # Helper function to safely get numeric values
    def safe_get_int(data, key, default=0):
        value = data.get(key, default)
        if isinstance(value, str):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        return value
    
    # Basic statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Identifications", safe_get_int(idi_emiti_stats, 'total_identifications'))
    
    with col2:
        st.metric("Languages Documented", safe_get_int(idi_emiti_stats, 'languages_documented'))
    
    with col3:
        st.metric("Dialects Documented", safe_get_int(idi_emiti_stats, 'dialects_documented'))
    
    with col4:
        st.metric("Audio Recordings", safe_get_int(idi_emiti_stats, 'audio_recordings'))
    
    # Detailed statistics
    total_identifications = idi_emiti_stats.get('total_identifications', 0)
    # Convert to int if it's a string
    if isinstance(total_identifications, str):
        try:
            total_identifications = int(total_identifications)
        except (ValueError, TypeError):
            total_identifications = 0
    
    if total_identifications > 0:
        st.markdown("#### 📊 Detailed Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top languages
            if idi_emiti_stats.get('top_languages'):
                st.markdown("**Top Languages:**")
                for lang, count in list(idi_emiti_stats['top_languages'].items())[:5]:
                    st.markdown(f"- {lang}: {count} identifications")
            else:
                st.info("No language data available")
        
        with col2:
            # Top dialects
            if idi_emiti_stats.get('top_dialects'):
                st.markdown("**Top Dialects:**")
                for dialect, count in list(idi_emiti_stats['top_dialects'].items())[:5]:
                    st.markdown(f"- {dialect}: {count} identifications")
            else:
                st.info("No dialect data available")
        
        # Confidence distribution
        if idi_emiti_stats.get('confidence_distribution'):
            st.markdown("#### 🎯 Confidence Distribution")
            confidence_data = idi_emiti_stats['confidence_distribution']
            st.bar_chart(confidence_data)
        
        # Recent Idi-Emiti submissions
        st.markdown("#### 📝 Recent Identifications")
        try:
            df = pd.read_csv(CSV_FILE)
            idi_emiti_df = df[df['category'] == 'Cultural Identification'].tail(10)
            if not idi_emiti_df.empty:
                display_df = idi_emiti_df[['timestamp', 'contributor_name', 'local_language_name', 'dialect_regional_variation', 'cultural_context']].copy()
                display_df.columns = ['Date', 'Contributor', 'Local Name', 'Dialect', 'Cultural Context']
                st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No recent identifications found")
        except:
            st.info("No identification data available")
    else:
        st.info("No Idi-Emiti data available yet. Encourage users to participate in the cultural identification game!")

if __name__ == "__main__":
    main() 