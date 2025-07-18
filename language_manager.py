"""
Language management utility for Cultural Corpus Collection Platform
Handles language switching, translations, and localization
"""

import streamlit as st
from config import SUPPORTED_LANGUAGES, TRANSLATIONS

def get_current_language():
    """Get the currently selected language from session state"""
    if 'current_language' not in st.session_state:
        st.session_state.current_language = 'en'  # Default to English
    return st.session_state.current_language

def set_language(language_code):
    """Set the current language"""
    if language_code in SUPPORTED_LANGUAGES:
        st.session_state.current_language = language_code
        return True
    return False

def get_text(key, language_code=None):
    """Get translated text for a given key and language"""
    if language_code is None:
        language_code = get_current_language()
    
    # Get translations for the language
    translations = TRANSLATIONS.get(language_code, TRANSLATIONS['en'])
    
    # Return translated text or fallback to English
    return translations.get(key, TRANSLATIONS['en'].get(key, key))

def render_language_selector():
    """Render language selector component"""
    current_lang = get_current_language()
    
    st.sidebar.markdown("### 🌐 " + get_text('language_selector'))
    
    # Create language options
    language_options = {name: code for code, name in SUPPORTED_LANGUAGES.items()}
    
    selected_language = st.sidebar.selectbox(
        get_text('change_language'),
        options=list(language_options.keys()),
        index=list(language_options.values()).index(current_lang),
        key="language_selector"
    )
    
    # Update language if changed
    if language_options[selected_language] != current_lang:
        set_language(language_options[selected_language])
        st.rerun()

def get_language_name(language_code):
    """Get the display name for a language code"""
    return SUPPORTED_LANGUAGES.get(language_code, 'English')

def get_language_code(language_name):
    """Get the language code for a language name"""
    for code, name in SUPPORTED_LANGUAGES.items():
        if name == language_name:
            return code
    return 'en'

def is_rtl_language(language_code):
    """Check if the language is right-to-left (RTL)"""
    rtl_languages = ['ur', 'ar']  # Urdu, Arabic
    return language_code in rtl_languages

def get_text_direction(language_code=None):
    """Get text direction for the language"""
    if language_code is None:
        language_code = get_current_language()
    
    return 'rtl' if is_rtl_language(language_code) else 'ltr'

def apply_language_styles():
    """Apply language-specific CSS styles"""
    current_lang = get_current_language()
    direction = get_text_direction(current_lang)
    
    css = f"""
    <style>
        /* Language-specific styles */
        .stApp {{
            direction: {direction};
        }}
        
        /* RTL language adjustments */
        {f'''
        .stTextInput > div > div > input {{
            text-align: right;
        }}
        .stTextArea > div > div > textarea {{
            text-align: right;
        }}
        ''' if direction == 'rtl' else ''}
        
        /* Language selector styles */
        .language-selector {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        .language-flag {{
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def get_language_flag(language_code):
    """Get flag emoji for language"""
    flags = {
        'en': '🇺🇸',
        'hi': '🇮🇳',
        'te': '🇮🇳',
        'ta': '🇮🇳',
        'bn': '🇮🇳',
        'mr': '🇮🇳',
        'gu': '🇮🇳',
        'kn': '🇮🇳',
        'ml': '🇮🇳',
        'pa': '🇮🇳',
        'or': '🇮🇳',
        'as': '🇮🇳',
        'sa': '🇮🇳',
        'ur': '🇵🇰'
    }
    return flags.get(language_code, '🌐')

def render_language_banner():
    """Render a language banner showing current language"""
    current_lang = get_current_language()
    flag = get_language_flag(current_lang)
    language_name = get_language_name(current_lang)
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); 
                border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 15px; 
                padding: 0.5rem 1rem; margin: 0.5rem 0; text-align: center;">
        <span style="font-size: 1.2rem;">{flag}</span>
        <span style="margin-left: 0.5rem; font-weight: bold;">{language_name}</span>
    </div>
    """, unsafe_allow_html=True)

def initialize_language_session():
    """Initialize language session state"""
    if 'current_language' not in st.session_state:
        st.session_state.current_language = 'en'
    
    # Apply language-specific styles
    apply_language_styles()

def get_translated_categories():
    """Get categories translated to current language"""
    current_lang = get_current_language()
    
    # Category translations
    category_translations = {
        'en': [
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
        ],
        'hi': [
            "पारंपरिक वस्त्र और वस्त्र",
            "संगीत वाद्ययंत्र",
            "खाना पकाने के बर्तन और औजार",
            "धार्मिक और अनुष्ठानिक वस्तुएं",
            "कृषि उपकरण",
            "कला और शिल्प",
            "आभूषण और सामान",
            "खेल और खिलौने",
            "स्थापत्य और संरचनाएं",
            "भोजन और पेय",
            "अन्य"
        ],
        'te': [
            "సాంప్రదాయ వస్త్రాలు మరియు వస్త్రాలు",
            "సంగీత వాయిద్యాలు",
            "వంట పాత్రలు మరియు ఉపకరణాలు",
            "మత మరియు ఆచార వస్తువులు",
            "వ్యవసాయ ఉపకరణాలు",
            "కళ మరియు చేతి వృత్తులు",
            "నగలు మరియు అలంకారాలు",
            "ఆటలు మరియు బొమ్మలు",
            "వాస్తుకళ మరియు నిర్మాణాలు",
            "ఆహారం మరియు పానీయాలు",
            "ఇతరములు"
        ]
    }
    
    return category_translations.get(current_lang, category_translations['en'])

def get_translated_placeholders():
    """Get form placeholders translated to current language"""
    current_lang = get_current_language()
    
    placeholder_translations = {
        'en': {
            'name': 'Enter your name',
            'description': 'Describe the cultural object, its significance, and usage...',
            'user_details': 'Share your cultural background, profession, and location...',
            'latitude': 'Enter latitude (optional)',
            'longitude': 'Enter longitude (optional)',
            'title': 'Enter a title for this cultural object',
            'category': 'Select a category'
        },
        'hi': {
            'name': 'अपना नाम दर्ज करें',
            'description': 'सांस्कृतिक वस्तु का वर्णन करें, इसका महत्व और उपयोग...',
            'user_details': 'अपनी सांस्कृतिक पृष्ठभूमि, पेशा और स्थान साझा करें...',
            'latitude': 'अक्षांश दर्ज करें (वैकल्पिक)',
            'longitude': 'देशांतर दर्ज करें (वैकल्पिक)',
            'title': 'इस सांस्कृतिक वस्तु के लिए शीर्षक दर्ज करें',
            'category': 'एक श्रेणी चुनें'
        },
        'te': {
            'name': 'మీ పేరును నమోదు చేయండి',
            'description': 'సాంస్కృతిక వస్తువును వివరించండి, దాని ప్రాముఖ్యత మరియు ఉపయోగం...',
            'user_details': 'మీ సాంస్కృతిక నేపథ్యం, వృత్తి మరియు స్థానాన్ని పంచుకోండి...',
            'latitude': 'అక్షాంశాన్ని నమోదు చేయండి (ఐచ్ఛికం)',
            'longitude': 'రేఖాంశాన్ని నమోదు చేయండి (ఐచ్ఛికం)',
            'title': 'ఈ సాంస్కృతిక వస్తువుకు శీర్షికను నమోదు చేయండి',
            'category': 'ఒక వర్గాన్ని ఎంచుకోండి'
        }
    }
    
    return placeholder_translations.get(current_lang, placeholder_translations['en']) 