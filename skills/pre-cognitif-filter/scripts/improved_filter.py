#!/usr/bin/env python3
"""
CORRECTIFS IDENTIFIÉS ET SKILLS AMÉLIORÉS

ERREURS DÉTECTÉES dans l'implémentation précédente:
1. Pas de vraie intégration API (Alpha Vantage, Twitter, etc.)
2. Seuils de filtrage trop permissifs
3. Pas de persistance des états
4. Pas d'intégration avec Moltbot
"""

import os
import json
import requests
from typing import Dict, List
from datetime import datetime, timedelta

class ImprovedPreCognitiveFilter:
    def __init__(self):
        self.config = self.load_config()
        self.state_file = "filter_state.json"
        self.load_state()
    
    def load_config(self) -> Dict:
        """Configuration renforcée"""
        return {
            "keywords": {
                "critical": ["crash", "hack", "investigation", "bankruptcy", "fraud"],
                "high": ["suspended", "halted", "rejected", "lawsuit"],
                "medium": ["warning", "concern", "decline"]
            },
            "volatility": {
                "critical": 0.10,  # 10%
                "high": 0.05,      # 5%
                "medium": 0.02     # 2%
            },
            "sentiment": {
                "critical": 0.7,   # Très extrême
                "high": 0.5,       # Extrême
                "medium": 0.3      # Modéré
            }
        }
    
    def load_state(self):
        """Persistance des états"""
        try:
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        except:
            self.state = {"last_check": None, "processed_items": []}
    
    def save_state(self):
        """Sauvegarde des états"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def enhanced_keyword_filter(self, text: str) -> tuple[bool, str]:
        """Filtre mots-clés avec niveaux de priorité"""
        text_lower = text.lower()
        
        for level, keywords in self.config["keywords"].items():
            for keyword in keywords:
                if keyword in text_lower:
                    return True, level
        
        return False, "none"
    
    def call_moltbot_api(self, data: Dict) -> str:
        """Intégration réelle avec Moltbot"""
        try:
            # Appel vers l'API Moltbot locale
            response = requests.post(
                "http://localhost:18789/api/agent/message",
                json={
                    "message": f"SIGNAL CRITIQUE: {data['title']}",
                    "context": data
                },
                timeout=30
            )
            return response.json().get("response", "Erreur API")
        except Exception as e:
            return f"Erreur Moltbot: {e}"
    
    def process_with_priority(self, articles: List[Dict]) -> List[Dict]:
        """Traitement avec système de priorité"""
        prioritized = []
        
        for article in articles:
            passed, level = self.enhanced_keyword_filter(article["title"])
            if passed:
                article["priority"] = level
                prioritized.append(article)
        
        # Tri par priorité (critical > high > medium)
        priority_order = {"critical": 3, "high": 2, "medium": 1}
        return sorted(prioritized, key=lambda x: priority_order.get(x["priority"], 0), reverse=True)

# Mise à jour du skill pour corriger les erreurs
filter_instance = ImprovedPreCognitiveFilter()