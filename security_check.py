#!/usr/bin/env python3
"""
Security Audit Script
Checks the security status of the options scalping bot
"""

import os
import json
import hashlib
from datetime import datetime
from config.security_config import get_security_manager

def check_file_permissions():
    """Check file permissions for security"""
    print("🔍 Checking file permissions...")
    
    sensitive_files = [
        "config/.secret_key",
        "config/secure_config.json",
        "config/schwab_tokens.json",
        "logs/security_events.json"
    ]
    
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            # Check if file is readable only by owner
            stat = os.stat(file_path)
            mode = stat.st_mode & 0o777
            
            if mode == 0o600:  # Owner read/write only
                print(f"✅ {file_path}: Secure permissions (600)")
            else:
                print(f"⚠️ {file_path}: Insecure permissions ({oct(mode)})")
        else:
            print(f"ℹ️ {file_path}: File not found (OK if not created yet)")

def check_environment_security():
    """Check environment security"""
    print("\n🔍 Checking environment security...")
    
    # Check for environment variables
    env_vars = [
        "SCHWAB_CLIENT_ID",
        "SCHWAB_CLIENT_SECRET",
        "SCHWAB_REDIRECT_URI"
    ]
    
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ {var}: Set")
        else:
            print(f"ℹ️ {var}: Not set (will use config file)")

def check_dependencies():
    """Check for security-related dependencies"""
    print("\n🔍 Checking dependencies...")
    
    try:
        import cryptography
        print("✅ cryptography: Installed")
    except ImportError:
        print("❌ cryptography: Not installed")
    
    try:
        import secrets
        print("✅ secrets: Available")
    except ImportError:
        print("❌ secrets: Not available")
    
    try:
        import hashlib
        print("✅ hashlib: Available")
    except ImportError:
        print("❌ hashlib: Not available")

def check_configuration_security():
    """Check configuration security"""
    print("\n🔍 Checking configuration security...")
    
    security_manager = get_security_manager()
    
    # Test encryption/decryption
    test_data = "test_secret_data"
    encrypted = security_manager.encrypt_data(test_data)
    decrypted = security_manager.decrypt_data(encrypted)
    
    if decrypted == test_data:
        print("✅ Encryption/Decryption: Working")
    else:
        print("❌ Encryption/Decryption: Failed")
    
    # Test input validation
    test_cases = [
        ("META", True),  # Valid ticker
        ("INVALID", False),  # Invalid ticker
        ("", False),  # Empty ticker
        ("123", False),  # Numeric ticker
    ]
    
    for ticker, expected in test_cases:
        result = security_manager.validate_ticker(ticker)
        if result == expected:
            print(f"✅ Ticker validation '{ticker}': {'Valid' if expected else 'Invalid'}")
        else:
            print(f"❌ Ticker validation '{ticker}': Expected {expected}, got {result}")

def check_logging_security():
    """Check logging security"""
    print("\n🔍 Checking logging security...")
    
    # Check if logs directory exists
    if os.path.exists("logs"):
        print("✅ Logs directory: Exists")
    else:
        print("ℹ️ Logs directory: Not created yet")
    
    # Test security event logging
    security_manager = get_security_manager()
    security_manager.log_security_event("security_audit", "Security audit test", "audit_script")
    print("✅ Security event logging: Working")

def generate_security_report():
    """Generate security report"""
    print("\n📋 Generating security report...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "security_checks": {
            "file_permissions": "Checked",
            "environment": "Checked",
            "dependencies": "Checked",
            "configuration": "Checked",
            "logging": "Checked"
        },
        "recommendations": [
            "Keep dependencies updated",
            "Use strong passwords",
            "Enable two-factor authentication",
            "Regularly review logs",
            "Monitor for suspicious activity"
        ]
    }
    
    # Save report
    with open("security_audit_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Security report saved to security_audit_report.json")

def main():
    """Run security audit"""
    print("🔒 Security Audit for Options Scalping Bot")
    print("=" * 50)
    
    check_file_permissions()
    check_environment_security()
    check_dependencies()
    check_configuration_security()
    check_logging_security()
    generate_security_report()
    
    print("\n" + "=" * 50)
    print("✅ Security audit completed!")
    print("📋 Review the security_audit_report.json for details")

if __name__ == "__main__":
    main() 