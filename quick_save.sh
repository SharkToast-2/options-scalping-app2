#!/bin/bash

# Quick Save Script for Options Scalping Application
echo "💾 Quick Save - Options Scalping Application"
echo "============================================"

# Get timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. Save to Git
echo "📝 Saving to Git..."
git add .
git commit -m "Quick save: $(date '+%Y-%m-%d %H:%M:%S')"

# 2. Create simple backup
echo "📦 Creating backup..."
BACKUP_DIR="backups/quick_save_$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

# Copy essential files
cp -r ui/ "$BACKUP_DIR/"
cp -r data/ "$BACKUP_DIR/"
cp -r modules/ "$BACKUP_DIR/"
cp -r signals/ "$BACKUP_DIR/"
cp -r trading/ "$BACKUP_DIR/"
cp -r utils/ "$BACKUP_DIR/"
cp -r config/ "$BACKUP_DIR/"
cp *.py "$BACKUP_DIR/" 2>/dev/null || true
cp *.md "$BACKUP_DIR/" 2>/dev/null || true
cp requirements.txt "$BACKUP_DIR/"
cp config.json.example "$BACKUP_DIR/"

# 3. Create deployment package
echo "📦 Creating deployment package..."
zip -r "deployment_$TIMESTAMP.zip" . \
    -x "*.pyc" \
    -x "__pycache__/*" \
    -x "*.log" \
    -x "config.json" \
    -x ".env*" \
    -x "*.db" \
    -x "backups/*" \
    -x "bin/*" \
    -x "include/*" \
    -x "lib/*" \
    -x "share/*" \
    -x "pyvenv.cfg" \
    -x "test_*.py" \
    -x ".DS_Store"

# 4. Show summary
echo ""
echo "✅ Quick Save Complete!"
echo "======================"
echo "📁 Backup: $BACKUP_DIR"
echo "📦 Deployment: deployment_$TIMESTAMP.zip"
echo "🔧 Git: Latest commit saved"
echo ""
echo "🚀 Ready for deployment!" 