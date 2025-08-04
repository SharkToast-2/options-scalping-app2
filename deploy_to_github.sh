#!/bin/bash

# Deploy Options Scalping App to GitHub and Streamlit Cloud
echo "🚀 Deploying Options Scalping App to GitHub and Streamlit Cloud"
echo "=============================================================="

# Check if GitHub username is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide your GitHub username"
    echo "Usage: ./deploy_to_github.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "Example: ./deploy_to_github.sh markrasdall"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="options-scalping-app"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo "📋 Deployment Configuration:"
echo "   GitHub Username: $GITHUB_USERNAME"
echo "   Repository Name: $REPO_NAME"
echo "   Repository URL: $REPO_URL"
echo ""

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists. Removing it..."
    git remote remove origin
fi

# Add GitHub remote
echo "🔗 Adding GitHub remote..."
git remote add origin $REPO_URL

# Set branch to main
echo "🌿 Setting branch to main..."
git branch -M main

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "=================================="
    echo "🌐 Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "🚀 Next Steps for Streamlit Cloud Deployment:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select repository: $REPO_NAME"
    echo "5. Set main file path: ui/streamlit_app.py"
    echo "6. Click 'Deploy'"
    echo ""
    echo "🔐 After deployment, add these secrets in Streamlit Cloud:"
    echo "   [api_keys]"
    echo "   polygon_api_key = \"ylJB2jaCAWQaHTa7BZFB60GAoapmK97P\""
    echo "   schwab_trading_key = \"3ZHxbk0X7QYK6s0T8VkKNfSkKI1M8LQu\""
    echo "   schwab_trading_secret = \"eUDIuuRPUDz524ih\""
    echo ""
    echo "🎉 Your app will be live at: https://your-app-name.streamlit.app"
else
    echo ""
    echo "❌ Failed to push to GitHub. Please check:"
    echo "1. Repository exists on GitHub"
    echo "2. You have write access to the repository"
    echo "3. Your GitHub credentials are correct"
    echo ""
    echo "💡 Make sure you've created the repository at:"
    echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
fi 