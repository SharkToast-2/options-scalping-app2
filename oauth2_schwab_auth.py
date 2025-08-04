#!/usr/bin/env python3
"""
OAuth 2.0 Schwab Authentication Implementation
Following RFC 6749 OAuth 2.0 Authorization Framework
"""

import requests
import json
import os
import time
import base64
from urllib.parse import urlparse, parse_qs

class OAuth2SchwabAuth:
    def __init__(self):
        # Schwab OAuth 2.0 Configuration
        self.client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
        self.redirect_uri = "https://developer.schwab.com/oauth2-redirect.html"
        self.auth_url = "https://api.schwabapi.com/v1/oauth/authorize"
        self.token_url = "https://api.schwabapi.com/v1/oauth/token"
        
        # Authorization code from the redirect URL (fresh code)
        self.auth_code = "C0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.7uYMlGQFHMKgmcDq51_PRu7OMmb-P45ZCKYe9LbuhH8@"
        
        # Tokens
        self.access_token = None
        self.refresh_token = None
        
    def get_client_secret(self):
        """Get client secret from environment or use provided secret"""
        client_secret = os.getenv('SCHWAB_CLIENT_SECRET')
        
        if not client_secret:
            # Use the provided client secret
            client_secret = "67zvYgAIa8bqWr2v"
            os.environ['SCHWAB_CLIENT_SECRET'] = client_secret
            print("✅ Using provided client secret")
        
        return client_secret
    
    def exchange_code_for_token_rfc6749(self):
        """
        Exchange authorization code for access token following RFC 6749
        Section 4.1.3: Access Token Request
        """
        client_secret = self.get_client_secret()
        
        if not client_secret:
            return False
        
        print("🔄 Exchanging authorization code for access token (RFC 6749)...")
        print(f"🔑 Client ID: {self.client_id}")
        print(f"🔐 Client Secret: {client_secret[:10]}..." if len(client_secret) > 10 else "🔐 Client Secret: [Short]")
        print(f"🎫 Auth Code: {self.auth_code[:20]}...")
        print(f"📡 Token URL: {self.token_url}")
        
        # According to RFC 6749 Section 4.1.3, the request should include:
        # - grant_type: "authorization_code"
        # - code: the authorization code
        # - redirect_uri: must match the one used in authorization request
        # - client_id: if client is not authenticated
        # - client_secret: if client is authenticated
        
        # Method 1: Try with client authentication in request body (RFC 6749 Section 2.3.1)
        print("\n📋 Method 1: Client authentication in request body...")
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
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response Headers: {dict(response.headers)}")
            print(f"📝 Response Body: {response.text}")
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                
                print(f"\n✅ Token exchange successful!")
                print(f"🔑 Access Token: {self.access_token[:20]}..." if self.access_token else "❌ No access token")
                print(f"🔄 Refresh Token: {self.refresh_token[:20]}..." if self.refresh_token else "❌ No refresh token")
                
                self.save_tokens()
                return True
                
            elif response.status_code == 401:
                print(f"\n❌ Method 1 failed: {response.status_code}")
                print(f"Error: {response.text}")
                
                # Method 2: Try with Basic authentication (RFC 6749 Section 2.3.1)
                print("\n📋 Method 2: Basic authentication...")
                return self.try_basic_auth(client_secret)
                
            else:
                print(f"\n❌ Token exchange failed: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error during token exchange: {e}")
            return False
    
    def try_basic_auth(self, client_secret):
        """Try Basic authentication as per RFC 6749 Section 2.3.1"""
        try:
            # Encode client_id:client_secret in base64
            credentials = f"{self.client_id}:{client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            token_data = {
                'grant_type': 'authorization_code',
                'code': self.auth_code,
                'redirect_uri': self.redirect_uri
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'Authorization': f'Basic {encoded_credentials}'
            }
            
            print(f"🔐 Using Basic authentication with encoded credentials")
            
            response = requests.post(self.token_url, data=token_data, headers=headers)
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response Headers: {dict(response.headers)}")
            print(f"📝 Response Body: {response.text}")
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                
                print(f"\n✅ Basic authentication successful!")
                print(f"🔑 Access Token: {self.access_token[:20]}..." if self.access_token else "❌ No access token")
                print(f"🔄 Refresh Token: {self.refresh_token[:20]}..." if self.refresh_token else "❌ No refresh token")
                
                self.save_tokens()
                return True
                
            else:
                print(f"\n❌ Basic authentication failed: {response.status_code}")
                print(f"Error: {response.text}")
                
                # Method 3: Try without client authentication (public client)
                print("\n📋 Method 3: Public client (no client authentication)...")
                return self.try_public_client()
                
        except Exception as e:
            print(f"❌ Error during Basic authentication: {e}")
            return False
    
    def try_public_client(self):
        """Try as public client without client authentication"""
        try:
            token_data = {
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'code': self.auth_code,
                'redirect_uri': self.redirect_uri
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }
            
            print(f"🔐 Trying as public client (no client secret)")
            
            response = requests.post(self.token_url, data=token_data, headers=headers)
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response Headers: {dict(response.headers)}")
            print(f"📝 Response Body: {response.text}")
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                
                print(f"\n✅ Public client authentication successful!")
                print(f"🔑 Access Token: {self.access_token[:20]}..." if self.access_token else "❌ No access token")
                print(f"🔄 Refresh Token: {self.refresh_token[:20]}..." if self.refresh_token else "❌ No refresh token")
                
                self.save_tokens()
                return True
                
            else:
                print(f"\n❌ Public client authentication failed: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error during public client authentication: {e}")
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

def main():
    print("🔐 OAuth 2.0 Schwab Authentication (RFC 6749)")
    print("=" * 60)
    
    auth = OAuth2SchwabAuth()
    
    # Exchange authorization code for access token using RFC 6749 methods
    success = auth.exchange_code_for_token_rfc6749()
    
    if success:
        print("\n🎉 OAuth 2.0 authentication completed successfully!")
        print("📋 Following RFC 6749 OAuth 2.0 Authorization Framework")
        print("1. Your access token is saved in config.json")
        print("2. You can now use the Schwab Trader API")
        print("3. The token will expire and need to be refreshed")
        
    else:
        print("\n❌ OAuth 2.0 authentication failed")
        print("💡 Troubleshooting tips:")
        print("1. Verify your client_id and client_secret are correct")
        print("2. Ensure the authorization code hasn't expired")
        print("3. Check that the redirect_uri matches exactly")
        print("4. Verify your app is properly registered with Schwab")
        print("5. Check if your app requires specific OAuth 2.0 flow type")

if __name__ == "__main__":
    main() 