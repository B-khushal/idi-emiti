import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import get_recent_responses, get_language_stats, get_image_stats, get_submission_count
from config import *

# Page configuration
st.set_page_config(
    page_title=f"Admin Dashboard - {APP_TITLE}",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title(f"📊 Admin Dashboard - {APP_TITLE}")
    st.markdown("---")
    
    # Check if data exists
    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            st.warning("No data available yet. Start collecting responses!")
            return
    except FileNotFoundError:
        st.warning("No data file found. Start collecting responses!")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_submissions = len(df)
        st.metric("Total Submissions", total_submissions)
    
    with col2:
        unique_users = df['session_id'].nunique()
        st.metric("Unique Sessions", unique_users)
    
    with col3:
        languages_used = df['language'].nunique()
        st.metric("Languages Used", languages_used)
    
    with col4:
        images_used = df['image_filename'].nunique()
        st.metric("Images Used", images_used)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Submissions by Language")
        lang_counts = df['language'].value_counts()
        fig_lang = px.bar(
            x=lang_counts.index, 
            y=lang_counts.values,
            title="Responses by Language"
        )
        fig_lang.update_layout(xaxis_title="Language", yaxis_title="Count")
        st.plotly_chart(fig_lang, use_container_width=True)
    
    with col2:
        st.subheader("🖼️ Submissions by Image")
        img_counts = df['image_filename'].value_counts().head(10)
        fig_img = px.bar(
            x=img_counts.index, 
            y=img_counts.values,
            title="Top 10 Most Viewed Images"
        )
        fig_img.update_layout(xaxis_title="Image", yaxis_title="Count")
        fig_img.update_xaxes(tickangle=45)
        st.plotly_chart(fig_img, use_container_width=True)
    
    # Recent submissions timeline
    st.subheader("📅 Recent Submissions Timeline")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_sorted = df.sort_values('timestamp')
    
    fig_timeline = px.line(
        df_sorted, 
        x='timestamp', 
        y=range(len(df_sorted)),
        title="Cumulative Submissions Over Time"
    )
    fig_timeline.update_layout(xaxis_title="Time", yaxis_title="Cumulative Submissions")
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Recent responses table
    st.subheader("📝 Recent Responses")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        language_filter = st.selectbox(
            "Filter by Language:",
            ["All"] + list(df['language'].unique())
        )
    
    with col2:
        limit = st.slider("Number of responses to show:", 5, 50, 20)
    
    # Apply filters
    filtered_df = df.copy()
    if language_filter != "All":
        filtered_df = filtered_df[filtered_df['language'] == language_filter]
    
    # Display recent responses
    recent_df = filtered_df.tail(limit)[['timestamp', 'name', 'language', 'description', 'image_filename']]
    recent_df['timestamp'] = pd.to_datetime(recent_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        recent_df,
        column_config={
            "timestamp": "Time",
            "name": "Name",
            "language": "Language", 
            "description": "Description",
            "image_filename": "Image"
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Export functionality
    st.markdown("---")
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Click to download",
                data=csv,
                file_name=f"cultural_responses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Download Summary Report"):
            # Create summary report
            summary = f"""
Cultural Responses Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Submissions: {len(df)}
Unique Sessions: {df['session_id'].nunique()}
Languages Used: {df['language'].nunique()}
Images Used: {df['image_filename'].nunique()}

Top Languages:
{df['language'].value_counts().head(5).to_string()}

Top Images:
{df['image_filename'].value_counts().head(5).to_string()}

Recent Activity (Last 10 responses):
{df.tail(10)[['timestamp', 'language', 'description']].to_string()}
            """
            
            st.download_button(
                label="Click to download report",
                data=summary,
                file_name=f"cultural_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main() 