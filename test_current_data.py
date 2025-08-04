#!/usr/bin/env python3
"""
Test Current Market Data
"""

import time
from data.data_fetcher import DataFetcher

def test_current_data():
    print("📊 Testing Current Market Data")
    print("=" * 40)
    
    # Initialize data fetcher
    data_fetcher = DataFetcher(use_schwab=False, use_alpaca=False, use_tos=False)
    print(f"📊 Data Source: {data_fetcher.get_data_source()}")
    
    # Test symbols
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    
    print(f"\n🔍 Testing {len(symbols)} symbols...")
    
    for symbol in symbols:
        try:
            print(f"\n📈 {symbol}:")
            
            # Get real-time quote
            quote = data_fetcher.get_real_time_quote(symbol)
            if quote:
                price = quote.get('price', 0)
                change = quote.get('change', 0)
                change_percent = quote.get('change_percent', 0)
                
                print(f"   Price: ${price:.2f}")
                print(f"   Change: {change:+.2f} ({change_percent:+.2f}%)")
                print(f"   Source: {quote.get('data_source', 'Unknown')}")
            else:
                print(f"   ❌ No data available")
            
            # Small delay to avoid rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Test completed!")
    print(f"💡 Data source: {data_fetcher.get_data_source()}")

if __name__ == "__main__":
    test_current_data() 