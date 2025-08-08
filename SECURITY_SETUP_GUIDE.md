# 🔒 Security Setup Guide - Options Scalping Bot

This guide will help you secure your GitHub repository data and properly input your Schwab API keys with enterprise-grade encryption.

## 🚀 Quick Start

### Step 1: Run the Secure Setup Script

```bash
# Make the script executable
chmod +x secure_setup.py

# Run the secure setup
python3 secure_setup.py
```

This script will:
- ✅ Secure your GitHub repository data
- ✅ Input and encrypt your Schwab API keys
- ✅ Validate security settings
- ✅ Generate a security report

### Step 2: Run Security Audit

```bash
# Run security audit to verify setup
python3 security_audit.py
```

## 📋 Prerequisites

### Required Schwab API Keys

Before running the setup, you'll need these keys from Schwab:

1. **Client ID** (Required)
   - Get from: https://developer.schwab.com
   - Used for OAuth2 authentication

2. **Client Secret** (Required)
   - Get from: https://developer.schwab.com
   - Used for OAuth2 authentication

3. **Market Data Key** (Optional)
   - Separate key for market data access
   - May be the same as Client ID

4. **Market Data Secret** (Optional)
   - Separate secret for market data access
   - May be the same as Client Secret

5. **Trading Key** (Optional)
   - Separate key for trading operations
   - May be the same as Client ID

6. **Trading Secret** (Optional)
   - Separate secret for trading operations
   - May be the same as Client Secret

## 🔑 Getting Schwab API Keys

### 1. Create Schwab Developer Account

