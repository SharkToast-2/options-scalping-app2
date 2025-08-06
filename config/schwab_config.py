#!/usr/bin/env python3
"""
Schwab API Configuration
"""

# Schwab OAuth2 Configuration
SCHWAB_CLIENT_ID = "your_client_id"
SCHWAB_CLIENT_SECRET = "your_secret"
SCHWAB_REDIRECT_URI = "http://localhost"

# Schwab API URLs
SCHWAB_AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
SCHWAB_TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"

# Token storage
TOKEN_PATH = "config/schwab_tokens.json"

def get_auth_url():
    """Generate Schwab authorization URL"""
    from urllib.parse import urlencode
    
    params = {
        "response_type": "code",
        "client_id": SCHWAB_CLIENT_ID,
        "redirect_uri": SCHWAB_REDIRECT_URI
    }
    
    query_string = urlencode(params)
    return f"{SCHWAB_AUTH_URL}?{query_string}"

def get_config():
    """Get complete Schwab configuration"""
    return {
        "client_id": SCHWAB_CLIENT_ID,
        "client_secret": SCHWAB_CLIENT_SECRET,
        "redirect_uri": SCHWAB_REDIRECT_URI,
        "auth_url": SCHWAB_AUTH_URL,
        "token_url": SCHWAB_TOKEN_URL,
        "token_path": TOKEN_PATH
    } 