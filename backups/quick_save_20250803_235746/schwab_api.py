import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import streamlit as st

class SchwabAPI:
    def __init__(self, api_key=None, secret_key=None, base_url="https://api.schwab.com"):
        """
        Initialize Schwab API client
        
        Note: You'll need to register for Schwab API access and get your API key and secret
        from: https://developer.schwab.com/
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.session = requests.Session()
        
        if api_key and secret_key:
            # Use both API key and secret for authentication
            self.session.headers.update({
                'X-API-Key': api_key,
                'X-Secret-Key': secret_key,
                'Content-Type': 'application/json'
            })
        elif api_key:
            # Fallback to Bearer token if only API key provided
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
    
    def get_quote(self, symbol):
        """Get real-time quote for a symbol"""
        try:
            # Schwab API endpoint for quotes
            url = f"{self.base_url}/v1/quotes/{symbol}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_quote_data(data)
            else:
                st.error(f"Error fetching quote for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Error accessing Schwab API: {e}")
            return None
    
    def get_historical_data(self, symbol, period="1y", interval="1d"):
        """
        Get historical data for a symbol
        
        Args:
            symbol (str): Stock symbol
            period (str): Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval (str): Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        """
        try:
            # Calculate start and end dates
            end_date = datetime.now()
            
            if period == "1d":
                start_date = end_date - timedelta(days=1)
            elif period == "5d":
                start_date = end_date - timedelta(days=5)
            elif period == "1mo":
                start_date = end_date - timedelta(days=30)
            elif period == "3mo":
                start_date = end_date - timedelta(days=90)
            elif period == "6mo":
                start_date = end_date - timedelta(days=180)
            elif period == "1y":
                start_date = end_date - timedelta(days=365)
            elif period == "2y":
                start_date = end_date - timedelta(days=730)
            elif period == "5y":
                start_date = end_date - timedelta(days=1825)
            else:
                start_date = end_date - timedelta(days=365)  # Default to 1 year
            
            # Schwab API endpoint for historical data
            url = f"{self.base_url}/v1/history/{symbol}"
            params = {
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'interval': interval
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_historical_data(data)
            else:
                st.error(f"Error fetching historical data for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Error accessing Schwab API: {e}")
            return None
    
    def get_market_data(self, symbols):
        """Get market data for multiple symbols"""
        try:
            # Schwab API endpoint for market data
            url = f"{self.base_url}/v1/market-data"
            params = {'symbols': ','.join(symbols)}
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_market_data(data)
            else:
                st.error(f"Error fetching market data: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Error accessing Schwab API: {e}")
            return None
    
    def _parse_quote_data(self, data):
        """Parse quote data from Schwab API response"""
        try:
            # This is a placeholder - adjust based on actual Schwab API response format
            quote = {
                'symbol': data.get('symbol'),
                'price': data.get('lastPrice'),
                'change': data.get('change'),
                'changePercent': data.get('changePercent'),
                'volume': data.get('volume'),
                'high': data.get('high'),
                'low': data.get('low'),
                'open': data.get('open'),
                'previousClose': data.get('previousClose'),
                'timestamp': datetime.now()
            }
            return quote
        except Exception as e:
            st.error(f"Error parsing quote data: {e}")
            return None
    
    def _parse_historical_data(self, data):
        """Parse historical data from Schwab API response"""
        try:
            # This is a placeholder - adjust based on actual Schwab API response format
            records = []
            
            for item in data.get('items', []):
                record = {
                    'Date': pd.to_datetime(item.get('date')),
                    'Open': item.get('open'),
                    'High': item.get('high'),
                    'Low': item.get('low'),
                    'Close': item.get('close'),
                    'Volume': item.get('volume')
                }
                records.append(record)
            
            df = pd.DataFrame(records)
            df.set_index('Date', inplace=True)
            return df
            
        except Exception as e:
            st.error(f"Error parsing historical data: {e}")
            return None
    
    def _parse_market_data(self, data):
        """Parse market data from Schwab API response"""
        try:
            # This is a placeholder - adjust based on actual Schwab API response format
            market_data = {}
            
            for item in data.get('items', []):
                symbol = item.get('symbol')
                market_data[symbol] = {
                    'price': item.get('lastPrice'),
                    'change': item.get('change'),
                    'changePercent': item.get('changePercent'),
                    'volume': item.get('volume')
                }
            
            return market_data
            
        except Exception as e:
            st.error(f"Error parsing market data: {e}")
            return None

# Mock Schwab API for demonstration (when you don't have API access yet)
class MockSchwabAPI:
    def __init__(self):
        self.base_url = "mock"
    
    def get_quote(self, symbol):
        """Mock quote data"""
        import numpy as np
        
        base_price = 150.0
        change = np.random.normal(0, 2)
        price = base_price + change
        
        return {
            'symbol': symbol,
            'price': price,
            'change': change,
            'changePercent': (change / base_price) * 100,
            'volume': np.random.randint(1000000, 10000000),
            'high': price + np.random.uniform(0, 5),
            'low': price - np.random.uniform(0, 5),
            'open': base_price + np.random.normal(0, 1),
            'previousClose': base_price,
            'timestamp': datetime.now()
        }
    
    def get_historical_data(self, symbol, period="1y", interval="1d"):
        """Mock historical data"""
        import numpy as np
        
        # Generate realistic mock data
        days = 252 if period == "1y" else 30
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Generate price movements
        returns = np.random.normal(0.0005, 0.02, days)
        prices = [150.0]
        
        for i in range(1, days):
            new_price = prices[-1] * (1 + returns[i])
            prices.append(new_price)
        
        # Create DataFrame
        data = pd.DataFrame({
            'Open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000000, 10000000, days)
        }, index=dates)
        
        return data
    
    def get_market_data(self, symbols):
        """Mock market data"""
        import numpy as np
        
        market_data = {}
        for symbol in symbols:
            base_price = 150.0
            change = np.random.normal(0, 2)
            price = base_price + change
            
            market_data[symbol] = {
                'price': price,
                'change': change,
                'changePercent': (change / base_price) * 100,
                'volume': np.random.randint(1000000, 10000000)
            }
        
        return market_data

def get_schwab_client(api_key=None, secret_key=None, use_mock=True):
    """
    Get Schwab API client
    
    Args:
        api_key (str): Your Schwab API key
        secret_key (str): Your Schwab secret key
        use_mock (bool): Use mock data if no API key provided
    """
    if api_key and secret_key and api_key != "your_schwab_api_key_here" and secret_key != "your_schwab_secret_key_here" and not use_mock:
        return SchwabAPI(api_key, secret_key)
    else:
        return MockSchwabAPI() 