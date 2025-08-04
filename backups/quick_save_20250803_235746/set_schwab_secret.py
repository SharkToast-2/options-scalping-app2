#!/usr/bin/env python3
"""
Set Schwab Client Secret and Complete Authentication
"""

import os
import sys

def set_client_secret():
    print("🔐 Setting Schwab Client Secret...")
    print("Please enter your Schwab client secret:")
    
    # For security, we'll use getpass to hide the input
    try:
        import getpass
        client_secret = getpass.getpass("Client Secret: ")
    except ImportError:
        client_secret = input("Client Secret: ")
    
    if not client_secret:
        print("❌ No client secret provided")
        return False
    
    # Set environment variable
    os.environ['SCHWAB_CLIENT_SECRET'] = client_secret
    print("✅ Client secret set as environment variable")
    
    # Now complete the authentication
    print("\n🔄 Completing authentication...")
    try:
        from complete_schwab_auth import complete_authentication
        return complete_authentication()
    except ImportError:
        print("❌ Could not import complete_schwab_auth module")
        return False

if __name__ == "__main__":
    success = set_client_secret()
    if success:
        print("\n🎉 Schwab authentication completed successfully!")
        print("You can now use the Schwab API in your application.")
    else:
        print("\n❌ Authentication failed. Please check your credentials.")
        sys.exit(1) 