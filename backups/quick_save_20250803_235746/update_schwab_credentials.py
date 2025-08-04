#!/usr/bin/env python3
"""
Update Schwab Market Data and Trading API credentials
"""

import json
import os

def update_schwab_credentials():
    """Update Schwab API credentials in config.json"""
    
    print("🔧 Schwab API Credentials Update Tool")
    print("=" * 60)
    print("📊 This tool helps you configure both:")
    print("   • Schwab Market Data API (for real-time prices)")
    print("   • Schwab Trading API (for executing trades)")
    print("=" * 60)
    
    # Check if config.json exists
    if not os.path.exists('config.json'):
        print("❌ config.json not found!")
        print("💡 Please make sure you're in the project directory")
        return False
    
    # Load current config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return False
    
    # Show current keys
    current_market_key = config.get('api_keys', {}).get('schwab_market_data_key', '')
    current_market_secret = config.get('api_keys', {}).get('schwab_market_data_secret', '')
    current_trading_key = config.get('api_keys', {}).get('schwab_trading_key', '')
    current_trading_secret = config.get('api_keys', {}).get('schwab_trading_secret', '')
    
    print(f"📋 Current Market Data API Key: {current_market_key[:10]}..." if len(current_market_key) > 10 else "Not set")
    print(f"📋 Current Market Data Secret: {current_market_secret[:10]}..." if len(current_market_secret) > 10 else "Not set")
    print(f"📋 Current Trading API Key: {current_trading_key[:10]}..." if len(current_trading_key) > 10 else "Not set")
    print(f"📋 Current Trading Secret: {current_trading_secret[:10]}..." if len(current_trading_secret) > 10 else "Not set")
    
    # Check if keys are already configured
    market_configured = (current_market_key and current_market_key != "your_schwab_market_data_key_here" and 
                        current_market_secret and current_market_secret != "your_schwab_market_data_secret_here")
    
    trading_configured = (current_trading_key and current_trading_key != "your_schwab_trading_api_key_here" and 
                         current_trading_secret and current_trading_secret != "your_schwab_trading_secret_here")
    
    if market_configured and trading_configured:
        print("\n✅ You already have both Market Data and Trading APIs configured!")
        response = input("Do you want to update them? (y/n): ").lower()
        if response != 'y':
            print("👋 No changes made")
            return True
    
    print("\n" + "=" * 60)
    print("📊 SCHWAB MARKET DATA API SETUP")
    print("=" * 60)
    print("💡 This API provides real-time market prices and data")
    print("💡 You need this for the app to show current stock prices")
    
    # Get Market Data API credentials
    print("\n🔑 Enter your Schwab Market Data API key:")
    print("💡 If you don't have one, press Enter to skip")
    new_market_key = input("Market Data API Key: ").strip()
    
    print("\n🔑 Enter your Schwab Market Data Secret key:")
    print("💡 If you don't have one, press Enter to skip")
    new_market_secret = input("Market Data Secret Key: ").strip()
    
    print("\n" + "=" * 60)
    print("🚀 SCHWAB TRADING API SETUP")
    print("=" * 60)
    print("💡 This API allows you to execute actual trades")
    print("💡 You need this for the app to place orders")
    print("⚠️  WARNING: This will execute real trades with real money!")
    
    # Get Trading API credentials
    print("\n🔑 Enter your Schwab Trading API key:")
    print("💡 If you don't have one, press Enter to skip")
    new_trading_key = input("Trading API Key: ").strip()
    
    print("\n🔑 Enter your Schwab Trading Secret key:")
    print("💡 If you don't have one, press Enter to skip")
    new_trading_secret = input("Trading Secret Key: ").strip()
    
    # Update config
    if new_market_key:
        config['api_keys']['schwab_market_data_key'] = new_market_key
    if new_market_secret:
        config['api_keys']['schwab_market_data_secret'] = new_market_secret
    if new_trading_key:
        config['api_keys']['schwab_trading_key'] = new_trading_key
    if new_trading_secret:
        config['api_keys']['schwab_trading_secret'] = new_trading_secret
    
    # Save config
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("\n✅ Credentials updated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False

def test_credentials():
    """Test the Schwab credentials after update"""
    print("\n🧪 Testing Schwab credentials...")
    
    try:
        from data.data_fetcher import DataFetcher
        
        data_fetcher = DataFetcher(use_schwab=True, use_alpaca=False, use_tos=False)
        
        print(f"📊 Data Source: {data_fetcher.get_data_source()}")
        
        if data_fetcher.get_data_source() == "schwab":
            print("✅ Schwab Market Data API is working!")
            
            # Test market data
            quote = data_fetcher.get_real_time_quote("AAPL")
            if quote:
                print(f"✅ Market data working! AAPL: ${quote.get('price', 'N/A')}")
            else:
                print("⚠️ Market data not working - check your credentials")
        else:
            print(f"⚠️ Data source is: {data_fetcher.get_data_source()}")
            print("💡 Market data API might not be configured correctly")
        
        # Test trading API
        try:
            from trading.schwab_trading import get_schwab_trading_client
            
            trading_client = get_schwab_trading_client(
                data_fetcher.schwab_trading_key, 
                data_fetcher.schwab_trading_secret, 
                use_mock=False
            )
            
            account_info = trading_client.get_account_info()
            if account_info:
                print("✅ Schwab Trading API is working!")
                print(f"📊 Account Balance: ${account_info.get('balance', 'N/A')}")
            else:
                print("⚠️ Trading API not working - check your credentials")
                
        except Exception as e:
            print(f"⚠️ Trading API test failed: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Options Scalping App - Schwab Credentials Setup")
    print("=" * 70)
    
    # Update credentials
    success = update_schwab_credentials()
    
    if success:
        # Test credentials
        test_credentials()
        
        print("\n📋 Next Steps:")
        print("1. Run: python3 test_schwab_live_data.py")
        print("2. Run: python3 main.py")
        print("3. Check the dashboard for live data and trading capabilities")
        
        print("\n💡 Important Notes:")
        print("- Market Data API: Required for real-time prices")
        print("- Trading API: Required for executing trades")
        print("- Both APIs need separate credentials from Schwab")
        print("- If you don't have credentials, the app will use Yahoo Finance for data")
        
    else:
        print("\n❌ Failed to update credentials")
        print("💡 Try editing config.json manually") 