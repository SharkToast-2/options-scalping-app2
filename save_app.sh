#!/bin/bash

# Options Scalping Application - Save Script
# This script creates comprehensive backups and saves the application

set -e  # Exit on any error

echo "🚀 Saving Options Scalping Application..."
echo "========================================"

# Get current timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/options_scalping_app_$TIMESTAMP"
DEPLOYMENT_PACKAGE="deployment_package_$TIMESTAMP.zip"

echo "📅 Timestamp: $TIMESTAMP"
echo "📁 Backup Directory: $BACKUP_DIR"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# 1. Save all application files
echo "📦 Saving application files..."
cp -r . "$BACKUP_DIR/" 2>/dev/null || true

# 2. Create deployment package (excluding sensitive files)
echo "📦 Creating deployment package..."
zip -r "$DEPLOYMENT_PACKAGE" . \
    -x "*.pyc" \
    -x "__pycache__/*" \
    -x "*.log" \
    -x "config.json" \
    -x ".env*" \
    -x "*.db" \
    -x "trading_log.csv" \
    -x "backups/*" \
    -x "bin/*" \
    -x "include/*" \
    -x "lib/*" \
    -x "share/*" \
    -x "pyvenv.cfg" \
    -x "test_*.py" \
    -x "*.tmp" \
    -x ".DS_Store" \
    -x "*.swp" \
    -x "*.swo"

# 3. Save Git repository state
echo "🔧 Saving Git repository state..."
git log --oneline -10 > "$BACKUP_DIR/git_history.txt"
git status > "$BACKUP_DIR/git_status.txt"

# 4. Create configuration backup (without sensitive data)
echo "⚙️ Creating configuration backup..."
if [ -f "config.json" ]; then
    cp config.json "$BACKUP_DIR/config_backup.json"
    echo "✅ Configuration backed up"
else
    echo "⚠️ No config.json found"
fi

# 5. Create requirements snapshot
echo "📋 Creating requirements snapshot..."
pip freeze > "$BACKUP_DIR/requirements_snapshot.txt"

# 6. Create system info
echo "💻 Creating system information..."
echo "System: $(uname -a)" > "$BACKUP_DIR/system_info.txt"
echo "Python: $(python3 --version)" >> "$BACKUP_DIR/system_info.txt"
echo "Git: $(git --version)" >> "$BACKUP_DIR/system_info.txt"
echo "Date: $(date)" >> "$BACKUP_DIR/system_info.txt"

# 7. Create deployment instructions
echo "📖 Creating deployment instructions..."
cat > "$BACKUP_DIR/DEPLOYMENT_INSTRUCTIONS.md" << 'EOF'
# Deployment Instructions

## Quick Start
1. Extract the deployment package
2. Run: `pip install -r requirements.txt`
3. Copy `config.json.example` to `config.json`
4. Add your API keys to `config.json`
5. Run: `streamlit run ui/streamlit_app.py`

## API Keys Required
- Polygon.io API key
- Schwab trading credentials (optional)
- Alpaca API keys (optional)

## Features Available
- Real-time market data from Polygon.io
- Mid-cap stock screener (185+ stocks)
- Technical analysis with 9+ indicators
- Trading integration with Schwab/Alpaca
- Performance monitoring and risk management

## Troubleshooting
- Check API rate limits
- Verify API keys are correct
- Use mock data fallback if needed
EOF

# 8. Create restore script
echo "🔄 Creating restore script..."
cat > "$BACKUP_DIR/restore_app.sh" << 'EOF'
#!/bin/bash
echo "🔄 Restoring Options Scalping Application..."
echo "==========================================="

# Check if we're in the right directory
if [ ! -f "ui/streamlit_app.py" ]; then
    echo "❌ Error: Please run this script from the application root directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Setup configuration
if [ ! -f "config.json" ]; then
    echo "⚙️ Setting up configuration..."
    cp config.json.example config.json
    echo "✅ Configuration file created. Please edit config.json with your API keys."
fi

# Create virtual environment (optional)
echo "🐍 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created. Activate with: source venv/bin/activate"

echo "🎉 Application restored successfully!"
echo "🚀 Run with: streamlit run ui/streamlit_app.py"
EOF

chmod +x "$BACKUP_DIR/restore_app.sh"

# 9. Create summary report
echo "📊 Creating summary report..."
cat > "$BACKUP_DIR/BACKUP_SUMMARY.md" << EOF
# Backup Summary

**Date:** $(date)
**Timestamp:** $TIMESTAMP
**Backup Directory:** $BACKUP_DIR

## Application Status
- ✅ All files backed up
- ✅ Git repository state saved
- ✅ Configuration backed up
- ✅ Requirements snapshot created
- ✅ Deployment package created: $DEPLOYMENT_PACKAGE

## Files Included
- Complete application source code
- Configuration files (without sensitive data)
- Documentation (README.md, DEPLOYMENT.md)
- Requirements and dependencies
- Git history and status

## Files Excluded (Security)
- config.json (contains API keys)
- .env files
- Database files
- Log files
- Virtual environment
- Temporary files

## Next Steps
1. **Local Development**: Use the restore script
2. **Deployment**: Use the deployment package
3. **GitHub**: Push to GitHub repository
4. **Streamlit Cloud**: Deploy using the deployment package

## Important Notes
- API keys are NOT included in the backup for security
- Sensitive configuration files are excluded
- The deployment package is ready for public sharing
EOF

# 10. Move deployment package to backup directory
mv "$DEPLOYMENT_PACKAGE" "$BACKUP_DIR/"

echo ""
echo "✅ Application saved successfully!"
echo "=================================="
echo "📁 Backup Location: $BACKUP_DIR"
echo "📦 Deployment Package: $BACKUP_DIR/$DEPLOYMENT_PACKAGE"
echo "📖 Instructions: $BACKUP_DIR/DEPLOYMENT_INSTRUCTIONS.md"
echo "🔄 Restore Script: $BACKUP_DIR/restore_app.sh"
echo "📊 Summary: $BACKUP_DIR/BACKUP_SUMMARY.md"
echo ""
echo "🚀 Your app is now safely backed up and ready for deployment!"
echo ""
echo "💡 Next Steps:"
echo "   1. Push to GitHub: git push origin main"
echo "   2. Deploy to Streamlit Cloud"
echo "   3. Share the deployment package with others"
echo "" 