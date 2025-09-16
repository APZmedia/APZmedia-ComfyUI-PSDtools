#!/usr/bin/env python3
"""
Automatic dependency installer for ComfyUI-APZmedia-PSDtools

This module provides automatic dependency installation that runs when the extension loads.
It checks for missing dependencies and installs them automatically without user intervention.
"""

import subprocess
import sys
import os
import importlib
import logging
from typing import List, Tuple, Optional

# Set up logging
logger = logging.getLogger(__name__)

class Colors:
    """Color codes for console output"""
    ORANGE = '\033[38;5;208m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class AutoInstaller:
    """Automatic dependency installer for PSD tools extension"""
    
    def __init__(self):
        self.required_packages = [
            ("pytoshop", "pytoshop>=0.1.0", "-I --no-cache-dir"),
            ("PIL", "Pillow>=8.0.0", None),
            ("torch", "torch>=1.7.0", None),
            ("numpy", "numpy>=1.19.0", None),
            ("psd_tools", "psd-tools", "--no-deps")
        ]
        self.installation_log = []
        
    def print_status(self, message: str, status: str = "INFO", use_colors: bool = True) -> None:
        """Print status messages with optional color formatting"""
        if use_colors:
            colors = {
                "INFO": Colors.BLUE,
                "SUCCESS": Colors.GREEN,
                "WARNING": Colors.YELLOW,
                "ERROR": Colors.RED,
                "RESET": Colors.END
            }
            color = colors.get(status, Colors.WHITE)
            print(f"{color}[{status}]{Colors.END} {message}")
        else:
            print(f"[{status}] {message}")
        
        # Log to file as well
        log_message = f"[{status}] {message}"
        self.installation_log.append(log_message)
        logger.info(log_message)
    
    def check_package_available(self, package_name: str) -> bool:
        """Check if a package is available for import"""
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False
    
    def install_package(self, package_name: str, pip_name: str, flags: Optional[str] = None) -> bool:
        """Install a package using pip with error handling"""
        try:
            # Build command
            cmd = [sys.executable, "-m", "pip", "install"]
            
            # Add flags if provided
            if flags:
                cmd.extend(flags.split())
            
            # Add package name
            cmd.append(pip_name)
            
            self.print_status(f"Installing {pip_name}...", "INFO")
            
            # Try installation with --user flag first
            cmd_with_user = cmd + ["--user"]
            try:
                result = subprocess.run(
                    cmd_with_user, 
                    capture_output=True, 
                    text=True, 
                    timeout=300  # 5 minute timeout
                )
                if result.returncode == 0:
                    self.print_status(f"Successfully installed {pip_name}", "SUCCESS")
                    return True
                else:
                    self.print_status(f"Failed with --user flag: {result.stderr}", "WARNING")
            except subprocess.TimeoutExpired:
                self.print_status(f"Installation timeout for {pip_name}", "WARNING")
            except Exception as e:
                self.print_status(f"Exception with --user flag: {e}", "WARNING")
            
            # Try without --user flag as fallback
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=300
                )
                if result.returncode == 0:
                    self.print_status(f"Successfully installed {pip_name}", "SUCCESS")
                    return True
                else:
                    self.print_status(f"Failed to install {pip_name}: {result.stderr}", "ERROR")
                    return False
            except subprocess.TimeoutExpired:
                self.print_status(f"Installation timeout for {pip_name}", "ERROR")
                return False
            except Exception as e:
                self.print_status(f"Exception installing {pip_name}: {e}", "ERROR")
                return False
                
        except Exception as e:
            self.print_status(f"Unexpected error installing {pip_name}: {e}", "ERROR")
            return False
    
    def check_and_install_dependencies(self, silent: bool = False) -> Tuple[bool, List[str]]:
        """
        Check for missing dependencies and install them automatically
        
        Args:
            silent: If True, suppress most output (useful for background installation)
            
        Returns:
            Tuple of (success, list_of_missing_packages)
        """
        if not silent:
            self.print_status("Checking dependencies for APZmedia PSD Tools...", "INFO")
            self.print_status("=" * 50, "INFO")
        
        missing_packages = []
        installed_packages = []
        
        # Check each required package
        for package_name, pip_name, flags in self.required_packages:
            if not silent:
                self.print_status(f"Checking {package_name}...", "INFO")
            
            if self.check_package_available(package_name):
                if not silent:
                    self.print_status(f"✓ {package_name} is available", "SUCCESS")
                installed_packages.append(package_name)
            else:
                if not silent:
                    self.print_status(f"✗ {package_name} is missing", "WARNING")
                missing_packages.append((package_name, pip_name, flags))
        
        # Install missing packages
        if missing_packages:
            if not silent:
                self.print_status(f"Installing {len(missing_packages)} missing packages...", "INFO")
            
            success_count = 0
            for package_name, pip_name, flags in missing_packages:
                if self.install_package(package_name, pip_name, flags):
                    success_count += 1
                    installed_packages.append(package_name)
                else:
                    if not silent:
                        self.print_status(f"Failed to install {package_name}", "ERROR")
            
            if not silent:
                self.print_status(f"Installation complete: {success_count}/{len(missing_packages)} packages installed", 
                                "SUCCESS" if success_count == len(missing_packages) else "WARNING")
        else:
            if not silent:
                self.print_status("All dependencies are already installed!", "SUCCESS")
        
        # Final verification
        all_available = True
        for package_name, _, _ in self.required_packages:
            if not self.check_package_available(package_name):
                all_available = False
                if not silent:
                    self.print_status(f"Verification failed: {package_name} still not available", "ERROR")
        
        if not silent:
            if all_available:
                self.print_status("🎉 All dependencies are ready!", "SUCCESS")
            else:
                self.print_status("⚠️ Some dependencies may not be working properly", "WARNING")
        
        return all_available, [pkg[0] for pkg in missing_packages]
    
    def get_installation_summary(self) -> str:
        """Get a summary of the installation process"""
        return "\n".join(self.installation_log)

# Global installer instance
_installer = None

def get_installer() -> AutoInstaller:
    """Get the global installer instance"""
    global _installer
    if _installer is None:
        _installer = AutoInstaller()
    return _installer

def auto_install_dependencies(silent: bool = False) -> bool:
    """
    Automatically install missing dependencies
    
    Args:
        silent: If True, suppress most output
        
    Returns:
        True if all dependencies are available, False otherwise
    """
    installer = get_installer()
    success, missing = installer.check_and_install_dependencies(silent=silent)
    return success

def check_dependencies_only() -> bool:
    """
    Check if all dependencies are available without installing
    
    Returns:
        True if all dependencies are available, False otherwise
    """
    installer = get_installer()
    all_available = True
    
    for package_name, _, _ in installer.required_packages:
        if not installer.check_package_available(package_name):
            all_available = False
            break
    
    return all_available

# Convenience function for quick dependency check and install
def ensure_dependencies() -> bool:
    """
    Ensure all dependencies are available, installing if necessary
    
    Returns:
        True if all dependencies are available, False otherwise
    """
    if check_dependencies_only():
        return True
    else:
        return auto_install_dependencies(silent=True)

if __name__ == "__main__":
    # Allow running this script directly for testing
    print("APZmedia PSD Tools - Automatic Dependency Installer")
    print("=" * 60)
    
    success = auto_install_dependencies(silent=False)
    
    if success:
        print("\n✅ All dependencies are ready!")
        sys.exit(0)
    else:
        print("\n❌ Some dependencies could not be installed.")
        sys.exit(1)
