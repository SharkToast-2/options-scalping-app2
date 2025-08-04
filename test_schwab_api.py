#!/usr/bin/env python3
"""
Test script for Schwab API integration
"""

from schwab_api import get_schwab_client
import pandas as pd

def test_schwab_api():
    """Test the Schwab API functionality"""
    print("🧪 Testing Schwab API Integration...")
    
    # Get Schwab client (using mock data for testing)
    client = get_schwab_client(use_mock=True)
    
    # Test symbols
    symbols = ["AAPL", "GOOGL", "MSFT"]
    
    print("\n📊 Testing Quote Data:")
    for symbol in symbols:
        quote = client.get_quote(symbol)
        if quote:
            print(f"✅ {symbol}: ${quote['price']:.2f} ({quote['changePercent']:+.2f}%)")
        else:
            print(f"❌ {symbol}: Failed to get quote")
    
    print("\n📈 Testing Historical Data:")
    for symbol in symbols[:1]:  # Test with just one symbol
        data = client.get_historical_data(symbol, period="1y")
        if data is not None and not data.empty:
            print(f"✅ {symbol}: {len(data)} days of data")
            print(f"   Latest: ${data['Close'].iloc[-1]:.2f}")
            print(f"   Range: ${data['Low'].min():.2f} - ${data['High'].max():.2f}")
        else:
            print(f"❌ {symbol}: Failed to get historical data")
    
    print("\n📋 Testing Market Data:")
    market_data = client.get_market_data(symbols)
    if market_data:
        for symbol, data in market_data.items():
            print(f"✅ {symbol}: ${data['price']:.2f} ({data['changePercent']:+.2f}%)")
    else:
        print("❌ Failed to get market data")
    
    print("\n🎉 Schwab API test completed!")

if __name__ == "__main__":
    test_schwab_api() 