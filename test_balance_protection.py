#!/usr/bin/env python3
"""
Test script for account balance protection functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trading.risk_manager import RiskManager
from config.settings import TRADING_CONFIG

def test_balance_protection():
    """Test the balance protection functionality"""
    print("🧪 Testing Account Balance Protection")
    print("=" * 50)
    
    # Initialize risk manager
    risk_manager = RiskManager()
    
    # Test 1: Set initial balance
    print("\n1. Setting initial balance...")
    risk_manager.set_initial_balance(10000.0)
    status = risk_manager.get_account_status()
    print(f"   Initial balance: ${status['initial_balance']:,.2f}")
    print(f"   Current balance: ${status['current_balance']:,.2f}")
    print(f"   Trading enabled: {status['trading_enabled']}")
    
    # Test 2: Check balance protection thresholds
    print("\n2. Checking balance protection thresholds...")
    min_balance = TRADING_CONFIG["MIN_ACCOUNT_BALANCE"]
    buffer = TRADING_CONFIG["ACCOUNT_BALANCE_BUFFER"]
    required_balance = min_balance + buffer
    print(f"   Minimum balance: ${min_balance:,.2f}")
    print(f"   Safety buffer: ${buffer:,.2f}")
    print(f"   Required total: ${required_balance:,.2f}")
    
    # Test 3: Simulate profitable trade
    print("\n3. Simulating profitable trade...")
    profit = 500.0
    risk_manager.update_account_balance(profit)
    status = risk_manager.get_account_status()
    print(f"   Profit: ${profit:,.2f}")
    print(f"   New balance: ${status['current_balance']:,.2f}")
    print(f"   Trading enabled: {status['trading_enabled']}")
    print(f"   Warning level: {risk_manager.get_balance_warning_level()}")
    
    # Test 4: Simulate losing trade that triggers protection
    print("\n4. Simulating losing trade that triggers protection...")
    loss = -8000.0  # This should trigger protection
    risk_manager.update_account_balance(loss)
    status = risk_manager.get_account_status()
    print(f"   Loss: ${loss:,.2f}")
    print(f"   New balance: ${status['current_balance']:,.2f}")
    print(f"   Trading enabled: {status['trading_enabled']}")
    print(f"   Protection triggered: {status['balance_protection_triggered']}")
    print(f"   Warning level: {risk_manager.get_balance_warning_level()}")
    
    # Test 5: Try to enable trading manually
    print("\n5. Testing manual trading enable...")
    risk_manager.enable_trading()
    status = risk_manager.get_account_status()
    print(f"   Trading enabled: {status['trading_enabled']}")
    
    # Test 6: Reset balance protection
    print("\n6. Resetting balance protection...")
    new_balance = 15000.0
    risk_manager.reset_balance_protection(new_balance)
    status = risk_manager.get_account_status()
    print(f"   New balance: ${status['current_balance']:,.2f}")
    print(f"   Trading enabled: {status['trading_enabled']}")
    print(f"   Protection triggered: {status['balance_protection_triggered']}")
    print(f"   Warning level: {risk_manager.get_balance_warning_level()}")
    
    # Test 7: Test risk limits check
    print("\n7. Testing risk limits check...")
    risk_check = risk_manager.check_risk_limits("META", "call", 10, 5.0)
    print(f"   Trade allowed: {risk_check['trade_allowed']}")
    print(f"   Current balance: ${risk_check['current_balance']:,.2f}")
    print(f"   Required balance: ${risk_check['required_balance']:,.2f}")
    
    print("\n✅ Balance protection test completed!")

if __name__ == "__main__":
    test_balance_protection() 