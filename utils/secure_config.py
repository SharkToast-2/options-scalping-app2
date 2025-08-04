#!/usr/bin/env python3
"""
Secure Configuration Manager
Handles API keys and sensitive data securely
"""

import os
import json
import logging
from typing import Dict, Optional
from cryptography.fernet import Fernet
import base64

logger = logging.getLogger(__name__)

class SecureConfig:
    """Secure configuration manager for API keys and sensitive data"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.encryption_key = None
        self._load_encryption_key()
    
    def _load_encryption_key(self):
        """Load or generate encryption key"""
        key_file = ".encryption_key"
        
        if os.path.exists(key_file):
            # Load existing key
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Generate new key
            self.encryption_key = Fernet.generate_key()
            # Save key securely
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            # Set restrictive permissions
            os.chmod(key_file, 0o600)
    
    def _encrypt_value(self, value: str) -> str:
        """Encrypt a string value"""
        if not value or value.startswith("your_") or value == "":
            return value
        
        f = Fernet(self.encryption_key)
        encrypted = f.encrypt(value.encode())
        return base64.b64encode(encrypted).decode()
    
    def _decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt a string value"""
        if not encrypted_value or encrypted_value.startswith("your_") or encrypted_value == "":
            return encrypted_value
        
        try:
            f = Fernet(self.encryption_key)
            decoded = base64.b64decode(encrypted_value.encode())
            decrypted = f.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            logger.warning(f"Failed to decrypt value: {e}")
            return encrypted_value
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """Get API key from environment variable or config file"""
        
        # First, try environment variable
        env_var = f"SCHWAB_{key_name.upper()}"
        env_value = os.getenv(env_var)
        if env_value:
            logger.info(f"Using {key_name} from environment variable")
            return env_value
        
        # Fallback to config file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                api_keys = config.get('api_keys', {})
                encrypted_value = api_keys.get(key_name, '')
                
                if encrypted_value:
                    decrypted_value = self._decrypt_value(encrypted_value)
                    if decrypted_value and not decrypted_value.startswith("your_"):
                        return decrypted_value
                        
            except Exception as e:
                logger.error(f"Error reading config file: {e}")
        
        return None
    
    def save_api_key(self, key_name: str, value: str):
        """Save API key to config file (encrypted)"""
        
        if not os.path.exists(self.config_file):
            # Create from example if it doesn't exist
            example_file = "config_example.json"
            if os.path.exists(example_file):
                with open(example_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {"api_keys": {}}
        else:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        
        # Encrypt the value
        encrypted_value = self._encrypt_value(value)
        
        # Update config
        if 'api_keys' not in config:
            config['api_keys'] = {}
        
        config['api_keys'][key_name] = encrypted_value
        
        # Save config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        # Set restrictive permissions
        os.chmod(self.config_file, 0o600)
        
        logger.info(f"Saved encrypted {key_name} to config file")
    
    def get_all_api_keys(self) -> Dict[str, str]:
        """Get all API keys"""
        keys = {}
        
        # Common API key names
        key_names = [
            'schwab_market_data_key',
            'schwab_market_data_secret',
            'schwab_trading_key',
            'schwab_trading_secret',
            'alpaca_api_key',
            'alpaca_secret_key',
            'news_api_key',
            'alpha_vantage',
            'polygon',
            'finnhub'
        ]
        
        for key_name in key_names:
            value = self.get_api_key(key_name)
            if value:
                keys[key_name] = value
        
        return keys
    
    def validate_security(self) -> Dict[str, bool]:
        """Validate security settings"""
        security_report = {
            'config_file_exists': os.path.exists(self.config_file),
            'config_file_secure': False,
            'encryption_key_exists': os.path.exists('.encryption_key'),
            'encryption_key_secure': False,
            'environment_variables_used': False
        }
        
        # Check file permissions
        if security_report['config_file_exists']:
            try:
                stat = os.stat(self.config_file)
                security_report['config_file_secure'] = (stat.st_mode & 0o777) == 0o600
            except Exception:
                pass
        
        if security_report['encryption_key_exists']:
            try:
                stat = os.stat('.encryption_key')
                security_report['encryption_key_secure'] = (stat.st_mode & 0o777) == 0o600
            except Exception:
                pass
        
        # Check if environment variables are used
        env_vars = ['SCHWAB_MARKET_DATA_KEY', 'SCHWAB_MARKET_DATA_SECRET', 
                   'SCHWAB_TRADING_KEY', 'SCHWAB_TRADING_SECRET']
        security_report['environment_variables_used'] = any(os.getenv(var) for var in env_vars)
        
        return security_report

def create_secure_config():
    """Create a secure configuration setup"""
    
    print("🔒 Setting up Secure Configuration")
    print("=" * 50)
    
    # Check if config.json exists
    if os.path.exists('config.json'):
        print("⚠️  config.json already exists!")
        response = input("Do you want to encrypt existing keys? (y/n): ").lower()
        if response != 'y':
            print("👋 No changes made")
            return
    
    secure_config = SecureConfig()
    
    # Get API keys from user
    print("\n🔑 Enter your API keys (press Enter to skip):")
    
    keys_to_get = [
        ('schwab_market_data_key', 'Schwab Market Data API Key'),
        ('schwab_market_data_secret', 'Schwab Market Data Secret'),
        ('schwab_trading_key', 'Schwab Trading API Key'),
        ('schwab_trading_secret', 'Schwab Trading Secret'),
        ('alpaca_api_key', 'Alpaca API Key'),
        ('alpaca_secret_key', 'Alpaca Secret Key'),
        ('news_api_key', 'News API Key'),
        ('alpha_vantage', 'Alpha Vantage API Key')
    ]
    
    for key_name, display_name in keys_to_get:
        value = input(f"{display_name}: ").strip()
        if value:
            secure_config.save_api_key(key_name, value)
    
    # Validate security
    security_report = secure_config.validate_security()
    
    print("\n🔒 Security Report:")
    print("=" * 30)
    for check, status in security_report.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check.replace('_', ' ').title()}")
    
    print("\n💡 Security Recommendations:")
    print("1. Use environment variables for production")
    print("2. Never commit config.json to version control")
    print("3. Regularly rotate your API keys")
    print("4. Use a dedicated trading account with limited funds")

if __name__ == "__main__":
    create_secure_config() 