#!/usr/bin/env python3
"""
ThinkOrSwim API Integration for Options Scalping Application
"""

import requests
import pandas as pd
import numpy as np
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import websocket
import threading
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class TOSCredentials:
    """ThinkOrSwim API credentials"""
    username: str
    password: str
    client_id: str = ""
    access_token: str = ""
    refresh_token: str = ""
    expires_at: datetime = None

class ThinkOrSwimAPI:
    """ThinkOrSwim API client for real-time market data"""
    
    def __init__(self, credentials: TOSCredentials = None):
        self.credentials = credentials
        self.session = requests.Session()
        self.base_url = "https://api.tdameritrade.com/v1"
        self.stream_url = "wss://streamer-ws.tdameritrade.com/ws"
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        
        # Headers for API requests
        self.session.headers.update({
            'User-Agent': 'OptionsScalpingApp/1.0',
            'Content-Type': 'application/json'
        })
        
        # WebSocket connection for real-time data
        self.ws = None
        self.ws_connected = False
        self.real_time_data = {}
        
        # Initialize connection
        if credentials:
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with ThinkOrSwim API"""
        try:
            if not self.credentials:
                logger.warning("No TOS credentials provided")
                return False
            
            # For now, we'll use a simplified approach
            # In production, you'd implement OAuth2 flow
            logger.info("TOS API authentication placeholder - implement OAuth2 flow")
            return True
            
        except Exception as e:
            logger.error(f"TOS authentication error: {e}")
            return False
    
    def get_stock_data(self, symbol: str, interval: str = "1m", period: str = "1d") -> Optional[pd.DataFrame]:
        """Get historical stock data from ThinkOrSwim"""
        try:
            # Map interval to TOS format
            interval_map = {
                "1m": "1",
                "5m": "5", 
                "15m": "15",
                "30m": "30",
                "1h": "60",
                "1d": "daily"
            }
            
            tos_interval = interval_map.get(interval, "1")
            
            # Calculate date range
            end_date = datetime.now()
            if period == "1d":
                start_date = end_date - timedelta(days=1)
            elif period == "5d":
                start_date = end_date - timedelta(days=5)
            elif period == "1mo":
                start_date = end_date - timedelta(days=30)
            else:
                start_date = end_date - timedelta(days=1)
            
            # TOS API endpoint for price history
            url = f"{self.base_url}/marketdata/{symbol}/pricehistory"
            params = {
                'apikey': self.credentials.client_id if self.credentials else '',
                'periodType': 'day',
                'frequencyType': 'minute' if tos_interval != 'daily' else 'daily',
                'frequency': tos_interval,
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'needExtendedHoursData': 'true'
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'candles' in data:
                    # Convert to DataFrame
                    df_data = []
                    for candle in data['candles']:
                        df_data.append({
                            'Open': candle['open'],
                            'High': candle['high'],
                            'Low': candle['low'],
                            'Close': candle['close'],
                            'Volume': candle['volume'],
                            'Date': pd.to_datetime(candle['datetime'], unit='ms')
                        })
                    
                    df = pd.DataFrame(df_data)
                    df.set_index('Date', inplace=True)
                    
                    logger.info(f"✅ TOS: Retrieved {len(df)} bars for {symbol}")
                    return df
                else:
                    logger.warning(f"⚠️ TOS: No candle data for {symbol}")
                    return None
            else:
                logger.error(f"❌ TOS API error for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ TOS error fetching data for {symbol}: {e}")
            return None
    
    def get_real_time_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from ThinkOrSwim"""
        try:
            url = f"{self.base_url}/marketdata/quotes"
            params = {
                'apikey': self.credentials.client_id if self.credentials else '',
                'symbol': symbol
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if symbol in data:
                    quote = data[symbol]
                    return {
                        "symbol": symbol,
                        "price": quote.get('lastPrice', 0),
                        "bid": quote.get('bidPrice', 0),
                        "ask": quote.get('askPrice', 0),
                        "volume": quote.get('totalVolume', 0),
                        "change": quote.get('netChange', 0),
                        "change_percent": quote.get('netPercentChangeInDouble', 0),
                        "high": quote.get('highPrice', 0),
                        "low": quote.get('lowPrice', 0),
                        "open": quote.get('openPrice', 0),
                        "data_source": "thinkorswim",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    logger.warning(f"⚠️ TOS: No quote data for {symbol}")
                    return None
            else:
                logger.error(f"❌ TOS quote API error for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ TOS quote error for {symbol}: {e}")
            return None
    
    def get_options_chain(self, symbol: str) -> Optional[Dict]:
        """Get options chain data from ThinkOrSwim"""
        try:
            url = f"{self.base_url}/marketdata/chains"
            params = {
                'apikey': self.credentials.client_id if self.credentials else '',
                'symbol': symbol
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'callExpDateMap' in data and 'putExpDateMap' in data:
                    # Get nearest expiration
                    call_dates = list(data['callExpDateMap'].keys())
                    put_dates = list(data['putExpDateMap'].keys())
                    
                    if call_dates and put_dates:
                        nearest_date = min(call_dates[0], put_dates[0])
                        
                        calls = []
                        puts = []
                        
                        # Process calls
                        if nearest_date in data['callExpDateMap']:
                            for strike, options in data['callExpDateMap'][nearest_date].items():
                                for option in options:
                                    calls.append({
                                        'strike': float(strike),
                                        'bid': option.get('bid', 0),
                                        'ask': option.get('ask', 0),
                                        'last': option.get('last', 0),
                                        'volume': option.get('totalVolume', 0),
                                        'openInterest': option.get('openInterest', 0),
                                        'impliedVolatility': option.get('impliedVolatility', 0),
                                        'delta': option.get('delta', 0),
                                        'gamma': option.get('gamma', 0),
                                        'theta': option.get('theta', 0),
                                        'vega': option.get('vega', 0)
                                    })
                        
                        # Process puts
                        if nearest_date in data['putExpDateMap']:
                            for strike, options in data['putExpDateMap'][nearest_date].items():
                                for option in options:
                                    puts.append({
                                        'strike': float(strike),
                                        'bid': option.get('bid', 0),
                                        'ask': option.get('ask', 0),
                                        'last': option.get('last', 0),
                                        'volume': option.get('totalVolume', 0),
                                        'openInterest': option.get('openInterest', 0),
                                        'impliedVolatility': option.get('impliedVolatility', 0),
                                        'delta': option.get('delta', 0),
                                        'gamma': option.get('gamma', 0),
                                        'theta': option.get('theta', 0),
                                        'vega': option.get('vega', 0)
                                    })
                        
                        return {
                            "symbol": symbol,
                            "expiration": nearest_date,
                            "calls": pd.DataFrame(calls),
                            "puts": pd.DataFrame(puts)
                        }
                
                logger.warning(f"⚠️ TOS: No options chain data for {symbol}")
                return None
            else:
                logger.error(f"❌ TOS options API error for {symbol}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ TOS options error for {symbol}: {e}")
            return None
    
    def start_real_time_stream(self, symbols: List[str]):
        """Start real-time data stream for symbols"""
        try:
            # Create WebSocket connection
            self.ws = websocket.WebSocketApp(
                self.stream_url,
                on_open=self._on_ws_open,
                on_message=self._on_ws_message,
                on_error=self._on_ws_error,
                on_close=self._on_ws_close
            )
            
            # Start WebSocket in a separate thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            # Subscribe to symbols
            self._subscribe_to_symbols(symbols)
            
            logger.info(f"✅ TOS real-time stream started for {len(symbols)} symbols")
            
        except Exception as e:
            logger.error(f"❌ TOS stream error: {e}")
    
    def _on_ws_open(self, ws):
        """WebSocket open callback"""
        logger.info("✅ TOS WebSocket connected")
        self.ws_connected = True
    
    def _on_ws_message(self, ws, message):
        """WebSocket message callback"""
        try:
            data = json.loads(message)
            
            if 'data' in data:
                for item in data['data']:
                    symbol = item.get('key')
                    if symbol:
                        self.real_time_data[symbol] = {
                            'price': item.get('1', 0),
                            'bid': item.get('2', 0),
                            'ask': item.get('3', 0),
                            'volume': item.get('8', 0),
                            'timestamp': datetime.now().isoformat()
                        }
                        
        except Exception as e:
            logger.error(f"❌ TOS WebSocket message error: {e}")
    
    def _on_ws_error(self, ws, error):
        """WebSocket error callback"""
        logger.error(f"❌ TOS WebSocket error: {error}")
        self.ws_connected = False
    
    def _on_ws_close(self, ws, close_status_code, close_msg):
        """WebSocket close callback"""
        logger.info("🔌 TOS WebSocket disconnected")
        self.ws_connected = False
    
    def _subscribe_to_symbols(self, symbols: List[str]):
        """Subscribe to real-time data for symbols"""
        if not self.ws_connected:
            return
        
        subscribe_message = {
            "requests": [
                {
                    "service": "QUOTE",
                    "command": "SUBS",
                    "parameters": {
                        "keys": ",".join(symbols),
                        "fields": "1,2,3,8"  # price, bid, ask, volume
                    }
                }
            ]
        }
        
        self.ws.send(json.dumps(subscribe_message))
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Get latest real-time data for a symbol"""
        return self.real_time_data.get(symbol)
    
    def stop_real_time_stream(self):
        """Stop real-time data stream"""
        if self.ws:
            self.ws.close()
        self.ws_connected = False
        logger.info("🔌 TOS real-time stream stopped")

class MockThinkOrSwimAPI:
    """Mock ThinkOrSwim API for testing without credentials"""
    
    def __init__(self):
        logger.info("📊 Using Mock TOS API for testing")
    
    def get_stock_data(self, symbol: str, interval: str = "1m", period: str = "1d") -> Optional[pd.DataFrame]:
        """Generate mock stock data"""
        try:
            # Generate realistic mock data
            np.random.seed(hash(symbol) % 1000)  # Different seed per symbol
            
            # Calculate number of bars
            if interval == "1m":
                bars = 390 if period == "1d" else 1950  # Market hours
            elif interval == "5m":
                bars = 78 if period == "1d" else 390
            else:
                bars = 100
            
            # Generate price data
            start_price = 150.0 + np.random.uniform(-50, 50)
            # Map interval to pandas frequency format
            freq_map = {
                "1m": "1min",
                "5m": "5min", 
                "15m": "15min",
                "30m": "30min",
                "1h": "1H",
                "1d": "1D"
            }
            pandas_freq = freq_map.get(interval, "1min")
            dates = pd.date_range(end=datetime.now(), periods=bars, freq=pandas_freq)
            
            # Generate realistic price movements
            returns = np.random.normal(0.0001, 0.01, bars)
            prices = [start_price]
            
            for i in range(1, bars):
                new_price = prices[-1] * (1 + returns[i])
                prices.append(new_price)
            
            # Create DataFrame
            data = pd.DataFrame({
                'Open': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
                'High': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
                'Low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
                'Close': prices,
                'Volume': np.random.randint(100000, 5000000, bars)
            }, index=dates)
            
            logger.info(f"✅ Mock TOS: Generated {len(data)} bars for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"❌ Mock TOS error for {symbol}: {e}")
            return None
    
    def get_real_time_quote(self, symbol: str) -> Optional[Dict]:
        """Generate mock real-time quote"""
        try:
            # Generate realistic quote data
            base_price = 150.0 + np.random.uniform(-50, 50)
            change = np.random.uniform(-5, 5)
            change_percent = (change / base_price) * 100
            
            return {
                "symbol": symbol,
                "price": base_price,
                "bid": base_price - 0.01,
                "ask": base_price + 0.01,
                "volume": np.random.randint(100000, 5000000),
                "change": change,
                "change_percent": change_percent,
                "high": base_price + abs(change),
                "low": base_price - abs(change),
                "open": base_price - change * 0.5,
                "data_source": "mock_thinkorswim",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Mock TOS quote error for {symbol}: {e}")
            return None
    
    def get_options_chain(self, symbol: str) -> Optional[Dict]:
        """Generate mock options chain"""
        try:
            current_price = 150.0 + np.random.uniform(-50, 50)
            
            # Generate strikes around current price
            strikes = np.arange(current_price - 20, current_price + 21, 5)
            
            calls = []
            puts = []
            
            for strike in strikes:
                # Calculate mock option prices using Black-Scholes approximation
                time_to_expiry = 30 / 365  # 30 days
                volatility = 0.3
                
                # Simplified option pricing
                if strike < current_price:
                    call_price = max(0, current_price - strike + 2)
                    put_price = max(0, strike - current_price + 1)
                else:
                    call_price = max(0, current_price - strike + 1)
                    put_price = max(0, strike - current_price + 2)
                
                calls.append({
                    'strike': strike,
                    'bid': call_price * 0.95,
                    'ask': call_price * 1.05,
                    'last': call_price,
                    'volume': np.random.randint(0, 1000),
                    'openInterest': np.random.randint(100, 5000),
                    'impliedVolatility': volatility + np.random.uniform(-0.1, 0.1),
                    'delta': np.random.uniform(0, 1),
                    'gamma': np.random.uniform(0, 0.1),
                    'theta': np.random.uniform(-0.1, 0),
                    'vega': np.random.uniform(0, 0.5)
                })
                
                puts.append({
                    'strike': strike,
                    'bid': put_price * 0.95,
                    'ask': put_price * 1.05,
                    'last': put_price,
                    'volume': np.random.randint(0, 1000),
                    'openInterest': np.random.randint(100, 5000),
                    'impliedVolatility': volatility + np.random.uniform(-0.1, 0.1),
                    'delta': np.random.uniform(-1, 0),
                    'gamma': np.random.uniform(0, 0.1),
                    'theta': np.random.uniform(-0.1, 0),
                    'vega': np.random.uniform(0, 0.5)
                })
            
            return {
                "symbol": symbol,
                "expiration": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                "calls": pd.DataFrame(calls),
                "puts": pd.DataFrame(puts)
            }
            
        except Exception as e:
            logger.error(f"❌ Mock TOS options error for {symbol}: {e}")
            return None

def get_tos_client(use_mock: bool = None) -> ThinkOrSwimAPI:
    """Get ThinkOrSwim API client"""
    # Try to load configuration
    try:
        from tos_config import get_tos_credentials
        credentials = get_tos_credentials()
        
        if credentials:
            logger.info("🔑 Using real ThinkOrSwim API credentials")
            return ThinkOrSwimAPI(credentials)
        else:
            logger.info("📊 Using Mock ThinkOrSwim API (no real credentials)")
            return MockThinkOrSwimAPI()
            
    except ImportError:
        # Fallback to mock if config not available
        logger.info("📊 Using Mock ThinkOrSwim API (no config file)")
        return MockThinkOrSwimAPI() 