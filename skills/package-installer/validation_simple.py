#!/usr/bin/env python3
"""
Simple validation tests for package-installer skill
"""

import sys
import os
import json
import subprocess
from datetime import datetime

def test_skill_structure():
    """Test skill file structure"""
    print("=== TEST 1: Skill Structure ===")
    required_files = [
        'SKILL.md',
        'requirements.txt',
        'scripts/environment_manager.py',
        'scripts/package_installer.py',
        'scripts/security_checker.py',
        'references/package_database.json',
        'references/security_guidelines.md',
        'references/approved_packages_list.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        return False, f"Fichiers manquants: {missing_files}"
    
    print("All required files present")
    return True, "Structure du skill complete"

def test_environment_manager():
    """Test Environment Manager functionality"""
    print("\n=== TEST 2: Environment Manager ===")
    try:
        sys.path.append('scripts')
        from environment_manager import EnvironmentManager
        
        env_manager = EnvironmentManager()
        envs = env_manager.list_environments()
        
        print(f"Environnements disponibles: {len(envs)}")
        for env in envs:
            print(f"  - {env['name']}: {env['size_mb']:.1f}MB")
            
        return True, "EnvironmentManager fonctionne"
        
    except Exception as e:
        return False, f"EnvironmentManager erreur: {e}"

def test_security_checker():
    """Test Security Checker functionality"""
    print("\n=== TEST 3: Security Checker ===")
    try:
        sys.path.append('scripts')
        from security_checker import SecurityChecker
        
        checker = SecurityChecker()
        
        # Tester un package sûr
        safety_report = checker.check_package_safety('requests')
        print(f"Status: {safety_report['overall_status']}")
        print(f"Score: {safety_report['score']}/100")
        
        return True, "SecurityChecker fonctionne"
        
    except Exception as e:
        return False, f"SecurityChecker erreur: {e}"

def test_package_database():
    """Test Package Database"""
    print("\n=== TEST 4: Package Database ===")
    try:
        with open('references/package_database.json', 'r') as f:
            db = json.load(f)
        
        print(f"Categories: {len(db['trusted_packages'])}")
        total_packages = sum(len(packages) for packages in db['trusted_packages'].values())
        print(f"Total packages: {total_packages}")
        print(f"Whitelist: {len(db['security_whitelist'])} packages")
        
        return True, "Package database valide"
        
    except Exception as e:
        return False, f"Package database erreur: {e}"

def test_main_commands():
    """Test command line commands"""
    print("\n=== TEST 5: Command Line Commands ===")
    try:
        # Test environment listing
        result = subprocess.run([sys.executable, 'scripts/environment_manager.py', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("Environment listing command works")
        else:
            print(f"Environment listing command failed: {result.stderr}")
            return False, f"Environment listing failed"
        
        # Test security check
        result = subprocess.run([sys.executable, 'scripts/security_checker.py', 'requests'], 
                              capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print("Security check command works")
        else:
            print(f"Security check command failed: {result.stderr}")
            return False, f"Security check failed"
        
        return True, "Commandes operationnelles"
        
    except Exception as e:
        return False, f"Commandes erreur: {e}"

def main():
    """Run all validation tests"""
    print("VALIDATION TESTS - PACKAGE-INSTALLER SKILL")
    print("=" * 50)
    
    tests = [
        test_skill_structure,
        test_environment_manager,
        test_security_checker,
        test_package_database,
        test_main_commands
    ]
    
    results = []
    
    for test_func in tests:
        try:
            success, message = test_func()
            status = "PASS" if success else "FAIL"
            print(f"{status}: {message}")
            results.append((test_func.__name__, success, message))
        except Exception as e:
            print(f"ERROR in {test_func.__name__}: {e}")
            results.append((test_func.__name__, False, str(e)))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Tests passes: {passed}/{total}")
    
    if passed == total:
        print("\nALL TESTS PASSED - SKILL READY FOR PRODUCTION")
        return 0
    else:
        print(f"\n{total - passed} tests failed - SKILL NEEDS FIXES")
        return 1

if __name__ == "__main__":
    exit(main())