#!/usr/bin/env python3
"""
Environment Configuration
"""

import os

# Schwab API Configuration
SCHWAB_CLIENT_ID = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
SCHWAB_CLIENT_SECRET = "67zvYgAIa8bqWr2v"
SCHWAB_REDIRECT_URI = "https://developer.schwab.com/oauth2-redirect.html"

# Polygon.io API Configuration
POLYGON_API_KEY = "ylJB2jaCAWQaHTa7BZFB60GAoapmK97P"

# Schwab Trading Account API Key
SCHWAB_TRADING_KEY = "3ZHxbk0X7QYK6s0T8VkKNfSkKI1M8LQu"
SCHWAB_TRADING_SECRET = "eUDIuuRPUDz524ih"

# Data Source Configuration
USE_POLYGON = True
USE_SCHWAB = True  # Enable Schwab with the new trading credentials
USE_ALPACA = False
USE_TOS = False

# Cache Configuration
CACHE_DURATION = 300
RATE_LIMIT_DELAY = 1.0

def get_config():
    """Get configuration dictionary"""
    return {
        'schwab_client_id': SCHWAB_CLIENT_ID,
        'schwab_client_secret': SCHWAB_CLIENT_SECRET,
        'schwab_redirect_uri': SCHWAB_REDIRECT_URI,
        'polygon_api_key': POLYGON_API_KEY,
        'schwab_trading_key': SCHWAB_TRADING_KEY,
        'schwab_trading_secret': SCHWAB_TRADING_SECRET,
        'use_polygon': USE_POLYGON,
        'use_schwab': USE_SCHWAB,
        'use_alpaca': USE_ALPACA,
        'use_tos': USE_TOS,
        'cache_duration': CACHE_DURATION,
        'rate_limit_delay': RATE_LIMIT_DELAY
    } 