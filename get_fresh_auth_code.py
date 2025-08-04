#!/usr/bin/env python3
"""
Get Fresh Authorization Code from Schwab OAuth 2.0
"""

import webbrowser
import time

def get_fresh_auth_code():
    print("🔐 Getting Fresh Authorization Code from Schwab")
    print("=" * 50)
    
    # Schwab OAuth 2.0 Configuration
    client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"
    redirect_uri = "https://developer.schwab.com/oauth2-redirect.html"
    auth_url = "https://api.schwabapi.com/v1/oauth/authorize"
    
    # Construct authorization URL
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': 'readonly',
        'redirect_uri': redirect_uri
    }
    
    auth_url_full = f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in auth_params.items()])}"
    
    print(f"🔑 Client ID: {client_id}")
    print(f"🔗 Redirect URI: {redirect_uri}")
    print(f"📡 Auth URL: {auth_url_full}")
    
    print("\n📱 Opening browser for authorization...")
    print("📋 Please authorize the application and copy the redirect URL.")
    
    try:
        webbrowser.open(auth_url_full)
        print("🌐 Browser opened to Schwab authorization page.")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print(f"🔗 Please manually visit: {auth_url_full}")
    
    print("\n📋 After authorization, you'll be redirected to a URL like:")
    print("https://developer.schwab.com/oauth2-redirect.html?code=YOUR_AUTH_CODE&session=...")
    print("\n📝 Please copy and paste the entire redirect URL here:")
    
    redirect_url = input("Redirect URL: ").strip()
    
    if not redirect_url:
        print("❌ No redirect URL provided")
        return None
    
    # Extract authorization code
    try:
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' in query_params:
            auth_code = query_params['code'][0]
            print(f"\n✅ Authorization code extracted: {auth_code[:20]}...")
            return auth_code
        else:
            print("❌ No authorization code found in URL")
            return None
            
    except Exception as e:
        print(f"❌ Error parsing redirect URL: {e}")
        return None

def main():
    auth_code = get_fresh_auth_code()
    
    if auth_code:
        print(f"\n🎉 Fresh authorization code obtained!")
        print(f"🎫 Auth Code: {auth_code}")
        print("\n📋 You can now use this code with the OAuth 2.0 authentication script.")
        
        # Save the auth code to a file for easy access
        with open('fresh_auth_code.txt', 'w') as f:
            f.write(auth_code)
        print("💾 Authorization code saved to fresh_auth_code.txt")
        
    else:
        print("\n❌ Failed to get authorization code")

if __name__ == "__main__":
    main() 