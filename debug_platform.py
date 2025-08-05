#!/usr/bin/env python3

import platform
import os
import sys

print("=== Platform Detection Debug ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"System: {platform.system()}")
print(f"Platform: {platform.platform()}")
print(f"Machine: {platform.machine()}")
print(f"Release: {platform.release()}")
print(f"Architecture: {platform.architecture()}")
print(f"Processor: {platform.processor()}")

print("\n=== Environment Variables ===")
env_vars = ['PLATFORM', 'OS', 'OSTYPE', 'MACHTYPE', 'SYSTEM']
for var in env_vars:
    value = os.environ.get(var, 'Not set')
    print(f"{var}: {value}")

print("\n=== File System Check ===")
print(f"/Applications exists: {os.path.exists('/Applications')}")
print(f"/System exists: {os.path.exists('/System')}")
print(f"/Users exists: {os.path.exists('/Users')}")

print("\n=== Platform Detection Logic ===")
system = platform.system()
platform_info = platform.platform().lower()
machine = platform.machine().lower()

is_macos = (system == "Darwin" or 
           system == "macOS" or 
           "darwin" in platform_info or
           "mac" in platform_info or
           "darwin" in machine or
           "mac" in machine)

print(f"system == 'Darwin': {system == 'Darwin'}")
print(f"system == 'macOS': {system == 'macOS'}")
print(f"'darwin' in platform_info: {'darwin' in platform_info}")
print(f"'mac' in platform_info: {'mac' in platform_info}")
print(f"'darwin' in machine: {'darwin' in machine}")
print(f"'mac' in machine: {'mac' in machine}")
print(f"Final is_macos: {is_macos}") 