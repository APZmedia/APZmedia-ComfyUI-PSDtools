#!/usr/bin/env python3
"""
Complete setup script for ComfyUI-APZmedia-PSDtools

This script:
1. Installs all required dependencies
2. Validates the installation
3. Sets up the extension for ComfyUI
"""

import subprocess
import sys
import os
import importlib

def print_status(message, status="INFO"):
    """Print status messages with formatting"""
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "RESET": "\033[0m"     # Reset
    }
    print(f"{colors.get(status, '')}[{status}]{colors['RESET']} {message}")

def install_package(package):
    """Install a package using pip"""
    try:
        print_status(f"Installing {package}...", "INFO")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_status(f"Successfully installed {package}", "SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install {package}: {e}", "ERROR")
        return False

def check_package(package_name):
    """Check if a package is installed and importable"""
    try:
        importlib.import_module(package_name)
        print_status(f"{package_name} is available", "SUCCESS")
        return True
    except ImportError:
        print_status(f"{package_name} is not available", "ERROR")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print_status("Installing dependencies...", "INFO")
    
    packages = [
        "pytoshop -I --no-cache-dir",
        "psd-tools --no-deps",
        "Pillow>=8.0.0",
        "torch>=1.7.0",
        "numpy>=1.19.0"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    return success_count == len(packages)

def validate_installation():
    """Validate that all dependencies are properly installed"""
    print_status("Validating installation...", "INFO")
    
    required_packages = [
        "pytoshop",
        "PIL",
        "torch", 
        "numpy"
    ]
    
    all_available = True
    for package in required_packages:
        if not check_package(package):
            all_available = False
    
    return all_available

def test_psd_functionality():
    """Test basic PSD functionality"""
    print_status("Testing PSD functionality...", "INFO")
    
    try:
        from utils.apz_psd_conversion import check_pytoshop_available
        check_pytoshop_available()
        print_status("PSD functionality test passed", "SUCCESS")
        return True
    except ImportError as e:
        print_status(f"PSD functionality test failed: {e}", "ERROR")
        return False

def setup_extension():
    """Complete setup process"""
    print_status("ComfyUI-APZmedia-PSDtools Setup", "INFO")
    print_status("=" * 50, "INFO")
    
    # Step 1: Install dependencies
    print_status("Step 1: Installing dependencies", "INFO")
    if not install_dependencies():
        print_status("Failed to install all dependencies", "ERROR")
        return False
    
    # Step 2: Validate installation
    print_status("Step 2: Validating installation", "INFO")
    if not validate_installation():
        print_status("Installation validation failed", "ERROR")
        return False
    
    # Step 3: Test functionality
    print_status("Step 3: Testing functionality", "INFO")
    if not test_psd_functionality():
        print_status("Functionality test failed", "ERROR")
        return False
    
    # Step 4: Success
    print_status("=" * 50, "SUCCESS")
    print_status("Setup completed successfully!", "SUCCESS")
    print_status("You can now restart ComfyUI to use the PSD tools.", "SUCCESS")
    
    return True

def main():
    """Main setup function"""
    try:
        success = setup_extension()
        return 0 if success else 1
    except KeyboardInterrupt:
        print_status("Setup cancelled by user", "WARNING")
        return 1
    except Exception as e:
        print_status(f"Unexpected error during setup: {e}", "ERROR")
        return 1

if __name__ == "__main__":
    sys.exit(main())
