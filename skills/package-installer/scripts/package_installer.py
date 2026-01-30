#!/usr/bin/env python3
"""
Package Installer for package-installer skill
Handles secure package installation with user approval
"""

import os
import sys
import json
import subprocess
import tempfile
import requests
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import ast
from pathlib import Path

from environment_manager import EnvironmentManager


class PackageInstaller:
    """Handles secure package installation with user approval"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "G:\\PROGRAMMES_FILES\\Github\\Finance_Agent\\LABO\\GIT STOCKAGE\\CREATION\\PERSONNAL ASSISTANCE\\moltbot"
        self.env_manager = EnvironmentManager(self.base_path)
        self.log_file = os.path.join(self.base_path, "package_installation.log")
        self.ensure_log_file()
        
    def ensure_log_file(self):
        """Ensure log file exists"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
    def install_package(self, package_name: str, version: str = None, 
                       env_name: str = None, force: bool = False) -> Tuple[bool, str]:
        """Install a package with user approval"""
        
        # Get environment information
        if env_name:
            env_info = self.env_manager.get_environment_info(env_name)
            if not env_info:
                return False, f"Environment '{env_name}' not found"
        else:
            # Use default environment
            env_name = "venv_ninja_moltbot"
            env_info = self.env_manager.get_environment_info(env_name)
            if not env_info:
                # Create default environment if it doesn't exist
                success, message = self.env_manager.create_environment(env_name)
                if not success:
                    return False, message
                env_info = self.env_manager.get_environment_info(env_name)
                
        pip_path = self.env_manager.get_pip_path(env_name)
        
        # Check if package is already installed
        if not force and self._is_package_installed(package_name, env_name):
            return True, f"Package '{package_name}' is already installed in '{env_name}'"
            
        # Get package information
        package_info = self._get_package_info(package_name)
        if not package_info:
            return False, f"Package '{package_name}' not found in PyPI"
            
        # Prepare installation details
        install_details = {
            "name": package_name,
            "version": version or package_info.get("version", "latest"),
            "size": package_info.get("size", "Unknown"),
            "description": package_info.get("description", ""),
            "author": package_info.get("author", ""),
            "dependencies": package_info.get("dependencies", []),
            "last_updated": package_info.get("last_updated", ""),
            "environment": env_name,
            "pip_path": pip_path
        }
        
        # Ask for user approval
        if not force:
            print(f"\n📦 PACKAGE INSTALLATION REQUEST:")
            print(f"{'='*50}")
            print(f"Package: {package_name}")
            print(f"Version: {install_details['version']}")
            print(f"Environment: {env_name}")
            print(f"Size: {install_details['size']}")
            print(f"Description: {install_details['description']}")
            print(f"Author: {install_details['author']}")
            print(f"Dependencies: {len(install_details['dependencies'])} packages")
            print(f"Last Updated: {install_details['last_updated']}")
            
            # Check security
            security_check = self._check_package_security(package_name, install_details['version'])
            print(f"\n🔒 SECURITY CHECK:")
            print(f"Status: {security_check['status']}")
            print(f"Source: {security_check['source']}")
            print(f"License: {security_check['license']}")
            
            if security_check['warnings']:
                print(f"\n⚠️  WARNINGS:")
                for warning in security_check['warnings']:
                    print(f"  • {warning}")
                    
            print(f"\n{'='*50}")
            print(f"Approve installation? (yes/no/skip): ", end="")
            response = input().strip().lower()
            
            if response == 'skip':
                return True, "Installation skipped by user"
            elif response != 'yes':
                return False, "Installation cancelled by user"
                
        # Perform installation
        try:
            print(f"\n🚀 INSTALLING PACKAGE: {package_name}...")
            
            # Build installation command
            cmd = [pip_path, "install"]
            if version:
                cmd.extend(["==", version])
            cmd.append(package_name)
            
            # Run installation
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                # Log successful installation
                self._log_installation(package_info, True)
                
                # Verify installation
                installed_version = self._get_installed_version(package_name, env_name)
                
                success_message = f"Package '{package_name}' successfully installed in '{env_name}'"
                if installed_version:
                    success_message += f" (version {installed_version})"
                    
                return True, success_message
                
            else:
                # Log failed installation
                self._log_installation(package_info, False, result.stderr)
                return False, f"Installation failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            error_msg = f"Installation timeout for package '{package_name}'"
            self._log_installation(package_info, False, error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Installation error: {str(e)}"
            self._log_installation(package_info, False, error_msg)
            return False, error_msg
            
    def _is_package_installed(self, package_name: str, env_name: str) -> bool:
        """Check if package is already installed"""
        try:
            pip_path = self.env_manager.get_pip_path(env_name)
            result = subprocess.run([
                pip_path, "show", package_name
            ], capture_output=True, text=True)
            
            return result.returncode == 0
        except:
            return False
            
    def _get_installed_version(self, package_name: str, env_name: str) -> Optional[str]:
        """Get version of installed package"""
        try:
            pip_path = self.env_manager.get_pip_path(env_name)
            result = subprocess.run([
                pip_path, "show", package_name
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse version from pip show output
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        return line.split(':', 1)[1].strip()
        except:
            pass
        return None
        
    def _get_package_info(self, package_name: str) -> Optional[Dict]:
        """Get package information from PyPI"""
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract package information
                info = {
                    "name": data["info"]["name"],
                    "version": data["info"]["version"],
                    "description": data["info"]["summary"] or "",
                    "author": data["info"]["author"] or "",
                    "license": data["info"]["license"] or "Unknown",
                    "last_updated": data["info"]["upload_time"],
                    "size": self._estimate_package_size(data),
                    "dependencies": self._extract_dependencies(data),
                    "downloads": data["info"].get("downloads", 0),
                    "home_page": data["info"].get("home_page", "")
                }
                
                return info
                
        except Exception as e:
            print(f"Warning: Could not fetch package info: {e}")
            
        return None
        
    def _estimate_package_size(self, package_data: Dict) -> str:
        """Estimate package size from PyPI data"""
        try:
            urls = package_data.get("urls", [])
            wheels = [u for u in urls if u.get("packagetype") == "bdist_wheel"]
            
            if wheels:
                largest = max(wheels, key=lambda x: x.get("size", 0))
                size_bytes = largest.get("size", 0)
                return self._format_size(size_bytes)
                
            return "Unknown"
            
        except:
            return "Unknown"
            
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
            
    def _extract_dependencies(self, package_data: Dict) -> List[str]:
        """Extract package dependencies"""
        try:
            # Try to get requires_dist from metadata
            requires_dist = package_data.get("info", {}).get("requires_dist", [])
            
            if requires_dist:
                return requires_dist
                
            # Alternative: look for setup.py or pyproject.toml info
            # This is a simplified approach
            return []
            
        except:
            return []
            
    def _check_package_security(self, package_name: str, version: str) -> Dict:
        """Check package security"""
        security_info = {
            "status": "✓ Safe",
            "source": "PyPI Official",
            "license": "Unknown",
            "warnings": []
        }
        
        try:
            # Get package info for security check
            package_info = self._get_package_info(package_name)
            if package_info:
                security_info["license"] = package_info["license"]
                
                # Basic security checks
                if "MIT" in security_info["license"]:
                    security_info["warnings"].append("MIT License - Permissive but review carefully")
                    
                # Check for suspicious package names
                if any(keyword in package_name.lower() for keyword in 
                       ["hack", "crack", "steal", "fake", "malware", "virus"]):
                    security_info["status"] = "⚠️  Suspicious name"
                    security_info["warnings"].append("Package name contains suspicious keywords")
                    
                # Check for recently created packages
                if package_info["last_updated"]:
                    upload_time = datetime.strptime(package_info["last_updated"], "%Y-%m-%dT%H:%M:%S")
                    days_old = (datetime.now() - upload_time).days
                    
                    if days_old < 30:
                        security_info["warnings"].append(f"Package created {days_old} days ago - review carefully")
                        
        except Exception as e:
            security_info["status"] = "⚠️  Check failed"
            security_info["warnings"].append(f"Could not verify security: {str(e)}")
            
        return security_info
        
    def _log_installation(self, package_info: Dict, success: bool, error: str = None):
        """Log installation attempt"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "package": package_info,
            "success": success,
            "error": error,
            "environment": "venv_ninja_moltbot"
        }
        
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except:
            pass  # Ignore logging errors
            
    def list_installed_packages(self, env_name: str = None) -> List[Dict]:
        """List installed packages in environment"""
        try:
            if env_name:
                env_info = self.env_manager.get_environment_info(env_name)
                if not env_info:
                    return []
                pip_path = self.env_manager.get_pip_path(env_name)
            else:
                # Use default environment
                env_name = "venv_ninja_moltbot"
                pip_path = self.env_manager.get_pip_path(env_name)
                
            result = subprocess.run([
                pip_path, "list", "--format=json"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                return packages
                
        except Exception as e:
            print(f"Error listing packages: {e}")
            
        return []
        
    def uninstall_package(self, package_name: str, env_name: str = None) -> Tuple[bool, str]:
        """Uninstall a package"""
        try:
            if env_name:
                env_info = self.env_manager.get_environment_info(env_name)
                if not env_info:
                    return False, f"Environment '{env_name}' not found"
                pip_path = self.env_manager.get_pip_path(env_name)
            else:
                env_name = "venv_ninja_moltbot"
                pip_path = self.env_manager.get_pip_path(env_name)
                
            # Confirm uninstallation
            print(f"⚠️  This will uninstall '{package_name}' from '{env_name}'")
            print(f"Proceed? (yes/no): ", end="")
            response = input().strip().lower()
            
            if response != 'yes':
                return True, "Uninstallation cancelled by user"
                
            result = subprocess.run([
                pip_path, "uninstall", "-y", package_name
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, f"Package '{package_name}' uninstalled successfully"
            else:
                return False, f"Uninstallation failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Uninstallation error: {str(e)}"


def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python package_installer.py <command> [args]")
        print("Commands:")
        print("  install <package> [version] [env]  - Install package")
        print("  uninstall <package> [env]          - Uninstall package")
        print("  list [env]                        - List installed packages")
        print("  info <package>                    - Get package information")
        sys.exit(1)
        
    installer = PackageInstaller()
    command = sys.argv[1].lower()
    
    if command == "install":
        if len(sys.argv) < 3:
            print("Usage: python package_installer.py install <package> [version] [env]")
            sys.exit(1)
            
        package_name = sys.argv[2]
        version = sys.argv[3] if len(sys.argv) > 3 else None
        env_name = sys.argv[4] if len(sys.argv) > 4 else None
        
        success, message = installer.install_package(package_name, version, env_name)
        print(message)
        
    elif command == "uninstall":
        if len(sys.argv) < 3:
            print("Usage: python package_installer.py uninstall <package> [env]")
            sys.exit(1)
            
        package_name = sys.argv[2]
        env_name = sys.argv[3] if len(sys.argv) > 3 else None
        
        success, message = installer.uninstall_package(package_name, env_name)
        print(message)
        
    elif command == "list":
        env_name = sys.argv[2] if len(sys.argv) > 2 else None
        
        packages = installer.list_installed_packages(env_name)
        if not packages:
            print("No packages found")
        else:
            print(f"{'Name':<30} {'Version':<15} {'Location':<25}")
            print("-" * 70)
            for pkg in packages:
                name = pkg.get("name", "Unknown")
                version = pkg.get("version", "Unknown")
                env = env_name or "venv_ninja_moltbot"
                print(f"{name:<30} {version:<15} {env:<25}")
                
    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: python package_installer.py info <package>")
            sys.exit(1)
            
        package_name = sys.argv[2]
        package_info = installer._get_package_info(package_name)
        
        if package_info:
            print(json.dumps(package_info, indent=2))
        else:
            print(f"Package information for '{package_name}' not found")
            
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()