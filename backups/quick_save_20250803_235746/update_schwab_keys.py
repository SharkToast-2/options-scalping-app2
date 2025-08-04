#!/usr/bin/env python3
"""
Update Schwab API key and secret key
"""

import json
import os

def update_schwab_credentials():
    """Update Schwab API key and secret key in config.json"""
    
    print("🔧 Schwab API Credentials Update Tool")
    print("=" * 50)
    
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
    current_api_key = config.get('api_keys', {}).get('schwab_api_key', '')
    current_secret_key = config.get('api_keys', {}).get('schwab_secret_key', '')
    
    print(f"📋 Current Schwab API Key: {current_api_key[:10]}..." if len(current_api_key) > 10 else "Not set")
    print(f"📋 Current Schwab Secret Key: {current_secret_key[:10]}..." if len(current_secret_key) > 10 else "Not set")
    
    # Check if both keys are already configured
    if (current_api_key and current_api_key != "your_schwab_api_key_here" and 
        current_secret_key and current_secret_key != "your_schwab_secret_key_here"):
        print("✅ You already have both Schwab API key and secret key configured!")
        response = input("Do you want to update them? (y/n): ").lower()
        if response != 'y':
            print("👋 No changes made")
            return True
    
    # Get new API key
    print("\n🔑 Enter your Schwab API key:")
    print("💡 If you don't have one, press Enter to skip")
    new_api_key = input("API Key: ").strip()
    
    # Get new secret key
    print("\n🔑 Enter your Schwab Secret key:")
    print("💡 If you don't have one, press Enter to skip")
    new_secret_key = input("Secret Key: ").strip()
    
    # Update config
    if new_api_key:
        config['api_keys']['schwab_api_key'] = new_api_key
    if new_secret_key:
        config['api_keys']['schwab_secret_key'] = new_secret_key
    
    # Save config
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("✅ Credentials updated successfully!")
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
        
        if data_fetcher.get_data_source() == "schwab":
            print("✅ Schwab API is now the primary data source")
            
            # Test with a simple quote
            quote = data_fetcher.get_real_time_quote("AAPL")
            if quote:
                print(f"✅ Live data working! AAPL: ${quote.get('price', 'N/A')}")
                return True
            else:
                print("⚠️ Credentials updated but no live data received")
                print("💡 This might be normal if markets are closed")
                return True
        else:
            print(f"⚠️ Data source is: {data_fetcher.get_data_source()}")
            print("💡 Schwab API might not be available or configured correctly")
            return False
            
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Options Scalping App - Schwab Credentials Update")
    print("=" * 60)
    
    # Update credentials
    success = update_schwab_credentials()
    
    if success:
        # Test credentials
        test_credentials()
        
        print("\n📋 Next Steps:")
        print("1. Run: python3 test_schwab_live_data.py")
        print("2. Run: python3 main.py")
        print("3. Check the dashboard for live data")
        
        print("\n💡 If you don't have Schwab API credentials:")
        print("- The app will automatically use Yahoo Finance")
        print("- Check SCHWAB_API_SETUP_GUIDE.md for alternatives")
    else:
        print("\n❌ Failed to update credentials")
        print("💡 Try editing config.json manually") 