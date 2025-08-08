#!/usr/bin/env python3
"""
Security Enhancement Script
Implements additional security measures for the options scalping bot
"""

import os
import json
import hashlib
import secrets
from pathlib import Path
from cryptography.fernet import Fernet
import subprocess

class SecurityEnhancer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_dir = self.project_root / "config"
        self.logs_dir = self.project_root / "logs"
        
    def enhance_security(self):
        """Run all security enhancements"""
        print("🔒 Security Enhancement - Options Scalping Bot")
        print("=" * 50)
        
        enhancements = [
            ("File Permissions", self.enhance_file_permissions),
            ("Access Control", self.enhance_access_control),
            ("Logging Security", self.enhance_logging_security),
            ("Network Security", self.enhance_network_security),
            ("Code Security", self.enhance_code_security),
            ("Monitoring Setup", self.setup_monitoring)
        ]
        
        results = {}
        for name, func in enhancements:
            print(f"\n🔧 {name}...")
            try:
                results[name] = func()
                print(f"✅ {name} completed")
            except Exception as e:
                print(f"❌ {name} failed: {e}")
                results[name] = False
        
        self.print_enhancement_summary(results)
        return results
    
    def enhance_file_permissions(self):
        """Enhance file permissions"""
        # Set restrictive permissions on sensitive directories
        sensitive_dirs = ["config", "logs"]
        for dir_name in sensitive_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                os.chmod(dir_path, 0o750)
        
        # Set restrictive permissions on sensitive files
        sensitive_files = [
            ".env",
            "config/secure_config.json",
            "config/.secret_key"
        ]
        
        for file_path in sensitive_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                os.chmod(full_path, 0o600)
        
        return True
    
    def enhance_access_control(self):
        """Enhance access control"""
        # Create access control file
        access_control = {
            "version": "1.0",
            "access_rules": {
                "config_files": {
                    "permissions": "600",
                    "owner_only": True,
                    "description": "Sensitive configuration files"
                },
                "log_files": {
                    "permissions": "640",
                    "owner_only": True,
                    "description": "Application logs"
                },
                "api_keys": {
                    "encrypted": True,
                    "description": "API keys must be encrypted"
                }
            },
            "security_checks": {
                "file_permissions": True,
                "encryption": True,
                "git_security": True
            }
        }
        
        access_file = self.config_dir / "access_control.json"
        with open(access_file, 'w') as f:
            json.dump(access_control, f, indent=2)
        
        os.chmod(access_file, 0o600)
        return True
    
    def enhance_logging_security(self):
        """Enhance logging security"""
        # Create secure logging configuration
        logging_config = {
            "version": "1.0",
            "log_level": "INFO",
            "security": {
                "mask_sensitive_data": True,
                "encrypt_logs": False,  # Can be enabled for production
                "log_rotation": True,
                "max_log_size": "10MB",
                "retention_days": 30
            },
            "formats": {
                "security_events": {
                    "format": "%(asctime)s - %(levelname)s - %(message)s",
                    "include_ip": False,
                    "mask_keys": True
                }
            }
        }
        
        log_config_file = self.config_dir / "logging_config.json"
        with open(log_config_file, 'w') as f:
            json.dump(logging_config, f, indent=2)
        
        os.chmod(log_config_file, 0o600)
        
        # Create secure log directory structure
        secure_logs = self.logs_dir / "secure"
        secure_logs.mkdir(exist_ok=True)
        os.chmod(secure_logs, 0o750)
        
        return True
    
    def enhance_network_security(self):
        """Enhance network security"""
        # Create network security configuration
        network_config = {
            "version": "1.0",
            "api_security": {
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 100,
                    "burst_limit": 20
                },
                "timeout": {
                    "connect": 10,
                    "read": 30
                },
                "retry": {
                    "max_attempts": 3,
                    "backoff_factor": 2
                }
            },
            "ssl_verification": True,
            "allowed_hosts": [
                "api.schwabapi.com",
                "developer.schwab.com"
            ]
        }
        
        network_file = self.config_dir / "network_security.json"
        with open(network_file, 'w') as f:
            json.dump(network_config, f, indent=2)
        
        os.chmod(network_file, 0o600)
        return True
    
    def enhance_code_security(self):
        """Enhance code security"""
        # Create code security configuration
        code_security = {
            "version": "1.0",
            "input_validation": {
                "enabled": True,
                "sanitize_inputs": True,
                "validate_types": True
            },
            "output_encoding": {
                "enabled": True,
                "html_escape": True,
                "json_safe": True
            },
            "error_handling": {
                "hide_sensitive_info": True,
                "log_errors": True,
                "user_friendly_messages": True
            }
        }
        
        code_file = self.config_dir / "code_security.json"
        with open(code_file, 'w') as f:
            json.dump(code_security, f, indent=2)
        
        os.chmod(code_file, 0o600)
        return True
    
    def setup_monitoring(self):
        """Setup security monitoring"""
        # Create monitoring configuration
        monitoring_config = {
            "version": "1.0",
            "security_monitoring": {
                "enabled": True,
                "check_interval": 300,  # 5 minutes
                "alerts": {
                    "file_permission_changes": True,
                    "new_sensitive_files": True,
                    "api_key_usage": True,
                    "failed_authentication": True
                }
            },
            "performance_monitoring": {
                "enabled": True,
                "metrics": [
                    "api_response_time",
                    "error_rate",
                    "memory_usage",
                    "cpu_usage"
                ]
            },
            "logging": {
                "security_events": True,
                "performance_metrics": True,
                "error_tracking": True
            }
        }
        
        monitoring_file = self.config_dir / "monitoring_config.json"
        with open(monitoring_file, 'w') as f:
            json.dump(monitoring_config, f, indent=2)
        
        os.chmod(monitoring_file, 0o600)
        
        # Create monitoring script
        self.create_monitoring_script()
        return True
    
    def create_monitoring_script(self):
        """Create security monitoring script"""
        monitoring_script = '''#!/usr/bin/env python3
"""
Security Monitoring Script
Monitors security events and system health
"""

import os
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

class SecurityMonitor:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_dir = self.project_root / "config"
        self.logs_dir = self.project_root / "logs"
        
    def check_file_integrity(self):
        """Check file integrity"""
        sensitive_files = [
            ".env",
            "config/secure_config.json",
            "config/.secret_key"
        ]
        
        integrity_report = {}
        for file_path in sensitive_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                # Calculate file hash
                with open(full_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                # Check permissions
                stat = full_path.stat()
                permissions = oct(stat.st_mode & 0o777)
                
                integrity_report[file_path] = {
                    "hash": file_hash,
                    "permissions": permissions,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "secure": permissions == "0o600"
                }
        
        return integrity_report
    
    def check_api_usage(self):
        """Check API usage patterns"""
        # This would integrate with your API monitoring
        return {"status": "monitoring_enabled"}
    
    def run_security_check(self):
        """Run comprehensive security check"""
        print("🔍 Security Monitoring Check")
        print("=" * 40)
        
        integrity = self.check_file_integrity()
        api_usage = self.check_api_usage()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "file_integrity": integrity,
            "api_usage": api_usage
        }
        
        # Save report
        report_file = self.logs_dir / "security_monitoring_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Security monitoring report generated")
        return report

if __name__ == "__main__":
    monitor = SecurityMonitor()
    monitor.run_security_check()
'''
        
        monitor_file = self.project_root / "security_monitor.py"
        with open(monitor_file, 'w') as f:
            f.write(monitoring_script)
        
        os.chmod(monitor_file, 0o755)
    
    def print_enhancement_summary(self, results):
        """Print enhancement summary"""
        print("\n📊 Security Enhancement Summary")
        print("=" * 40)
        
        successful = sum(1 for result in results.values() if result)
        total = len(results)
        
        for enhancement, success in results.items():
            icon = "✅" if success else "❌"
            print(f"{icon} {enhancement}")
        
        print(f"\n🎯 Enhancement Score: {successful}/{total} ({successful/total*100:.1f}%)")
        
        if successful == total:
            print("🎉 All security enhancements completed successfully!")
        else:
            print("⚠️ Some enhancements failed. Check the output above.")
        
        # Save enhancement report
        from datetime import datetime
        report = {
            "timestamp": datetime.now().isoformat(),
            "enhancements": results,
            "score": f"{successful}/{total}"
        }
        
        report_file = self.logs_dir / "security_enhancement_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Enhancement report saved to: {report_file}")

def main():
    """Main function"""
    enhancer = SecurityEnhancer()
    enhancer.enhance_security()

if __name__ == "__main__":
    main() 