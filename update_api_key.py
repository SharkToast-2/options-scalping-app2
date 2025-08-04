#!/usr/bin/env python3
"""
Simple script to update your Schwab API key
"""

import json
import os

def update_schwab_api_key():
    """Update Schwab API key in config.json"""
    
    print("🔧 Schwab API Key Update Tool")
    print("=" * 40)
    
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
    
    # Show current key
    current_key = config.get('api_keys', {}).get('schwab', '')
    print(f"📋 Current Schwab API Key: {current_key}")
    
    if current_key and current_key != "YOUR_ACTUAL_SCHWAB_API_KEY_HERE" and current_key != "your_schwab_api_key_here":
        print("✅ You already have a Schwab API key configured!")
        response = input("Do you want to update it? (y/n): ").lower()
        if response != 'y':
            print("👋 No changes made")
            return True
    
    # Get new API key
    print("\n🔑 Enter your Schwab API key:")
    print("💡 If you don't have one, press Enter to skip")
    new_key = input("API Key: ").strip()
    
    if not new_key:
        print("⚠️ No API key entered. Keeping current configuration.")
        return True
    
    # Update config
    config['api_keys']['schwab'] = new_key
    
    # Save config
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("✅ API key updated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False

def test_connection():
    """Test the API connection after update"""
    print("\n🧪 Testing API connection...")
    
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
                print("⚠️ API key updated but no live data received")
                print("💡 This might be normal if markets are closed")
                return True
        else:
            print(f"⚠️ Data source is: {data_fetcher.get_data_source()}")
            print("💡 Schwab API might not be available or configured correctly")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Options Scalping App - API Key Update")
    print("=" * 50)
    
    # Update API key
    success = update_schwab_api_key()
    
    if success:
        # Test connection
        test_connection()
        
        print("\n📋 Next Steps:")
        print("1. Run: python3 test_schwab_live_data.py")
        print("2. Run: python3 main.py")
        print("3. Check the dashboard for live data")
        
        print("\n💡 If you don't have a Schwab API key:")
        print("- The app will automatically use Yahoo Finance")
        print("- Check SCHWAB_API_SETUP_GUIDE.md for alternatives")
    else:
        print("\n❌ Failed to update API key")
        print("💡 Try editing config.json manually") 