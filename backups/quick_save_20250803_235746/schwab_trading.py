#!/usr/bin/env python3
"""
Schwab Trading API for executing trades
"""

import requests
import json
import logging
from datetime import datetime
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class SchwabTradingAPI:
    def __init__(self, api_key: str, secret_key: str, base_url: str = "https://api.schwab.com"):
        """
        Initialize Schwab Trading API client
        
        Args:
            api_key (str): Your Schwab Trading API key
            secret_key (str): Your Schwab Trading secret key
            base_url (str): Schwab API base URL
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.session = requests.Session()
        
        # Set up authentication headers
        self.session.headers.update({
            'X-API-Key': api_key,
            'X-Secret-Key': secret_key,
            'Content-Type': 'application/json'
        })
    
    def get_account_info(self) -> Optional[Dict]:
        """Get account information"""
        try:
            url = f"{self.base_url}/v1/accounts"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting account info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error accessing Schwab Trading API: {e}")
            return None
    
    def get_positions(self) -> Optional[List[Dict]]:
        """Get current positions"""
        try:
            url = f"{self.base_url}/v1/positions"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting positions: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error accessing Schwab Trading API: {e}")
            return None
    
    def place_order(self, symbol: str, quantity: int, side: str, order_type: str = "market") -> Optional[Dict]:
        """
        Place a trade order
        
        Args:
            symbol (str): Stock symbol
            quantity (int): Number of shares
            side (str): "buy" or "sell"
            order_type (str): "market" or "limit"
        """
        try:
            url = f"{self.base_url}/v1/orders"
            
            order_data = {
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "type": order_type,
                "time_in_force": "day"
            }
            
            response = self.session.post(url, json=order_data)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error placing order: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None
    
    def place_options_order(self, symbol: str, quantity: int, side: str, option_type: str, 
                          strike_price: float, expiration_date: str, order_type: str = "market") -> Optional[Dict]:
        """
        Place an options trade order
        
        Args:
            symbol (str): Stock symbol
            quantity (int): Number of contracts
            side (str): "buy" or "sell"
            option_type (str): "call" or "put"
            strike_price (float): Strike price
            expiration_date (str): Expiration date (YYYY-MM-DD)
            order_type (str): "market" or "limit"
        """
        try:
            url = f"{self.base_url}/v1/orders/options"
            
            order_data = {
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "option_type": option_type,
                "strike_price": strike_price,
                "expiration_date": expiration_date,
                "type": order_type,
                "time_in_force": "day"
            }
            
            response = self.session.post(url, json=order_data)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error placing options order: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error placing options order: {e}")
            return None
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        try:
            url = f"{self.base_url}/v1/orders/{order_id}/cancel"
            response = self.session.post(url)
            
            if response.status_code == 200:
                return True
            else:
                logger.error(f"Error canceling order: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error canceling order: {e}")
            return False
    
    def get_order_status(self, order_id: str) -> Optional[Dict]:
        """Get order status"""
        try:
            url = f"{self.base_url}/v1/orders/{order_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting order status: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting order status: {e}")
            return None

class MockSchwabTradingAPI:
    """Mock Schwab Trading API for testing"""
    
    def __init__(self):
        self.base_url = "mock"
    
    def get_account_info(self) -> Optional[Dict]:
        """Mock account info"""
        return {
            "account_id": "MOCK123456",
            "account_type": "individual",
            "balance": 50000.00,
            "buying_power": 45000.00,
            "cash": 10000.00
        }
    
    def get_positions(self) -> Optional[List[Dict]]:
        """Mock positions"""
        return []
    
    def place_order(self, symbol: str, quantity: int, side: str, order_type: str = "market") -> Optional[Dict]:
        """Mock order placement"""
        return {
            "order_id": f"MOCK_{datetime.now().timestamp()}",
            "symbol": symbol,
            "quantity": quantity,
            "side": side,
            "type": order_type,
            "status": "filled",
            "filled_price": 150.00,
            "timestamp": datetime.now().isoformat()
        }
    
    def place_options_order(self, symbol: str, quantity: int, side: str, option_type: str, 
                          strike_price: float, expiration_date: str, order_type: str = "market") -> Optional[Dict]:
        """Mock options order placement"""
        return {
            "order_id": f"MOCK_OPT_{datetime.now().timestamp()}",
            "symbol": symbol,
            "quantity": quantity,
            "side": side,
            "option_type": option_type,
            "strike_price": strike_price,
            "expiration_date": expiration_date,
            "type": order_type,
            "status": "filled",
            "filled_price": 2.50,
            "timestamp": datetime.now().isoformat()
        }
    
    def cancel_order(self, order_id: str) -> bool:
        """Mock order cancellation"""
        return True
    
    def get_order_status(self, order_id: str) -> Optional[Dict]:
        """Mock order status"""
        return {
            "order_id": order_id,
            "status": "filled",
            "filled_quantity": 100,
            "filled_price": 150.00
        }

def get_schwab_trading_client(api_key: str = None, secret_key: str = None, use_mock: bool = True):
    """
    Get Schwab Trading API client
    
    Args:
        api_key (str): Your Schwab Trading API key
        secret_key (str): Your Schwab Trading secret key
        use_mock (bool): Use mock data if no API key provided
    """
    if api_key and secret_key and api_key != "your_schwab_trading_api_key_here" and secret_key != "your_schwab_trading_secret_here" and not use_mock:
        return SchwabTradingAPI(api_key, secret_key)
    else:
        return MockSchwabTradingAPI() 