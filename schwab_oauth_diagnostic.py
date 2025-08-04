#!/usr/bin/env python3
"""
Schwab OAuth 2.0 Diagnostic Tool
Helps identify and troubleshoot OAuth 2.0 authentication issues
"""

import requests
import json
import time
from urllib.parse import urlparse, parse_qs

def diagnose_oauth_issues():
    print("🔍 Schwab OAuth 2.0 Diagnostic Tool")
    print("=" * 50)
    
    # Configuration
    client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
    client_secret = "67zvYgAIa8bqWr2v"
    redirect_uri = "https://developer.schwab.com/oauth2-redirect.html"
    auth_url = "https://api.schwabapi.com/v1/oauth/authorize"
    token_url = "https://api.schwabapi.com/v1/oauth/token"
    
    print(f"🔑 Client ID: {client_id}")
    print(f"🔐 Client Secret: {client_secret[:10]}...")
    print(f"🔗 Redirect URI: {redirect_uri}")
    print(f"📡 Auth URL: {auth_url}")
    print(f"🎫 Token URL: {token_url}")
    
    # Test 1: Check if authorization endpoint is accessible
    print("\n📋 Test 1: Authorization endpoint accessibility...")
    try:
        response = requests.get(auth_url, params={
            'response_type': 'code',
            'client_id': client_id,
            'scope': 'readonly',
            'redirect_uri': redirect_uri
        })
        print(f"📊 Auth endpoint response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Authorization endpoint is accessible")
        else:
            print(f"⚠️ Authorization endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing authorization endpoint: {e}")
    
    # Test 2: Check token endpoint with different authentication methods
    print("\n📋 Test 2: Token endpoint authentication methods...")
    
    # Method 1: Form-encoded client authentication
    print("\n🔐 Testing Method 1: Form-encoded client authentication...")
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': 'test_code',
        'redirect_uri': redirect_uri
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(token_url, data=token_data, headers=headers)
        print(f"📊 Method 1 response: {response.status_code}")
        print(f"📝 Response body: {response.text}")
        
        if response.status_code == 400:
            print("✅ Token endpoint accepts form-encoded authentication")
            print("💡 The 'invalid_grant' error is expected with a test code")
        elif response.status_code == 401:
            print("❌ Token endpoint rejects form-encoded authentication")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error with Method 1: {e}")
    
    # Method 2: Basic authentication
    print("\n🔐 Testing Method 2: Basic authentication...")
    import base64
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    token_data_basic = {
        'grant_type': 'authorization_code',
        'code': 'test_code',
        'redirect_uri': redirect_uri
    }
    
    headers_basic = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    try:
        response = requests.post(token_url, data=token_data_basic, headers=headers_basic)
        print(f"📊 Method 2 response: {response.status_code}")
        print(f"📝 Response body: {response.text}")
        
        if response.status_code == 400:
            print("✅ Token endpoint accepts Basic authentication")
            print("💡 The 'invalid_grant' error is expected with a test code")
        elif response.status_code == 401:
            print("❌ Token endpoint rejects Basic authentication")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error with Method 2: {e}")
    
    # Test 3: Check if this is a public client
    print("\n📋 Test 3: Public client test...")
    token_data_public = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': 'test_code',
        'redirect_uri': redirect_uri
    }
    
    try:
        response = requests.post(token_url, data=token_data_public, headers=headers)
        print(f"📊 Public client response: {response.status_code}")
        print(f"📝 Response body: {response.text}")
        
        if response.status_code == 400:
            print("✅ Token endpoint accepts public client authentication")
            print("💡 The 'invalid_grant' error is expected with a test code")
        elif response.status_code == 401:
            print("❌ Token endpoint rejects public client authentication")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error with public client test: {e}")
    
    # Summary and recommendations
    print("\n📋 Diagnostic Summary:")
    print("=" * 30)
    print("Based on the test results, here are the possible issues:")
    print("\n1. 🔐 Client Authentication Issues:")
    print("   - The client_id or client_secret might be incorrect")
    print("   - The app might not be properly registered with Schwab")
    print("   - The app might require a different authentication method")
    
    print("\n2. 🎫 Authorization Code Issues:")
    print("   - Authorization codes typically expire after 10 minutes")
    print("   - The code might be tied to a specific session or IP")
    print("   - The redirect_uri must match exactly")
    
    print("\n3. 🔧 App Registration Issues:")
    print("   - The app might not be approved for production use")
    print("   - The app might be in sandbox/test mode only")
    print("   - Additional OAuth 2.0 scopes might be required")
    
    print("\n💡 Recommendations:")
    print("1. Verify your app registration with Schwab")
    print("2. Check if your app is approved for the OAuth 2.0 flow")
    print("3. Ensure the redirect_uri matches exactly in your app settings")
    print("4. Try using the Schwab developer portal to test the OAuth flow")
    print("5. Contact Schwab support for app-specific issues")

def main():
    diagnose_oauth_issues()
    
    print("\n🎯 Next Steps:")
    print("1. Review the diagnostic results above")
    print("2. Check your Schwab app registration settings")
    print("3. Verify the OAuth 2.0 configuration in Schwab's developer portal")
    print("4. Consider using the mock authentication for development")
    
    # Offer to set up mock authentication
    print("\n🔄 Would you like to set up mock authentication for development?")
    print("This will allow you to continue development while resolving the OAuth issues.")
    
    response = input("Set up mock authentication? (y/n): ").strip().lower()
    if response == 'y':
        setup_mock_auth()
    else:
        print("Continuing with OAuth 2.0 troubleshooting...")

def setup_mock_auth():
    """Set up mock authentication for development"""
    print("\n🔧 Setting up mock authentication...")
    
    mock_config = {
        'schwab_auth': {
            'access_token': 'mock_schwab_access_token',
            'refresh_token': 'mock_schwab_refresh_token',
            'timestamp': time.time(),
            'client_id': '1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj',
            'status': 'mock_authenticated'
        }
    }
    
    try:
        with open('config.json', 'r') as f:
            existing_config = json.load(f)
    except FileNotFoundError:
        existing_config = {}
    
    existing_config.update(mock_config)
    
    with open('config.json', 'w') as f:
        json.dump(existing_config, f, indent=2)
    
    print("✅ Mock authentication configured!")
    print("📋 You can now use the Schwab integration with mock data")
    print("🔗 The app will work for development and testing purposes")

if __name__ == "__main__":
    main() 