1. Go to [Schwab Developer Portal](https://developer.schwab.com)
2. Sign up for a developer account
3. Complete the application process
4. Wait for approval (usually 1-2 business days)

### 2. Create Application

1. Log into the Schwab Developer Portal
2. Click "Create New Application"
3. Fill in application details:
   - **Application Name**: Options Scalping Bot
   - **Description**: Automated options trading bot
   - **Callback URL**: `http://localhost:8501/callback`
   - **Scopes**: Select all available scopes
     - `trading` - Execute trades
     - `market_data` - Access market data
     - `account_read` - Read account information

### 3. Get Your Keys

After approval, you'll receive:
- **Client ID**: A long string of letters and numbers
- **Client Secret**: A secret key for authentication

## 🔒 Security Features

### Encryption

All sensitive data is encrypted using:
- **Fernet encryption** (AES-128 in CBC mode)
- **Secure key generation** using cryptographically secure random numbers
- **Restrictive file permissions** (600 - owner read/write only)

### File Security

The setup creates these secure files:
- `config/.secret_key` - Encryption key (600 permissions)
- `config/secure_config.json` - Encrypted API keys (600 permissions)
- `.env` - Environment variables (600 permissions)

### Git Security

The setup automatically:
- Updates `.gitignore` with security patterns
- Removes sensitive files from Git tracking
- Prevents accidental commits of secrets

## 📁 File Structure After Setup

```
options_scalping_project/
├── config/
│   ├── .secret_key              # 🔒 Encryption key (600 permissions)
│   ├── secure_config.json       # 🔒 Encrypted API keys (600 permissions)
│   └── env_template.txt         # Template for environment variables
├── logs/
│   └── security_audit_report.json  # Security audit results
├── .env                         # 🔒 Environment variables (600 permissions)
├── .gitignore                   # Updated with security patterns
├── secure_setup.py              # Secure setup script
├── security_audit.py            # Security audit script
└── README.md                    # This guide
```

## 🔍 Security Validation

### What the Security Audit Checks

1. **File Permissions**
   - Ensures sensitive files have 600 permissions
   - Checks encryption key security

2. **Sensitive Files**
   - Scans for API keys, certificates, tokens
   - Verifies files are properly ignored by Git

3. **Git Security**
   - Checks for sensitive files in Git history
   - Validates .gitignore configuration

4. **Encryption Setup**
   - Verifies encryption key exists
   - Checks encrypted configuration

5. **API Key Security**
   - Validates API key format
   - Checks for hardcoded keys in code

6. **Environment Security**
   - Verifies .env file security
   - Checks debug mode settings

7. **Dependencies**
   - Scans for vulnerable packages
   - Validates requirements.txt

8. **Code Security**
   - Checks for dangerous code patterns
   - Validates input handling

## 🚨 Security Best Practices

### ✅ Do's

- ✅ Use the secure setup script for initial configuration
- ✅ Run security audit regularly
- ✅ Keep encryption keys secure
- ✅ Use environment variables in production
- ✅ Regularly rotate API keys
- ✅ Enable 2FA on your Schwab account
- ✅ Monitor API usage
- ✅ Use a dedicated trading account with limited funds

### ❌ Don'ts

- ❌ Never commit API keys to Git
- ❌ Don't share encryption keys
- ❌ Don't use debug mode in production
- ❌ Don't hardcode secrets in code
- ❌ Don't use the same keys for multiple applications
- ❌ Don't store keys in plain text files

## 🔧 Troubleshooting

### Common Issues

#### 1. "No Git repository found"
```bash
# Initialize Git repository
git init
git add .
git commit -m "Initial commit"
```

#### 2. "Invalid API key format"
- Ensure your API key is at least 20 characters long
- Check for extra spaces or special characters
- Verify you copied the key correctly from Schwab

#### 3. "Permission denied" errors
```bash
# Fix file permissions
chmod 600 config/.secret_key
chmod 600 config/secure_config.json
chmod 600 .env
```

#### 4. "Encryption key not found"
```bash
# Regenerate encryption key
rm config/.secret_key
python3 secure_setup.py
```

### Security Score Interpretation

- **90-100%**: Excellent security posture
- **75-89%**: Good security posture
- **50-74%**: Security improvements needed
- **0-49%**: Critical security issues found

## 📞 Support

### Getting Help

If you encounter issues:

1. **Check the logs**: `logs/security_audit_report.json`
2. **Run security audit**: `python3 security_audit.py`
3. **Review this guide**: Check troubleshooting section
4. **Check Schwab documentation**: [Schwab Developer Portal](https://developer.schwab.com)

### Security Issues

If you discover a security vulnerability:
1. **Do NOT create a public issue**
2. **Email us directly** with "SECURITY" in the subject
3. **Include details** about the vulnerability

## 🔄 Regular Maintenance

### Monthly Security Tasks

1. **Run security audit**
   ```bash
   python3 security_audit.py
   ```

2. **Check API key usage**
   - Monitor Schwab Developer Portal
   - Review API call logs

3. **Update dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **Review file permissions**
   ```bash
   ls -la config/.secret_key
   ls -la config/secure_config.json
   ls -la .env
   ```

### Quarterly Security Tasks

1. **Rotate API keys**
   - Generate new keys in Schwab Developer Portal
   - Update using secure setup script

2. **Review security logs**
   - Check `logs/security_audit_report.json`
   - Review any warnings or issues

3. **Update security patterns**
   - Review .gitignore patterns
   - Update security scripts if needed

## 🎯 Next Steps

After completing the secure setup:

1. **Test your configuration**
   ```bash
   python3 security_audit.py
   ```

2. **Start the application**
   ```bash
   streamlit run app.py
   ```

3. **Monitor security**
   - Run security audit weekly
   - Check logs regularly
   - Monitor API usage

4. **Scale securely**
   - Use environment variables in production
   - Implement proper logging
   - Set up monitoring and alerts

---

**🔒 Remember: Security is an ongoing process, not a one-time setup!**

For additional security resources, see:
- [SECURITY.md](SECURITY.md) - Detailed security documentation
- [SECURITY_SUMMARY.md](SECURITY_SUMMARY.md) - Security overview
- [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) - Performance and security optimizations 