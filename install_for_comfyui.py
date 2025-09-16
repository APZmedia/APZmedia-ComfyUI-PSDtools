#!/usr/bin/env python3
"""
Installation script specifically for ComfyUI environment
This script installs pytoshop and other dependencies in the ComfyUI Python environment
"""

import subprocess
import sys
import os

def install_package(package, flags=None):
    """Install a package using pip with optional flags"""
    try:
        cmd = [sys.executable, "-m", "pip", "install"]
        if flags:
            cmd.extend(flags.split())
        cmd.append(package)
        
        print(f"Installing {package}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully installed {package}")
            return True
        else:
            print(f"❌ Failed to install {package}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception installing {package}: {e}")
        return False

def main():
    """Main installation function for ComfyUI"""
    print("=" * 60)
    print("APZmedia PSD Tools - ComfyUI Installation")
    print("=" * 60)
    
    # Check if we're in a ComfyUI environment
    current_dir = os.getcwd()
    if "ComfyUI" not in current_dir:
        print("⚠️  Warning: This doesn't appear to be a ComfyUI directory")
        print(f"   Current directory: {current_dir}")
        print("   Make sure you're running this from the ComfyUI directory")
    
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {current_dir}")
    
    # Install packages with specific flags as used in ComfyUI-Layers
    packages = [
        ("pytoshop", "-I --no-cache-dir"),
        ("psd-tools", "--no-deps"),
        ("Pillow>=8.0.0", None),
        ("torch>=1.7.0", None),
        ("numpy>=1.19.0", None)
    ]
    
    success_count = 0
    for package, flags in packages:
        if install_package(package, flags):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Installation Summary: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("🎉 All dependencies installed successfully!")
        print("Please restart ComfyUI to use the PSD tools.")
        return True
    else:
        print("⚠️  Some dependencies failed to install.")
        print("Please check the error messages above.")
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
