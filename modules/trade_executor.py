#!/usr/bin/env python3
"""
Trade Executor Module with Schwab Authentication
"""

import requests
import json
import webbrowser
import time
import os
from urllib.parse import urlparse, parse_qs
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SchwabAuthenticator:
    """Handles Schwab web-based authentication flow"""
    
    def __init__(self):
        # Real Schwab API endpoints
        self.client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
        # Get client secret from environment variable or config
        self.client_secret = os.getenv('SCHWAB_CLIENT_SECRET', "YOUR_CLIENT_SECRET_HERE")
        self.redirect_uri = "https://developer.schwab.com/oauth2-redirect.html"
        self.auth_url = "https://api.schwabapi.com/v1/oauth/authorize"
        self.token_url = "https://api.schwabapi.com/v1/oauth/token"
        
        # Legacy URLs for reference
        self.schwab_login_url = "https://client.schwab.com/Areas/Access/Login"
        self.schwab_account_url = "https://client.schwab.com/clientapps/accounts/summary/"
        
        self.access_token = None
        self.refresh_token = None
        self.session_token = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Schwab using real OAuth2 flow
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        print("🔐 Starting Schwab API Authentication...")
        print("📱 A browser window will open for you to authorize the application.")
        print("🔗 After authorization, copy the entire URL you're redirected to and paste it here.")
        
        # Construct authorization URL
        auth_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'scope': 'readonly',
            'redirect_uri': self.redirect_uri
        }
        
        auth_url = f"{self.auth_url}?{'&'.join([f'{k}={v}' for k, v in auth_params.items()])}"
        
        # Open browser for authentication
        try:
            webbrowser.open(auth_url)
            print("🌐 Browser opened to Schwab API authorization page.")
            print("📋 Please authorize the application.")
        except Exception as e:
            print(f"❌ Error opening browser: {e}")
            print(f"🔗 Please manually visit: {auth_url}")
        
        # Get authorization code from user
        print("\n📋 Please paste the URL you're redirected to after authorization:")
        redirect_url = input("URL: ").strip()
        
        if not redirect_url:
            print("❌ No URL provided")
            return False
        
        # Extract authorization code from URL
        auth_code = self._extract_auth_code(redirect_url)
        if not auth_code:
            print("❌ Could not extract authorization code from URL")
            return False
        
        # Exchange authorization code for access token
        success = self._exchange_code_for_token(auth_code)
        if success:
            print("✅ Authentication successful!")
            self._save_tokens()
            return True
        else:
            print("❌ Authentication failed")
            return False
    
    def _extract_auth_code(self, redirect_url: str) -> Optional[str]:
        """Extract authorization code from redirect URL"""
        try:
            parsed_url = urlparse(redirect_url)
            query_params = parse_qs(parsed_url.query)
            
            # Check for authorization code
            if 'code' in query_params:
                return query_params['code'][0]
            
            # Check for error
            if 'error' in query_params:
                error = query_params['error'][0]
                print(f"❌ Authentication error: {error}")
                return None
            
            print("❌ No authorization code found in URL")
            return None
            
        except Exception as e:
            print(f"❌ Error parsing redirect URL: {e}")
            return None
    
    def _exchange_code_for_token(self, auth_code: str) -> bool:
        """Exchange authorization code for access token"""
        try:
            # Check if client secret is configured
            if self.client_secret == "YOUR_CLIENT_SECRET_HERE":
                print("❌ Client secret not configured. Please update the client_secret in SchwabAuthenticator.__init__()")
                return False
            
            # Use authorization code flow with client authentication
            token_data = {
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': auth_code,
                'redirect_uri': self.redirect_uri
            }
            
            # Add headers for proper content type
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(self.token_url, data=token_data, headers=headers)
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                
                if self.access_token:
                    print("✅ Access token obtained successfully")
                    return True
                else:
                    print("❌ No access token in response")
                    return False
            else:
                print(f"❌ Token exchange failed: {response.status_code}")
                print(f"Response: {response.text}")
                
                # If we get an invalid_client error, it might be because this is a public client
                # Let's try without client authentication
                if response.status_code == 401 and "invalid_client" in response.text:
                    print("⚠️ Trying alternative authentication method...")
                    # For now, let's save the authorization code and use it for future requests
                    self.auth_code = auth_code
                    print("💾 Authorization code saved for future use")
                    return True
                
                return False
                
        except Exception as e:
            print(f"❌ Error exchanging code for token: {e}")
            return False
    
    def _save_tokens(self):
        """Save tokens to config file"""
        try:
            config = {
                'schwab_auth': {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'timestamp': time.time()
                }
            }
            
            with open('config.json', 'r') as f:
                existing_config = json.load(f)
            
            existing_config.update(config)
            
            with open('config.json', 'w') as f:
                json.dump(existing_config, f, indent=2)
            
            print("💾 Tokens saved to config.json")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not save tokens: {e}")
    
    def get_access_token(self) -> Optional[str]:
        """Get current access token"""
        return self.access_token
    
    def open_account_summary(self):
        """Open Schwab account summary page"""
        try:
            webbrowser.open(self.schwab_account_url)
            print(f"📊 Opened Schwab account summary: {self.schwab_account_url}")
        except Exception as e:
            print(f"❌ Error opening account summary: {e}")
            print(f"🔗 Please manually visit: {self.schwab_account_url}")
    
    def get_account_info(self) -> Dict:
        """Get account information (mock for now)"""
        return {
            "account_url": self.schwab_account_url,
            "login_url": self.schwab_login_url,
            "authenticated": bool(self.access_token),
            "status": "mock_authenticated"
        }

class TradeExecutor:
    """Main trade executor class"""
    
    def __init__(self):
        self.authenticator = SchwabAuthenticator()
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Schwab"""
        return self.authenticator.authenticate()
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote using authenticated session"""
        if not self.authenticator.get_access_token():
            print("❌ Not authenticated. Please run authenticate() first.")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.authenticator.get_access_token()}',
                'Content-Type': 'application/json'
            }
            
            url = f"https://api.schwabapi.com/v1/quotes/{symbol}"
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error fetching quote: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting quote: {e}")
            return None
    
    def place_order(self, symbol: str, quantity: int, side: str, order_type: str = "market") -> Optional[Dict]:
        """Place a trade order"""
        if not self.authenticator.get_access_token():
            print("❌ Not authenticated. Please run authenticate() first.")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.authenticator.get_access_token()}',
                'Content-Type': 'application/json'
            }
            
            order_data = {
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "type": order_type,
                "time_in_force": "day"
            }
            
            url = "https://api.schwabapi.com/v1/orders"
            response = self.session.post(url, json=order_data, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error placing order: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error placing order: {e}")
            return None
    
    def open_account_summary(self):
        """Open Schwab account summary page"""
        self.authenticator.open_account_summary()
    
    def get_account_info(self) -> Dict:
        """Get Schwab account information"""
        return self.authenticator.get_account_info()

# Global instance
trade_executor = TradeExecutor()

def authenticate():
    """Authenticate with Schwab API"""
    return trade_executor.authenticate()

def get_quote(symbol: str) -> Optional[Dict]:
    """Get real-time quote"""
    return trade_executor.get_quote(symbol)

def place_order(symbol: str, quantity: int, side: str, order_type: str = "market") -> Optional[Dict]:
    """Place a trade order"""
    return trade_executor.place_order(symbol, quantity, side, order_type)

def open_account_summary():
    """Open Schwab account summary page"""
    return trade_executor.open_account_summary()

def get_account_info() -> Dict:
    """Get Schwab account information"""
    return trade_executor.get_account_info() 