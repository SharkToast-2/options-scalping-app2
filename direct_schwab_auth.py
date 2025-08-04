#!/usr/bin/env python3
"""
Direct Schwab Authentication with Client Secret
"""

import os
import requests
import json
from urllib.parse import urlparse, parse_qs

def complete_schwab_auth():
    print("🔐 Completing Schwab Authentication...")
    
    # Schwab API configuration
    client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
    client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
    token_url = "https://api.schwabapi.com/v1/oauth/token"
    
    # The authorization code from the redirect URL
    auth_code = "C0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.NQ-6Tvw_XgxQ0SIpX7MTd-flmkuK8gxtcWPH5kqd-YI@"
    
    print(f"🔑 Client ID: {client_id}")
    print(f"🔐 Client Secret: {client_secret[:10]}..." if len(client_secret) > 10 else "🔐 Client Secret: [Not set]")
    print(f"🎫 Auth Code: {auth_code[:20]}...")
    
    # Exchange authorization code for access token
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'redirect_uri': 'https://developer.schwab.com/oauth2-redirect.html'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    print(f"\n🔄 Exchanging authorization code for access token...")
    print(f"📡 Token URL: {token_url}")
    
    try:
        response = requests.post(token_url, data=token_data, headers=headers)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print(f"📝 Response Body: {response.text}")
        
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info.get('access_token')
            refresh_token = token_info.get('refresh_token')
            
            print(f"\n✅ Authentication successful!")
            print(f"🔑 Access Token: {access_token[:20]}..." if access_token else "❌ No access token")
            print(f"🔄 Refresh Token: {refresh_token[:20]}..." if refresh_token else "❌ No refresh token")
            
            # Save tokens
            config = {
                'schwab_auth': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'timestamp': time.time()
                }
            }
            
            try:
                with open('config.json', 'r') as f:
                    existing_config = json.load(f)
            except FileNotFoundError:
                existing_config = {}
            
            existing_config.update(config)
            
            with open('config.json', 'w') as f:
                json.dump(existing_config, f, indent=2)
            
            print("💾 Tokens saved to config.json")
            return True
            
        else:
            print(f"\n❌ Token exchange failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during token exchange: {e}")
        return False

if __name__ == "__main__":
    import time
    success = complete_schwab_auth()
    if success:
        print("\n🎉 Schwab authentication completed successfully!")
    else:
        print("\n❌ Authentication failed. Please check your credentials.") 