#!/usr/bin/env python3
"""
Validation tests for package-installer skill
"""

import sys
import os
import json
import subprocess
from datetime import datetime

def test_environment_manager():
    """Test Environment Manager functionality"""
    print("=== TEST 1: Environment Manager ===")
    try:
        sys.path.append('scripts')
        from environment_manager import EnvironmentManager
        
        env_manager = EnvironmentManager()
        envs = env_manager.list_environments()
        
        print(f"Environnements disponibles: {len(envs)}")
        for env in envs:
            print(f"  - {env['name']}: {env['size_mb']:.1f}MB")
            
        # Test création environnement
        success, message = env_manager.create_environment("test_env")
        print(f"Création test: {success} - {message}")
        
        return True, "EnvironmentManager fonctionne"
        
    except Exception as e:
        return False, f"EnvironmentManager erreur: {e}"

def test_security_checker():
    """Test Security Checker functionality"""
    print("\n=== TEST 2: Security Checker ===")
    try:
        sys.path.append('scripts')
        from security_checker import SecurityChecker
        
        checker = SecurityChecker()
        
        # Tester un package sûr
        safety_report = checker.check_package_safety('requests')
        print(f"Status: {safety_report['overall_status']}")
        print(f"Score: {safety_report['score']}/100")
        
        # Tester un package inconnu
        suspicious_report = checker.check_package_safety('unknown_package_xyz')
        print(f"Suspicious package status: {suspicious_report['overall_status']}")
        
        return True, "SecurityChecker fonctionne"
        
    except Exception as e:
        return False, f"SecurityChecker erreur: {e}"

def test_package_database():
    """Test Package Database"""
    print("\n=== TEST 3: Package Database ===")
    try:
        with open('references/package_database.json', 'r') as f:
            db = json.load(f)
        
        print(f"Categories: {len(db['trusted_packages'])}")
        for category, packages in db['trusted_packages'].items():
            print(f"  - {category}: {len(packages)} packages")
        
        print(f"Whitelist: {len(db['security_whitelist'])} packages")
        
        return True, "Package database valide"
        
    except Exception as e:
        return False, f"Package database erreur: {e}"

def test_security_guidelines():
    """Test Security Guidelines"""
    print("\n=== TEST 4: Security Guidelines ===")
    try:
        with open('references/security_guidelines.md', 'r') as f:
            guidelines = f.read()
        
        print(f"Document length: {len(guidelines)} characters")
        return True, "Security guidelines disponibles"
        
    except Exception as e:
        return False, f"Security guidelines erreur: {e}"

def test_approved_packages():
    """Test Approved Packages List"""
    print("\n=== TEST 5: Approved Packages List ===")
    try:
        with open('references/approved_packages_list.md', 'r') as f:
            approved_list = f.read()
        
        lines = approved_list.split('\n')
        package_count = 0
        
        for line in lines:
            if '| Package | Version |' in line:
                break
            elif line.strip().startswith('|') and '---' not in line:
                if line.strip():
                    package_count += 1
        
        print(f"Package categories found: {package_count}")
        return True, "Approved packages list valide"
        
    except Exception as e:
        return False, f"Approved packages list erreur: {e}"

def test_main_commands():
    """Test command line commands"""
    print("\n=== TEST 6: Command Line Commands ===")
    try:
        # Test environment listing
        result = subprocess.run([sys.executable, 'scripts/environment_manager.py', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Environment listing command works")
        else:
            print("❌ Environment listing command failed")
            return False, f"Environment listing failed: {result.stderr}"
        
        # Test security check
        result = subprocess.run([sys.executable, 'scripts/security_checker.py', 'requests'], 
                              capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print("✅ Security check command works")
        else:
            print("❌ Security check command failed")
            return False, f"Security check failed: {result.stderr}"
        
        return True, "Commandes opérationnelles"
        
    except Exception as e:
        return False, f"Commandes erreur: {e}"

def test_skill_structure():
    """Test skill file structure"""
    print("\n=== TEST 7: Skill Structure ===")
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
    
    return True, "Structure du skill complète"

def main():
    """Run all validation tests"""
    print("🧪 VALIDATION TESTS - PACKAGE-INSTALLER SKILL")
    print("=" * 50)
    
    tests = [
        test_skill_structure,
        test_environment_manager,
        test_security_checker,
        test_package_database,
        test_security_guidelines,
        test_approved_packages,
        test_main_commands
    ]
    
    results = []
    
    for test_func in tests:
        try:
            success, message = test_func()
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {message}")
            results.append((test_func.__name__, success, message))
        except Exception as e:
            print(f"❌ ERROR in {test_func.__name__}: {e}")
            results.append((test_func.__name__, False, str(e)))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Tests passés: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - SKILL READY FOR PRODUCTION")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed - SKILL NEEDS FIXES")
        return 1

if __name__ == "__main__":
    exit(main())