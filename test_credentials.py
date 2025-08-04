#!/usr/bin/env python3
"""
Test Schwab Credentials
"""

import json

def test_credentials():
    print("🔑 Testing Schwab Credentials")
    print("=" * 40)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    api_keys = config.get('api_keys', {})
    
    # Check Market Data credentials
    market_key = api_keys.get('schwab_market_data_key', '')
    market_secret = api_keys.get('schwab_market_data_secret', '')
    
    print(f"📊 Market Data API Key: {market_key[:10]}..." if len(market_key) > 10 else "Not set")
    print(f"📊 Market Data Secret: {'✅ Set' if market_secret and market_secret != 'your_schwab_market_data_secret_here' else '❌ Not set'}")
    
    # Check Trading credentials
    trading_key = api_keys.get('schwab_trading_key', '')
    trading_secret = api_keys.get('schwab_trading_secret', '')
    
    print(f"🚀 Trading API Key: {trading_key[:10]}..." if len(trading_key) > 10 else "Not set")
    print(f"🚀 Trading Secret: {'✅ Set' if trading_secret and trading_secret != 'your_schwab_trading_secret_here' else '❌ Not set'}")
    
    # Test data fetcher
    print("\n🧪 Testing Data Fetcher...")
    try:
        from data.data_fetcher import DataFetcher
        
        data_fetcher = DataFetcher(use_schwab=True, use_alpaca=False, use_tos=False)
        print(f"📊 Data Source: {data_fetcher.get_data_source()}")
        
        if data_fetcher.get_data_source() == "schwab":
            print("✅ Schwab API is the primary data source!")
            
            # Test with a simple quote
            quote = data_fetcher.get_real_time_quote("AAPL")
            if quote:
                print(f"✅ Live AAPL: ${quote.get('price', 'N/A')}")
            else:
                print("⚠️ No live data received (this might be normal if markets are closed)")
        else:
            print(f"⚠️ Data source is: {data_fetcher.get_data_source()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n💡 Status:")
    if market_key and market_secret and market_secret != 'your_schwab_market_data_secret_here':
        print("✅ Market Data API: Ready")
    else:
        print("❌ Market Data API: Not configured")
    
    if trading_key and trading_secret and trading_secret != 'your_schwab_trading_secret_here':
        print("✅ Trading API: Ready")
    else:
        print("❌ Trading API: Not configured")

if __name__ == "__main__":
    test_credentials() 