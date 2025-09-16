#!/usr/bin/env python3
"""
Automatic dependency installer for ComfyUI-APZmedia-PSDtools

This script automatically installs the required dependencies for the PSD tools extension.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"Installing {package}...")
        # Try with --user flag first to avoid permission issues
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package} with --user flag: {e}")
        # Try without --user flag as fallback
        try:
            print(f"Retrying without --user flag...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Successfully installed {package}")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"✗ Failed to install {package}: {e2}")
            return False

def check_package(package_name):
    """Check if a package is already installed"""
    try:
        __import__(package_name)
        print(f"✓ {package_name} is already installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is not installed")
        return False

def main():
    """Main installation function"""
    print("ComfyUI-APZmedia-PSDtools Dependency Installer")
    print("=" * 50)
    
    # Required packages
    packages = [
        ("pytoshop", "pytoshop>=0.1.0"),
        ("PIL", "Pillow>=8.0.0"),
        ("torch", "torch>=1.7.0"),
        ("numpy", "numpy>=1.19.0")
    ]
    
    print("\nChecking current installation status:")
    missing_packages = []
    
    for package_name, pip_name in packages:
        if not check_package(package_name):
            missing_packages.append(pip_name)
    
    if not missing_packages:
        print("\n✓ All dependencies are already installed!")
        print("You can now use the PSD tools extension.")
        return True
    
    print(f"\nInstalling {len(missing_packages)} missing packages...")
    
    success_count = 0
    for package in missing_packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    print("Installation Summary:")
    print(f"Successfully installed: {success_count}/{len(missing_packages)} packages")
    
    if success_count == len(missing_packages):
        print("✓ All dependencies installed successfully!")
        print("Please restart ComfyUI to use the PSD tools extension.")
        return True
    else:
        print("✗ Some dependencies failed to install.")
        print("Please check the error messages above and try manual installation.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
