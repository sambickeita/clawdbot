#!/usr/bin/env python3
"""
FILTRE PRE-COGNITIF - Architecture "Entonnoir"
Philosophie: BRUIT vs SIGNAL (99% filtré, 1% vers IA)
"""

import requests
import time
import json
from typing import Dict, List, Optional
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# =============================================================================
# CONFIGURATION ZERO-TOKEN
# =============================================================================

# Mots-clés DANGER (Filtre 1)
TRIGGER_KEYWORDS = [
    "crash", "scam", "hack", "crisis", "default", "halted", "investigation",
    "bankruptcy", "ceo resigns", "sec", "fda rejected", "exploit", "breach",
    "suspended", "delisted", "fraud", "lawsuit", "emergency", "collapse"
]

# Seuils de volatilité (Filtre 2)
VOLATILITY_THRESHOLD = 0.05  # 5% de mouvement
PRICE_CHANGE_THRESHOLD = 0.02  # 2% de la moyenne

# Sentiment (Filtre 3)
SENTIMENT_THRESHOLD = 0.5  # Seuil pour réveiller l'IA

# =============================================================================
# OUTILS GRATUITS (ZERO TOKEN)
# =============================================================================

analyzer = SentimentIntensityAnalyzer()

def fetch_news_api() -> List[Dict]:
    """ÉTAPE A: L'ASPIRATEUR - Scraping hard-coded"""
    # Simulation - remplacer par vos vraies sources
    mock_news = [
        {"title": "Apple stock rises 1% on earnings", "source": "Reuters"},
        {"title": "Tesla CEO resigns amid SEC investigation", "source": "Bloomberg"},
        {"title": "Bitcoin crashes 15% after exchange hack", "source": "CoinDesk"},
        {"title": "Weather forecast: sunny skies ahead", "source": "Weather.com"}
    ]
    return mock_news

def fetch_price_data(symbol: str) -> Optional[Dict]:
    """Récupération des prix (Alpha Vantage, Yahoo, etc.)"""
    # Simulation - remplacer par vraie API
    return {
        "current": 150.0,
        "previous": 148.0,
        "average_5d": 145.0,
        "change_1min": 0.02
    }

# =============================================================================
# ÉTAPE B: LE TAMIS HEURISTIQUE (LE SECRET)
# =============================================================================

def filter_keywords(text: str) -> bool:
    """Filtre 1: Mots-clés DANGER"""
    text_lower = text.lower()
    has_keyword = any(keyword in text_lower for keyword in TRIGGER_KEYWORDS)
    
    if not has_keyword:
        print(f"💤 FILTRE 1: Aucun mot-clé danger -> POUBELLE")
        return False
    
    print(f"⚠️  FILTRE 1: Mot-clé détecté -> GARDE")
    return True

def filter_volatility(price_data: Dict) -> bool:
    """Filtre 2: Volatilité mathématique"""
    if not price_data:
        return False
    
    current = price_data.get("current", 0)
    previous = price_data.get("previous", 0)
    average = price_data.get("average_5d", 0)
    change_1min = abs(price_data.get("change_1min", 0))
    
    # Mouvement rapide (1 minute)
    if change_1min > VOLATILITY_THRESHOLD:
        print(f"🚨 FILTRE 2: Mouvement rapide {change_1min:.1%} -> GARDE")
        return True
    
    # Écart à la moyenne
    if average > 0:
        deviation = abs(current - average) / average
        if deviation < PRICE_CHANGE_THRESHOLD:
            print(f"💤 FILTRE 2: Prix stable ({deviation:.1%}) -> POUBELLE")
            return False
    
    print(f"📈 FILTRE 2: Volatilité détectée -> GARDE")
    return True

