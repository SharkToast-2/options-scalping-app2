#!/usr/bin/env python3
"""
Test script to verify Schwab API connectivity and get live data
"""

import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_schwab_connection():
    """Test Schwab API connection and get live data"""
    
    print("🔍 Testing Schwab API Connection")
    print("=" * 50)
    
    # Load config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            schwab_key = config.get('api_keys', {}).get('schwab', '')
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False
    
    print(f"📋 Schwab API Key: {schwab_key[:10]}..." if len(schwab_key) > 10 else "❌ No API key found")
    
    if schwab_key == "your_schwab_api_key_here" or not schwab_key:
        print("❌ Please update your Schwab API key in config.json")
        print("💡 Replace 'your_schwab_api_key_here' with your actual API key")
        return False
    
    # Test data fetcher
    try:
        from data.data_fetcher import DataFetcher
        
        print("\n📊 Initializing Data Fetcher...")
        data_fetcher = DataFetcher(use_schwab=True, use_alpaca=False, use_tos=False)
        
        print(f"✅ Data Source: {data_fetcher.get_data_source()}")
        
        # Test with a simple symbol
        test_symbol = "AAPL"
        print(f"\n🔍 Testing live data for {test_symbol}...")
        
        # Get real-time quote
        quote = data_fetcher.get_real_time_quote(test_symbol)
        if quote:
            print(f"✅ Live Quote for {test_symbol}:")
            print(f"   Price: ${quote.get('price', 'N/A')}")
            print(f"   Change: {quote.get('change', 'N/A')}")
            print(f"   Volume: {quote.get('volume', 'N/A')}")
            print(f"   Data Source: {quote.get('data_source', 'N/A')}")
        else:
            print(f"❌ No live quote data for {test_symbol}")
        
        # Get stock data
        print(f"\n📈 Testing historical data for {test_symbol}...")
        data = data_fetcher.get_stock_data(test_symbol, "1m", "1d")
        if data is not None and not data.empty:
            print(f"✅ Historical Data for {test_symbol}:")
            print(f"   Latest Price: ${data['Close'].iloc[-1]:.2f}")
            print(f"   Data Points: {len(data)}")
            print(f"   Date Range: {data.index[0]} to {data.index[-1]}")
            print(f"   Columns: {list(data.columns)}")
        else:
            print(f"❌ No historical data for {test_symbol}")
        
        # Test multiple symbols
        symbols = ["AAPL", "MSFT", "GOOGL"]
        print(f"\n🔄 Testing batch data for {symbols}...")
        batch_data = data_fetcher.get_market_data_batch(symbols)
        if batch_data:
            print(f"✅ Batch Data Retrieved:")
            for symbol, quote in batch_data.items():
                if quote:
                    print(f"   {symbol}: ${quote.get('price', 'N/A')}")
                else:
                    print(f"   {symbol}: ❌ No data")
        else:
            print("❌ No batch data retrieved")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing data fetcher: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_schwab_key():
    """Helper function to update Schwab API key"""
    print("\n🔧 To update your Schwab API key:")
    print("1. Open config.json in a text editor")
    print("2. Replace 'your_schwab_api_key_here' with your actual API key")
    print("3. Save the file")
    print("4. Run this test again")
    
    # Show current config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            current_key = config.get('api_keys', {}).get('schwab', '')
            print(f"\n📋 Current Schwab key: {current_key}")
    except Exception as e:
        print(f"❌ Error reading config: {e}")

def test_alternative_sources():
    """Test alternative data sources if Schwab fails"""
    print("\n🔄 Testing Alternative Data Sources")
    print("=" * 40)
    
    try:
        from data.data_fetcher import DataFetcher
        
        # Test Yahoo Finance
        print("\n📊 Testing Yahoo Finance...")
        data_fetcher = DataFetcher(use_schwab=False, use_alpaca=False, use_tos=False)
        
        test_symbol = "AAPL"
        quote = data_fetcher.get_real_time_quote(test_symbol)
        if quote:
            print(f"✅ Yahoo Finance Quote for {test_symbol}:")
            print(f"   Price: ${quote.get('price', 'N/A')}")
            print(f"   Data Source: {quote.get('data_source', 'N/A')}")
        else:
            print(f"❌ No Yahoo Finance data for {test_symbol}")
        
        # Test Alpaca
        print("\n📊 Testing Alpaca...")
        data_fetcher = DataFetcher(use_schwab=False, use_alpaca=True, use_tos=False)
        quote = data_fetcher.get_real_time_quote(test_symbol)
        if quote:
            print(f"✅ Alpaca Quote for {test_symbol}:")
            print(f"   Price: ${quote.get('price', 'N/A')}")
            print(f"   Data Source: {quote.get('data_source', 'N/A')}")
        else:
            print(f"❌ No Alpaca data for {test_symbol}")
            
    except Exception as e:
        print(f"❌ Error testing alternative sources: {e}")

if __name__ == "__main__":
    print("🚀 Schwab API Live Data Test")
    print("=" * 50)
    
    # Test Schwab connection
    success = test_schwab_connection()
    
    if not success:
        update_schwab_key()
        test_alternative_sources()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Schwab API test completed successfully!")
        print("✅ You should now have live data in your application")
    else:
        print("⚠️ Schwab API test failed")
        print("💡 Try updating your API key or use alternative data sources")
    
    print("\n📋 Next Steps:")
    print("1. If Schwab works: Run your main application")
    print("2. If Schwab fails: Update API key or use Yahoo Finance")
    print("3. For help: Check the documentation in README.md") 