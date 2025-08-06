#!/usr/bin/env python3
"""
Data Fetcher Module
Fetches minute-level market data for options scalping
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

def get_minute_data(ticker, period="1d"):
    """
    Get minute-level data for a given ticker
    
    Args:
        ticker (str): Stock ticker symbol
        period (str): Time period (default: "1d")
    
    Returns:
        pd.DataFrame: Minute-level OHLCV data
    """
    try:
        # Get ticker object
        stock = yf.Ticker(ticker)
        
        # Get minute data
        data = stock.history(period=period, interval="1m")
        
        if data.empty:
            print(f"❌ No data available for {ticker}")
            return pd.DataFrame()
        
        # Add timestamp column
        data['timestamp'] = data.index
        
        print(f"✅ Fetched {len(data)} minutes of data for {ticker}")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def get_real_time_price(ticker):
    """
    Get real-time price for a ticker
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        float: Current price
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get('regularMarketPrice', 0)
    except Exception as e:
        print(f"❌ Error getting real-time price for {ticker}: {e}")
        return 0

def get_market_data_batch(tickers, period="1d"):
    """
    Get market data for multiple tickers
    
    Args:
        tickers (list): List of ticker symbols
        period (str): Time period
    
    Returns:
        dict: Dictionary with ticker as key and data as value
    """
    data_dict = {}
    
    for ticker in tickers:
        data = get_minute_data(ticker, period)
        if not data.empty:
            data_dict[ticker] = data
        time.sleep(0.1)  # Rate limiting
    
    return data_dict 