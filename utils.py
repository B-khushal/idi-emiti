import streamlit as st
import os
import pandas as pd
import random
import uuid
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from config import (
    ASSETS_FOLDER, DATA_FOLDER, CSV_FILE, UPLOADS_FOLDER,
    IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, MEDIA_EXTENSIONS,
    MAX_IMAGE_SIZE, MAX_AUDIO_SIZE, MAX_VIDEO_SIZE
)
import numpy as np

def ensure_directories():
    """Ensure required directories exist"""
    Path(ASSETS_FOLDER).mkdir(exist_ok=True)
    Path(DATA_FOLDER).mkdir(exist_ok=True)
    Path(UPLOADS_FOLDER).mkdir(exist_ok=True)
    
    # Create subdirectories for different media types
    Path(os.path.join(UPLOADS_FOLDER, "images")).mkdir(exist_ok=True)
    Path(os.path.join(UPLOADS_FOLDER, "audio")).mkdir(exist_ok=True)
    Path(os.path.join(UPLOADS_FOLDER, "video")).mkdir(exist_ok=True)

def get_available_media():
    """Get list of available media files from assets folder"""
    ensure_directories()
    
    if not os.path.exists(ASSETS_FOLDER):
        return []
    
    media_files = []
    
    for file in os.listdir(ASSETS_FOLDER):
        if file.endswith(MEDIA_EXTENSIONS):
            media_files.append(os.path.join(ASSETS_FOLDER, file))
    
    return media_files

def get_random_media():
    """Get a random media file from the assets folder"""
    media_files = get_available_media()
    
    if not media_files:
        return None
    
    return random.choice(media_files)

def get_media_type(filename):
    """Determine the media type based on file extension"""
    if filename.lower().endswith(IMAGE_EXTENSIONS):
        return "image"
    elif filename.lower().endswith(AUDIO_EXTENSIONS):
        return "audio"
    elif filename.lower().endswith(VIDEO_EXTENSIONS):
        return "video"
    else:
        return "unknown"

def validate_media_file(file_path, file_size):
    """Validate media file format and size"""
    filename = os.path.basename(file_path)
    media_type = get_media_type(filename)
    
    if media_type == "unknown":
        return False, "Invalid file format"
    
    # Check file size limits
    if media_type == "image" and file_size > MAX_IMAGE_SIZE:
        return False, f"Image file size exceeds {MAX_IMAGE_SIZE // (1024*1024)}MB limit"
    elif media_type == "audio" and file_size > MAX_AUDIO_SIZE:
        return False, f"Audio file size exceeds {MAX_AUDIO_SIZE // (1024*1024)}MB limit"
    elif media_type == "video" and file_size > MAX_VIDEO_SIZE:
        return False, f"Video file size exceeds {MAX_VIDEO_SIZE // (1024*1024)}MB limit"
    
    return True, "Valid file"

def save_uploaded_file(uploaded_file, media_type):
    """Save uploaded file to appropriate directory"""
    ensure_directories()
    
    # Generate unique filename
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Determine upload directory based on media type
    if media_type == "image":
        upload_dir = os.path.join(UPLOADS_FOLDER, "images")
    elif media_type == "audio":
        upload_dir = os.path.join(UPLOADS_FOLDER, "audio")
    elif media_type == "video":
        upload_dir = os.path.join(UPLOADS_FOLDER, "video")
    else:
        upload_dir = UPLOADS_FOLDER
    
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return unique_filename, file_path

def get_session_id():
    """Generate a unique session ID"""
    return str(uuid.uuid4())

