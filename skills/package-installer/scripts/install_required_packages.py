#!/usr/bin/env python3
"""
Script to install required packages for WALLACE system
Installs: chromadb, openai, yfinance, aiohttp, pandas, numpy, python-dotenv
"""

import sys
import os
import json
from typing import List, Tuple

# Add scripts to path
sys.path.append('scripts')

from package_installer import PackageInstaller
from environment_manager import EnvironmentManager

def main():
    """Install required packages with security checks"""
    print("=" * 60)
    print("INSTALLATION DES BIBLIOTHEQUES REQUISES POUR WALLACE")
    print("=" * 60)
    
    # Initialize components
    installer = PackageInstaller()
    env_manager = EnvironmentManager()
    
    # Required packages list
    required_packages = [
        {
            "name": "chromadb",
            "version": None,
            "description": "Vector database for AI applications"
        },
        {
            "name": "openai", 
            "version": None,
            "description": "OpenAI API client for GPT models"
        },
        {
            "name": "yfinance",
            "version": None,
            "description": "Yahoo Finance market data downloader"
        },
        {
            "name": "aiohttp",
            "version": None,
            "description": "Async HTTP client/server framework"
        },
        {
            "name": "pandas",
            "version": None,
            "description": "Data manipulation and analysis library"
        },
        {
            "name": "numpy",
            "version": None,
            "description": "Fundamental package for scientific computing"
        },
        {
            "name": "python-dotenv",
            "version": None,
            "description": "Python dotenv file parsing"
        }
    ]
    
    print(f"\n📋 Packages à installer: {len(required_packages)}")
    print("-" * 60)
    
    for pkg in required_packages:
        print(f"• {pkg['name']}: {pkg['description']}")
    
    print("\n" + "=" * 60)
    print("🔒 VERIFICATION DE SECURITE")
    print("=" * 60)
    
    # Check environment
    default_env = "venv_ninja_moltbot"
    env_info = env_manager.get_environment_info(default_env)
    
    if not env_info:
        print(f"⚠️  L'environnement '{default_env}' n'existe pas")
        print("🔄 Création de l'environnement...")
        
        success, message = env_manager.create_environment(default_env)
        if success:
            print(f"✅ Environnement '{default_env}' créé avec succès")
            env_info = env_manager.get_environment_info(default_env)
        else:
            print(f"❌ Échec de création: {message}")
            return False
    
    print(f"\n📁 Environnement cible: {default_env}")
    print(f"📍 Chemin: {env_info['path']}")
    print(f"🐍 Python: {env_info['python_version']}")
    
    # Install packages with security checks
    successful_installs = []
    failed_installs = []
    
    for package_info in required_packages:
        package_name = package_info["name"]
        
        print(f"\n🔄 Installation de: {package_name}")
        print("-" * 40)
        
        try:
            # Perform security check first
            from security_checker import SecurityChecker
            checker = SecurityChecker()
            
            print("🔍 Vérification de sécurité en cours...")
            safety_report = checker.check_package_safety(package_name)
            
            print(f"📊 Rapport de sécurité:")
            print(f"   Status: {safety_report['overall_status']}")
            print(f"   Score: {safety_report['score']}/100")
            
            if safety_report['warnings']:
                print(f"⚠️  Avertissements:")
                for warning in safety_report['warnings']:
                    print(f"   • {warning}")
            
            if safety_report['score'] < 70:
                print(f"❌ Score sécurité trop bas ({safety_report['score']}/100) - Installation refusée")
                failed_installs.append(package_info)
                continue
            
            # Ask for user approval
            if safety_report['warnings']:
                print(f"\n⚠️  Avertissements détectés - Confirmer installation? (oui/non): ", end="")
                response = input().strip().lower()
                if response != 'oui':
                    print(f"❌ Installation annulée par l'utilisateur")
                    failed_installs.append(package_info)
                    continue
            
            # Install package
            print(f"\n🚀 Installation en cours...")
            success, message = installer.install_package(
                package_name=package_name,
                version=None,
                env_name=default_env,
                force=False
            )
            
            if success:
                print(f"✅ Installation réussie: {message}")
                successful_installs.append(package_info)
                
                # Verify installation
                installed_version = installer._get_installed_version(package_name, default_env)
                if installed_version:
                    print(f"📦 Version installée: {installed_version}")
            else:
                print(f"❌ Échec d'installation: {message}")
                failed_installs.append(package_info)
                
        except Exception as e:
            print(f"❌ Erreur lors de l'installation de {package_name}: {str(e)}")
            failed_installs.append(package_info)
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL D'INSTALLATION")
    print("=" * 60)
    
    print(f"✅ Installations réussies: {len(successful_installs)}/{len(required_packages)}")
    print(f"❌ Échecs: {len(failed_installs)}/{len(required_packages)}")
    
    if successful_installs:
        print(f"\n🎉 Packages installés avec succès:")
        for pkg in successful_installs:
            installed_version = installer._get_installed_version(pkg['name'], default_env)
            print(f"   • {pkg['name']}: {installed_version or 'version inconnue'}")
    
    if failed_installs:
        print(f"\n💔 Packages non installés:")
        for pkg in failed_installs:
            print(f"   • {pkg['name']}")
    
    # Test installation
    print(f"\n🧪 TEST DES INSTALLATIONS")
    print("-" * 30)
    
    for package_info in successful_installs:
        package_name = package_info["name"]
        try:
            # Test import
            test_env = {
                'venv_ninja_moltbot': f"venv_ninja_moltbot\\Scripts\\python.exe" if os.name == 'nt' else "venv_ninja_moltbot/bin/python"
            }
            
            import subprocess
            test_script = f"""
import sys
sys.path.insert(0, 'G:\\\\PROGRAMMES_FILES\\\\Github\\\\Finance_Agent\\\\LABO\\\\GIT STOCKAGE\\\\CREATION\\\\PERSONNAL ASSISTANCE\\\\moltbot\\\\venv_ninja_moltbot\\\\Lib\\\\site-packages')
try:
    import {package_name}
    print(f"✅ {package_name} importé avec succès")
except ImportError as e:
    print(f"❌ {package_name} import échoué: {{e}}")
"""
            
            result = subprocess.run([sys.executable, '-c', test_script], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"✅ {package_name}: Test OK")
            else:
                print(f"❌ {package_name}: Test échoué - {result.stderr.strip()}")
                
        except Exception as e:
            print(f"❌ {package_name}: Test erreur - {str(e)}")
    
    print(f"\n{'='*60}")
    if len(successful_installs) == len(required_packages):
        print("🎉 TOUS LES PACKAGES ONT ÉTÉ INSTALLÉS AVEC SUCCÈS!")
        print("WALLACE EST PRÊT POUR LA PROCHAINE MISSION!")
    else:
        print(f"⚠️  {len(failed_installs)} package(s) n'ont pas pu être installés")
        print("Veuillez vérifier les échecs et réessayer")
    
    print(f"{'='*60}")
    
    return len(successful_installs) == len(required_packages)

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Installation interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur critique: {str(e)}")
        sys.exit(1)