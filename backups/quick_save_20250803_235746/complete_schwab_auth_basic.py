#!/usr/bin/env python3
"""
Complete Schwab Authentication with Basic Auth
"""

import requests
import json
import base64
from urllib.parse import unquote

def complete_schwab_auth_basic():
    """Complete Schwab OAuth authentication using Basic authentication"""
    
    # Your Schwab API credentials
    client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
    client_secret = "67zvYgAIa8bqWr2v"
    redirect_uri = "https://developer.schwab.com/oauth2-redirect.html"
    
    # The authorization code from the redirect URL
    auth_code = "C0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.VSFO-6rUJBRT6Cm-5V-eKymbndJMK6bhwhhC0maYynE%40"
    
    # Decode the URL-encoded authorization code
    auth_code = unquote(auth_code)
    
    print("🔐 Completing Schwab OAuth Authentication (Basic Auth)")
    print("=" * 60)
    print(f"Client ID: {client_id}")
    print(f"Auth Code: {auth_code[:20]}...")
    print(f"Redirect URI: {redirect_uri}")
    print()
    
    # Token exchange endpoint
    token_url = "https://api.schwabapi.com/v1/oauth/token"
    
    # Create Basic authentication header
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    # Prepare the token request (without client credentials in body)
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    try:
        print("🔄 Exchanging authorization code for access token (Basic Auth)...")
        response = requests.post(token_url, data=token_data, headers=headers)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print(f"📝 Response Body: {response.text}")
        
        if response.status_code == 200:
            tokens = response.json()
            print("\n✅ Authentication successful!")
            print(f"🔑 Access Token: {tokens.get('access_token', 'N/A')[:20]}...")
            print(f"🔄 Refresh Token: {tokens.get('refresh_token', 'N/A')[:20]}...")
            print(f"⏰ Expires In: {tokens.get('expires_in', 'N/A')} seconds")
            print(f"📋 Token Type: {tokens.get('token_type', 'N/A')}")
            
            # Save tokens to config.json
            config_file = 'config.json'
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {}
            
            # Update Schwab authentication section
            if 'schwab_auth' not in config:
                config['schwab_auth'] = {}
            
            config['schwab_auth'].update({
                'access_token': tokens.get('access_token'),
                'refresh_token': tokens.get('refresh_token'),
                'expires_in': tokens.get('expires_in'),
                'token_type': tokens.get('token_type'),
                'timestamp': tokens.get('timestamp', ''),
                'status': 'authenticated'
            })
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"\n💾 Tokens saved to {config_file}")
            print("🎉 Schwab authentication completed successfully!")
            
            return True
            
        else:
            print(f"\n❌ Authentication failed: {response.status_code}")
            print(f"Error: {response.text}")
            
            # Try public client approach
            print("\n🔄 Trying public client approach...")
            return try_public_client_auth(auth_code, redirect_uri)
            
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")
        return False

def try_public_client_auth(auth_code, redirect_uri):
    """Try authentication as a public client (no client secret)"""
    
    client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
    token_url = "https://api.schwabapi.com/v1/oauth/token"
    
    # Prepare the token request for public client
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': auth_code,
        'redirect_uri': redirect_uri
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(token_url, data=token_data, headers=headers)
        
        print(f"📊 Public Client Response Status: {response.status_code}")
        print(f"📝 Public Client Response Body: {response.text}")
        
        if response.status_code == 200:
            tokens = response.json()
            print("\n✅ Public client authentication successful!")
            print(f"🔑 Access Token: {tokens.get('access_token', 'N/A')[:20]}...")
            
            # Save tokens
            config_file = 'config.json'
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {}
            
            if 'schwab_auth' not in config:
                config['schwab_auth'] = {}
            
            config['schwab_auth'].update({
                'access_token': tokens.get('access_token'),
                'refresh_token': tokens.get('refresh_token'),
                'expires_in': tokens.get('expires_in'),
                'token_type': tokens.get('token_type'),
                'timestamp': tokens.get('timestamp', ''),
                'status': 'authenticated_public'
            })
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"\n💾 Tokens saved to {config_file}")
            return True
        else:
            print(f"\n❌ Public client authentication also failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during public client authentication: {e}")
        return False

if __name__ == "__main__":
    success = complete_schwab_auth_basic()
    if success:
        print("\n🚀 You can now use Schwab API features in your application!")
    else:
        print("\n⚠️ Authentication failed. Please check your credentials and try again.") 