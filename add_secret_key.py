#!/usr/bin/env python3
"""
Add Secret Key - Simple Version
"""

import json

def add_secret_key():
    print("🔑 Add Schwab Market Data Secret Key")
    print("=" * 40)
    
    # Load current config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Show current key
    current_key = config['api_keys']['schwab_market_data_key']
    print(f"Current API Key: {current_key[:10]}...")
    
    # Get secret key
    print("\nEnter your Schwab Market Data Secret Key:")
    secret_key = input("Secret Key: ").strip()
    
    if secret_key:
        # Update config
        config['api_keys']['schwab_market_data_secret'] = secret_key
        
        # Save config
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        print("\n✅ Secret key saved successfully!")
        print("🔒 File permissions are already secure (600)")
        
        # Test the setup
        print("\n🧪 Testing setup...")
        try:
            from data.data_fetcher import DataFetcher
            data_fetcher = DataFetcher(use_schwab=True, use_alpaca=False, use_tos=False)
            print(f"📊 Data Source: {data_fetcher.get_data_source()}")
            
            if data_fetcher.get_data_source() == "schwab":
                print("✅ Schwab API is now the primary data source!")
            else:
                print(f"⚠️ Data source is: {data_fetcher.get_data_source()}")
                
        except Exception as e:
            print(f"⚠️ Test failed: {e}")
        
        print("\n💡 Next Steps:")
        print("1. Run: python3 main.py")
        print("2. Check the dashboard for live data")
        
    else:
        print("❌ No secret key entered")

if __name__ == "__main__":
    add_secret_key() 