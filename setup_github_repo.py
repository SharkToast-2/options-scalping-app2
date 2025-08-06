#!/usr/bin/env python3
"""
GitHub Repository Setup Helper
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            return result.stdout.strip()
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return None

def main():
    print("🚀 GitHub Repository Setup Helper")
    print("=" * 50)
    
    # Check if git is available
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git first.")
        return
    
    # Check current git status
    print("\n📊 Current Git Status:")
    run_command("git status", "Checking git status")
    
    # Check if GitHub CLI is available
    gh_version = run_command("gh --version", "Checking GitHub CLI installation")
    
    if gh_version:
        print("\n🔐 GitHub CLI Setup:")
        print("1. Run: gh auth login")
        print("2. Choose HTTPS when prompted")
        print("3. Follow the browser authentication")
        print("4. Then run: ./create_new_repo.sh")
    else:
        print("\n📋 Manual GitHub Repository Setup:")
        print("1. Go to https://github.com/new")
        print("2. Repository name: updated-Options-King")
        print("3. Description: Advanced options scalping bot with Schwab API integration")
        print("4. Make it Public")
        print("5. Don't initialize with README (we'll push existing code)")
        print("6. Click 'Create repository'")
        print("\n7. Then run these commands:")
        print("   git remote add new-origin https://github.com/YOUR_USERNAME/updated-Options-King.git")
        print("   git push -u new-origin main")
    
    print("\n📁 Current Project Structure:")
    run_command("ls -la", "Listing project files")
    
    print("\n📋 Next Steps:")
    print("1. Set up GitHub repository (see instructions above)")
    print("2. Update Schwab credentials in config/schwab_config.py")
    print("3. Test the OAuth script: python3 schwab_oauth.py")
    print("4. Run the Streamlit app: streamlit run app.py")
    print("5. Share your repository!")

if __name__ == "__main__":
    main() 