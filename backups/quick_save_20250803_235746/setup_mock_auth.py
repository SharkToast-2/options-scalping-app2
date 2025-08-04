#!/usr/bin/env python3
"""
Setup Mock Authentication for Schwab Integration
This allows development to continue while OAuth 2.0 issues are resolved
"""

import json
import time

def setup_mock_authentication():
    print("🔧 Setting up Mock Authentication for Schwab Integration")
    print("=" * 60)
    
    # Mock authentication configuration
    mock_config = {
        'schwab_auth': {
            'access_token': 'mock_schwab_access_token_development',
            'refresh_token': 'mock_schwab_refresh_token_development',
            'timestamp': time.time(),
            'client_id': '1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj',
            'status': 'mock_authenticated',
            'note': 'Mock authentication for development - OAuth 2.0 issues being resolved'
        }
    }
    
    try:
        # Load existing config
        try:
            with open('config.json', 'r') as f:
                existing_config = json.load(f)
        except FileNotFoundError:
            existing_config = {}
        
        # Update with mock authentication
        existing_config.update(mock_config)
        
        # Save updated config
        with open('config.json', 'w') as f:
            json.dump(existing_config, f, indent=2)
        
        print("✅ Mock authentication configured successfully!")
        print("📋 Configuration saved to config.json")
        
        # Test the configuration
        print("\n🧪 Testing mock configuration...")
        try:
            with open('config.json', 'r') as f:
                test_config = json.load(f)
            
            if 'schwab_auth' in test_config:
                auth_config = test_config['schwab_auth']
                print(f"🔑 Access Token: {auth_config.get('access_token', 'Not found')}")
                print(f"🔄 Refresh Token: {auth_config.get('refresh_token', 'Not found')}")
                print(f"📅 Timestamp: {auth_config.get('timestamp', 'Not found')}")
                print(f"🔐 Status: {auth_config.get('status', 'Not found')}")
                print("✅ Mock configuration test successful!")
            else:
                print("❌ Mock configuration not found in config.json")
                
        except Exception as e:
            print(f"❌ Error testing configuration: {e}")
        
        print("\n🎉 Mock authentication setup complete!")
        print("📋 You can now:")
        print("1. Use the Schwab integration functions")
        print("2. Test the trading application")
        print("3. Continue development while OAuth 2.0 issues are resolved")
        print("4. The app will use mock data for Schwab API calls")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up mock authentication: {e}")
        return False

def test_mock_integration():
    """Test the mock integration"""
    print("\n🧪 Testing Mock Integration...")
    
    try:
        # Test importing and using the trade executor
        from modules.trade_executor import get_account_info, get_quote, place_order
        
        print("✅ Successfully imported trade executor functions")
        
        # Test account info
        account_info = get_account_info()
        print(f"📊 Account Info: {account_info}")
        
        # Test quote
        quote = get_quote("AAPL")
        print(f"📈 AAPL Quote: {quote}")
        
        # Test order placement (mock)
        order = place_order("AAPL", 1, "buy", "market")
        print(f"📋 Order Result: {order}")
        
        print("✅ Mock integration test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing mock integration: {e}")
        return False

def main():
    print("🔧 Schwab Mock Authentication Setup")
    print("=" * 40)
    print("This will set up mock authentication to allow development")
    print("to continue while OAuth 2.0 issues are resolved.")
    print()
    
    # Set up mock authentication
    success = setup_mock_authentication()
    
    if success:
        # Test the integration
        test_mock_integration()
        
        print("\n🎯 Next Steps:")
        print("1. Your app is now configured with mock authentication")
        print("2. You can run the Streamlit app and test all features")
        print("3. The Schwab integration will use mock data")
        print("4. Continue development while resolving OAuth 2.0 issues")
        print("5. When OAuth 2.0 is working, replace mock with real authentication")
        
        print("\n🚀 Ready to continue development!")
        
    else:
        print("\n❌ Failed to set up mock authentication")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main() 