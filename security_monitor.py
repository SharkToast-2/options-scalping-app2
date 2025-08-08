#!/usr/bin/env python3
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
