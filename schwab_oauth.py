#!/usr/bin/env python3
"""
Schwab OAuth2 Authentication Script
Complete OAuth2 flow for Schwab API access
"""

import os
import json
import webbrowser
import requests
from urllib.parse import urlencode, urlparse, parse_qs

# Import configuration
from config.schwab_config import get_config, get_auth_url

# Load configuration
config = get_config()
SCHWAB_CLIENT_ID = config["client_id"]
SCHWAB_CLIENT_SECRET = config["client_secret"]
SCHWAB_REDIRECT_URI = config["redirect_uri"]
AUTH_URL = config["auth_url"]
TOKEN_URL = config["token_url"]
TOKEN_PATH = config["token_path"]

def get_authorization_code():
    """Get authorization code from Schwab OAuth2"""
    auth_url = get_auth_url()
    
    print("🔐 Schwab OAuth2 Authentication")
    print("=" * 50)
    print(f"Authorization URL: {auth_url}")
    print(f"Redirect URI: {SCHWAB_REDIRECT_URI}")
    print("\n📋 Steps:")
    print("1. Click the link above or it will open automatically")
    print("2. Sign in to your Schwab account")
    print("3. Authorize the application")
    print("4. Copy the entire URL you're redirected to")
    print("5. Paste it below when prompted")
    
    # Try to open browser automatically
    try:
        webbrowser.open(auth_url)
        print("\n🌐 Browser opened automatically!")
    except Exception as e:
        print(f"\n⚠️ Could not open browser automatically: {e}")
        print("Please manually open the authorization URL above")
    
    # Get redirect URL from user
    print("\n" + "=" * 50)
    redirect_url = input("Paste the redirect URL here: ").strip()
    
    # Extract authorization code
    try:
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' in query_params:
            auth_code = query_params['code'][0]
            print(f"✅ Authorization code extracted: {auth_code[:20]}...")
            return auth_code
        else:
            print("❌ No authorization code found in URL")
            return None
            
    except Exception as e:
        print(f"❌ Error parsing redirect URL: {e}")
        return None

def request_tokens(auth_code):
    """Exchange authorization code for access token"""
    print("\n🔄 Exchanging authorization code for access token...")
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": SCHWAB_REDIRECT_URI,
        "client_id": SCHWAB_CLIENT_ID,
        "client_secret": SCHWAB_CLIENT_SECRET
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Token exchange successful!")
            return token_data
        else:
            print(f"❌ Token exchange failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during token exchange: {e}")
        return None

def save_tokens(token_data):
    """Save tokens to file"""
    try:
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        
        # Add metadata
        token_data['client_id'] = SCHWAB_CLIENT_ID
        token_data['redirect_uri'] = SCHWAB_REDIRECT_URI
        
        with open(TOKEN_PATH, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print(f"✅ Tokens saved to {TOKEN_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving tokens: {e}")
        return False

def main():
    """Main authentication flow"""
    print("🚀 Schwab OAuth2 Authentication Script")
    print("=" * 50)
    print(f"Client ID: {SCHWAB_CLIENT_ID}")
    print(f"Redirect URI: {SCHWAB_REDIRECT_URI}")
    print("=" * 50)
    
    # Get authorization code
    auth_code = get_authorization_code()
    if not auth_code:
        print("❌ Failed to get authorization code")
        return None
    
    # Exchange for tokens
    token_data = request_tokens(auth_code)
    if not token_data:
        print("❌ Failed to exchange code for tokens")
        return None
    
    # Save tokens
    if not save_tokens(token_data):
        print("❌ Failed to save tokens")
        return None
    
    print("\n🎉 Authentication complete!")
    print("=" * 50)
    print("✅ Access token obtained")
    print("✅ Tokens saved to file")
    print("\nYou can now use the Schwab API!")
    
    return token_data

if __name__ == "__main__":
    result = main()
    
    if result:
        print(f"\n📊 Token Info:")
        print(f"Access Token: {result.get('access_token', 'N/A')[:20]}...")
        print(f"Token Type: {result.get('token_type', 'N/A')}")
        print(f"Expires In: {result.get('expires_in', 'N/A')} seconds")
        if 'refresh_token' in result:
            print(f"Refresh Token: {result['refresh_token'][:20]}...")
    else:
        print("\n❌ Authentication failed")
        print("\nTroubleshooting:")
        print("1. Check your Schwab credentials in config/schwab_config.py")
        print("2. Ensure you have internet connection")
        print("3. Verify your Schwab account is active")
        print("4. Try running the script again") 