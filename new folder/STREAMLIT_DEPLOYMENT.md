# Streamlit Cloud Deployment Guide

## 🚀 Deploying Cultural Corpus Collection Platform to Streamlit Cloud

This guide will help you deploy the Cultural Corpus Collection Platform to Streamlit Cloud with proper database configuration.

## 📋 Prerequisites

1. **GitHub Account**: Your code must be in a GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Python Dependencies**: All required packages are in `requirements.txt`

## 🔧 Deployment Steps

### 1. Prepare Your Repository

Ensure your repository contains:
- `app.py` (main application file)
- `requirements.txt` (dependencies)
- All supporting files (auth.py, config.py, utils.py, etc.)
- `data/` folder for JSON storage
- `assets/` folder for images

### 2. Database Configuration

The app automatically detects and uses the best available storage:

#### Option A: Local JSON Storage (Default)
- ✅ **Works out of the box** on Streamlit Cloud
- ✅ **No additional setup required**
- ✅ **Automatic fallback** when MySQL is not available

#### Option B: MySQL Database (Optional)
If you want to use MySQL on Streamlit Cloud:

1. **Set up a MySQL database** (e.g., PlanetScale, Railway, or AWS RDS)
2. **Configure environment variables** in Streamlit Cloud:
   - `MYSQL_HOST`: Your MySQL host
   - `MYSQL_USER`: Database username
   - `MYSQL_PASSWORD`: Database password
   - `MYSQL_DATABASE`: Database name

### 3. Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app**:
   - **Repository**: Select your GitHub repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom subdomain (optional)

5. **Click "Deploy"**

### 4. Environment Variables (Optional)

If using MySQL, add these in Streamlit Cloud settings:

```
MYSQL_HOST=your-mysql-host.com
MYSQL_USER=your-username
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=cultural_corpus_platform
```

## 🔍 Verification

After deployment, check:

1. **Storage Status**: The app shows which storage mode is active
2. **User Registration**: Test creating a new account
3. **File Uploads**: Test uploading images/audio/video
4. **Idi-Emiti Game**: Test the cultural object identification feature

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all required files are in the repository
   - Check `requirements.txt` has all dependencies

2. **File Permission Errors**
   - The app uses local JSON storage by default
   - No special permissions needed

3. **Database Connection Errors**
   - App automatically falls back to JSON storage
   - Check environment variables if using MySQL

4. **Memory Issues**
   - Streamlit Cloud has memory limits
   - Large file uploads may be restricted
   - Consider compressing images/videos

### Performance Tips

1. **Optimize Images**: Use compressed formats (JPEG, WebP)
2. **Limit File Sizes**: Keep uploads under 200MB
3. **Use Caching**: The app includes built-in caching
4. **Monitor Usage**: Check Streamlit Cloud analytics

## 📊 Monitoring

### Streamlit Cloud Dashboard
- Monitor app performance
- Check resource usage
- View error logs

### App Analytics
- User registration statistics
- Content submission metrics
- Platform usage analytics

## 🔄 Updates

To update your deployed app:

1. **Push changes** to your GitHub repository
2. **Streamlit Cloud automatically redeploys**
3. **Check the deployment status** in your dashboard

## 📞 Support

If you encounter issues:

1. **Check Streamlit Cloud logs** in your dashboard
2. **Review error messages** in the app
3. **Verify file structure** matches the repository
4. **Test locally** before deploying

## 🎉 Success!

Your Cultural Corpus Collection Platform is now live on Streamlit Cloud! 

The app will automatically:
- ✅ Use JSON storage by default
- ✅ Fall back gracefully if MySQL is unavailable
- ✅ Handle user authentication
- ✅ Support file uploads
- ✅ Provide analytics dashboard

Users can now contribute to cultural heritage preservation from anywhere in the world! 