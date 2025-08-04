#!/usr/bin/env python3
"""
Enter Schwab Client Secret Securely
"""

import getpass
import os

def enter_client_secret():
    print("🔐 Schwab Client Secret Entry")
    print("=" * 40)
    print("Please enter your Schwab client secret:")
    print("(The input will be hidden for security)")
    
    client_secret = getpass.getpass("Client Secret: ")
    
    if not client_secret:
        print("❌ No client secret provided")
        return None
    
    print(f"✅ Client secret received (length: {len(client_secret)})")
    
    # Set as environment variable
    os.environ['SCHWAB_CLIENT_SECRET'] = client_secret
    print("💾 Client secret set as environment variable")
    
    return client_secret

if __name__ == "__main__":
    secret = enter_client_secret()
    if secret:
        print("\n🎉 Client secret configured successfully!")
        print("You can now run the authentication script.")
    else:
        print("\n❌ Failed to configure client secret.") 