def filter_sentiment(text: str) -> bool:
    """Filtre 3: Sentiment GRATUIT (VADER)"""
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']  # -1 (horrible) à +1 (génial)
    
    # On ne réveille l'IA que pour les extrêmes
    if abs(compound) < SENTIMENT_THRESHOLD:
        print(f"💤 FILTRE 3: Sentiment neutre ({compound:.2f}) -> POUBELLE")
        return False
    
    sentiment_label = "TRÈS NÉGATIF" if compound < 0 else "TRÈS POSITIF"
    print(f"😱 FILTRE 3: {sentiment_label} ({compound:.2f}) -> GARDE")
    return True

def check_news_relevance(article: Dict) -> bool:
    """
    TAMIS HEURISTIQUE COMPLET
    Retourne True si l'info mérite de réveiller l'IA
    """
    title = article.get("title", "")
    
    print(f"\n🔍 ANALYSE: {title}")
    
    # Les 3 filtres en cascade
    if not filter_keywords(title):
        return False
    
    if not filter_sentiment(title):
        return False
    
    # Optionnel: vérifier la volatilité si on a un symbole
    # price_data = fetch_price_data("AAPL")  # Exemple
    # if not filter_volatility(price_data):
    #     return False
    
    return True

# =============================================================================
# ÉTAPE C: LE RÉVEIL (HANDOFF VERS IA)
# =============================================================================

def call_sila_ai(article: Dict) -> str:
    """
    SEULEMENT ICI on dépense des tokens
    Appel vers Moltbot/Claude/GPT
    """
    prompt = f"""
    SIGNAL CRITIQUE DÉTECTÉ par le filtre pré-cognitif:
    
    Titre: {article['title']}
    Source: {article.get('source', 'Unknown')}
    
    Analyse cette information et détermine:
    1. Niveau de gravité (1-10)
    2. Actions recommandées
    3. Symboles/secteurs impactés
    """
    
    # Simulation d'appel API (remplacer par vraie intégration)
    print(f"🤖 APPEL IA: Analyse en cours...")
    time.sleep(1)  # Simulation
    
    return "ANALYSE IA: Gravité 8/10 - Vendre positions Tesla immédiatement"

def execute_trade(analysis: str):
    """Exécution des ordres basés sur l'analyse IA"""
    print(f"💰 EXÉCUTION: {analysis}")

# =============================================================================
# BOUCLE PRINCIPALE
# =============================================================================

def main_loop():
    """Boucle de surveillance continue"""
    print("🚀 DÉMARRAGE DU FILTRE PRE-COGNITIF")
    print("📊 Philosophie: 99% BRUIT filtré, 1% SIGNAL vers IA")
    
    cycle = 0
    
    while True:
        cycle += 1
        print(f"\n{'='*50}")
        print(f"CYCLE {cycle} - {time.strftime('%H:%M:%S')}")
        print(f"{'='*50}")
        
        try:
            # ÉTAPE A: Aspiration des données
            latest_news = fetch_news_api()
            print(f"📥 {len(latest_news)} articles récupérés")
            
            signals_detected = 0
            
            # ÉTAPE B: Filtrage heuristique
            for article in latest_news:
                if check_news_relevance(article):
                    signals_detected += 1
                    
                    print(f"\n🚨 SIGNAL #{signals_detected} DÉTECTÉ!")
                    print(f"⚡ Activation de l'IA pour analyse profonde...")
                    
                    # ÉTAPE C: Réveil de l'IA (COÛT EN TOKENS)
                    sila_response = call_sila_ai(article)
                    execute_trade(sila_response)
            
            if signals_detected == 0:
                print(f"✅ Aucun signal critique - {len(latest_news)} articles filtrés")
            
            print(f"💰 COÛT: {signals_detected} appels IA sur {len(latest_news)} articles")
            print(f"📊 EFFICACITÉ: {((len(latest_news) - signals_detected) / len(latest_news) * 100):.1f}% de bruit filtré")
            
        except Exception as e:
            print(f"❌ ERREUR: {e}")
        
        # Attente avant le prochain cycle
        time.sleep(30)  # 30 secondes

if __name__ == "__main__":
    main_loop()