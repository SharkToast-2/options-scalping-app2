#!/usr/bin/env python3
"""
Optimized Data Fetcher for Options Scalping Application
"""

import json
import time
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import pandas as pd
from functools import lru_cache
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import configuration
from config.settings import API_CONFIG, DATA_CONFIG

logger = logging.getLogger(__name__)

class OptimizedDataFetcher:
    """Optimized data fetcher with caching, async support, and efficient rate limiting"""
    
    def __init__(self, use_schwab: bool = False, use_alpaca: bool = False, use_tos: bool = False, use_polygon: bool = True):
        # API configuration - default to False to force yfinance
        self.use_schwab = use_schwab
        self.use_alpaca = use_alpaca
        self.use_tos = use_tos
        self.use_polygon = use_polygon
        
        # Schwab API credentials
        self.schwab_market_data_key = None
        self.schwab_market_data_secret = None
        self.schwab_trading_key = None
        self.schwab_trading_secret = None
        
        # API clients
        self.alpaca_data_client = None
        self.alpaca_trading_client = None
        self.tos_client = None
        
        # Optimized caching
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_duration = DATA_CONFIG.get("CACHE_DURATION", 300)  # 5 minutes
        
        # Rate limiting
        self.request_timestamps = {}
        self.rate_limit_delay = DATA_CONFIG.get("RATE_LIMIT_DELAY", 1.0)
        
        # Data source priority
        self.data_source = "yfinance"
        
        # Initialize
        self._load_api_keys()
        self._initialize_data_source()
        self._initialize_clients()
    
    def _load_api_keys(self):
        """Load API keys from config file"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                api_keys = config.get('api_keys', {})
                
                # Schwab Market Data API
                self.schwab_market_data_key = api_keys.get('schwab_market_data_key', '')
                self.schwab_market_data_secret = api_keys.get('schwab_market_data_secret', '')
                
                # Schwab Trading API
                self.schwab_trading_key = api_keys.get('schwab_trading_key', '')
                self.schwab_trading_secret = api_keys.get('schwab_trading_secret', '')
                
        except Exception as e:
            logger.error(f"Error loading API keys: {e}")
            self.schwab_market_data_key = ''
            self.schwab_market_data_secret = ''
            self.schwab_trading_key = ''
            self.schwab_trading_secret = ''
    
    def _initialize_data_source(self):
        """Initialize data source with priority"""
        # Priority: Polygon > Alpaca > Schwab > TOS > Yahoo Finance
        if self.use_polygon:
            # Initialize Polygon.io
            try:
                from data.polygon_data import initialize_polygon
                polygon_api_key = "ylJB2jaCAWQaHTa7BZFB60GAoapmK97P"  # Your Polygon API key
                initialize_polygon(polygon_api_key)
                self.data_source = "polygon"
                logger.info("✅ Using Polygon.io as data source")
                return
            except Exception as e:
                logger.warning(f"Failed to initialize Polygon.io: {e}")
        
        if (self.use_alpaca and API_CONFIG["ALPACA"]["API_KEY"] and 
            API_CONFIG["ALPACA"]["API_KEY"] != "your_alpaca_api_key_here"):
            self.data_source = "alpaca"
            logger.info("✅ Using Alpaca API as data source")
        elif (self.use_schwab and self.schwab_market_data_key and self.schwab_market_data_secret and
              self.schwab_market_data_key != "your_schwab_market_data_key_here" and
              self.schwab_market_data_secret != "your_schwab_market_data_secret_here" and
              self.schwab_market_data_key != "" and self.schwab_market_data_secret != ""):
            self.data_source = "schwab"
            logger.info("✅ Using Schwab Market Data API as data source")
        elif self.use_tos and self.tos_client:
            self.data_source = "thinkorswim"
            logger.info("✅ Using ThinkOrSwim API as data source")
        else:
            self.data_source = "yfinance"
            logger.info("📊 Using Yahoo Finance as primary data source")
    
    def _initialize_clients(self):
        """Initialize API clients"""
        # Initialize Alpaca
        if self.data_source == "alpaca":
            self._initialize_alpaca()
        
        # Initialize TOS
        if self.use_tos:
            self._initialize_tos()
    
    def _initialize_alpaca(self):
        """Initialize Alpaca API clients"""
        try:
            from alpaca.data import StockHistoricalDataClient
            from alpaca.trading import TradingClient
            
            self.alpaca_data_client = StockHistoricalDataClient(
                API_CONFIG["ALPACA"]["API_KEY"],
                API_CONFIG["ALPACA"]["SECRET_KEY"]
            )
            self.alpaca_trading_client = TradingClient(
                API_CONFIG["ALPACA"]["API_KEY"],
                API_CONFIG["ALPACA"]["SECRET_KEY"],
                paper=True
            )
            logger.info("✅ Alpaca clients initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize Alpaca: {e}")
    
    def _initialize_tos(self):
        """Initialize ThinkOrSwim client"""
        try:
            from tos_api import get_tos_client
            self.tos_client = get_tos_client()
            if self.tos_client:
                logger.info("✅ ThinkOrSwim client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize ThinkOrSwim: {e}")
    
    def _check_cache(self, key: str) -> Optional[Dict]:
        """Check if data is cached and still valid"""
        if key in self.cache:
            timestamp = self.cache_timestamps.get(key, 0)
            if time.time() - timestamp < self.cache_duration:
                return self.cache[key]
            else:
                # Remove expired cache
                del self.cache[key]
                del self.cache_timestamps[key]
        return None
    
    def _update_cache(self, key: str, data: Dict):
        """Update cache with new data"""
        self.cache[key] = data
        self.cache_timestamps[key] = time.time()
    
    def _rate_limit(self, source: str):
        """Implement rate limiting"""
        current_time = time.time()
        last_request = self.request_timestamps.get(source, 0)
        
        if current_time - last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - (current_time - last_request)
            time.sleep(sleep_time)
        
        self.request_timestamps[source] = time.time()
    
    @lru_cache(maxsize=100)
    def get_stock_data(self, symbol: str, interval: str = "1m", period: str = "1d") -> Optional[pd.DataFrame]:
        """Get stock data with caching"""
        cache_key = f"stock_data_{symbol}_{interval}_{period}"
        cached_data = self._check_cache(cache_key)
        if cached_data:
            return pd.DataFrame(cached_data)
        
        # Get data based on source
        if self.data_source == "polygon":
            data = self._get_polygon_stock_data(symbol, interval, period)
        elif self.data_source == "alpaca":
            data = self._get_alpaca_stock_data(symbol, interval, period)
        elif self.data_source == "schwab":
            data = self._get_schwab_stock_data(symbol, interval, period)
        elif self.data_source == "thinkorswim":
            data = self._get_tos_stock_data(symbol, interval, period)
        else:
            data = self._get_yfinance_stock_data(symbol, interval, period)
        
        if data is not None and not data.empty:
            self._update_cache(cache_key, data.to_dict('records'))
        
        return data
    
    def get_real_time_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote with caching"""
        cache_key = f"quote_{symbol}"
        cached_quote = self._check_cache(cache_key)
        if cached_quote:
            return cached_quote
        
        # Try to get quote based on source
        quote = None
        
        if self.data_source == "polygon":
            quote = self._get_polygon_quote(symbol)
        elif self.data_source == "alpaca":
            quote = self._get_alpaca_quote(symbol)
        elif self.data_source == "schwab":
            quote = self._get_schwab_quote(symbol)
        elif self.data_source == "thinkorswim":
            quote = self._get_tos_quote(symbol)
        else:
            quote = self._get_yfinance_quote(symbol)
        
        # If no quote from primary source, try fallback
        if not quote:
            if self.data_source != "yfinance":
                quote = self._get_yfinance_quote(symbol)
            if not quote:
                # Final fallback to mock data
                from data.mock_data_provider import get_mock_quote
                quote = get_mock_quote(symbol)
                if quote:
                    logger.warning(f"⚠️ No data from {self.data_source} for {symbol}, using mock data")
        
        # If no quote from primary source, fallback to mock data
        if not quote:
            logger.warning(f"⚠️ No data from {self.data_source} for {symbol}, using mock data")
            from data.mock_data import mock_data_provider
            quote = mock_data_provider.get_mock_quote(symbol)
        
        if quote:
            self._update_cache(cache_key, quote)
        
        return quote
    
    def get_market_data_batch(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get market data for multiple symbols efficiently"""
        results = {}
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=min(len(symbols), 5)) as executor:
            # Submit all requests
            future_to_symbol = {
                executor.submit(self.get_real_time_quote, symbol): symbol 
                for symbol in symbols
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    quote = future.result()
                    if quote:
                        results[symbol] = quote
                except Exception as e:
                    logger.error(f"Error fetching data for {symbol}: {e}")
        
        return results
    
    def _get_yfinance_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from Yahoo Finance with optimized retry logic"""
        self._rate_limit("yfinance")
        
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                import yfinance as yf
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                current_price = info.get('regularMarketPrice', 0)
                previous_close = info.get('regularMarketPreviousClose', current_price)
                change = current_price - previous_close if previous_close else 0
                change_percent = (change / previous_close * 100) if previous_close else 0
                
                quote_data = {
                    "symbol": symbol,
                    "price": current_price,
                    "previous_close": previous_close,
                    "change": change,
                    "change_percent": change_percent,
                    "volume": info.get('volume', 0),
                    "avg_volume": info.get('averageVolume', 0),
                    "market_cap": info.get('marketCap', 0),
                    "pe_ratio": info.get('trailingPE', 0),
                    "data_source": "yfinance",
                    "timestamp": datetime.now().isoformat()
                }
                
                return quote_data
                
            except Exception as e:
                error_msg = str(e).lower()
                if "rate limited" in error_msg or "too many requests" in error_msg:
                    if attempt < max_retries - 1:
                        logger.warning(f"⚠️ yfinance rate limited for {symbol}, retrying in {retry_delay}s")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    else:
                        logger.warning(f"⚠️ yfinance rate limited for {symbol}, using mock data")
                        from data.mock_data import mock_data_provider
                        return mock_data_provider.get_mock_quote(symbol)
                else:
                    logger.error(f"❌ yfinance error for {symbol}: {e}")
                    return None
        
        return None
    
    def _get_yfinance_stock_data(self, symbol: str, interval: str, period: str) -> Optional[pd.DataFrame]:
        """Get historical stock data from Yahoo Finance"""
        self._rate_limit("yfinance")
        
        try:
            import yfinance as yf
            
            # Map intervals
            interval_map = {
                "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
                "1h": "1h", "1d": "1d", "1w": "1wk", "1mo": "1mo"
            }
            yf_interval = interval_map.get(interval, "1d")
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=yf_interval, prepost=True)
            
            if data.empty:
                return None
            
            # Standardize column names
            data.columns = [col.title() for col in data.columns]
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching yfinance data for {symbol}: {e}")
            return None
    
    def _get_alpaca_stock_data(self, symbol: str, interval: str, period: str) -> Optional[pd.DataFrame]:
        """Get stock data from Alpaca"""
        if not self.alpaca_data_client:
            return None
        
        try:
            from alpaca.data.requests import StockBarsRequest
            from alpaca.data.timeframe import TimeFrame
            
            # Map intervals to Alpaca timeframes
            timeframe_map = {
                "1m": TimeFrame.Minute,
                "5m": TimeFrame.Minute(5),
                "15m": TimeFrame.Minute(15),
                "30m": TimeFrame.Minute(30),
                "1h": TimeFrame.Hour,
                "1d": TimeFrame.Day
            }
            
            timeframe = timeframe_map.get(interval, TimeFrame.Day)
            
            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=timeframe,
                start=datetime.now() - timedelta(days=30)
            )
            
            bars = self.alpaca_data_client.get_stock_bars(request)
            
            if bars and len(bars.data) > 0:
                df = bars.df
                if symbol in df.index.get_level_values(0):
                    df = df.loc[symbol]
                    df.columns = [col.title() for col in df.columns]
                    return df
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching Alpaca data for {symbol}: {e}")
            return None
    
    def _get_alpaca_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from Alpaca"""
        if not self.alpaca_data_client:
            return None
        
        try:
            from alpaca.data.requests import StockLatestQuoteRequest
            
            request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quote = self.alpaca_data_client.get_stock_latest_quote(request)
            
            if quote and symbol in quote:
                q = quote[symbol]
                return {
                    "symbol": symbol,
                    "price": q.ask_price or q.bid_price or 0,
                    "bid": q.bid_price,
                    "ask": q.ask_price,
                    "volume": q.bid_size + q.ask_size if q.bid_size and q.ask_size else 0,
                    "data_source": "alpaca",
                    "timestamp": datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching Alpaca quote for {symbol}: {e}")
            return None
    
    def _get_schwab_stock_data(self, symbol: str, interval: str, period: str) -> Optional[pd.DataFrame]:
        """Get stock data from Schwab API"""
        try:
            from schwab_api import get_schwab_client
            client = get_schwab_client(self.schwab_market_data_key, self.schwab_market_data_secret, use_mock=False)
            data = client.get_historical_data(symbol, period=period, interval=interval)
            
            if data and not data.empty:
                return data
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching Schwab data for {symbol}: {e}")
            return None
    
    def _get_schwab_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from Schwab API"""
        try:
            from schwab_api import get_schwab_client
            client = get_schwab_client(self.schwab_market_data_key, self.schwab_market_data_secret, use_mock=False)
            quote_data = client.get_quote(symbol)
            
            if quote_data:
                return {
                    "symbol": symbol,
                    "price": quote_data.get('price', 0),
                    "change": quote_data.get('change', 0),
                    "change_percent": quote_data.get('changePercent', 0),
                    "volume": quote_data.get('volume', 0),
                    "data_source": "schwab",
                    "timestamp": datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching Schwab quote for {symbol}: {e}")
            return None
    
    def _get_tos_stock_data(self, symbol: str, interval: str, period: str) -> Optional[pd.DataFrame]:
        """Get stock data from ThinkOrSwim"""
        if not self.tos_client:
            return None
        
        try:
            data = self.tos_client.get_historical_data(symbol, period=period, interval=interval)
            return data
            
        except Exception as e:
            logger.error(f"Error fetching TOS data for {symbol}: {e}")
            return None
    
    def _get_polygon_quote(self, symbol: str) -> Optional[Dict]:
        """Get quote from Polygon.io API"""
        try:
            from data.polygon_data import get_polygon_quote
            quote = get_polygon_quote(symbol)
            if quote:
                logger.info(f"✅ Polygon.io quote for {symbol}: ${quote.get('price', 0):.2f}")
            return quote
            
        except Exception as e:
            logger.error(f"Error fetching Polygon quote for {symbol}: {e}")
            return None
    
    def _get_polygon_stock_data(self, symbol: str, interval: str, period: str) -> Optional[pd.DataFrame]:
        """Get historical stock data from Polygon.io API"""
        try:
            from data.polygon_data import get_polygon_data
            data = get_polygon_data(symbol, interval, period)
            if data is not None and not data.empty:
                logger.info(f"✅ Polygon.io data for {symbol}: {len(data)} records")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching Polygon data for {symbol}: {e}")
            return None
    
    def _get_tos_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from ThinkOrSwim"""
        if not self.tos_client:
            return None
        
        try:
            quote_data = self.tos_client.get_quote(symbol)
            
            if quote_data:
                return {
                    "symbol": symbol,
                    "price": quote_data.get('price', 0),
                    "change": quote_data.get('change', 0),
                    "change_percent": quote_data.get('changePercent', 0),
                    "volume": quote_data.get('volume', 0),
                    "data_source": "thinkorswim",
                    "timestamp": datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching TOS quote for {symbol}: {e}")
            return None
    
    def get_data_source(self) -> str:
        """Get the current data source being used"""
        return self.data_source
    
    def get_api_status(self) -> Dict[str, bool]:
        """Get status of various APIs"""
        return {
            "schwab_market_data": bool(self.schwab_market_data_key and self.schwab_market_data_secret and 
                                     self.schwab_market_data_key != "your_schwab_market_data_key_here" and 
                                     self.schwab_market_data_secret != "your_schwab_market_data_secret_here"),
            "schwab_trading": bool(self.schwab_trading_key and self.schwab_trading_secret and 
                                 self.schwab_trading_key != "your_schwab_trading_api_key_here" and 
                                 self.schwab_trading_secret != "your_schwab_trading_secret_here"),
            "alpaca": bool(self.alpaca_data_client is not None),
            "thinkorswim": bool(self.tos_client is not None)
        }
    
    def get_data_source_info(self) -> Dict[str, str]:
        """Get information about the current data source"""
        source_info = {
            "polygon": {
                "name": "Polygon.io API",
                "description": "Professional real-time market data and financial APIs",
                "status": "✅ Active",
                "limitations": "Rate limited based on subscription tier"
            },
            "thinkorswim": {
                "name": "ThinkOrSwim API",
                "description": "Professional-grade real-time data from TD Ameritrade",
                "status": "✅ Active",
                "limitations": "Requires TOS credentials, currently using mock data"
            },
            "yfinance": {
                "name": "Yahoo Finance",
                "description": "Free market data with no API key required",
                "status": "✅ Active",
                "limitations": "15-minute delay for some data, rate limited"
            },
            "alpaca": {
                "name": "Alpaca API",
                "description": "Professional trading and market data API",
                "status": "✅ Active",
                "limitations": "Requires API key, paper trading available"
            },
            "schwab": {
                "name": "Schwab API",
                "description": "Schwab market data and trading API",
                "status": "⚠️ Limited",
                "limitations": "API endpoints not publicly available yet"
            }
        }
        
        return source_info.get(self.data_source, {
            "name": "Unknown",
            "description": "Unknown data source",
            "status": "❌ Inactive",
            "limitations": "No data available"
        })
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_timestamps.clear()
        logger.info("Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            "cached_items": len(self.cache),
            "cache_hits": getattr(self, '_cache_hits', 0),
            "cache_misses": getattr(self, '_cache_misses', 0)
        }

# Backward compatibility
DataFetcher = OptimizedDataFetcher 