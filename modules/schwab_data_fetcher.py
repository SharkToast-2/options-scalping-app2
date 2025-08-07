#!/usr/bin/env python3
"""
Schwab Data Fetcher Module
Provides real-time market data and options data from Schwab API
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time
import logging
from config.schwab_config import schwab_config, SchwabEndpoints

logger = logging.getLogger(__name__)

class SchwabDataFetcher:
    """Real-time data fetcher using Schwab API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.cache_ttl = 30  # 30 seconds cache for real-time data
        self.last_request_time = 0
        self.rate_limit_delay = 0.1  # 100ms between requests
        
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make authenticated request to Schwab API"""
        try:
            self._rate_limit()
            
            headers = schwab_config.get_headers()
            
            if method == "GET":
                response = self.session.get(url, headers=headers)
            elif method == "POST":
                response = self.session.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Token expired, try to refresh
                logger.warning("Token expired, attempting refresh...")
                schwab_config.refresh_access_token(schwab_config.load_tokens()['refresh_token'])
                headers = schwab_config.get_headers()
                
                # Retry request
                if method == "GET":
                    response = self.session.get(url, headers=headers)
                else:
                    response = self.session.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"API request failed after token refresh: {response.status_code}")
            else:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error making Schwab API request: {e}")
            raise
    
    def get_real_time_quote(self, symbol: str) -> Dict:
        """Get real-time quote for a symbol"""
        cache_key = f"quote_{symbol}"
        
        # Check cache first
        if cache_key in self.cache:
            cache_time, cache_data = self.cache[cache_key]
            if time.time() - cache_time < self.cache_ttl:
                return cache_data
        
        try:
            url = SchwabEndpoints.get_quotes([symbol])
            data = self._make_request(url)
            
            # Cache the result
            self.cache[cache_key] = (time.time(), data)
            
            return data
            
        except Exception as e:
            logger.error(f"Error getting quote for {symbol}: {e}")
            return {}
    
    def get_minute_data(self, symbol: str, period: str = "1d") -> pd.DataFrame:
        """
        Get minute-level data for a symbol
        Note: Schwab API may have different data granularity than yfinance
        """
        try:
            # Get real-time quote
            quote_data = self.get_real_time_quote(symbol)
            
            if not quote_data:
                return pd.DataFrame()
            
            # For now, create a simple DataFrame with current data
            # In a full implementation, you'd fetch historical minute data
            current_time = datetime.now()
            
            # Create a simple OHLCV structure
            data = {
                'Open': [quote_data.get('open', 0)],
                'High': [quote_data.get('high', 0)],
                'Low': [quote_data.get('low', 0)],
                'Close': [quote_data.get('last', 0)],
                'Volume': [quote_data.get('volume', 0)],
                'timestamp': [current_time]
            }
            
            df = pd.DataFrame(data)
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting minute data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_options_chain(self, symbol: str, expiration_date: str = None) -> Dict:
        """Get options chain for a symbol"""
        try:
            url = SchwabEndpoints.get_options_chain(symbol, expiration_date)
            data = self._make_request(url)
            return data
            
        except Exception as e:
            logger.error(f"Error getting options chain for {symbol}: {e}")
            return {}
    
    def get_account_info(self) -> Dict:
        """Get account information"""
        try:
            url = SchwabEndpoints.get_accounts()
            data = self._make_request(url)
            return data
            
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return {}
    
    def get_positions(self, account_id: str) -> Dict:
        """Get current positions for an account"""
        try:
            url = SchwabEndpoints.get_account_positions(account_id)
            data = self._make_request(url)
            return data
            
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return {}
    
    def get_market_status(self) -> Dict:
        """Get current market status"""
        try:
            # Check if market is open (simplified)
            now = datetime.now()
            
            # US Market hours: 9:30 AM - 4:00 PM ET (simplified)
            market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
            market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
            
            is_open = market_open <= now <= market_close and now.weekday() < 5
            
            return {
                'is_open': is_open,
                'current_time': now.isoformat(),
                'market_open': market_open.isoformat(),
                'market_close': market_close.isoformat(),
                'time_to_open': (market_open - now).total_seconds() if now < market_open else 0,
                'time_to_close': (market_close - now).total_seconds() if now < market_close else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting market status: {e}")
            return {'is_open': False, 'current_time': datetime.now().isoformat()}
    
    def get_comprehensive_data(self, symbol: str) -> Dict:
        """Get comprehensive data for a symbol including options"""
        try:
            # Get real-time quote
            quote_data = self.get_real_time_quote(symbol)
            
            # Get options chain
            options_data = self.get_options_chain(symbol)
            
            # Get account info
            account_data = self.get_account_info()
            
            return {
                'quote': quote_data,
                'options': options_data,
                'account': account_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting comprehensive data for {symbol}: {e}")
            return {}
    
    def find_options_contracts(self, symbol: str, strike_price: float, 
                             option_type: str = "call", days_to_expiry: int = 30) -> List[Dict]:
        """Find suitable options contracts for scalping"""
        try:
            options_data = self.get_options_chain(symbol)
            
            if not options_data or 'options' not in options_data:
                return []
            
            suitable_contracts = []
            target_expiry = datetime.now() + timedelta(days=days_to_expiry)
            
            for option in options_data['options']:
                if (option.get('optionType', '').lower() == option_type.lower() and
                    abs(float(option.get('strikePrice', 0)) - strike_price) < 1.0):
                    
                    expiry_date = datetime.strptime(option.get('expirationDate'), '%Y-%m-%d')
                    if expiry_date <= target_expiry:
                        suitable_contracts.append(option)
            
            return suitable_contracts
            
        except Exception as e:
            logger.error(f"Error finding options contracts: {e}")
            return []
    
    def get_historical_data(self, symbol: str, period: str = "1d") -> pd.DataFrame:
        """
        Get historical data for backtesting
        Note: This would need to be implemented based on Schwab's historical data API
        """
        # Placeholder for historical data implementation
        logger.warning("Historical data not yet implemented for Schwab API")
        return pd.DataFrame()

# Global instance
schwab_data_fetcher = SchwabDataFetcher()

# Backward compatibility functions
def get_schwab_quote(symbol: str) -> Dict:
    """Get real-time quote from Schwab"""
    return schwab_data_fetcher.get_real_time_quote(symbol)

def get_schwab_minute_data(symbol: str, period: str = "1d") -> pd.DataFrame:
    """Get minute data from Schwab"""
    return schwab_data_fetcher.get_minute_data(symbol, period)

def get_schwab_options_chain(symbol: str) -> Dict:
    """Get options chain from Schwab"""
    return schwab_data_fetcher.get_options_chain(symbol)

def get_schwab_account_info() -> Dict:
    """Get account information from Schwab"""
    return schwab_data_fetcher.get_account_info() 