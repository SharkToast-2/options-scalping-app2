#!/usr/bin/env python3
"""
Simple API Key Entry Tool
"""

import json
import os

def enter_api_keys():
    """Manually enter API keys"""
    
    print("🔑 API Key Entry Tool")
    print("=" * 40)
    print("Enter your API keys below (press Enter to skip)")
    print()
    
    # Load existing config or create new one
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
    else:
        config = {"api_keys": {}}
    
    # Get API keys from user
    print("📊 SCHWAB MARKET DATA API")
    print("-" * 30)
    
    current_market_key = config.get('api_keys', {}).get('schwab_market_data_key', '')
    if current_market_key and not current_market_key.startswith('your_'):
        print(f"Current Market Data Key: {current_market_key[:10]}...")
    
    market_key = input("Market Data API Key: ").strip()
    if market_key:
        config['api_keys']['schwab_market_data_key'] = market_key
    
    market_secret = input("Market Data Secret Key: ").strip()
    if market_secret:
        config['api_keys']['schwab_market_data_secret'] = market_secret
    
    print()
    print("🚀 SCHWAB TRADING API")
    print("-" * 30)
    
    current_trading_key = config.get('api_keys', {}).get('schwab_trading_key', '')
    if current_trading_key and not current_trading_key.startswith('your_'):
        print(f"Current Trading Key: {current_trading_key[:10]}...")
    
    trading_key = input("Trading API Key: ").strip()
    if trading_key:
        config['api_keys']['schwab_trading_key'] = trading_key
    
    trading_secret = input("Trading Secret Key: ").strip()
    if trading_secret:
        config['api_keys']['schwab_trading_secret'] = trading_secret
    
    print()
    print("📈 OTHER APIs")
    print("-" * 30)
    
    alpaca_key = input("Alpaca API Key: ").strip()
    if alpaca_key:
        config['api_keys']['alpaca_api_key'] = alpaca_key
    
    alpaca_secret = input("Alpaca Secret Key: ").strip()
    if alpaca_secret:
        config['api_keys']['alpaca_secret_key'] = alpaca_secret
    
    news_key = input("News API Key: ").strip()
    if news_key:
        config['api_keys']['news_api_key'] = news_key
    
    alpha_key = input("Alpha Vantage API Key: ").strip()
    if alpha_key:
        config['api_keys']['alpha_vantage'] = alpha_key
    
    # Save config
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    # Set secure permissions
    os.chmod('config.json', 0o600)
    
    print()
    print("✅ API keys saved successfully!")
    print("📁 File permissions set to secure (600)")
    
    # Show what was saved
    print()
    print("📋 Saved Keys:")
    print("-" * 20)
    
    api_keys = config.get('api_keys', {})
    for key, value in api_keys.items():
        if value and not value.startswith('your_'):
            masked_value = value[:4] + '***' + value[-4:] if len(value) > 8 else '***'
            print(f"✅ {key}: {masked_value}")
        else:
            print(f"📄 {key}: Not set")
    
    print()
    print("💡 Next Steps:")
    print("1. Run: python3 test_schwab_live_data.py")
    print("2. Run: python3 main.py")
    print("3. Check the dashboard for live data")

if __name__ == "__main__":
    enter_api_keys() 