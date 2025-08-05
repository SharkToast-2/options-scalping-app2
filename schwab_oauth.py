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
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load credentials from config
SCHWAB_CLIENT_ID = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
SCHWAB_CLIENT_SECRET = "67zvYgAIa8bqWr2v"
SCHWAB_REDIRECT_URI = "https://developer.schwab.com/oauth2-redirect.html"
AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
TOKEN_PATH = "config/schwab_tokens.json"

def get_authorization_code():
    """Get authorization code from Schwab OAuth2"""
    params = {
        "response_type": "code",
        "client_id": SCHWAB_CLIENT_ID,
        "scope": "readonly",
        "redirect_uri": SCHWAB_REDIRECT_URI
    }
    
    # Build authorization URL
    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    
    print("🔐 Schwab OAuth2 Authentication")
    print("=" * 50)
    print(f"Authorization URL: {auth_url}")
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

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access token"""
    print("\n🔄 Exchanging authorization code for access token...")
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": SCHWAB_CLIENT_ID,
        "client_secret": SCHWAB_CLIENT_SECRET,
        "redirect_uri": SCHWAB_REDIRECT_URI
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
        
        # Add timestamp and metadata
        token_data['timestamp'] = datetime.now().isoformat()
        token_data['expires_at'] = (datetime.now() + timedelta(hours=1)).isoformat()
        token_data['client_id'] = SCHWAB_CLIENT_ID
        
        with open(TOKEN_PATH, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print(f"✅ Tokens saved to {TOKEN_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving tokens: {e}")
        return False

def load_tokens():
    """Load tokens from file"""
    try:
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'r') as f:
                token_data = json.load(f)
            
            # Check if token is expired
            expires_at = datetime.fromisoformat(token_data.get('expires_at', '2000-01-01'))
            if datetime.now() < expires_at:
                print("✅ Valid tokens found")
                return token_data
            else:
                print("⚠️ Tokens expired")
                return None
        else:
            print("⚠️ No tokens found")
            return None
            
    except Exception as e:
        print(f"❌ Error loading tokens: {e}")
        return None

def refresh_token(refresh_token_value):
    """Refresh access token using refresh token"""
    print("🔄 Refreshing access token...")
    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_value,
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
            print("✅ Token refresh successful!")
            return token_data
        else:
            print(f"❌ Token refresh failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during token refresh: {e}")
        return None

def test_api_connection(access_token):
    """Test API connection with access token"""
    print("\n🧪 Testing API connection...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test with account endpoint
    test_url = "https://api.schwabapi.com/trading/v1/accounts"
    
    try:
        response = requests.get(test_url, headers=headers)
        
        if response.status_code == 200:
            print("✅ API connection successful!")
            return True
        else:
            print(f"❌ API connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API connection: {e}")
        return False

def main():
    """Main authentication flow"""
    print("🚀 Schwab OAuth2 Authentication Script")
    print("=" * 50)
    
    # Check if we have valid tokens
    token_data = load_tokens()
    
    if token_data:
        access_token = token_data.get('access_token')
        if access_token and test_api_connection(access_token):
            print("\n✅ Already authenticated and connected!")
            return token_data
    
    # Check if we have refresh token
    if token_data and 'refresh_token' in token_data:
        print("\n🔄 Attempting token refresh...")
        new_token_data = refresh_token(token_data['refresh_token'])
        if new_token_data:
            save_tokens(new_token_data)
            if test_api_connection(new_token_data.get('access_token')):
                print("\n✅ Token refresh successful!")
                return new_token_data
    
    # Full OAuth2 flow
    print("\n🔄 Starting full OAuth2 authentication...")
    
    # Get authorization code
    auth_code = get_authorization_code()
    if not auth_code:
        print("❌ Failed to get authorization code")
        return None
    
    # Exchange for tokens
    token_data = exchange_code_for_token(auth_code)
    if not token_data:
        print("❌ Failed to exchange code for tokens")
        return None
    
    # Save tokens
    if not save_tokens(token_data):
        print("❌ Failed to save tokens")
        return None
    
    # Test connection
    access_token = token_data.get('access_token')
    if not test_api_connection(access_token):
        print("❌ Failed to connect to API")
        return None
    
    print("\n🎉 Authentication complete!")
    print("=" * 50)
    print("✅ Access token obtained")
    print("✅ Tokens saved to file")
    print("✅ API connection verified")
    print("\nYou can now use the Schwab API!")
    
    return token_data

def get_auth_status():
    """Get current authentication status"""
    token_data = load_tokens()
    
    if not token_data:
        return {
            'authenticated': False,
            'status': 'No tokens found'
        }
    
    expires_at = datetime.fromisoformat(token_data.get('expires_at', '2000-01-01'))
    is_expired = datetime.now() >= expires_at
    
    if is_expired:
        return {
            'authenticated': False,
            'status': 'Tokens expired',
            'has_refresh_token': 'refresh_token' in token_data
        }
    
    return {
        'authenticated': True,
        'status': 'Valid tokens',
        'expires_at': expires_at.isoformat(),
        'has_refresh_token': 'refresh_token' in token_data
    }

if __name__ == "__main__":
    # Run authentication
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
        print("1. Check your Schwab credentials in config/.env")
        print("2. Ensure you have internet connection")
        print("3. Verify your Schwab account is active")
        print("4. Try running the script again") 