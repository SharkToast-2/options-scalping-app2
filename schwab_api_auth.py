#!/usr/bin/env python3
"""
Schwab Trader API Authentication
Based on Schwab Trader API Documentation
"""

import requests
import json
import os
import time
from urllib.parse import urlparse, parse_qs

class SchwabAPIAuth:
    def __init__(self):
        # Schwab Trader API Configuration
        self.client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
        self.redirect_uri = "https://developer.schwab.com/oauth2-redirect.html"
        self.auth_url = "https://api.schwabapi.com/v1/oauth/authorize"
        self.token_url = "https://api.schwabapi.com/v1/oauth/token"
        
        # Authorization code from the redirect URL
        self.auth_code = "C0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.NQ-6Tvw_XgxQ0SIpX7MTd-flmkuK8gxtcWPH5kqd-YI@"
        
        # Tokens
        self.access_token = None
        self.refresh_token = None
        
    def get_client_secret(self):
        """Get client secret from environment or prompt user"""
        client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
        
        if not client_secret:
            print("🔐 Client secret not found in environment variables.")
            print("Please enter your Schwab client secret:")
            try:
                import getpass
                client_secret = getpass.getpass("Client Secret: ")
            except ImportError:
                client_secret = input("Client Secret: ")
            
            if client_secret:
                os.environ['SCHWAB_CLIENT_SECRET'] = client_secret
                print("✅ Client secret set as environment variable")
            else:
                print("❌ No client secret provided")
                return None
        
        return client_secret
    
    def exchange_code_for_token(self):
        """Exchange authorization code for access token"""
        client_secret = self.get_client_secret()
        
        if not client_secret:
            return False
        
        print("🔄 Exchanging authorization code for access token...")
        print(f"🔑 Client ID: {self.client_id}")
        print(f"🔐 Client Secret: {client_secret[:10]}..." if len(client_secret) > 10 else "🔐 Client Secret: [Short]")
        print(f"🎫 Auth Code: {self.auth_code[:20]}...")
        print(f"📡 Token URL: {self.token_url}")
        
        # Prepare token exchange request
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': client_secret,
            'code': self.auth_code,
            'redirect_uri': self.redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(self.token_url, data=token_data, headers=headers)
            
            print(f"\n📊 Response Status: {response.status_code}")
            print(f"📄 Response Headers: {dict(response.headers)}")
            print(f"📝 Response Body: {response.text}")
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                
                print(f"\n✅ Token exchange successful!")
                print(f"🔑 Access Token: {self.access_token[:20]}..." if self.access_token else "❌ No access token")
                print(f"🔄 Refresh Token: {self.refresh_token[:20]}..." if self.refresh_token else "❌ No refresh token")
                
                # Save tokens
                self.save_tokens()
                return True
                
            else:
                print(f"\n❌ Token exchange failed: {response.status_code}")
                print(f"Error: {response.text}")
                
                # Try to provide helpful error information
                if response.status_code == 401:
                    print("\n💡 Troubleshooting tips:")
                    print("1. Verify your client_id and client_secret are correct")
                    print("2. Ensure the authorization code hasn't expired")
                    print("3. Check that the redirect_uri matches exactly")
                    print("4. Verify your app is properly registered with Schwab")
                
                return False
                
        except Exception as e:
            print(f"❌ Error during token exchange: {e}")
            return False
    
    def save_tokens(self):
        """Save tokens to config file"""
        try:
            config = {
                'schwab_auth': {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'timestamp': time.time(),
                    'client_id': self.client_id
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
            
        except Exception as e:
            print(f"⚠️ Warning: Could not save tokens: {e}")
    
    def test_api_access(self):
        """Test API access with the obtained token"""
        if not self.access_token:
            print("❌ No access token available for testing")
            return False
        
        print("\n🧪 Testing API access...")
        
        # Test with a simple API call (this would depend on Schwab's API endpoints)
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }
        
        # Try to get account information (example endpoint)
        try:
            # This is a placeholder - actual endpoint would be from Schwab's API docs
            test_url = "https://api.schwabapi.com/v1/accounts"
            response = requests.get(test_url, headers=headers)
            
            print(f"📊 Test API Response: {response.status_code}")
            if response.status_code == 200:
                print("✅ API access successful!")
                return True
            else:
                print(f"⚠️ API test returned: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing API access: {e}")
            return False

def main():
    print("🔐 Schwab Trader API Authentication")
    print("=" * 50)
    
    auth = SchwabAPIAuth()
    
    # Exchange authorization code for access token
    success = auth.exchange_code_for_token()
    
    if success:
        print("\n🎉 Authentication completed successfully!")
        
        # Test API access
        auth.test_api_access()
        
        print("\n📋 Next steps:")
        print("1. Your access token is saved in config.json")
        print("2. You can now use the Schwab Trader API")
        print("3. The token will expire and need to be refreshed")
        
    else:
        print("\n❌ Authentication failed")
        print("Please check your credentials and try again")

if __name__ == "__main__":
    main() 