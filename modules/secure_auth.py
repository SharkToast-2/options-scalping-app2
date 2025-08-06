#!/usr/bin/env python3
"""
Secure Authentication Module
Handles secure authentication and session management
"""

import streamlit as st
import hashlib
import secrets
from datetime import datetime, timedelta
from config.security_config import get_security_manager

class SecureAuth:
    def __init__(self):
        self.security_manager = get_security_manager()
        self.session_key = "secure_session"
        
    def show_login(self):
        """Show secure login interface"""
        st.header("🔐 Secure Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", max_chars=50)
            password = st.text_input("Password", type="password", max_chars=100)
            submit = st.form_submit_button("Login")
            
            if submit:
                if self.authenticate_user(username, password):
                    self.create_session(username)
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
    
    def authenticate_user(self, username, password):
        """Authenticate user with secure validation"""
        # Sanitize inputs
        username = self.security_manager.sanitize_input(username)
        password = self.security_manager.sanitize_input(password)
        
        # Validate inputs
        if not username or not password:
            return False
        
        if len(username) < 3 or len(password) < 8:
            return False
        
        # In production, check against database
        # For demo, use simple validation
        if username == "admin" and len(password) >= 8:
            return True
        
        return False
    
    def create_session(self, username):
        """Create secure session"""
        session_data = {
            'username': username,
            'token': self.security_manager.generate_session_token(),
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        st.session_state[self.session_key] = session_data
        self.security_manager.log_security_event("login_success", f"User {username} logged in", username)
    
    def check_session(self):
        """Check if user has valid session"""
        if self.session_key not in st.session_state:
            return False
        
        session_data = st.session_state[self.session_key]
        
        # Check expiration
        expires_at = datetime.fromisoformat(session_data['expires_at'])
        if datetime.now() > expires_at:
            self.logout()
            return False
        
        return True
    
    def logout(self):
        """Logout user"""
        if self.session_key in st.session_state:
            username = st.session_state[self.session_key].get('username', 'unknown')
            self.security_manager.log_security_event("logout", f"User {username} logged out", username)
            del st.session_state[self.session_key]
    
    def show_secure_interface(self):
        """Show secure interface after authentication"""
        if not self.check_session():
            self.show_login()
            return False
        
        session_data = st.session_state[self.session_key]
        username = session_data['username']
        
        # Show user info and logout button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"👤 Logged in as: {username}")
        with col2:
            if st.button("🚪 Logout"):
                self.logout()
                st.rerun()
        
        return True 