# Filtre Pré-Cognitif

Filtre "bête et méchant" (zéro token) qui ne réveille l'IA que si c'est grave.

## Architecture

**ÉTAPE A : L'ASPIRATEUR** - Scraping hard-coded sans IA
**ÉTAPE B : LE TAMIS HEURISTIQUE** - Filtres Python purs (0 token)  
**ÉTAPE C : LE RÉVEIL** - Handoff vers l'IA seulement si nécessaire

## Utilisation

```bash
python scripts/scout.py
```

Le script fonctionne en boucle continue et ne consomme des tokens que pour les signaux critiques détectés.