#!/usr/bin/env python3
"""
Fix data source to use yfinance and test fallback
"""

from data.data_fetcher import OptimizedDataFetcher
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_data_fetcher():
    print("🔧 Testing data fetcher with forced yfinance...")
    
    # Create data fetcher
    fetcher = OptimizedDataFetcher()
    
    # Force data source to yfinance
    fetcher.data_source = "yfinance"
    print(f"📊 Data source set to: {fetcher.data_source}")
    
    # Test getting quotes
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
    
    for symbol in symbols:
        print(f"\n📈 Testing {symbol}...")
        quote = fetcher.get_real_time_quote(symbol)
        
        if quote:
            price = quote.get('price', 'N/A')
            prev_close = quote.get('previous_close', 'N/A')
            change = quote.get('change', 'N/A')
            change_pct = quote.get('change_percent', 'N/A')
            source = quote.get('data_source', 'N/A')
            
            print(f"   Price: ${price}")
            print(f"   Previous Close: ${prev_close}")
            print(f"   Change: ${change} ({change_pct}%)")
            print(f"   Source: {source}")
        else:
            print(f"   ❌ No data returned")
    
    # Test batch data
    print(f"\n🔄 Testing batch data...")
    batch_data = fetcher.get_market_data_batch(symbols)
    
    if batch_data:
        print(f"✅ Got data for {len(batch_data)} symbols:")
        for symbol, data in batch_data.items():
            price = data.get('price', 'N/A')
            source = data.get('data_source', 'N/A')
            print(f"   {symbol}: ${price} (Source: {source})")
    else:
        print("❌ No batch data returned")

if __name__ == "__main__":
    test_data_fetcher() 