#!/usr/bin/env python3
"""
Simple test script for Yahoo Finance with rate limiting
"""

import sys
import os
import time
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import DataFetcher

def test_yfinance_simple():
    """Simple test for Yahoo Finance with rate limiting"""
    print("🚀 Testing Yahoo Finance (Simple)")
    print("=" * 40)
    
    # Initialize data fetcher
    print("📊 Initializing Data Fetcher...")
    data_fetcher = DataFetcher(use_schwab=False, use_alpaca=False)
    
    # Check data source
    data_source_info = data_fetcher.get_data_source_info()
    print(f"✅ Data Source: {data_source_info['name']}")
    print(f"📋 Status: {data_source_info['status']}")
    print()
    
    # Test single symbol with delay
    test_symbol = "AAPL"
    print(f"🔍 Testing {test_symbol}...")
    
    try:
        # Get stock data
        print("  📈 Fetching stock data...")
        data = data_fetcher.get_stock_data(test_symbol, "1d", "5d")
        
        if data is not None and not data.empty:
            print(f"  ✅ Data retrieved: {len(data)} bars")
            print(f"  📊 Latest price: ${data['Close'].iloc[-1]:.2f}")
            print(f"  📈 Volume: {data['Volume'].iloc[-1]:,}")
            print(f"  🕒 Latest timestamp: {data.index[-1]}")
        else:
            print(f"  ❌ No data retrieved for {test_symbol}")
            
    except Exception as e:
        print(f"  ❌ Error fetching data for {test_symbol}: {e}")
    
    # Wait before next request
    print("\n⏳ Waiting 3 seconds before next request...")
    time.sleep(3)
    
    # Test quote
    print(f"💹 Testing quote for {test_symbol}...")
    
    try:
        quote = data_fetcher.get_real_time_quote(test_symbol)
        
        if quote:
            print(f"  ✅ {test_symbol}: ${quote['price']:.2f} ({quote['change_percent']:+.2f}%)")
            print(f"     Volume: {quote['volume']:,}")
            print(f"     Market Cap: ${quote['market_cap']:,.0f}")
        else:
            print(f"  ❌ No quote data for {test_symbol}")
            
    except Exception as e:
        print(f"  ❌ Error fetching quote for {test_symbol}: {e}")
    
    print(f"\n🎉 Simple Yahoo Finance Test Completed!")
    print(f"📊 Data Source: {data_source_info['name']}")

if __name__ == "__main__":
    test_yfinance_simple() 