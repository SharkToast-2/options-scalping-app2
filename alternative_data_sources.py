#!/usr/bin/env python3
"""
Alternative Data Sources for Real Market Data
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class AlphaVantageAPI:
    """Alpha Vantage API for real market data"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "demo"  # Use demo key if none provided
        self.base_url = "https://www.alphavantage.co/query"
        
    def get_stock_data(self, symbol: str, interval: str = "1min", period: str = "1d") -> Optional[pd.DataFrame]:
        """Get real-time stock data from Alpha Vantage"""
        try:
            # Map interval to Alpha Vantage format
            interval_map = {
                "1m": "1min",
                "5m": "5min",
                "15m": "15min",
                "30m": "30min",
                "1h": "60min",
                "1d": "daily"
            }
            
            av_interval = interval_map.get(interval, "1min")
            
            params = {
                'function': 'TIME_SERIES_INTRADAY' if av_interval != 'daily' else 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'interval': av_interval,
                'apikey': self.api_key,
                'outputsize': 'compact'
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract time series data
                if av_interval == 'daily':
                    time_series = data.get('Time Series (Daily)', {})
                else:
                    time_series = data.get(f'Time Series ({av_interval})', {})
                
                if time_series:
                    df_data = []
                    for timestamp, values in time_series.items():
                        df_data.append({
                            'Open': float(values['1. open']),
                            'High': float(values['2. high']),
                            'Low': float(values['3. low']),
                            'Close': float(values['4. close']),
                            'Volume': int(values['5. volume']),
                            'Date': pd.to_datetime(timestamp)
                        })
                    
                    df = pd.DataFrame(df_data)
                    df.set_index('Date', inplace=True)
                    df = df.sort_index()
                    
                    logger.info(f"✅ Alpha Vantage: Retrieved {len(df)} bars for {symbol}")
                    return df
                else:
                    logger.warning(f"⚠️ Alpha Vantage: No data for {symbol}")
                    return None
            else:
                logger.error(f"❌ Alpha Vantage API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Alpha Vantage error for {symbol}: {e}")
            return None
    
    def get_real_time_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from Alpha Vantage"""
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                quote = data.get('Global Quote', {})
                
                if quote:
                    return {
                        "symbol": symbol,
                        "price": float(quote.get('05. price', 0)),
                        "change": float(quote.get('09. change', 0)),
                        "change_percent": float(quote.get('10. change percent', '0%').replace('%', '')),
                        "volume": int(quote.get('06. volume', 0)),
                        "high": float(quote.get('03. high', 0)),
                        "low": float(quote.get('04. low', 0)),
                        "open": float(quote.get('02. open', 0)),
                        "data_source": "alphavantage",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    logger.warning(f"⚠️ Alpha Vantage: No quote data for {symbol}")
                    return None
            else:
                logger.error(f"❌ Alpha Vantage quote API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Alpha Vantage quote error for {symbol}: {e}")
            return None

class FinnhubAPI:
    """Finnhub API for real market data"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "demo"  # Use demo key if none provided
        self.base_url = "https://finnhub.io/api/v1"
        
    def get_stock_data(self, symbol: str, interval: str = "1", period: str = "1d") -> Optional[pd.DataFrame]:
        """Get real-time stock data from Finnhub"""
        try:
            # Calculate timestamps
            end_time = int(datetime.now().timestamp())
            if period == "1d":
                start_time = end_time - (24 * 60 * 60)  # 1 day ago
            elif period == "5d":
                start_time = end_time - (5 * 24 * 60 * 60)  # 5 days ago
            else:
                start_time = end_time - (24 * 60 * 60)  # Default to 1 day
            
            url = f"{self.base_url}/stock/candle"
            params = {
                'symbol': symbol,
                'resolution': interval,
                'from': start_time,
                'to': end_time,
                'token': self.api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['s'] == 'ok' and data['t']:  # Status OK and has data
                    df_data = []
                    for i in range(len(data['t'])):
                        df_data.append({
                            'Open': data['o'][i],
                            'High': data['h'][i],
                            'Low': data['l'][i],
                            'Close': data['c'][i],
                            'Volume': data['v'][i],
                            'Date': pd.to_datetime(data['t'][i], unit='s')
                        })
                    
                    df = pd.DataFrame(df_data)
                    df.set_index('Date', inplace=True)
                    
                    logger.info(f"✅ Finnhub: Retrieved {len(df)} bars for {symbol}")
                    return df
                else:
                    logger.warning(f"⚠️ Finnhub: No data for {symbol}")
                    return None
            else:
                logger.error(f"❌ Finnhub API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Finnhub error for {symbol}: {e}")
            return None
    
    def get_real_time_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from Finnhub"""
        try:
            url = f"{self.base_url}/quote"
            params = {
                'symbol': symbol,
                'token': self.api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data:
                    return {
                        "symbol": symbol,
                        "price": data.get('c', 0),  # Current price
                        "change": data.get('d', 0),  # Change
                        "change_percent": data.get('dp', 0),  # Change percent
                        "high": data.get('h', 0),  # High
                        "low": data.get('l', 0),  # Low
                        "open": data.get('o', 0),  # Open
                        "volume": 0,  # Not provided in quote endpoint
                        "data_source": "finnhub",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    logger.warning(f"⚠️ Finnhub: No quote data for {symbol}")
                    return None
            else:
                logger.error(f"❌ Finnhub quote API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Finnhub quote error for {symbol}: {e}")
            return None

def get_best_available_data_source():
    """Get the best available data source"""
    # Try Alpha Vantage first (free tier available)
    try:
        alpha_vantage = AlphaVantageAPI()
        # Test with a simple request
        test_data = alpha_vantage.get_real_time_quote("AAPL")
        if test_data:
            logger.info("✅ Alpha Vantage API available")
            return alpha_vantage
    except Exception as e:
        logger.warning(f"⚠️ Alpha Vantage not available: {e}")
    
    # Try Finnhub as fallback
    try:
        finnhub = FinnhubAPI()
        # Test with a simple request
        test_data = finnhub.get_real_time_quote("AAPL")
        if test_data:
            logger.info("✅ Finnhub API available")
            return finnhub
    except Exception as e:
        logger.warning(f"⚠️ Finnhub not available: {e}")
    
    logger.warning("⚠️ No alternative data sources available")
    return None 