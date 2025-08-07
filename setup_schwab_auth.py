#!/usr/bin/env python3
"""
Schwab API Authentication Setup Script
Helps configure Schwab API credentials for the options scalping bot
"""

import os
import sys
from config.schwab_config import schwab_config, get_auth_url

def setup_schwab_credentials():
    """Interactive setup for Schwab API credentials"""
    print("🚀 Schwab API Setup for Options Scalping Bot")
    print("=" * 50)
    
    # Check if credentials are already set
    if schwab_config.client_id != "your_client_id":
        print("✅ Schwab credentials already configured!")
        print(f"Client ID: {schwab_config.client_id[:10]}...")
        return True
    
    print("\n📋 To get your Schwab API credentials:")
    print("1. Go to https://developer.schwab.com")
    print("2. Create a new application")
    print("3. Get your Client ID and Client Secret")
    print("4. Set the redirect URI to: http://localhost:8501/callback")
    
    print("\n🔧 Configuration Options:")
    print("1. Set environment variables (recommended)")
    print("2. Update config file directly")
    print("3. Use interactive setup")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        setup_environment_variables()
    elif choice == "2":
        update_config_file()
    elif choice == "3":
        interactive_setup()
    else:
        print("❌ Invalid choice. Please run the script again.")
        return False
    
    return True

def setup_environment_variables():
    """Set up environment variables"""
    print("\n🔧 Setting up environment variables...")
    
    client_id = input("Enter your Schwab Client ID: ").strip()
    client_secret = input("Enter your Schwab Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Client ID and Client Secret are required!")
        return False
    
    # Create .env file
    env_content = f"""# Schwab API Configuration
SCHWAB_CLIENT_ID={client_id}
SCHWAB_CLIENT_SECRET={client_secret}
SCHWAB_REDIRECT_URI=http://localhost:8501/callback

# Other configuration
DEBUG=True
LOG_LEVEL=INFO
"""
    
    with open("config/.env", "w") as f:
        f.write(env_content)
    
    print("✅ Environment variables configured!")
    print("📁 Created config/.env file")
    print("🔒 Make sure to add config/.env to your .gitignore file")
    
    return True

def update_config_file():
    """Update config file directly"""
    print("\n🔧 Updating config file...")
    
    client_id = input("Enter your Schwab Client ID: ").strip()
    client_secret = input("Enter your Schwab Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Client ID and Client Secret are required!")
        return False
    
    # Update the config file
    config_content = f'''#!/usr/bin/env python3
"""
Enhanced Schwab API Configuration for Options Scalping Bot
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests
from cryptography.fernet import Fernet

# Schwab OAuth2 Configuration
SCHWAB_CLIENT_ID = "{client_id}"
SCHWAB_CLIENT_SECRET = "{client_secret}"
SCHWAB_REDIRECT_URI = "http://localhost:8501/callback"

# Rest of the configuration remains the same...
'''
    
    # Read the rest of the original file
    with open("config/schwab_config.py", "r") as f:
        original_content = f.read()
    
    # Find where the configuration section ends
    lines = original_content.split('\n')
    start_line = 0
    for i, line in enumerate(lines):
        if line.startswith('# Schwab OAuth2 Configuration'):
            start_line = i
            break
    
    # Reconstruct the file
    new_content = config_content + '\n'.join(lines[start_line + 3:])
    
    with open("config/schwab_config.py", "w") as f:
        f.write(new_content)
    
    print("✅ Config file updated!")
    return True

def interactive_setup():
    """Interactive setup with step-by-step guidance"""
    print("\n🔧 Interactive Setup")
    print("=" * 30)
    
    print("\nStep 1: Get your Schwab API credentials")
    print("- Go to https://developer.schwab.com")
    print("- Sign in to your Schwab account")
    print("- Create a new application")
    print("- Note down your Client ID and Client Secret")
    
    input("\nPress Enter when you have your credentials...")
    
    client_id = input("Enter your Schwab Client ID: ").strip()
    if not client_id:
        print("❌ Client ID is required!")
        return False
    
    client_secret = input("Enter your Schwab Client Secret: ").strip()
    if not client_secret:
        print("❌ Client Secret is required!")
        return False
    
    print("\nStep 2: Configure redirect URI")
    print("In your Schwab application settings, set the redirect URI to:")
    print("http://localhost:8501/callback")
    
    input("\nPress Enter when you've configured the redirect URI...")
    
    # Set environment variables
    os.environ["SCHWAB_CLIENT_ID"] = client_id
    os.environ["SCHWAB_CLIENT_SECRET"] = client_secret
    os.environ["SCHWAB_REDIRECT_URI"] = "http://localhost:8501/callback"
    
    print("\nStep 3: Test authentication")
    try:
        auth_url = get_auth_url()
        print(f"✅ Authentication URL generated: {auth_url}")
        print("\nTo complete setup:")
        print("1. Open the URL above in your browser")
        print("2. Authorize the application")
        print("3. Copy the authorization code from the redirect URL")
        print("4. Run the authentication script")
        
    except Exception as e:
        print(f"❌ Error generating auth URL: {e}")
        return False
    
    return True

def test_connection():
    """Test Schwab API connection"""
    print("\n🧪 Testing Schwab API connection...")
    
    try:
        from config.schwab_config import is_authenticated
        
        if is_authenticated():
            print("✅ Successfully authenticated with Schwab API!")
            return True
        else:
            print("❌ Not authenticated. Please complete the setup process.")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Options Scalping Bot - Schwab API Setup")
    print("=" * 50)
    
    # Check if already configured
    if schwab_config.client_id != "your_client_id":
        print("✅ Schwab API already configured!")
        if test_connection():
            print("🎉 Setup complete! You can now run the bot with Schwab integration.")
            return
    
    # Run setup
    if setup_schwab_credentials():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: streamlit run app.py")
        print("2. Complete the OAuth flow in the app")
        print("3. Start trading with real Schwab data!")
    else:
        print("\n❌ Setup failed. Please try again.")

if __name__ == "__main__":
    main() 