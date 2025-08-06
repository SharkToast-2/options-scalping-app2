#!/bin/bash

echo "🚀 Creating new GitHub repository: 'updated Options King'"
echo "=================================================="

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it first:"
    echo "  macOS: brew install gh"
    echo "  Or visit: https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready"

# Create the new repository
echo "📦 Creating repository: updated-Options-King"
gh repo create "updated-Options-King" \
    --public \
    --description "Advanced options scalping bot with Schwab API integration - automated trading with real-time signals" \
    --homepage "https://github.com/$(gh api user --jq .login)/updated-Options-King"

if [ $? -eq 0 ]; then
    echo "✅ Repository created successfully!"
    
    # Add the new remote
    echo "🔗 Adding new remote..."
    git remote add new-origin https://github.com/$(gh api user --jq .login)/updated-Options-King.git
    
    # Push to the new repository
    echo "📤 Pushing code to new repository..."
    git push -u new-origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 SUCCESS! Your new repository is ready:"
        echo "🌐 https://github.com/$(gh api user --jq .login)/updated-Options-King"
        echo ""
        echo "📋 Next steps:"
        echo "1. Visit the repository URL above"
        echo "2. Update the README if needed"
        echo "3. Set up any additional GitHub features (Issues, Projects, etc.)"
        echo "4. Share your repository with others!"
        echo ""
        echo "🔧 To continue working with this repository:"
        echo "   git remote set-url origin https://github.com/$(gh api user --jq .login)/updated-Options-King.git"
    else
        echo "❌ Failed to push to new repository"
        exit 1
    fi
else
    echo "❌ Failed to create repository"
    exit 1
fi 