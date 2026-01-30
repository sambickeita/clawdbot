#!/usr/bin/env python3
"""
Security Checker for package-installer skill
Performs security validation of packages before installation
"""

import os
import sys
import json
import requests
import hashlib
import subprocess
import re
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
import tempfile
import shutil
from urllib.parse import urlparse


class SecurityChecker:
    """Performs security validation of Python packages"""
    
    def __init__(self):
        self.trusted_sources = [
            "https://pypi.org",
            "https://conda-forge.org"
        ]
        
        # Known malicious package patterns
        self.malicious_patterns = [
            r"hack",
            r"crack", 
            r"steal",
            r"password",
            r"keylog",
            r"spy",
            r"trojan",
            r"malware",
            r"virus",
            r"backdoor",
            r"rootkit"
        }
        
        # Common suspicious extensions
        self.suspicious_extensions = [
            ".exe", ".dll", ".so", ".dylib", ".app", ".scr", ".bat", ".cmd", ".ps1"
        ]
        
        # High-risk packages (use with caution)
        self.high_risk_packages = [
            "pip", "setuptools", "wheel", "cython", "numpy", "pandas"
        ]
        
    def check_package_safety(self, package_name: str, version: str = None) -> Dict:
        """Comprehensive safety check for a package"""
        
        safety_report = {
            "package": package_name,
            "version": version or "latest",
            "overall_status": "SAFE",
            "checks": {},
            "recommendations": [],
            "critical_issues": [],
            "warnings": [],
            "score": 100
        }
        
        try:
            # 1. Basic validation
            basic_check = self._basic_validation(package_name, version)
            safety_report["checks"]["basic_validation"] = basic_check
            self._update_score(safety_report, basic_check)
            
            # 2. Package name and metadata check
            metadata_check = self._check_package_metadata(package_name, version)
            safety_report["checks"]["metadata"] = metadata_check
            self._update_score(safety_report, metadata_check)
            
            # 4. Download URL validation
            url_check = self._check_download_urls(package_name, version)
            safety_report["checks"]["download_urls"] = url_check
            self._update_score(safety_report, url_check)
            
            # 5. File type and extension check
            filetype_check = self._check_file_types(package_name, version)
            safety_report["checks"]["file_types"] = filetype_check
            self._update_score(safety_report, filetype_check)
            
            # 6. Dependencies check
            deps_check = self._check_dependencies(package_name, version)
            safety_report["checks"]["dependencies"] = deps_check
            self._update_score(safety_report, deps_check)
            
            # 7. Age and popularity check
            age_check = self._check_package_age_and_popularity(package_name)
            safety_report["checks"]["age_popularity"] = age_check
            self._update_score(safety_report, age_check)
            
            # 8. Known vulnerabilities check
            vuln_check = self._check_known_vulnerabilities(package_name, version)
            safety_report["checks"]["vulnerabilities"] = vuln_check
            self._update_score(safety_report, vuln_check)
            
            # 9. License check
            license_check = self._check_license(package_name, version)
            safety_report["checks"]["license"] = license_check
            self._update_score(safety_report, license_check)
            
            # 10. Source code review check
            code_check = self._check_source_code_integrity(package_name, version)
            safety_report["checks"]["source_code"] = code_check
            self._update_score(safety_report, code_check)
            
        except Exception as e:
            safety_report["overall_status"] = "CHECK_FAILED"
            safety_report["critical_issues"].append(f"Security check failed: {str(e)}")
            
        # Generate final recommendations
        self._generate_recommendations(safety_report)
        
        return safety_report
        
    def _basic_validation(self, package_name: str, version: str = None) -> Dict:
        """Basic validation of package name and version"""
        result = {
            "status": "PASS",
            "issues": [],
            "details": {}
        }
        
        # Check package name format
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', package_name):
            result["status"] = "FAIL"
            result["issues"].append("Package name contains invalid characters")
            
        # Check for suspicious patterns
        for pattern in self.malicious_patterns:
            if re.search(pattern, package_name.lower()):
                result["status"] = "FAIL"
                result["issues"].append(f"Package name matches suspicious pattern: {pattern}")
                
        # Check version format if provided
        if version and not self._is_valid_version(version):
            result["warnings"].append("Version format appears unusual")
            
        result["details"]["name_format"] = "VALID" if result["status"] == "PASS" else "INVALID"
        result["details"]["suspicious_patterns"] = len(result["issues"])
        
        return result
        
    def _check_package_metadata(self, package_name: str, version: str = None) -> Dict:
        """Check package metadata from PyPI"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Get package info from PyPI
            url = f"https://pypi.org/pypi/{package_name}/json"
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
                
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                result["status"] = "FAIL"
                result["issues"].append(f"Package not found in PyPI: HTTP {response.status_code}")
                return result
                
            data = response.json()
            info = data.get("info", {})
            
            # Check basic metadata
            if not info.get("name"):
                result["status"] = "FAIL"
                result["issues"].append("Package has no name in metadata")
                
            if not info.get("version"):
                result["status"] = "FAIL"
                result["issues"].append("Package has no version in metadata")
                
            # Check for suspicious metadata
            summary = info.get("summary", "").lower()
            description = info.get("description", "").lower()
            
            for pattern in self.malicious_patterns:
                if pattern in summary or pattern in description:
                    result["warnings"].append(f"Suspicious keyword in metadata: {pattern}")
                    
            # Check author information
            author = info.get("author")
            if not author or author == "Unknown":
                result["warnings"].append("Missing or unknown author information")
                
            # Check license
            license_info = info.get("license")
            if not license_info:
                result["warnings"].append("No license information available")
            elif "unknown" in license_info.lower():
                result["warnings"].append("License marked as unknown")
                
            result["details"]["has_metadata"] = True
            result["details"]["author"] = author or "Unknown"
            result["details"]["license"] = license_info or "Unknown"
            result["details"]["summary"] = info.get("summary", "")
            
        except Exception as e:
            result["status"] = "FAIL"
            result["issues"].append(f"Failed to retrieve metadata: {str(e)}")
            
        return result
        
    def _check_download_urls(self, package_name: str, version: str = None) -> Dict:
        """Check download URLs for security"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Get package info
            url = f"https://pypi.org/pypi/{package_name}/json"
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
                
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return result
                
            data = response.json()
            urls = data.get("urls", [])
            
            trusted_domains = set(["pypi.org", "files.pythonhosted.org"])
            suspicious_urls = []
            
            for url_info in urls:
                download_url = url_info.get("upload_time")
                
                # Parse URL domain
                parsed_url = urlparse(download_url)
                domain = parsed_url.netloc.lower()
                
                if domain not in trusted_domains:
                    suspicious_urls.append(download_url)
                    result["warnings"].append(f"Untrusted domain: {domain}")
                    
                # Check file size
                file_size = url_info.get("size", 0)
                if file_size > 100 * 1024 * 1024:  # 100MB
                    result["warnings"].append(f"Large package size: {file_size} bytes")
                    
            result["details"]["total_urls"] = len(urls)
            result["details"]["suspicious_urls"] = len(suspicious_urls)
            
            if suspicious_urls:
                result["status"] = "WARNING"
                
        except Exception as e:
            result["issues"].append(f"Failed to check download URLs: {str(e)}")
            result["status"] = "FAIL"
            
        return result
        
    def _check_file_types(self, package_name: str, version: str = None) -> Dict:
        """Check for suspicious file types in package"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Get package info
            url = f"https://pypi.org/pypi/{package_name}/json"
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
                
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return result
                
            data = response.json()
            urls = data.get("urls", [])
            
            binary_files = []
            suspicious_files = []
            
            for url_info in urls:
                filename = url_info.get("filename", "")
                file_type = url_info.get("packagetype", "")
                
                # Check for binary file types
                if file_type in ["bdist_dumb", "bdist_wininst"]:
                    binary_files.append(filename)
                    
                # Check for suspicious extensions
                for ext in self.suspicious_extensions:
                    if filename.lower().endswith(ext):
                        suspicious_files.append(filename)
                        result["warnings"].append(f"Suspicious file extension: {ext}")
                        
            result["details"]["binary_files"] = len(binary_files)
            result["details"]["suspicious_files"] = len(suspicious_files)
            
            if suspicious_files:
                result["status"] = "WARNING"
                
        except Exception as e:
            result["issues"].append(f"Failed to check file types: {str(e)}")
            result["status"] = "FAIL"
            
        return result
        
    def _check_dependencies(self, package_name: str, version: str = None) -> Dict:
        """Check package dependencies for security risks"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Get package info
            url = f"https://pypi.org/pypi/{package_name}/json"
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
                
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return result
                
            data = response.json()
            requires_dist = data.get("info", {}).get("requires_dist", [])
            
            if not requires_dist:
                result["details"]["has_dependencies"] = False
                return result
                
            result["details"]["has_dependencies"] = True
            result["details"]["dependency_count"] = len(requires_dist)
            
            # Check for suspicious dependencies
            suspicious_deps = []
            for dep in requires_dist:
                dep_lower = dep.lower()
                for pattern in self.malicious_patterns:
                    if pattern in dep_lower:
                        suspicious_deps.append(dep)
                        result["warnings"].append(f"Suspicious dependency: {dep}")
                        break
                        
            result["details"]["suspicious_dependencies"] = len(suspicious_deps)
            
            if suspicious_deps:
                result["status"] = "WARNING"
                
        except Exception as e:
            result["issues"].append(f"Failed to check dependencies: {str(e)}")
            result["status"] = "FAIL"
            
        return result
        
    def _check_package_age_and_popularity(self, package_name: str) -> Dict:
        """Check package age and download statistics"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Get package info
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return result
                
            data = response.json()
            info = data.get("info", {})
            
            # Check upload time
            upload_time_str = info.get("upload_time")
            if upload_time_str:
                upload_time = datetime.strptime(upload_time_str, "%Y-%m-%dT%H:%M:%S")
                days_old = (datetime.now() - upload_time).days
                
                result["details"]["days_old"] = days_old
                result["details"]["upload_time"] = upload_time_str
                
                if days_old < 7:
                    result["warnings"].append("Package created less than 7 days ago")
                    result["status"] = "WARNING"
                elif days_old < 30:
                    result["warnings"].append("Package created less than 30 days ago")
                    
            # Check download count
            downloads = info.get("downloads", 0)
            result["details"]["downloads"] = downloads
            
            if downloads == 0:
                result["warnings"].append("Package has no downloads")
            elif downloads < 100:
                result["warnings"].append("Package has very few downloads")
                
        except Exception as e:
            result["issues"].append(f"Failed to check age and popularity: {str(e)}")
            result["status"] = "FAIL"
            
        return result
        
    def _check_known_vulnerabilities(self, package_name: str, version: str = None) -> Dict:
        """Check for known vulnerabilities in the package"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        # This is a simplified vulnerability check
        # In a real implementation, you would integrate with vulnerability databases
        
        try:
            # Basic checks for common vulnerable packages
            vulnerable_packages = {
                "requests": ["<2.25.0"],
                "django": ["<3.2.0"],
                "flask": ["<2.0.0"],
                "sqlalchemy": ["<1.4.0"]
            }
            
            package_lower = package_name.lower()
            
            if package_lower in vulnerable_packages:
                if version and self._is_version_older(version, vulnerable_packages[package_lower][0]):
                    result["status"] = "FAIL"
                    result["issues"].append(f"Package has known vulnerabilities in this version")
                    
            result["details"]["vulnerability_check"] = "SIMPLIFIED"
            
        except Exception as e:
            result["issues"].append(f"Failed to check vulnerabilities: {str(e)}")
            result["status"] = "FAIL"
            
        return result
        
    def _check_license(self, package_name: str, version: str = None) -> Dict:
        """Check package license"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Get package info
            url = f"https://pypi.org/pypi/{package_name}/json"
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
                
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return result
                
            data = response.json()
            license_info = data.get("info", {}).get("license", "")
            
            result["details"]["license"] = license_info or "Unknown"
            
            # Check for problematic licenses
            if "unknown" in license_info.lower():
                result["warnings"].append("License marked as unknown")
                
            # Check for permissive but review-required licenses
            permissive_licenses = ["MIT", "Apache", "BSD", "GPL"]
            license_lower = license_info.lower()
            
            for perm_license in permissive_licenses:
                if perm_license.lower() in license_lower:
                    result["details"]["license_type"] = "PERMISSIVE"
                    break
            else:
                result["details"]["license_type"] = "UNKNOWN"
                
        except Exception as e:
            result["issues"].append(f"Failed to check license: {str(e)}")
            result["status"] = "FAIL"
            
        return result
        
    def _check_source_code_integrity(self, package_name: str, version: str = None) -> Dict:
        """Basic source code integrity check"""
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        # This is a simplified check
        # In a real implementation, you would download and analyze the source code
        
        try:
            # Get package info
            url = f"https://pypi.org/pypi/{package_name}/json"
            if version:
                url = f"https://pypi.org/pypi/{package_name}/{version}/json"
                
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return result
                
            data = response.json()
            project_urls = data.get("info", {}).get("project_urls", {})
            
            # Check if source code is available
            source_url = None
            for url_type, url_value in project_urls.items():
                if "source" in url_type.lower() or "github" in url_value.lower():
                    source_url = url_value
                    break
                    
            result["details"]["has_source_code"] = source_url is not None
            result["details"]["source_url"] = source_url or "Not available"
            
            if not source_url:
                result["warnings"].append("Source code URL not available")
                
        except Exception as e:
            result["issues"].append(f"Failed to check source code: {str(e)}")
            result["status"] = "FAIL"
            
        return result
        
    def _update_score(self, safety_report: Dict, check_result: Dict):
        """Update safety score based on check result"""
        if check_result["status"] == "FAIL":
            safety_report["score"] -= 20
            safety_report["critical_issues"].extend(check_result["issues"])
        elif check_result["status"] == "WARNING":
            safety_report["score"] -= 10
            safety_report["warnings"].extend(check_result["warnings"])
            
    def _generate_recommendations(self, safety_report: Dict):
        """Generate recommendations based on safety report"""
        if safety_report["overall_status"] == "FAIL":
            safety_report["recommendations"].append("DO NOT INSTALL - Critical security issues found")
            return
            
        if safety_report["overall_status"] == "WARNING":
            safety_review.append("Review carefully before installation")
            
        if safety_report["score"] < 80:
            safety_report["recommendations"].append("Exercise caution - multiple warnings detected")
            
        # Check specific conditions
        if any("suspicious" in warning.lower() for warning in safety_report["warnings"]):
            safety_report["recommendations"].append("Strongly recommend manual review of source code")
            
    def _is_valid_version(self, version: str) -> bool:
        """Check if version format is valid"""
        try:
            # Simple version format check
            if version.startswith(("==", "!=", "<=", ">=", "~=", "===")):
                version = version[2:]
                
            # Basic semantic versioning check
            if re.match(r'^\d+\.\d+\.\d+([a-zA-Z0-9]+)?$', version):
                return True
                
            # Check for valid version components
            parts = version.split('.')
            for part in parts:
                if not part.isdigit() and not part.isalpha():
                    return False
                    
            return True
            
        except:
            return False
            
    def _is_version_older(self, version: str, threshold: str) -> bool:
        """Compare versions to check if older than threshold"""
        try:
            # Simple version comparison (not comprehensive)
            v_parts = [int(x) for x in version.split('.')]
            t_parts = [int(x) for x in threshold.split('.')]
            
            for v, t in zip(v_parts, t_parts):
                if v < t:
                    return True
                elif v > t:
                    return False
                    
            return len(v_parts) < len(t_parts)
            
        except:
            return False


def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 3:
        print("Usage: python security_checker.py <package> [version]")
        sys.exit(1)
        
    checker = SecurityChecker()
    package_name = sys.argv[2]
    version = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"🔒 SECURITY CHECK FOR: {package_name} ({version or 'latest'})")
    print("=" * 50)
    
    safety_report = checker.check_package_safety(package_name, version)
    
    # Print results
    print(f"Overall Status: {safety_report['overall_status']}")
    print(f"Safety Score: {safety_report['score']}/100")
    
    if safety_report['critical_issues']:
        print(f"\n❌ CRITICAL ISSUES:")
        for issue in safety_report['critical_issues']:
            print(f"  • {issue}")
            
    if safety_report['warnings']:
        print(f"\n⚠️  WARNINGS:")
        for warning in safety_report['warnings']:
            print(f"  • {warning}")
            
    if safety_report['recommendations']:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in safety_report['recommendations']:
            print(f"  • {rec}")
            
    print("\n" + "=" * 50)
    print("Security check completed.")


if __name__ == "__main__":
    main()