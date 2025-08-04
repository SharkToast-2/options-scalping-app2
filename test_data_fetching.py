#!/usr/bin/env python3
"""
Test script to debug data fetching issues
"""

from data.data_fetcher import OptimizedDataFetcher
import pandas as pd

def test_data_fetching():
    print("🔍 Testing Data Fetcher...")
    
    # Initialize data fetcher
    fetcher = OptimizedDataFetcher()
    
    # Test getting a quote
    print("\n📊 Testing AAPL quote...")
    quote = fetcher.get_real_time_quote('AAPL')
    if quote:
        print(f"✅ AAPL Quote: ${quote.get('price', 'N/A')} (Prev: ${quote.get('previous_close', 'N/A')})")
        print(f"   Change: {quote.get('change', 'N/A')} ({quote.get('change_percent', 'N/A')}%)")
        print(f"   Source: {quote.get('data_source', 'N/A')}")
    else:
        print("❌ No quote data returned")
    
    # Test getting stock data
    print("\n📈 Testing AAPL stock data...")
    stock_data = fetcher.get_stock_data('AAPL', '1d', '1d')
    if stock_data is not None and not stock_data.empty:
        print(f"✅ AAPL Stock Data Shape: {stock_data.shape}")
        print(f"   Latest Close: ${stock_data['Close'].iloc[-1]:.2f}")
        print(f"   Latest Open: ${stock_data['Open'].iloc[-1]:.2f}")
        print(f"   Latest High: ${stock_data['High'].iloc[-1]:.2f}")
        print(f"   Latest Low: ${stock_data['Low'].iloc[-1]:.2f}")
    else:
        print("❌ No stock data returned")
    
    # Test batch data
    print("\n🔄 Testing batch data...")
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
    batch_data = fetcher.get_market_data_batch(symbols)
    
    if batch_data:
        print(f"✅ Batch Data Keys: {list(batch_data.keys())}")
        for symbol, data in batch_data.items():
            price = data.get('price', 'N/A')
            prev_close = data.get('previous_close', 'N/A')
            change = data.get('change', 'N/A')
            change_pct = data.get('change_percent', 'N/A')
            source = data.get('data_source', 'N/A')
            
            print(f"   {symbol}: ${price} (Prev: ${prev_close}) | Change: {change} ({change_pct}%) | Source: {source}")
    else:
        print("❌ No batch data returned")
    
    # Test data source info
    print("\n📋 Data Source Info:")
    source_info = fetcher.get_data_source_info()
    print(f"   Source: {source_info.get('name', 'N/A')}")
    print(f"   Status: {source_info.get('status', 'N/A')}")
    print(f"   Description: {source_info.get('description', 'N/A')}")

if __name__ == "__main__":
    test_data_fetching() 