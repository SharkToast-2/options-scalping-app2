#!/usr/bin/env python3
"""
Security Audit for Options Scalping App
"""

import os
import json
import stat
from datetime import datetime

def check_file_permissions(file_path: str) -> dict:
    """Check file permissions"""
    try:
        st = os.stat(file_path)
        mode = st.st_mode
        return {
            'exists': True,
            'permissions': oct(mode & 0o777),
            'owner_readable': bool(mode & stat.S_IRUSR),
            'owner_writable': bool(mode & stat.S_IWUSR),
            'others_readable': bool(mode & stat.S_IROTH),
            'others_writable': bool(mode & stat.S_IWOTH),
            'secure': (mode & 0o777) == 0o600
        }
    except FileNotFoundError:
        return {'exists': False}
    except Exception as e:
        return {'exists': False, 'error': str(e)}

def check_git_status():
    """Check if sensitive files are tracked by git"""
    sensitive_files = [
        'config.json',
        '.env',
        '.encryption_key',
        'tos_tokens.json'
    ]
    
    git_status = {}
    for file in sensitive_files:
        if os.path.exists(file):
            # Check if file is tracked by git
            try:
                import subprocess
                result = subprocess.run(['git', 'status', '--porcelain', file], 
                                      capture_output=True, text=True)
                git_status[file] = {
                    'exists': True,
                    'tracked': result.stdout.strip() != '',
                    'status': result.stdout.strip() if result.stdout.strip() else 'untracked'
                }
            except Exception:
                git_status[file] = {'exists': True, 'tracked': 'unknown'}
        else:
            git_status[file] = {'exists': False}
    
    return git_status

def check_environment_variables():
    """Check for sensitive environment variables"""
    sensitive_vars = [
        'SCHWAB_MARKET_DATA_KEY',
        'SCHWAB_MARKET_DATA_SECRET',
        'SCHWAB_TRADING_KEY',
        'SCHWAB_TRADING_SECRET',
        'ALPACA_API_KEY',
        'ALPACA_SECRET_KEY',
        'NEWS_API_KEY',
        'ALPHA_VANTAGE_API_KEY'
    ]
    
    env_status = {}
    for var in sensitive_vars:
        value = os.getenv(var)
        env_status[var] = {
            'set': value is not None,
            'length': len(value) if value else 0,
            'masked': value[:4] + '***' + value[-4:] if value and len(value) > 8 else '***'
        }
    
    return env_status

def check_config_file():
    """Check config.json security"""
    config_status = {
        'exists': False,
        'readable': False,
        'contains_sensitive_data': False,
        'encrypted': False
    }
    
    if os.path.exists('config.json'):
        config_status['exists'] = True
        
        # Check permissions
        perm_check = check_file_permissions('config.json')
        config_status['secure_permissions'] = perm_check.get('secure', False)
        
        # Check content
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            api_keys = config.get('api_keys', {})
            
            # Check for sensitive data
            sensitive_keys = ['schwab_market_data_key', 'schwab_market_data_secret', 
                            'schwab_trading_key', 'schwab_trading_secret']
            
            for key in sensitive_keys:
                value = api_keys.get(key, '')
                if value and not value.startswith('your_') and value != '':
                    config_status['contains_sensitive_data'] = True
                    break
            
            # Check if values are encrypted (base64 encoded)
            encrypted_count = 0
            total_count = 0
            for key, value in api_keys.items():
                if value and not value.startswith('your_') and value != '':
                    total_count += 1
                    try:
                        # Try to decode as base64
                        import base64
                        decoded = base64.b64decode(value)
                        encrypted_count += 1
                    except:
                        pass
            
            if total_count > 0:
                config_status['encrypted'] = (encrypted_count / total_count) > 0.5
                
        except Exception as e:
            config_status['error'] = str(e)
    
    return config_status

