#!/usr/bin/env python3
"""
ThinkOrSwim Authentication Setup Script
"""

import os
import json
from oauth_callback import authenticate_tos, TOSOAuthHandler

def setup_tos_authentication():
    """Interactive setup for ThinkOrSwim authentication"""
    
    print("🚀 ThinkOrSwim API Authentication Setup")
    print("=" * 50)
    
    # Check if we already have tokens
    if os.path.exists("tos_tokens.json"):
        print("📄 Found existing tokens file")
        oauth_handler = TOSOAuthHandler("")
        oauth_handler.load_tokens()
        
        if oauth_handler.is_token_valid():
            print("✅ Existing tokens are valid!")
            return oauth_handler
        else:
            print("⚠️  Existing tokens are expired")
    
    print("\n📋 Setup Instructions:")
    print("1. Go to https://developer.tdameritrade.com/")
    print("2. Create a developer account")
    print("3. Create a new application")
    print("4. Set the callback URL to: http://localhost:8080/callback")
    print("5. Copy your Client ID")
    
    print("\n🔧 Configuration:")
    
    # Get client ID
    client_id = input("Enter your Client ID: ").strip()
    
    if not client_id:
        print("❌ Client ID is required")
        return None
    
    # Save client ID to config
    config = {
        "client_id": client_id,
        "redirect_uri": "http://localhost:8080/callback"
    }
    
    with open("tos_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to tos_config.json")
    
    # Start authentication
    print(f"\n🔐 Starting OAuth authentication...")
    print(f"📡 Callback URL: {config['redirect_uri']}")
    
    oauth_handler = authenticate_tos(client_id)
    
    if oauth_handler:
        print("\n🎉 Authentication successful!")
        print("✅ Tokens saved to tos_tokens.json")
        return oauth_handler
    else:
        print("\n❌ Authentication failed")
        return None

def test_authentication():
    """Test the authentication"""
    print("\n🧪 Testing authentication...")
    
    try:
        oauth_handler = TOSOAuthHandler("")
        oauth_handler.load_tokens()
        
        if oauth_handler.is_token_valid():
            print("✅ Authentication test passed!")
            print(f"🔑 Access Token: {oauth_handler.access_token[:20]}...")
            print(f"⏰ Expires: {oauth_handler.expires_at}")
            return True
        else:
            print("❌ Authentication test failed - tokens invalid")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
        return False

if __name__ == "__main__":
    print("ThinkOrSwim API Setup")
    print("=" * 30)
    
    # Run setup
    oauth_handler = setup_tos_authentication()
    
    if oauth_handler:
        # Test authentication
        test_authentication()
        
        print("\n📋 Next Steps:")
        print("1. Update tos_config.py with your client_id")
        print("2. Set use_real_api = True in tos_config.py")
        print("3. Run your options scalping application")
        
        print("\n🎯 Your callback URL is: http://localhost:8080/callback")
        print("   Make sure this is set in your TD Ameritrade developer app!")
    else:
        print("\n❌ Setup failed. Please try again.") 