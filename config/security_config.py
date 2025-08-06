#!/usr/bin/env python3
"""
Security Configuration Module
Handles encryption, validation, and security settings
"""

import os
import base64
import hashlib
import hmac
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re
import json
from datetime import datetime, timedelta

class SecurityManager:
    def __init__(self):
        self.secret_key = self._get_or_create_secret_key()
        self.cipher_suite = Fernet(self.secret_key)
        self.max_login_attempts = 3
        self.session_timeout = timedelta(hours=1)
        
    def _get_or_create_secret_key(self):
        """Get or create encryption key"""
        key_file = "config/.secret_key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        try:
            decrypted = self.cipher_suite.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception as e:
            print(f"❌ Decryption error: {e}")
            return None
    
    def hash_password(self, password):
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hash_obj.hex()}"
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        try:
            salt, hash_hex = hashed_password.split('$')
            hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return hmac.compare_digest(hash_obj.hex(), hash_hex)
        except Exception:
            return False
    
    def validate_api_key(self, api_key):
        """Validate API key format"""
        if not api_key:
            return False
        
        # Check length and format
        if len(api_key) < 20:
            return False
        
        # Check for common patterns
        if re.match(r'^[A-Za-z0-9_-]+$', api_key):
            return True
        
        return False
    
    def validate_ticker(self, ticker):
        """Validate stock ticker format"""
        if not ticker:
            return False
        
        # Check format (1-5 letters, uppercase)
        if re.match(r'^[A-Z]{1,5}$', ticker):
            return True
        
        return False
    
    def validate_trade_size(self, trade_size):
        """Validate trade size"""
        try:
            size = float(trade_size)
            return 0 < size <= 10000  # Max $10,000 per trade
        except (ValueError, TypeError):
            return False
    
    def sanitize_input(self, input_str):
        """Sanitize user input"""
        if not input_str:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', str(input_str))
        return sanitized.strip()
    
    def generate_session_token(self):
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def validate_session(self, token, timestamp):
        """Validate session token and timestamp"""
        try:
            session_time = datetime.fromisoformat(timestamp)
            if datetime.now() - session_time > self.session_timeout:
                return False
            return True
        except Exception:
            return False
    
    def log_security_event(self, event_type, details, user_id=None):
        """Log security events"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details,
            'user_id': user_id,
            'ip_address': '127.0.0.1'  # In production, get real IP
        }
        
        security_log_file = "logs/security_events.json"
        os.makedirs(os.path.dirname(security_log_file), exist_ok=True)
        
        try:
            logs = []
            if os.path.exists(security_log_file):
                with open(security_log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(security_log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error logging security event: {e}")
    
    def check_rate_limit(self, user_id, action_type):
        """Check rate limiting for actions"""
        # Simple rate limiting - in production, use Redis or similar
        rate_limits = {
            'login': 5,  # 5 attempts per minute
            'trade': 10,  # 10 trades per minute
            'api_call': 100  # 100 API calls per minute
        }
        
        # For now, return True (implement proper rate limiting in production)
        return True
    
    def encrypt_credentials(self, credentials):
        """Encrypt API credentials"""
        encrypted_creds = {}
        
        for key, value in credentials.items():
            if value:
                encrypted_creds[key] = self.encrypt_data(value).decode()
        
        return encrypted_creds
    
    def decrypt_credentials(self, encrypted_credentials):
        """Decrypt API credentials"""
        decrypted_creds = {}
        
        for key, encrypted_value in encrypted_credentials.items():
            if encrypted_value:
                decrypted_value = self.decrypt_data(encrypted_value.encode())
                if decrypted_value:
                    decrypted_creds[key] = decrypted_value
        
        return decrypted_creds

# Global security manager instance
security_manager = SecurityManager()

def get_security_manager():
    """Get security manager instance"""
    return security_manager

def validate_config(config):
    """Validate configuration security"""
    required_fields = ['schwab_client_id', 'schwab_client_secret']
    
    for field in required_fields:
        if field not in config or not config[field]:
            return False, f"Missing required field: {field}"
        
        if not security_manager.validate_api_key(config[field]):
            return False, f"Invalid API key format: {field}"
    
    return True, "Configuration valid"

def secure_config_load():
    """Securely load configuration"""
    try:
        # Load encrypted config
        config_file = "config/secure_config.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                encrypted_config = json.load(f)
            
            # Decrypt configuration
            config = security_manager.decrypt_credentials(encrypted_config)
            
            # Validate configuration
            is_valid, message = validate_config(config)
            if not is_valid:
                print(f"❌ Configuration validation failed: {message}")
                return None
            
            return config
        else:
            print("⚠️ No secure configuration found")
            return None
            
    except Exception as e:
        print(f"❌ Error loading secure configuration: {e}")
        return None

def secure_config_save(config):
    """Securely save configuration"""
    try:
        # Encrypt configuration
        encrypted_config = security_manager.encrypt_credentials(config)
        
        # Save encrypted config
        config_file = "config/secure_config.json"
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(encrypted_config, f, indent=2)
        
        print("✅ Configuration saved securely")
        return True
        
    except Exception as e:
        print(f"❌ Error saving secure configuration: {e}")
        return False 