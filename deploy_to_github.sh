#!/bin/bash

# Options Scalping App - GitHub Deployment Script
# This script helps you deploy your project to GitHub

set -e  # Exit on any error

echo "🚀 Options Scalping App - GitHub Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
else
    print_status "Git repository already exists"
fi

# Check if remote origin exists
if git remote get-url origin &> /dev/null; then
    print_status "Remote origin already configured"
    REMOTE_URL=$(git remote get-url origin)
    print_info "Current remote: $REMOTE_URL"
else
    print_warning "No remote origin configured"
    echo ""
    print_info "Please provide your GitHub repository URL:"
    echo "Example: https://github.com/yourusername/options-scalping-app.git"
    read -p "GitHub URL: " GITHUB_URL
    
    if [ -z "$GITHUB_URL" ]; then
        print_error "GitHub URL is required"
        exit 1
    fi
    
    git remote add origin "$GITHUB_URL"
    print_status "Remote origin added: $GITHUB_URL"
fi

# Check for sensitive files that shouldn't be committed
SENSITIVE_FILES=("config.json" "tos_config.py" "tos_tokens.json" ".env" "*.db" "*.log")

print_info "Checking for sensitive files..."

for file in "${SENSITIVE_FILES[@]}"; do
    if ls $file 2>/dev/null; then
        print_warning "Found sensitive file: $file"
        print_info "This file will be ignored by .gitignore"
    fi
done

# Add all files
print_info "Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    print_warning "No changes to commit"
else
    # Get commit message
    echo ""
    print_info "Enter commit message (or press Enter for default):"
    read -p "Commit message: " COMMIT_MESSAGE
    
    if [ -z "$COMMIT_MESSAGE" ]; then
        COMMIT_MESSAGE="Initial commit: Options Scalping Application"
    fi
    
    # Commit changes
    print_info "Committing changes..."
    git commit -m "$COMMIT_MESSAGE"
    print_status "Changes committed"
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
print_info "Current branch: $CURRENT_BRANCH"

# Push to GitHub
print_info "Pushing to GitHub..."
if git push -u origin "$CURRENT_BRANCH"; then
    print_status "Successfully pushed to GitHub!"
else
    print_error "Failed to push to GitHub"
    print_info "You may need to:"
    print_info "1. Create the repository on GitHub first"
    print_info "2. Authenticate with GitHub"
    print_info "3. Check your internet connection"
    exit 1
fi

echo ""
print_status "Deployment completed successfully!"
echo ""
print_info "Next steps:"
echo "1. Visit your GitHub repository"
echo "2. Set up GitHub Pages (optional)"
echo "3. Configure GitHub Actions (optional)"
echo "4. Add collaborators (optional)"
echo ""
print_info "Your repository URL:"
git remote get-url origin
echo ""
print_info "Happy coding! 🎉" 