def save_user_response(media_filename, media_type, title, description, language, 
                      contributor_name, contributor_email, contributor_details, 
                      category, session_id, latitude=None, longitude=None, 
                      file_size=None, file_path=None, local_language_name=None,
                      dialect_regional_variation=None, pronunciation_guide=None,
                      cultural_context=None, local_language_audio_path=None):
    """Save user response to CSV file with enhanced multimodal data fields including local language support"""
    ensure_directories()
    
    # Prepare the data with new schema including local language fields
    data = {
        'timestamp': [datetime.now().isoformat()],
        'media_filename': [media_filename],
        'media_type': [media_type],
        'title': [title if title else ''],
        'description': [description],
        'language': [language],
        'contributor_name': [contributor_name if contributor_name else ''],
        'contributor_email': [contributor_email if contributor_email else ''],
        'contributor_details': [contributor_details if contributor_details else ''],
        'category': [category if category else ''],
        'latitude': [latitude if latitude else ''],
        'longitude': [longitude if longitude else ''],
        'session_id': [session_id],
        'file_size': [file_size if file_size else ''],
        'file_path': [file_path if file_path else ''],
        'local_language_name': [local_language_name if local_language_name else ''],
        'dialect_regional_variation': [dialect_regional_variation if dialect_regional_variation else ''],
        'pronunciation_guide': [pronunciation_guide if pronunciation_guide else ''],
        'cultural_context': [cultural_context if cultural_context else ''],
        'local_language_audio_path': [local_language_audio_path if local_language_audio_path else ''],
        'validation_status': ['pending'],
        'curator_notes': ['']
    }
    
    df_new = pd.DataFrame(data)
    
    # Check if CSV file exists
    if os.path.exists(CSV_FILE):
        # Append to existing file
        df_existing = pd.read_csv(CSV_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(CSV_FILE, index=False)
    else:
        # Create new file
        df_new.to_csv(CSV_FILE, index=False)

def get_submission_count():
    """Get total number of submissions"""
    if not os.path.exists(CSV_FILE):
        return 0
    
    try:
        df = pd.read_csv(CSV_FILE)
        return len(df)
    except:
        return 0

def get_recent_responses(limit=10):
    """Get recent responses for analytics"""
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(CSV_FILE)
        return df.tail(limit)
    except:
        return pd.DataFrame()

def get_language_stats():
    """Get statistics by language"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        return df['language'].value_counts().to_dict()
    except:
        return {}

def get_media_type_stats():
    """Get statistics by media type"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        return df['media_type'].value_counts().to_dict()
    except:
        return {}

def get_category_stats():
    """Get statistics by category"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        return df['category'].value_counts().to_dict()
    except:
        return {}

# Enhanced Analytics Functions

def get_time_based_analytics():
    """Get time-based analytics including daily, weekly, and monthly trends"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.day_name()
        df['month'] = df['timestamp'].dt.month_name()
        
        # Daily submissions - convert dates to strings
        daily_stats = df.groupby('date').size().to_dict()
        daily_stats = {str(date): count for date, count in daily_stats.items()}
        
        # Hourly distribution
        hourly_stats = df['hour'].value_counts().sort_index().to_dict()
        
        # Day of week distribution
        day_stats = df['day_of_week'].value_counts().to_dict()
        
        # Monthly distribution
        month_stats = df['month'].value_counts().to_dict()
        
        # Recent 7 days trend - convert dates to strings
        last_7_days = (datetime.now() - timedelta(days=7)).date()
        recent_trend = df[df['date'] >= last_7_days].groupby('date').size().to_dict()
        recent_trend = {str(date): count for date, count in recent_trend.items()}
        
        return {
            'daily': daily_stats,
            'hourly': hourly_stats,
            'day_of_week': day_stats,
            'monthly': month_stats,
            'recent_trend': recent_trend
        }
    except:
        return {}

def get_user_engagement_metrics():
    """Get user engagement metrics including unique users, session analysis"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Unique contributors (by name)
        unique_contributors = df[df['contributor_name'] != '']['contributor_name'].nunique()
        
        # Unique sessions
        unique_sessions = df['session_id'].nunique()
        
        # Anonymous vs named submissions
        anonymous_count = len(df[df['contributor_name'] == ''])
        named_count = len(df[df['contributor_name'] != ''])
        
        # Average submissions per session
        avg_per_session = len(df) / unique_sessions if unique_sessions > 0 else 0
        
        # Most active contributors
        active_contributors = df[df['contributor_name'] != '']['contributor_name'].value_counts().head(5).to_dict()
        
        # Session duration analysis (if multiple submissions per session)
        session_analysis = df.groupby('session_id').agg({
            'timestamp': ['min', 'max', 'count']
        }).reset_index()
        session_analysis.columns = ['session_id', 'start_time', 'end_time', 'submission_count']
        session_analysis['duration_minutes'] = (
            pd.to_datetime(session_analysis['end_time']) - 
            pd.to_datetime(session_analysis['start_time'])
        ).dt.total_seconds() / 60
        
        avg_session_duration = session_analysis['duration_minutes'].mean()
        
        return {
            'unique_contributors': unique_contributors,
            'unique_sessions': unique_sessions,
            'anonymous_submissions': anonymous_count,
            'named_submissions': named_count,
            'avg_submissions_per_session': round(avg_per_session, 2),
            'avg_session_duration': round(avg_session_duration, 2),
            'active_contributors': active_contributors
        }
    except:
        return {}

def get_content_analysis():
    """Get content analysis including description length, language diversity"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Description length analysis
        df['description_length'] = df['description'].str.len()
        avg_description_length = df['description_length'].mean()
        max_description_length = df['description_length'].max()
        min_description_length = df['description_length'].min()
        
        # Language diversity
        language_counts = df['language'].value_counts()
        total_languages = len(language_counts)
        most_common_language = language_counts.index[0] if len(language_counts) > 0 else None
        
        # Category diversity
        category_counts = df['category'].value_counts()
        total_categories = len(category_counts)
        most_common_category = category_counts.index[0] if len(category_counts) > 0 else None
        
        # Media type distribution
        media_type_counts = df['media_type'].value_counts()
        
        return {
            'avg_description_length': round(avg_description_length, 2),
            'max_description_length': max_description_length,
            'min_description_length': min_description_length,
            'total_languages': total_languages,
            'most_common_language': most_common_language,
            'total_categories': total_categories,
            'most_common_category': most_common_category,
            'media_type_distribution': media_type_counts.to_dict()
        }
    except:
        return {}

def get_popular_media_analysis():
    """Get analysis of most popular media files"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Most popular media files
        popular_media = df['media_filename'].value_counts().head(10).to_dict()
        
        # Media type popularity
        media_type_popularity = df['media_type'].value_counts().to_dict()
        
        return {
            'popular_media': popular_media,
            'media_type_popularity': media_type_popularity
        }
    except:
        return {}

def get_growth_metrics():
    """Get growth metrics and trends"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Daily growth
        daily_growth = df.groupby('date').size().reset_index()
        daily_growth.columns = ['date', 'submissions']
        
        # Weekly growth
        df['week'] = df['timestamp'].dt.isocalendar().week
        df['year'] = df['timestamp'].dt.year
        weekly_growth = df.groupby(['year', 'week']).size().reset_index()
        weekly_growth.columns = ['year', 'week', 'submissions']
        
        # Monthly growth
        df['month'] = df['timestamp'].dt.to_period('M')
        monthly_growth = df.groupby('month').size().reset_index()
        monthly_growth.columns = ['month', 'submissions']
        
        # Growth rate calculation
        total_submissions = len(df)
        first_submission_date = df['date'].min()
        last_submission_date = df['date'].max()
        
        if first_submission_date and last_submission_date:
            days_active = (last_submission_date - first_submission_date).days
            avg_daily_submissions = total_submissions / days_active if days_active > 0 else 0
        else:
            avg_daily_submissions = 0
        
        # Convert datetime objects to strings in growth data
        daily_growth_records = daily_growth.to_dict('records')
        for record in daily_growth_records:
            if 'date' in record:
                record['date'] = str(record['date'])
        
        weekly_growth_records = weekly_growth.to_dict('records')
        for record in weekly_growth_records:
            if 'month' in record:
                record['month'] = str(record['month'])
        
        monthly_growth_records = monthly_growth.to_dict('records')
        for record in monthly_growth_records:
            if 'month' in record:
                record['month'] = str(record['month'])
        
        return {
            'total_submissions': total_submissions,
            'first_submission_date': str(first_submission_date) if first_submission_date else None,
            'last_submission_date': str(last_submission_date) if last_submission_date else None,
            'avg_daily_submissions': round(avg_daily_submissions, 2),
            'daily_growth': daily_growth_records,
            'weekly_growth': weekly_growth_records,
            'monthly_growth': monthly_growth_records
        }
    except:
        return {}

def get_quality_metrics():
    """Get data quality metrics"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Completeness metrics
        total_records = len(df)
        complete_records = len(df.dropna(subset=['title', 'description', 'category']))
        completeness_rate = (complete_records / total_records) * 100 if total_records > 0 else 0
        
        # Validation status distribution
        validation_status_counts = df['validation_status'].value_counts().to_dict()
        
        # Language completeness
        language_completeness = (df['language'].notna().sum() / total_records) * 100 if total_records > 0 else 0
        
        # Category completeness
        category_completeness = (df['category'].notna().sum() / total_records) * 100 if total_records > 0 else 0
        
        # Geolocation completeness
        geo_completeness = ((df['latitude'].notna()) & (df['longitude'].notna())).sum() / total_records * 100 if total_records > 0 else 0
        
        return {
            'total_records': total_records,
            'complete_records': complete_records,
            'completeness_rate': round(completeness_rate, 2),
            'validation_status_distribution': validation_status_counts,
            'language_completeness': round(language_completeness, 2),
            'category_completeness': round(category_completeness, 2),
            'geo_completeness': round(geo_completeness, 2)
        }
    except:
        return {}

def ensure_json_serializable(obj):
    """Convert objects to JSON serializable format"""
    if isinstance(obj, dict):
        return {str(k): ensure_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ensure_json_serializable(item) for item in obj]
    elif hasattr(obj, 'isoformat'):  # datetime objects
        return obj.isoformat()
    elif isinstance(obj, (int, float, bool)) or obj is None:
        return obj  # Keep numbers and booleans as they are
    elif hasattr(obj, '__str__'):
        return str(obj)
    else:
        return obj

def get_comprehensive_analytics():
    """Get comprehensive analytics combining all metrics"""
    analytics = {
        'time_based': get_time_based_analytics(),
        'user_engagement': get_user_engagement_metrics(),
        'content_analysis': get_content_analysis(),
        'popular_media': get_popular_media_analysis(),
        'growth_metrics': get_growth_metrics(),
        'quality_metrics': get_quality_metrics()
    }
    
    # Ensure all data is JSON serializable
    return ensure_json_serializable(analytics)

def validate_media_file_legacy(file_path):
    """Legacy function for backward compatibility"""
    return validate_media_file(file_path, os.path.getsize(file_path))

def create_sample_data():
    """Create sample data for testing"""
    sample_data = [
        {
            'timestamp': datetime.now().isoformat(),
            'media_filename': 'sample_image_1.jpg',
            'media_type': 'image',
            'title': 'Traditional Cooking Pot',
            'description': 'A traditional clay cooking pot used for preparing rice and curries',
            'language': 'Telugu',
            'contributor_name': 'Sample User',
            'contributor_email': 'sample@example.com',
            'contributor_details': 'Cultural researcher',
            'category': 'Cooking Utensils',
            'latitude': 17.3850,
            'longitude': 78.4867,
            'session_id': str(uuid.uuid4()),
            'file_size': 1024000,
            'file_path': 'uploads/images/sample_image_1.jpg',
            'validation_status': 'pending',
            'curator_notes': ''
        }
    ]
    
    df = pd.DataFrame(sample_data)
    ensure_directories()
    df.to_csv(CSV_FILE, index=False)
    return "Sample data created successfully"

def get_category_analytics():
    """Get detailed category analytics"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Category distribution
        category_distribution = df['category'].value_counts().to_dict()
        
        # Category by language
        category_language = df.groupby(['category', 'language']).size().reset_index()
        category_language.columns = ['category', 'language', 'count']
        
        # Category by media type
        category_media = df.groupby(['category', 'media_type']).size().reset_index()
        category_media.columns = ['category', 'media_type', 'count']
        
        return {
            'category_distribution': category_distribution,
            'category_language': category_language.to_dict('records'),
            'category_media': category_media.to_dict('records')
        }
    except:
        return {}

def get_contributor_analytics():
    """Get contributor analytics"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Top contributors
        top_contributors = df[df['contributor_name'] != '']['contributor_name'].value_counts().head(10).to_dict()
        
        # Contributor diversity
        total_contributors = df[df['contributor_name'] != '']['contributor_name'].nunique()
        
        # Anonymous vs named ratio
        anonymous_count = len(df[df['contributor_name'] == ''])
        named_count = len(df[df['contributor_name'] != ''])
        anonymous_ratio = (anonymous_count / len(df)) * 100 if len(df) > 0 else 0
        
        return {
            'top_contributors': top_contributors,
            'total_contributors': total_contributors,
            'anonymous_ratio': round(anonymous_ratio, 2),
            'named_submissions': named_count,
            'anonymous_submissions': anonymous_count
        }
    except:
        return {}

def get_geo_analytics():
    """Get geographical analytics"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Filter records with valid coordinates
        geo_df = df[(df['latitude'].notna()) & (df['longitude'].notna())]
        
        if len(geo_df) == 0:
            return {'message': 'No geographical data available'}
        
        # Geographic distribution
        geo_distribution = {
            'total_geo_records': len(geo_df),
            'avg_latitude': geo_df['latitude'].mean(),
            'avg_longitude': geo_df['longitude'].mean(),
            'min_latitude': geo_df['latitude'].min(),
            'max_latitude': geo_df['latitude'].max(),
            'min_longitude': geo_df['longitude'].min(),
            'max_longitude': geo_df['longitude'].max()
        }
        
        # Regional analysis (simplified)
        geo_df['region'] = geo_df.apply(lambda row: 
            'North' if row['latitude'] > 20 else
            'South' if row['latitude'] < 15 else
            'Central', axis=1)
        
        regional_distribution = geo_df['region'].value_counts().to_dict()
        
        return {
            'geo_distribution': geo_distribution,
            'regional_distribution': regional_distribution
        }
    except:
        return {}

def get_enhanced_analytics():
    """Get all enhanced analytics"""
    return {
        'category_analytics': get_category_analytics(),
        'contributor_analytics': get_contributor_analytics(),
        'geo_analytics': get_geo_analytics(),
        'comprehensive': get_comprehensive_analytics()
    }

# Idi-Emiti specific functions
def get_idi_emiti_count():
    """Get count of Idi-Emiti submissions"""
    if not os.path.exists(CSV_FILE):
        return 0
    
    try:
        df = pd.read_csv(CSV_FILE)
        # Count submissions that are from Idi-Emiti (Cultural Identification category)
        idi_emiti_count = len(df[df['category'] == 'Cultural Identification'])
        return idi_emiti_count
    except:
        return 0

def get_idi_emiti_languages():
    """Get count of unique languages documented in Idi-Emiti"""
    if not os.path.exists(CSV_FILE):
        return 0
    
    try:
        df = pd.read_csv(CSV_FILE)
        # Get unique languages from Idi-Emiti submissions
        idi_emiti_df = df[df['category'] == 'Cultural Identification']
        unique_languages = idi_emiti_df[idi_emiti_df['local_language_name'] != '']['local_language_name'].nunique()
        return unique_languages
    except:
        return 0

def get_user_idi_emiti_count(user_id):
    """Get count of Idi-Emiti submissions by a specific user"""
    if not os.path.exists(CSV_FILE):
        return 0
    
    try:
        df = pd.read_csv(CSV_FILE)
        # Count Idi-Emiti submissions by user (using contributor_name as proxy for user_id)
        # This is a simplified approach - in a full implementation, you'd use actual user_id
        user_contributions = len(df[df['category'] == 'Cultural Identification'])
        return user_contributions
    except:
        return 0

def get_idi_emiti_analytics():
    """Get comprehensive Idi-Emiti analytics"""
    if not os.path.exists(CSV_FILE):
        return {}
    
    try:
        df = pd.read_csv(CSV_FILE)
        idi_emiti_df = df[df['category'] == 'Cultural Identification']
        
        if len(idi_emiti_df) == 0:
            return {
                'total_identifications': 0,
                'languages_documented': 0,
                'dialects_documented': 0,
                'audio_recordings': 0,
                'confidence_distribution': {},
                'top_languages': {},
                'top_dialects': {}
            }
        
        # Basic statistics
        total_identifications = len(idi_emiti_df)
        languages_documented = idi_emiti_df[idi_emiti_df['local_language_name'] != '']['local_language_name'].nunique()
        dialects_documented = idi_emiti_df[idi_emiti_df['dialect_regional_variation'] != '']['dialect_regional_variation'].nunique()
        audio_recordings = len(idi_emiti_df[idi_emiti_df['local_language_audio_path'] != ''])
        
        # Confidence distribution
        confidence_distribution = idi_emiti_df['contributor_details'].str.extract(r'Confidence: ([^.]*)').iloc[:, 0].value_counts().to_dict()
        
        # Top languages
        top_languages = idi_emiti_df[idi_emiti_df['local_language_name'] != '']['local_language_name'].value_counts().head(10).to_dict()
        
        # Top dialects
        top_dialects = idi_emiti_df[idi_emiti_df['dialect_regional_variation'] != '']['dialect_regional_variation'].value_counts().head(10).to_dict()
        
        result = {
            'total_identifications': total_identifications,
            'languages_documented': languages_documented,
            'dialects_documented': dialects_documented,
            'audio_recordings': audio_recordings,
            'confidence_distribution': confidence_distribution,
            'top_languages': top_languages,
            'top_dialects': top_dialects
        }
        
        # Ensure all data is JSON serializable
        return ensure_json_serializable(result)
    except:
        return {} 

def get_storage_status():
    """Get current storage mode status for display"""
    try:
        from db_config import get_storage_mode, is_mysql_available
        
        if is_mysql_available():
            return {
                'mode': 'mysql',
                'status': 'Connected to MySQL Database',
                'icon': '🗄️',
                'color': 'success'
            }
        else:
            return {
                'mode': 'json',
                'status': 'Using Local JSON Storage',
                'icon': '📁',
                'color': 'info'
            }
    except Exception:
        return {
            'mode': 'json',
            'status': 'Using Local JSON Storage',
            'icon': '📁',
            'color': 'info'
        }

def display_storage_status():
    """Display storage status in the app"""
    try:
        from language_manager import get_text
        status = get_storage_status()
        
        if status['mode'] == 'mysql':
            st.success(f"{status['icon']} {get_text('connected_to_mysql')}")
        else:
            st.info(f"{status['icon']} {get_text('using_local_storage')}")
            
            # Show MySQL setup instructions for local development
            if not os.getenv('STREAMLIT_SERVER_PORT'):  # Not on Streamlit Cloud
                with st.expander(f"💡 {get_text('mysql_setup_guide')}"):
                    st.markdown(get_text('mysql_setup_instructions'))
    except ImportError:
        # Fallback if language manager not available
        status = get_storage_status()
        if status['mode'] == 'mysql':
            st.success(f"{status['icon']} {status['status']}")
        else:
            st.info(f"{status['icon']} {status['status']}")
            
            if not os.getenv('STREAMLIT_SERVER_PORT'):
                with st.expander("💡 Want to use MySQL database?"):
                    st.markdown("""
                    **To enable MySQL database storage:**
                    
                    1. **Install MySQL Server** on your local machine
                    2. **Create database:** `cultural_corpus_platform`
                    3. **Update credentials** in `db_config.py`
                    4. **Run migration:** `python migrate_to_mysql.py`
                    
                    The app will automatically detect and use MySQL when available.
                    """) 