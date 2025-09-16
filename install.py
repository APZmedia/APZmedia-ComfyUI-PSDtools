#!/usr/bin/env python3
"""
Installation script for ComfyUI-APZmedia-PSDtools

Based on the proven approach from ComfyUI-Layers:
https://github.com/alessandrozonta/ComfyUI-Layers
"""

import subprocess
import sys
import os

def install_package(package, flags=None):
    """Install a package using pip with optional flags"""
    try:
        cmd = [sys.executable, "-m", "pip", "install", "--user"]
        if flags:
            cmd.extend(flags.split())
        cmd.append(package)
        
        print(f"Installing {package}...")
        subprocess.check_call(cmd)
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package} with --user flag: {e}")
        # Try without --user flag as fallback
        try:
            print(f"Retrying without --user flag...")
            cmd = [sys.executable, "-m", "pip", "install"]
            if flags:
                cmd.extend(flags.split())
            cmd.append(package)
            subprocess.check_call(cmd)
            print(f"✓ Successfully installed {package}")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"✗ Failed to install {package}: {e2}")
            return False

def main():
    """Main installation function"""
    print("ComfyUI-APZmedia-PSDtools Installation")
    print("=" * 40)
    
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
    
    print("\n" + "=" * 40)
    print(f"Installation Summary: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("✓ All dependencies installed successfully!")
        print("Please restart ComfyUI to use the PSD tools.")
        return True
    else:
        print("✗ Some dependencies failed to install.")
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
