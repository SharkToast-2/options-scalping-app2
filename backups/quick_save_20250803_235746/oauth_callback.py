#!/usr/bin/env python3
"""
OAuth2 Callback Handler for ThinkOrSwim API
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger(__name__)

class TOSOAuthHandler:
    """Handle OAuth2 authentication for ThinkOrSwim API"""
    
    def __init__(self, client_id: str, redirect_uri: str = "http://localhost:8080/callback"):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_url = "https://auth.tdameritrade.com/auth"
        self.token_url = "https://api.tdameritrade.com/v1/oauth2/token"
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
    
    def get_authorization_url(self) -> str:
        """Generate authorization URL for user to visit"""
        params = {
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'scope': 'AccountAccess,MarketData,OptionChains'
        }
        
        auth_url = f"{self.auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        return auth_url
    
    def handle_callback(self, callback_url: str) -> bool:
        """Handle the OAuth callback and exchange code for tokens"""
        try:
            # Parse the callback URL
            parsed_url = urlparse(callback_url)
            query_params = parse_qs(parsed_url.query)
            
            # Extract authorization code
            if 'code' not in query_params:
                logger.error("No authorization code found in callback")
                return False
            
            auth_code = query_params['code'][0]
            
            # Exchange code for tokens
            token_data = {
                'grant_type': 'authorization_code',
                'access_type': 'offline',
                'code': auth_code,
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri
            }
            
            response = requests.post(self.token_url, data=token_data)
            
            if response.status_code == 200:
                token_info = response.json()
                
                self.access_token = token_info['access_token']
                self.refresh_token = token_info.get('refresh_token')
                self.expires_at = datetime.now() + timedelta(seconds=token_info['expires_in'])
                
                logger.info("✅ Successfully obtained access token")
                return True
            else:
                logger.error(f"❌ Token exchange failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Callback handling error: {e}")
            return False
    
    def refresh_access_token(self) -> bool:
        """Refresh the access token using refresh token"""
        try:
            if not self.refresh_token:
                logger.error("No refresh token available")
                return False
            
            token_data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': self.client_id
            }
            
            response = requests.post(self.token_url, data=token_data)
            
            if response.status_code == 200:
                token_info = response.json()
                
                self.access_token = token_info['access_token']
                self.expires_at = datetime.now() + timedelta(seconds=token_info['expires_in'])
                
                logger.info("✅ Successfully refreshed access token")
                return True
            else:
                logger.error(f"❌ Token refresh failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Token refresh error: {e}")
            return False
    
    def is_token_valid(self) -> bool:
        """Check if the current access token is still valid"""
        if not self.access_token or not self.expires_at:
            return False
        
        # Add 5-minute buffer before expiration
        return datetime.now() < (self.expires_at - timedelta(minutes=5))
    
    def get_valid_token(self) -> Optional[str]:
        """Get a valid access token, refreshing if necessary"""
        if not self.is_token_valid():
            if not self.refresh_access_token():
                return None
        
        return self.access_token
    
    def save_tokens(self, filename: str = "tos_tokens.json"):
        """Save tokens to file for persistence"""
        try:
            token_data = {
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'expires_at': self.expires_at.isoformat() if self.expires_at else None
            }
            
            with open(filename, 'w') as f:
                json.dump(token_data, f, indent=2)
            
            logger.info(f"✅ Tokens saved to {filename}")
            
        except Exception as e:
            logger.error(f"❌ Error saving tokens: {e}")
    
    def load_tokens(self, filename: str = "tos_tokens.json"):
        """Load tokens from file"""
        try:
            with open(filename, 'r') as f:
                token_data = json.load(f)
            
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            
            if token_data.get('expires_at'):
                self.expires_at = datetime.fromisoformat(token_data['expires_at'])
            
            logger.info(f"✅ Tokens loaded from {filename}")
            
        except FileNotFoundError:
            logger.info(f"📄 No token file found: {filename}")
        except Exception as e:
            logger.error(f"❌ Error loading tokens: {e}")

def start_oauth_server(port: int = 8080):
    """Start a simple HTTP server to handle OAuth callback"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import webbrowser
    import threading
    import time
    
    class OAuthCallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith('/callback'):
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                success_html = """
                <html>
                <head><title>OAuth Success</title></head>
                <body>
                    <h1>✅ Authentication Successful!</h1>
                    <p>You can close this window and return to your application.</p>
                    <script>window.close();</script>
                </body>
                </html>
                """
                self.wfile.write(success_html.encode())
                
                # Store the callback URL for processing
                self.server.callback_url = f"http://localhost:{port}{self.path}"
            else:
                self.send_response(404)
                self.end_headers()
    
    # Create server
    server = HTTPServer(('localhost', port), OAuthCallbackHandler)
    server.callback_url = None
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    return server

def authenticate_tos(client_id: str) -> Optional[TOSOAuthHandler]:
    """Complete OAuth2 authentication flow for ThinkOrSwim"""
    try:
        # Create OAuth handler
        oauth_handler = TOSOAuthHandler(client_id)
        
        # Start callback server
        server = start_oauth_server()
        
        # Generate authorization URL
        auth_url = oauth_handler.get_authorization_url()
        
        print(f"🔗 Authorization URL: {auth_url}")
        print("🌐 Opening browser for authentication...")
        
        # Open browser
        import webbrowser
        webbrowser.open(auth_url)
        
        # Wait for callback
        print("⏳ Waiting for authentication callback...")
        while not server.callback_url:
            time.sleep(1)
        
        # Handle callback
        if oauth_handler.handle_callback(server.callback_url):
            print("✅ Authentication successful!")
            
            # Save tokens
            oauth_handler.save_tokens()
            
            return oauth_handler
        else:
            print("❌ Authentication failed")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    CLIENT_ID = "your_client_id_here"
    
    print("🚀 Starting ThinkOrSwim OAuth Authentication")
    print("=" * 50)
    
    oauth_handler = authenticate_tos(CLIENT_ID)
    
    if oauth_handler:
        print(f"✅ Access Token: {oauth_handler.access_token[:20]}...")
        print(f"✅ Expires At: {oauth_handler.expires_at}")
        print("🎉 Authentication complete!")
    else:
        print("❌ Authentication failed") 