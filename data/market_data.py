#!/usr/bin/env python3
"""
Simple Market Data Module
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class MarketData:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_stock_data(self, symbol, period="1mo"):
        """Get stock data with caching"""
        cache_key = f"{symbol}_{period}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_duration):
                return cached_data
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            # Cache the data
            self.cache[cache_key] = (data, datetime.now())
            
            return data
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_real_time_quote(self, symbol):
        """Get real-time quote"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'price': info.get('regularMarketPrice', 0),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0)
            }
        except Exception as e:
            st.error(f"Error fetching quote for {symbol}: {e}")
            return None
    
    def get_market_data_batch(self, symbols, period="1mo"):
        """Get market data for multiple symbols"""
        results = {}
        
        for symbol in symbols:
            data = self.get_stock_data(symbol, period)
            if data is not None and not data.empty:
                results[symbol] = data
        
        return results
    
    def clear_cache(self):
        """Clear the data cache"""
        self.cache.clear()
        st.success("Cache cleared successfully") 