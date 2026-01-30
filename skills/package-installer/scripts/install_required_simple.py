#!/usr/bin/env python3
"""
Simple script to install required packages for WALLACE system
"""

import sys
import os
import subprocess

def install_packages():
    """Install required packages using venv_ninja_moltbot"""
    print("============================================================")
    print("INSTALLATION DES BIBLIOTHEQUES REQUISES POUR WALLACE")
    print("============================================================")
    
    packages = [
        "chromadb",
        "openai",
        "yfinance",
        "aiohttp",
        "pandas",
        "numpy",
        "python-dotenv"
    ]
    
    print(f"\nPackages a installer: {len(packages)}")
    print("-" * 60)
    
    for pkg in packages:
        print(f"* {pkg}")
    
    print("\n" + "=" * 60)
    print("VERIFICATION DE L'ENVIRONNEMENT")
    print("=" * 60)
    
    # Check if venv exists
    venv_path = "venv_ninja_moltbot"
    if os.name == 'nt':
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_path = os.path.join(venv_path, "bin", "python")
    
    if not os.path.exists(python_path):
        print(f"ERREUR: L'environnement {venv_path} n'existe pas")
        return False
    
    print(f"Environnement: {venv_path}")
    print(f"Python executable: {python_path}")
    
    # Test if python works
    try:
        result = subprocess.run([python_path, "--version"], 
                              capture_output=True, text=True)
        print(f"Version Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"ERREUR: Impossible de verifier Python: {e}")
        return False
    
    # Install packages
    print("\n" + "=" * 60)
    print("INSTALLATION DES PACKAGES")
    print("=" * 60)
    
    successful = []
    failed = []
    
    for package in packages:
        print(f"\nInstallation de: {package}")
        print("-" * 30)
        
        try:
            # First check if package already exists
            result = subprocess.run([python_path, "-m", "pip", "show", package], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Package deja installe: {result.stdout}")
                successful.append(package)
                continue
            
            # Install package
            cmd = [python_path, "-m", "pip", "install", package]
            print(f"Commande: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=120)
            
            if result.returncode == 0:
                print(f"Installation reussie: {package}")
                successful.append(package)
                
                # Verify installation
                verify_result = subprocess.run([python_path, "-c", f"import {package}; print('{package} OK')"], 
                                            capture_output=True, text=True)
                
                if verify_result.returncode == 0:
                    print(f"Verification: OK")
                else:
                    print(f"Verification: ECHOUE - {verify_result.stderr}")
                    
            else:
                print(f"Echec d'installation: {package}")
                print(f"Erreur: {result.stderr}")
                failed.append(package)
                
        except subprocess.TimeoutExpired:
            print(f"Timeout: {package}")
            failed.append(package)
        except Exception as e:
            print(f"ERREUR: {package} - {str(e)}")
            failed.append(package)
    
    # Summary
    print("\n" + "=" * 60)
    print("RÉSUMÉ FINAL")
    print("=" * 60)
    
    print(f"Reussies: {len(successful)}/{len(packages)}")
    print(f"Echouees: {len(failed)}/{len(packages)}")
    
    if successful:
        print(f"\nPackages installes:")
        for pkg in successful:
            print(f"  - {pkg}")
    
    if failed:
        print(f"\nPackages non installes:")
        for pkg in failed:
            print(f"  - {pkg}")
    
    # Final verification
    print(f"\nVERIFICATION FINALE")
    print("-" * 30)
    
    all_good = True
    for package in successful:
        try:
            result = subprocess.run([python_path, "-c", f"import {package}"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"OK: {package}")
            else:
                print(f"ERREUR: {package}")
                all_good = False
        except:
            print(f"ERREUR: {package}")
            all_good = False
    
    if len(failed) == 0 and all_good:
        print(f"\n{'='*60}")
        print("TOUS LES PACKAGES ONT ETE INSTALLES AVEC SUCCES!")
        print("WALLACE EST PRET!")
        print(f"{'='*60}")
        return True
    else:
        print(f"\n{'='*60}")
        print("CERTAINS PACKAGES N'ONT PAS POURRE ETRE INSTALLES")
        print("Veuillez verifier et reessayer")
        print(f"{'='*60}")
        return False

if __name__ == "__main__":
    try:
        success = install_packages()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInstallation interrompue")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERREUR CRITIQUE: {str(e)}")
        sys.exit(1)