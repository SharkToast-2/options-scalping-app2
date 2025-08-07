#!/usr/bin/env python3
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
SCHWAB_CLIENT_ID = os.getenv("SCHWAB_CLIENT_ID", "your_client_id")
SCHWAB_CLIENT_SECRET = os.getenv("SCHWAB_CLIENT_SECRET", "your_secret")
SCHWAB_REDIRECT_URI = os.getenv("SCHWAB_REDIRECT_URI", "http://localhost:8501/callback")

# Schwab API URLs
SCHWAB_AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
SCHWAB_TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
SCHWAB_BASE_URL = "https://api.schwabapi.com/v1"

# Market Data API
SCHWAB_MARKET_DATA_URL = "https://api.schwabapi.com/v1/market-data"
SCHWAB_QUOTES_URL = f"{SCHWAB_BASE_URL}/quotes"
SCHWAB_OPTIONS_URL = f"{SCHWAB_BASE_URL}/options"

# Trading API
SCHWAB_ACCOUNTS_URL = f"{SCHWAB_BASE_URL}/accounts"
SCHWAB_ORDERS_URL = f"{SCHWAB_BASE_URL}/orders"
SCHWAB_POSITIONS_URL = f"{SCHWAB_BASE_URL}/positions"

# Token storage
TOKEN_PATH = "config/schwab_tokens.json"
ENCRYPTION_KEY_PATH = "config/encryption.key"

class SchwabConfig:
    """Enhanced Schwab API configuration manager"""
    
    def __init__(self):
        self.client_id = SCHWAB_CLIENT_ID
        self.client_secret = SCHWAB_CLIENT_SECRET
        self.redirect_uri = SCHWAB_REDIRECT_URI
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for secure token storage"""
        if os.path.exists(ENCRYPTION_KEY_PATH):
            with open(ENCRYPTION_KEY_PATH, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(ENCRYPTION_KEY_PATH), exist_ok=True)
            with open(ENCRYPTION_KEY_PATH, 'wb') as f:
                f.write(key)
            return key
    
    def get_auth_url(self, state: str = None) -> str:
        """Generate Schwab authorization URL with proper scopes"""
        from urllib.parse import urlencode
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "trading market_data account_read",
            "state": state or "options_scalper"
        }
        
        query_string = urlencode(params)
        return f"{SCHWAB_AUTH_URL}?{query_string}"
    
    def exchange_code_for_token(self, authorization_code: str) -> Dict:
        """Exchange authorization code for access token"""
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        response = requests.post(SCHWAB_TOKEN_URL, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self._save_tokens(token_data)
            return token_data
        else:
            raise Exception(f"Token exchange failed: {response.text}")
    
    def refresh_access_token(self, refresh_token: str) -> Dict:
        """Refresh access token using refresh token"""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        response = requests.post(SCHWAB_TOKEN_URL, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self._save_tokens(token_data)
            return token_data
        else:
            raise Exception(f"Token refresh failed: {response.text}")
    
    def _save_tokens(self, token_data: Dict):
        """Save tokens securely with encryption"""
        encrypted_data = self.cipher.encrypt(json.dumps(token_data).encode())
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'wb') as f:
            f.write(encrypted_data)
    
    def load_tokens(self) -> Optional[Dict]:
        """Load tokens from secure storage"""
        if not os.path.exists(TOKEN_PATH):
            return None
        
        try:
            with open(TOKEN_PATH, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error loading tokens: {e}")
            return None
    
    def is_token_valid(self, token_data: Dict) -> bool:
        """Check if access token is still valid"""
        if not token_data or 'expires_at' not in token_data:
            return False
        
        expires_at = datetime.fromisoformat(token_data['expires_at'])
        return datetime.now() < expires_at
    
    def get_valid_access_token(self) -> Optional[str]:
        """Get a valid access token, refreshing if necessary"""
        token_data = self.load_tokens()
        if not token_data:
            return None
        
        if self.is_token_valid(token_data):
            return token_data['access_token']
        
        # Token expired, try to refresh
        if 'refresh_token' in token_data:
            try:
                new_token_data = self.refresh_access_token(token_data['refresh_token'])
                return new_token_data['access_token']
            except Exception as e:
                print(f"Token refresh failed: {e}")
                return None
        
        return None
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        access_token = self.get_valid_access_token()
        if not access_token:
            raise Exception("No valid access token available")
        
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

# API Endpoints for Options Scalping
class SchwabEndpoints:
    """Schwab API endpoints for options trading"""
    
    @staticmethod
    def get_accounts() -> str:
        """Get user accounts endpoint"""
        return f"{SCHWAB_ACCOUNTS_URL}"
    
    @staticmethod
    def get_account_positions(account_id: str) -> str:
        """Get account positions endpoint"""
        return f"{SCHWAB_ACCOUNTS_URL}/{account_id}/positions"
    
    @staticmethod
    def get_quotes(symbols: list) -> str:
        """Get real-time quotes endpoint"""
        symbols_str = ",".join(symbols)
        return f"{SCHWAB_QUOTES_URL}?symbols={symbols_str}"
    
    @staticmethod
    def get_options_chain(symbol: str, expiration_date: str = None) -> str:
        """Get options chain endpoint"""
        url = f"{SCHWAB_OPTIONS_URL}/chains/{symbol}"
        if expiration_date:
            url += f"?expirationDate={expiration_date}"
        return url
    
    @staticmethod
    def place_order(account_id: str) -> str:
        """Place order endpoint"""
        return f"{SCHWAB_ACCOUNTS_URL}/{account_id}/orders"
    
    @staticmethod
    def get_order_status(account_id: str, order_id: str) -> str:
        """Get order status endpoint"""
        return f"{SCHWAB_ACCOUNTS_URL}/{account_id}/orders/{order_id}"

# Global configuration instance
schwab_config = SchwabConfig()

def get_auth_url():
    """Generate Schwab authorization URL"""
    return schwab_config.get_auth_url()

def get_config():
    """Get complete Schwab configuration"""
    return {
        "client_id": schwab_config.client_id,
        "client_secret": schwab_config.client_secret,
        "redirect_uri": schwab_config.redirect_uri,
        "auth_url": SCHWAB_AUTH_URL,
        "token_url": SCHWAB_TOKEN_URL,
        "base_url": SCHWAB_BASE_URL,
        "token_path": TOKEN_PATH
    }

def is_authenticated() -> bool:
    """Check if user is authenticated with Schwab"""
    return schwab_config.get_valid_access_token() is not None 