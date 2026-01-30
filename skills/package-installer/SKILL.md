# package-installer Skill

## Description
Gestion sécurisée d'installations de bibliothèques Python avec approbation utilisateur. Cette compétence permet d'installer des packages Python dans un environnement virtuel isolé avec l'autorisation explicite de l'utilisateur.

## Capacités Principales

### 🔒 Installation Sécurisée
- Demande d'autorisation explicite pour chaque installation
- Vérification des sources PyPI/Conda-forge
- Scan de sécurité des packages
- Gestion des dépendances et des conflits

### 🗃️ Gestion d'Environnements
- Création et suppression d'environnements virtuels
- Activation/désactivation automatique
- Isolation complète des installations
- Support Python 3.8+

### 📊 Monitoring & Logging
- Journalisation complète des opérations
- Rapport de sécurité après chaque installation
- Suivi des versions installées
- Gestion des erreurs détaillée

## Commandes Disponibles

### Créer un environnement virtuel
```bash
wallace create-env nom_env python_version=3.9
# Ex: wallace create-env venv_trading python_version=3.9
```

### Supprimer un environnement
```bash
wallace remove-env nom_env
# Ex: wallace remove-env venv_trading
```

### Installer un package (avec approbation)
```bash
wallace install-package nom_package version="latest"
# Ex: wallace install-package pandas version="1.5.0"
```

### Lister les packages installés
```bash
wallace list-packages
```

### Vérifier un package
```bash
wallace verify-package nom_package
```

## Structure du Skill

```
package-installer/
├── SKILL.md (ce fichier)
├── scripts/
│   ├── environment_manager.py     # Gestion des environnements virtuels
│   ├── package_installer.py       # Installation avec approbation
│   ├── security_checker.py        # Vérification de sécurité
│   └── dependency_analyzer.py      # Analyse des dépendances
├── references/
│   ├── package_database.json      # Base de données des packages
│   ├── security_guidelines.md     # Guidelines de sécurité
│   └── approved_packages_list.md   # Liste des packages approuvés
└── requirements.txt               # Dépendances du skill
```

## Workflow Opérationnel

### 1. Demande d'Installation
```
Wallace requis installation de: pandas
Objectif: Analyse de données financières
Taille estimée: 45MB
Version: 1.5.0
Source: PyPI (officiel)
Sécurité: ✓ Vérifiée

Autoriser l'installation? (oui/non):
```

### 2. Vérification de Sécurité
- Scan des signatures numériques
- Vérification des dépendances
- Recherche de known vulnerabilities
- Validation des métadonnées

### 3. Installation Contrôlée
- Création de l'environnement si nécessaire
- Installation des dépendances
- Gestion des conflits
- Validation post-installation

### 4. Rapport d'Opération
```bash
Installation terminée avec succès:
├── Package: pandas 1.5.0
├── Taille: 47.2MB
├── Dépendances: 24 packages
├── Temps: 32 secondes
├── Sécurité: ✓
└── Environnement: venv_ninja_moltbot
```

## Configuration par Défaut

### Environnement Principal
- **Nom**: venv_ninja_moltbot
- **Chemin**: G:\PROGRAMMES_FILES\Github\Finance_Agent\LABO\GIT STOCKAGE\CREATION\PERSONNAL ASSISTANCE\moltbot\venv_ninja_moltbot
- **Python Version**: Python 3.9 (ou version système)

### Sources Autorisées
- **PyPI**: https://pypi.org/ (principal)
- **Conda-forge**: https://conda-forge.org/ (pour packages scientifiques)
- **Enterprise**: Packages internes (si configuré)

### Politique de Sécurité
- **Scan antivirus**: Activé
- **Version minimale**: Python 3.8
- **Whitelist**: Packages PyPI uniquement par défaut
- **Backup**: Restauration automatique en cas d'erreur

## Exemples d'Utilisation

### Installation pour Trading Bot
```bash
# Activer l'environnement de trading
wallace create-env venv_trading

# Installer les dépendances de trading
wallace install-package pandas
wallace install-package numpy
wallace install-package scikit-learn
```

### Installation pour Data Science
```bash
# Créer environnement dédié
wallace create-env venv_datascience python_version=3.10

# Installer stack data science
wallace install-package jupyter
wallace install-package matplotlib
wallace install-package tensorflow
```

### Gestion des Conflits
```bash
# Détection automatique
wallace install-package django  # Déclenche un conflit
# Résolution proposée:
# ├── Environment: venv_django
# └── Solution: Créer environnement dédié
```

## Dépannage

### Problèmes Courants
1. **Permission refusée**: Vérifier les droits d'administration
2. **Environnement existant**: Utiliser `wallace remove-env` puis recréer
3. **Package non trouvé**: Vérifier le nom exact et la version
4. **Conflit de dépendances**: Consulter le rapport d'analyse

### Commandes de Diagnostic
```bash
wallace check-environment
wallace list-depends nom_package
wallace security-scan
```

## Notes de Développement

### Extensions Possibles
- Support Docker pour isolation supplémentaire
- Intégration avec repository privé
- Gestion des versions précises
- Rapport d'impact sur le disque

### Architecture Sécurité
- **Sandboxing**: Isolation complète
- **Rollback**: Restauration automatique
- **Audit**: Logging complet opérations
- **Approval**: Double validation pour packages sensibles

---

**Créé par**: WALLACE System v2.1  
**Version**: 1.0.0  
**Dernière mise à jour**: 2026-01-29  
**Statut**: Production Ready