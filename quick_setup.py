#!/usr/bin/env python3
"""
Quick Secure Setup Script
Completes the secure setup with provided API keys
"""

import os
import sys
import json
from pathlib import Path
from cryptography.fernet import Fernet
import base64

class QuickSetup:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_dir = self.project_root / "config"
        self.secure_config_file = self.config_dir / "secure_config.json"
        self.encryption_key_file = self.config_dir / ".secret_key"
        self.env_file = self.project_root / ".env"
        
        # Create necessary directories
        self.config_dir.mkdir(exist_ok=True)
        
        # Initialize encryption
        self.cipher_suite = self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize or load encryption key"""
        if self.encryption_key_file.exists():
            with open(self.encryption_key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.encryption_key_file, 'wb') as f:
                f.write(key)
            os.chmod(self.encryption_key_file, 0o600)
            print(f"🔑 Generated new encryption key: {self.encryption_key_file}")
        
        return Fernet(key)
    
    def encrypt_value(self, value):
        """Encrypt a string value"""
        if not value:
            return ""
        return self.cipher_suite.encrypt(value.encode()).decode()
    
    def setup_with_keys(self, client_id, client_secret, market_data_key=None, 
                       market_data_secret=None, trading_key=None, trading_secret=None):
        """Setup with provided API keys"""
        print("🔒 Setting up secure configuration with provided keys...")
        
        # Prepare API keys
        api_keys = {
            "SCHWAB_CLIENT_ID": client_id,
            "SCHWAB_CLIENT_SECRET": client_secret
        }
        
        if market_data_key:
            api_keys["SCHWAB_MARKET_DATA_KEY"] = market_data_key
        if market_data_secret:
            api_keys["SCHWAB_MARKET_DATA_SECRET"] = market_data_secret
        if trading_key:
            api_keys["SCHWAB_TRADING_KEY"] = trading_key
        if trading_secret:
            api_keys["SCHWAB_TRADING_SECRET"] = trading_secret
        
        # Save encrypted keys
        self._save_encrypted_keys(api_keys)
        self._create_env_file(api_keys)
        
        print("✅ Secure configuration completed!")
        return True
    
    def _save_encrypted_keys(self, api_keys):
        """Save API keys in encrypted format"""
        encrypted_config = {
            "api_keys": {},
            "metadata": {
                "created": str(Path().cwd()),
                "encrypted": True,
                "version": "1.0"
            }
        }
        
        for key_name, value in api_keys.items():
            encrypted_config["api_keys"][key_name] = self.encrypt_value(value)
        
        with open(self.secure_config_file, 'w') as f:
            json.dump(encrypted_config, f, indent=2)
        
        os.chmod(self.secure_config_file, 0o600)
        print(f"✅ Saved encrypted API keys to {self.secure_config_file}")
    
    def _create_env_file(self, api_keys):
        """Create .env file with API keys"""
        env_content = [
            "# Schwab API Configuration",
            "# This file contains your API keys - DO NOT COMMIT TO GIT",
            ""
        ]
        
        for key_name, value in api_keys.items():
            env_content.append(f"{key_name}={value}")
        
        env_content.extend([
            "",
            "# Application Settings",
            "DEBUG=False",
            "LOG_LEVEL=INFO",
            "STREAMLIT_SERVER_PORT=8501",
            "STREAMLIT_SERVER_ADDRESS=localhost"
        ])
        
        with open(self.env_file, 'w') as f:
            f.write('\n'.join(env_content))
        
        os.chmod(self.env_file, 0o600)
        print(f"✅ Created .env file with API keys")

def main():
    """Main function with provided keys"""
    if len(sys.argv) < 3:
        print("Usage: python3 quick_setup.py <client_id> <client_secret> [market_data_key] [market_data_secret] [trading_key] [trading_secret]")
        sys.exit(1)
    
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    
    # Optional keys
    market_data_key = sys.argv[3] if len(sys.argv) > 3 else None
    market_data_secret = sys.argv[4] if len(sys.argv) > 4 else None
    trading_key = sys.argv[5] if len(sys.argv) > 5 else None
    trading_secret = sys.argv[6] if len(sys.argv) > 6 else None
    
    try:
        setup = QuickSetup()
        setup.setup_with_keys(
            client_id, client_secret, 
            market_data_key, market_data_secret,
            trading_key, trading_secret
        )
        print("🎉 Setup completed successfully!")
        print("You can now run: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 