import os
import json
import requests
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
from dotenv import load_dotenv

# Load Schwab API credentials from .env
load_dotenv("config/.env")

SCHWAB_CLIENT_ID = os.getenv("SCHWAB_CLIENT_ID")
SCHWAB_CLIENT_SECRET = os.getenv("SCHWAB_CLIENT_SECRET")
SCHWAB_REDIRECT_URI = os.getenv("SCHWAB_REDIRECT_URI")
AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
TOKEN_FILE = "config/schwab_tokens.json"

def get_authorization_url():
    params = {
        "response_type": "code",
        "client_id": SCHWAB_CLIENT_ID,
        "redirect_uri": SCHWAB_REDIRECT_URI,
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def save_tokens(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"\n✅ Access & refresh tokens saved to {TOKEN_FILE}\n")

def request_tokens(auth_code):
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": SCHWAB_REDIRECT_URI,
        "client_id": SCHWAB_CLIENT_ID,
        "client_secret": SCHWAB_CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    return response.json()

def main():
    print("🔐 Schwab OAuth Authorization\n")

    auth_url = get_authorization_url()
    print("Opening browser to log in with Schwab...")
    webbrowser.open(auth_url)

    print("After logging in, copy the FULL redirect URL (it contains the ?code=...)")
    
    # Get redirect URL with validation
    while True:
        redirect_url = input("Paste redirect URL here: ").strip()
        
        # Validate URL format
        if not redirect_url:
            print("❌ URL cannot be empty. Please try again.")
            continue
            
        if not redirect_url.startswith(('http://', 'https://')):
            print("❌ Invalid URL format. Please enter a valid URL.")
            continue
            
        if 'code=' not in redirect_url:
            print("❌ URL doesn't contain authorization code. Please check the URL.")
            continue
            
        break

    # Extract ?code= from URL
    parsed = urlparse(redirect_url)
    code = parse_qs(parsed.query).get("code")
    if not code:
        raise Exception("Authorization code not found in redirect URL.")

    token_data = request_tokens(code[0])
    save_tokens(token_data)
    print("🎉 Authentication complete.")

if __name__ == "__main__":
    main() 