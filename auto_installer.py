#!/usr/bin/env python3
"""
Automatic dependency installer for ComfyUI PSD Tools
This module handles automatic installation of required dependencies
"""

import subprocess
import sys
import os
import importlib
from typing import List, Tuple, Optional

class DependencyInstaller:
    """Handles automatic installation of dependencies"""
    
    def __init__(self):
        self.required_packages = [
            ("pytoshop", "pytoshop>=0.1.0", "-I --no-cache-dir"),
            ("psd-tools", "psd-tools", "--no-deps"),
            ("Pillow", "Pillow>=8.0.0", None),
            ("torch", "torch>=1.7.0", None),
            ("numpy", "numpy>=1.19.0", None)
        ]
    
    def is_package_installed(self, package_name: str) -> bool:
        """Check if a package is already installed"""
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False
    
    def install_package(self, package_name: str, package_spec: str, flags: Optional[str] = None) -> bool:
        """Install a single package"""
        try:
            cmd = [sys.executable, "-m", "pip", "install"]
            if flags:
                cmd.extend(flags.split())
            cmd.append(package_spec)
            
            print(f"[INFO] Installing {package_spec}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"[SUCCESS] Successfully installed {package_spec}")
                return True
            else:
                print(f"[ERROR] Failed to install {package_spec}")
                print(f"[ERROR] {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"[ERROR] Timeout installing {package_spec}")
            return False
        except Exception as e:
            print(f"[ERROR] Exception installing {package_spec}: {e}")
            return False
    
    def install_dependencies(self, silent: bool = False) -> bool:
        """Install all required dependencies"""
        if not silent:
            print("[INFO] Checking and installing dependencies automatically...")
        
        success_count = 0
        for package_name, package_spec, flags in self.required_packages:
            if self.is_package_installed(package_name):
                if not silent:
                    print(f"[INFO] {package_name} is already installed")
                success_count += 1
            else:
                if self.install_package(package_name, package_spec, flags):
                    success_count += 1
        
        all_installed = success_count == len(self.required_packages)
        if not silent:
            if all_installed:
                print("[SUCCESS] 🎉 All dependencies are ready!")
            else:
                print(f"[WARNING] {success_count}/{len(self.required_packages)} dependencies installed")
        
        return all_installed
    
    def ensure_dependencies(self) -> bool:
        """Ensure all dependencies are available"""
        return self.install_dependencies(silent=True)

def get_installer() -> DependencyInstaller:
    """Get a new instance of the dependency installer"""
    return DependencyInstaller()

def auto_install_dependencies(silent: bool = False) -> bool:
    """Auto-install dependencies"""
    installer = get_installer()
    return installer.install_dependencies(silent=silent)

def ensure_dependencies() -> bool:
    """Ensure all dependencies are available"""
    installer = get_installer()
    return installer.ensure_dependencies()

# Test the installer
if __name__ == "__main__":
    print("Testing dependency installer...")
    installer = get_installer()
    success = installer.install_dependencies()
    print(f"Installation successful: {success}")