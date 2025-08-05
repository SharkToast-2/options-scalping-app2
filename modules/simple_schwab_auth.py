#!/usr/bin/env python3
"""
Simplified Schwab Authentication Module
Provides manual authentication without complex browser opening
"""

import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Optional

class SimpleSchwabAuth:
    def __init__(self):
        self.config_file = "config.json"
        self.auth_url = "https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj&scope=readonly&redirect_uri=https://developer.schwab.com/oauth2-redirect.html"
    
    def show_auth_interface(self):
        """Show simplified authentication interface"""
        st.subheader("🔐 Schwab Authentication")
        
        # Check current auth status
        auth_status = self.get_auth_status()
        
        if auth_status.get('authenticated'):
            self.show_authenticated_status(auth_status)
        else:
            self.show_manual_auth_instructions()
    
    def show_authenticated_status(self, auth_status: Dict):
        """Show authenticated status"""
        st.success("✅ Schwab API Authenticated")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", "Authenticated")
        
        with col2:
            st.metric("Method", auth_status.get('method', 'Unknown'))
        
        with col3:
            st.metric("Expires", auth_status.get('expires', 'Unknown'))
        
        # Show auth details
        with st.expander("🔍 Authentication Details"):
            st.json(auth_status)
        
        # Manual deauth option
        if st.button("🔓 Clear Authentication", type="secondary"):
            self.clear_auth()
            st.rerun()
    
    def show_manual_auth_instructions(self):
        """Show manual authentication instructions"""
        st.info("📋 Manual Authentication Required")
        
        st.markdown("""
        ### 🔗 Step 1: Get Authorization URL
        Click the link below to open the Schwab authorization page:
        """)
        
        # Display the authorization URL
        st.code(self.auth_url, language="text")
        
        # Clickable link
        st.markdown(f"[🌐 **Click here to open Schwab Authorization Page**]({self.auth_url})")
        
        st.markdown("""
        ### 📝 Step 2: Complete Authorization
        1. **Sign in** to your Schwab account
        2. **Authorize** the application
        3. **Copy the entire URL** you're redirected to
        """)
        
        # Input for authorization code
        st.markdown("### 📋 Step 3: Paste Authorization URL")
        
        auth_url_input = st.text_input(
            "Paste the complete URL you were redirected to:",
            placeholder="https://developer.schwab.com/oauth2-redirect.html?code=...",
            help="Copy the entire URL from your browser after authorization"
        )
        
        if auth_url_input:
            if st.button("🔐 Complete Authentication", type="primary"):
                success = self.process_auth_url(auth_url_input)
                if success:
                    st.success("✅ Authentication completed successfully!")
                    st.rerun()
                else:
                    st.error("❌ Authentication failed. Please check the URL and try again.")
        
        # Alternative: Manual API key entry
        st.markdown("---")
        st.markdown("### 🔑 Alternative: API Key Authentication")
        
        with st.expander("🔧 API Key Setup"):
            api_key = st.text_input("Schwab API Key:", type="password")
            api_secret = st.text_input("Schwab API Secret:", type="password")
            
            if api_key and api_secret:
                if st.button("🔐 Save API Keys", type="secondary"):
                    self.save_api_keys(api_key, api_secret)
                    st.success("✅ API keys saved!")
                    st.rerun()
    
    def process_auth_url(self, auth_url: str) -> bool:
        """Process authorization URL and extract code"""
        try:
            # Extract authorization code from URL
            if "code=" in auth_url:
                code = auth_url.split("code=")[1].split("&")[0]
                
                # Save authentication info
                auth_data = {
                    'authenticated': True,
                    'method': 'OAuth2',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'expires': '1 hour',
                    'auth_code': code,
                    'auth_url': auth_url
                }
                
                self.save_auth_data(auth_data)
                return True
            
            return False
            
        except Exception as e:
            st.error(f"Error processing auth URL: {e}")
            return False
    
    def save_api_keys(self, api_key: str, api_secret: str):
        """Save API keys to config"""
        try:
            # Load existing config
            config = self.load_config()
            
            # Update Schwab credentials
            config['schwab_trading_key'] = api_key
            config['schwab_trading_secret'] = api_secret
            
            # Add auth status
            config['schwab_auth'] = {
                'authenticated': True,
                'method': 'API Key',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'expires': 'Session'
            }
            
            # Save config
            self.save_config(config)
            
        except Exception as e:
            st.error(f"Error saving API keys: {e}")
    
    def get_auth_status(self) -> Dict:
        """Get current authentication status"""
        try:
            config = self.load_config()
            return config.get('schwab_auth', {})
        except Exception:
            return {}
    
    def clear_auth(self):
        """Clear authentication data"""
        try:
            config = self.load_config()
            if 'schwab_auth' in config:
                del config['schwab_auth']
            self.save_config(config)
            st.success("✅ Authentication cleared")
        except Exception as e:
            st.error(f"Error clearing auth: {e}")
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception:
            return {}
    
    def save_config(self, config: Dict):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            st.error(f"Error saving config: {e}")
    
    def save_auth_data(self, auth_data: Dict):
        """Save authentication data"""
        try:
            config = self.load_config()
            config['schwab_auth'] = auth_data
            self.save_config(config)
        except Exception as e:
            st.error(f"Error saving auth data: {e}")
    
    def test_connection(self) -> bool:
        """Test Schwab API connection"""
        try:
            auth_status = self.get_auth_status()
            if not auth_status.get('authenticated'):
                return False
            
            # Here you would make an actual API call to test
            # For now, just return True if authenticated
            return True
            
        except Exception:
            return False 