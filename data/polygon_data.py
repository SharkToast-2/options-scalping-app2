#!/usr/bin/env python3
"""
Polygon.io Data Fetcher
Provides real-time market data using Polygon.io API
"""

import requests
import pandas as pd
import time
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class PolygonDataFetcher:
    """Polygon.io data fetcher for real-time market data"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def get_real_time_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote for a symbol"""
        try:
            # Try the latest trades endpoint first
            url = f"{self.base_url}/v2/last/trade/{symbol}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    trade = data['results']
                    return {
                        'symbol': symbol,
                        'price': trade.get('p', 0),
                        'change': 0,  # Would need previous close to calculate
                        'change_percent': 0,
                        'volume': trade.get('s', 0),
                        'high': 0,
                        'low': 0,
                        'open': 0,
                        'previous_close': 0,
                        'source': 'polygon',
                        'timestamp': trade.get('t', 0)
                    }
            
            # Try the previous close endpoint
            url = f"{self.base_url}/v2/aggs/ticker/{symbol}/prev"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    result = data['results'][0]
                    return {
                        'symbol': symbol,
                        'price': result.get('c', 0),
                        'change': result.get('c', 0) - result.get('o', 0),
                        'change_percent': ((result.get('c', 0) - result.get('o', 0)) / result.get('o', 1)) * 100,
                        'volume': result.get('v', 0),
                        'high': result.get('h', 0),
                        'low': result.get('l', 0),
                        'open': result.get('o', 0),
                        'previous_close': result.get('c', 0),
                        'source': 'polygon'
                    }
            else:
                logger.warning(f"Polygon API error for {symbol}: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching Polygon quote for {symbol}: {e}")
        
        return None
    
    def get_stock_data(self, symbol: str, interval: str = "1", period: str = "1") -> Optional[pd.DataFrame]:
        """Get historical stock data"""
        try:
            # Convert interval to Polygon format
            interval_map = {
                "1m": "1",
                "5m": "5", 
                "15m": "15",
                "30m": "30",
                "1h": "60",
                "1d": "1",
                "1w": "1",
                "1M": "1"
            }
            
            polygon_interval = interval_map.get(interval, "1")
            
            # Determine timespan based on period
            timespan_map = {
                "1d": "day",
                "5d": "day", 
                "1mo": "day",
                "3mo": "day",
                "6mo": "day",
                "1y": "day",
                "2y": "day",
                "5y": "day",
                "10y": "day",
                "ytd": "day",
                "max": "day"
            }
            
            timespan = timespan_map.get(period, "day")
            
            url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/{polygon_interval}/{timespan}/2024-01-01/2024-12-31"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and data['results']:
                    df = pd.DataFrame(data['results'])
                    df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
                    df = df.rename(columns={
                        'o': 'Open',
                        'h': 'High', 
                        'l': 'Low',
                        'c': 'Close',
                        'v': 'Volume',
                        'vw': 'Volume_Weighted_Price',
                        'n': 'Number_of_Transactions'
                    })
                    df = df.set_index('timestamp')
                    return df[['Open', 'High', 'Low', 'Close', 'Volume']]
            else:
                logger.warning(f"Polygon API error for {symbol} data: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching Polygon data for {symbol}: {e}")
        
        return None
    
    def get_market_data_batch(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get market data for multiple symbols"""
        results = {}
        
        for symbol in symbols:
            try:
                quote = self.get_real_time_quote(symbol)
                if quote:
                    results[symbol] = quote
                else:
                    logger.warning(f"No data returned for {symbol}")
                    
                # Rate limiting - Polygon free tier allows 5 requests per minute
                time.sleep(1.0)  # 1 second delay between requests for free tier
                
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
        
        return results
    
    def get_ticker_details(self, symbol: str) -> Optional[Dict]:
        """Get detailed information about a ticker"""
        try:
            url = f"{self.base_url}/v3/reference/tickers/{symbol}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json().get('results', {})
            else:
                logger.warning(f"Polygon API error for {symbol} details: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching ticker details for {symbol}: {e}")
        
        return None
    
    def search_tickers(self, search_term: str) -> List[Dict]:
        """Search for tickers"""
        try:
            url = f"{self.base_url}/v3/reference/tickers"
            params = {
                'search': search_term,
                'active': 'true',
                'limit': 10
            }
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            else:
                logger.warning(f"Polygon API error for search: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error searching tickers: {e}")
        
        return []

# Global instance
polygon_fetcher = None

def initialize_polygon(api_key: str):
    """Initialize the global Polygon fetcher"""
    global polygon_fetcher
    polygon_fetcher = PolygonDataFetcher(api_key)
    logger.info("Polygon.io data fetcher initialized")

def get_polygon_quote(symbol: str) -> Optional[Dict]:
    """Get quote using Polygon.io"""
    if polygon_fetcher:
        return polygon_fetcher.get_real_time_quote(symbol)
    return None

def get_polygon_data(symbol: str, interval: str = "1", period: str = "1") -> Optional[pd.DataFrame]:
    """Get historical data using Polygon.io"""
    if polygon_fetcher:
        return polygon_fetcher.get_stock_data(symbol, interval, period)
    return None

def get_polygon_batch_data(symbols: List[str]) -> Dict[str, Dict]:
    """Get batch data using Polygon.io"""
    if polygon_fetcher:
        return polygon_fetcher.get_market_data_batch(symbols)
    return {} 