def run_security_audit():
    """Run comprehensive security audit"""
    
    print("🔒 Security Audit Report")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check file permissions
    print("📁 File Security:")
    print("-" * 20)
    
    sensitive_files = ['config.json', '.encryption_key', '.env']
    for file in sensitive_files:
        status = check_file_permissions(file)
        if status['exists']:
            secure_icon = "✅" if status.get('secure', False) else "❌"
            print(f"{secure_icon} {file}: {status['permissions']}")
            if not status.get('secure', False):
                print(f"   ⚠️  Insecure permissions - should be 600")
        else:
            print(f"📄 {file}: Not found")
    
    print()
    
    # Check git status
    print("📦 Git Security:")
    print("-" * 20)
    
    git_status = check_git_status()
    for file, status in git_status.items():
        if status['exists']:
            if status.get('tracked', False):
                print(f"❌ {file}: Tracked by git (SECURITY RISK!)")
            else:
                print(f"✅ {file}: Not tracked by git")
        else:
            print(f"📄 {file}: Not found")
    
    print()
    
    # Check environment variables
    print("🌍 Environment Variables:")
    print("-" * 20)
    
    env_status = check_environment_variables()
    env_vars_found = 0
    for var, status in env_status.items():
        if status['set']:
            env_vars_found += 1
            print(f"✅ {var}: {status['masked']}")
    
    if env_vars_found == 0:
        print("📄 No sensitive environment variables found")
    
    print()
    
    # Check config file
    print("⚙️  Configuration Security:")
    print("-" * 20)
    
    config_status = check_config_file()
    if config_status['exists']:
        print(f"📄 config.json: Found")
        
        if config_status.get('secure_permissions', False):
            print("✅ File permissions: Secure (600)")
        else:
            print("❌ File permissions: Insecure")
        
        if config_status.get('contains_sensitive_data', False):
            if config_status.get('encrypted', False):
                print("✅ Sensitive data: Encrypted")
            else:
                print("❌ Sensitive data: Plain text (SECURITY RISK!)")
        else:
            print("📄 No sensitive data found")
    else:
        print("📄 config.json: Not found")
    
    print()
    
    # Security recommendations
    print("💡 Security Recommendations:")
    print("-" * 20)
    
    recommendations = []
    
    if not config_status.get('secure_permissions', False):
        recommendations.append("Set config.json permissions to 600: chmod 600 config.json")
    
    if config_status.get('contains_sensitive_data', False) and not config_status.get('encrypted', False):
        recommendations.append("Encrypt sensitive data in config.json")
    
    if env_vars_found == 0:
        recommendations.append("Consider using environment variables for API keys")
    
    for file, status in git_status.items():
        if status.get('tracked', False):
            recommendations.append(f"Remove {file} from git tracking: git rm --cached {file}")
    
    if not recommendations:
        print("✅ Your setup appears secure!")
    else:
        for rec in recommendations:
            print(f"🔧 {rec}")
    
    print()
    print("🔒 Security Score:")
    print("-" * 20)
    
    # Calculate security score
    score = 0
    total = 0
    
    # File permissions
    for file in sensitive_files:
        status = check_file_permissions(file)
        if status['exists']:
            total += 1
            if status.get('secure', False):
                score += 1
    
    # Git tracking
    git_status = check_git_status()
    for file, status in git_status.items():
        if status['exists']:
            total += 1
            if not status.get('tracked', False):
                score += 1
    
    # Encryption
    config_status = check_config_file()
    if config_status.get('contains_sensitive_data', False):
        total += 1
        if config_status.get('encrypted', False):
            score += 1
    
    # Environment variables
    env_status = check_environment_variables()
    if any(status['set'] for status in env_status.values()):
        score += 1
    total += 1
    
    security_percentage = (score / total * 100) if total > 0 else 100
    
    if security_percentage >= 80:
        print(f"🟢 {security_percentage:.0f}% - Good Security")
    elif security_percentage >= 60:
        print(f"🟡 {security_percentage:.0f}% - Moderate Security")
    else:
        print(f"🔴 {security_percentage:.0f}% - Poor Security")

if __name__ == "__main__":
    run_security_audit() 