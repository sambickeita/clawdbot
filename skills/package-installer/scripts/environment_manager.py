#!/usr/bin/env python3
"""
Environment Manager for package-installer skill
Handles creation, deletion, and activation of virtual environments
"""

import os
import sys
import subprocess
import json
import venv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil

class EnvironmentManager:
    """Manages Python virtual environments"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "G:\\PROGRAMMES_FILES\\Github\\Finance_Agent\\LABO\\GIT STOCKAGE\\CREATION\\PERSONNAL ASSISTANCE\\moltbot"
        self.envs_path = os.path.join(self.base_path, "virtual_envs")
        self.ensure_envs_directory()
        
    def ensure_envs_directory(self):
        """Ensure the environments directory exists"""
        os.makedirs(self.envs_path, exist_ok=True)
        
    def list_environments(self) -> List[Dict]:
        """List all available environments"""
        environments = []
        
        if not os.path.exists(self.envs_path):
            return environments
            
        for env_name in os.listdir(self.envs_path):
            env_path = os.path.join(self.envs_path, env_name)
            if os.path.isdir(env_path):
                py_exe = self.get_python_path(env_name)
                info = {
                    "name": env_name,
                    "path": env_path,
                    "python_executable": py_exe,
                    "size_mb": self.get_directory_size(env_path) / (1024*1024),
                    "exists": os.path.exists(py_exe)
                }
                environments.append(info)
                
        return environments
        
    def create_environment(self, env_name: str, python_version: str = None) -> Tuple[bool, str]:
        """Create a new virtual environment"""
        try:
            env_path = os.path.join(self.envs_path, env_name)
            
            # Check if environment already exists
            if os.path.exists(env_path):
                return False, f"Environment '{env_name}' already exists"
                
            # Create the environment
            if python_version:
                # For specific Python version, try to find the executable
                python_exe = self.find_python_executable(python_version)
                if not python_exe:
                    return False, f"Python {python_version} not found"
                    
                # Create environment with specific Python version
                subprocess.run([
                    python_exe, "-m", "venv", 
                    "--clear", env_path
                ], check=True, capture_output=True)
            else:
                # Use current Python version
                venv.create(env_path, with_pip=True)
                
            # Verify creation
            py_path = self.get_python_path(env_name)
            if not os.path.exists(py_path):
                return False, f"Failed to create Python executable in environment '{env_name}'"
                
            # Install basic packages
            self._install_basic_packages(env_name)
            
            return True, f"Environment '{env_name}' created successfully"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to create environment: {str(e)}"
        except Exception as e:
            return False, f"Error creating environment: {str(e)}"
            
    def remove_environment(self, env_name: str) -> Tuple[bool, str]:
        """Remove a virtual environment"""
        try:
            env_path = os.path.join(self.envs_path, env_name)
            
            if not os.path.exists(env_path):
                return False, f"Environment '{env_name}' does not exist"
                
            # Ask for confirmation before deletion
            print(f"WARNING: This will permanently delete environment '{env_name}'")
            print(f"Path: {env_path}")
            print("Are you sure? (yes/no): ", end="")
            confirm = input().strip().lower()
            
            if confirm != 'yes':
                return False, "Environment deletion cancelled"
                
            # Remove the environment
            shutil.rmtree(env_path)
            return True, f"Environment '{env_name}' removed successfully"
            
        except Exception as e:
            return False, f"Error removing environment: {str(e)}"
            
    def get_python_path(self, env_name: str) -> str:
        """Get the Python executable path for an environment"""
        # Support for both Windows and Unix-like systems
        if sys.platform == "win32":
            return os.path.join(self.envs_path, env_name, "Scripts", "python.exe")
        else:
            return os.path.join(self.envs_path, env_name, "bin", "python")
            
    def get_pip_path(self, env_name: str) -> str:
        """Get the pip executable path for an environment"""
        if sys.platform == "win32":
            return os.path.join(self.envs_path, env_name, "Scripts", "pip.exe")
        else:
            return os.path.join(self.envs_path, env_name, "bin", "pip")
            
    def activate_environment(self, env_name: str) -> str:
        """Get activation command for an environment"""
        if sys.platform == "win32":
            return f"CALL {os.path.join(self.envs_path, env_name, 'Scripts', 'activate.bat')}"
        else:
            return f"source {os.path.join(self.envs_path, env_name, 'bin', 'activate')}"
            
    def find_python_executable(self, version: str) -> Optional[str]:
        """Find Python executable for a specific version"""
        possible_names = [
            f"python{version}",
            f"python{version.split('.')[0]}.{version.split('.')[1]}",
            f"python{version.split('.')[0]}",
            "python"
        ]
        
        for name in possible_names:
            try:
                result = subprocess.run([name, "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0 and version in result.stdout:
                    return name
            except:
                continue
                
        return None
        
    def _install_basic_packages(self, env_name: str):
        """Install basic packages in the environment"""
        try:
            pip_path = self.get_pip_path(env_name)
            subprocess.run([
                pip_path, "install", "--upgrade", "pip", "setuptools", "wheel"
            ], check=True, capture_output=True)
        except:
            # Ignore errors for basic packages
            pass
            
    def get_directory_size(self, path: str) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
        return total_size
        
    def get_environment_info(self, env_name: str) -> Optional[Dict]:
        """Get detailed information about an environment"""
        env_path = os.path.join(self.envs_path, env_name)
        
        if not os.path.exists(env_path):
            return None
            
        py_path = self.get_python_path(env_name)
        pip_path = self.get_pip_path(env_name)
        
        info = {
            "name": env_name,
            "path": env_path,
            "python_executable": py_path,
            "pip_executable": pip_path,
            "size_bytes": self.get_directory_size(env_path),
            "python_version": self._get_python_version(py_path),
            "platform": sys.platform,
            "exists": os.path.exists(py_path)
        }
        
        return info
        
    def _get_python_version(self, python_path: str) -> str:
        """Get Python version from executable"""
        try:
            result = subprocess.run([python_path, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().replace("Python ", "")
        except:
            pass
        return "Unknown"


def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python environment_manager.py <command> [args]")
        print("Commands:")
        print("  list                    - List all environments")
        print("  create <name> [version] - Create new environment")
        print("  remove <name>           - Remove environment")
        print("  info <name>             - Get environment info")
        sys.exit(1)
        
    manager = EnvironmentManager()
    command = sys.argv[1].lower()
    
    if command == "list":
        environments = manager.list_environments()
        if not environments:
            print("No environments found")
        else:
            print(f"{'Name':<20} {'Size (MB)':<10} {'Python':<10} {'Status':<10}")
            print("-" * 50)
            for env in environments:
                status = "✓" if env["exists"] else "✗"
                print(f"{env['name']:<20} {env['size_mb']:<10.1f} {env['python_executable'].split('/')[-1]:<10} {status:<10}")
                
    elif command == "create":
        if len(sys.argv) < 3:
            print("Usage: python environment_manager.py create <name> [python_version]")
            sys.exit(1)
            
        env_name = sys.argv[2]
        python_version = sys.argv[3] if len(sys.argv) > 3 else None
        
        success, message = manager.create_environment(env_name, python_version)
        print(message)
        
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: python environment_manager.py remove <name>")
            sys.exit(1)
            
        env_name = sys.argv[2]
        success, message = manager.remove_environment(env_name)
        print(message)
        
    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: python environment_manager.py info <name>")
            sys.exit(1)
            
        env_name = sys.argv[2]
        info = manager.get_environment_info(env_name)
        
        if info:
            print(json.dumps(info, indent=2))
        else:
            print(f"Environment '{env_name}' not found")
            
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()