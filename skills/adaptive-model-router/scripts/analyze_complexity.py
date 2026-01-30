#!/usr/bin/env python3
"""
Analyze task complexity and recommend optimal GLM model.

Routes to:
- Tier 1 (GLM-4.5-Flash): Simple, fast tasks
- Tier 2 (GLM-4.7-Flash): Medium complexity, balanced
- Tier 3 (GLM-4.7): Complex, high-quality tasks
"""

import re
import sys
from typing import Dict, List, Tuple


class ComplexityAnalyzer:
    """Analyzes task complexity and recommends model."""

    def __init__(self):
        self.tier1_keywords = {
            'quick', 'simple', 'basic', 'what', 'who', 'where', 'when', 'how',
            'explain briefly', 'summarize', 'translate', 'fix error', 'bug fix',
            'capitalize', 'format', 'check', 'verify', 'validate'
        }

        self.tier2_keywords = {
            'analyze', 'improve', 'refactor', 'compare', 'discuss', 'evaluate',
            'write', 'create', 'generate', 'optimize', 'moderate', 'balanced',
            'structure', 'format', 'json', 'xml', 'design simple', 'plan'
        }

        self.tier3_keywords = {
            'complex', 'design', 'architecture', 'strategy', 'comprehensive',
            'research', 'synthesis', 'multi-step', 'deep', 'thorough',
            'system', 'trading', 'finance', 'security', 'production',
            'microservices', 'scalable', 'enterprise', 'optimize performance',
            'portfolio', 'market analysis', 'hft', 'high frequency'
        }

        self.code_keywords = {
            'code', 'function', 'class', 'script', 'program', 'algorithm',
            'implementation', 'api', 'database', 'sql', 'python', 'rust',
            'javascript', 'typescript', 'html', 'css', 'docker', 'kubernetes'
        }

        self.reasoning_indicators = {
            'because', 'therefore', 'however', 'although', 'considering',
            'taking into account', 'given that', 'assuming', 'if-then',
            'trade-off', 'weighing', 'balancing', 'decision'
        }

    def analyze(self, query: str) -> Dict:
        """
        Analyze query complexity and return recommendation.

        Args:
            query: User's task/query string

        Returns:
            Dict with:
                - tier: 1, 2, or 3
                - model: Model alias to use
                - confidence: Float 0-1
                - reasoning: Explanation of classification
        """
        query_lower = query.lower()
        length = len(query.split())
        code_ratio = self._code_ratio(query_lower)
        reasoning_depth = self._reasoning_depth(query_lower)
        keywords = self._extract_keywords(query_lower)

        # Score each tier
        tier1_score = self._score_tier1(query_lower, length, code_ratio, reasoning_depth)
        tier2_score = self._score_tier2(query_lower, length, code_ratio, reasoning_depth)
        tier3_score = self._score_tier3(query_lower, length, code_ratio, reasoning_depth)

        # Determine winner
        if tier3_score >= 7:
            tier = 3
            model = "glm-4.7"
            confidence = min(0.9, tier3_score / 10 + 0.4)
        elif tier2_score >= 5:
            tier = 2
            model = "glm-4.7-flash"
            confidence = min(0.95, tier2_score / 10 + 0.55)
        else:
            tier = 1
            model = "glm-4.5-flash"
            confidence = min(0.95, tier1_score / 10 + 0.6)

        reasoning = self._generate_reasoning(
            tier, tier1_score, tier2_score, tier3_score,
            length, code_ratio, reasoning_depth, keywords
        )

        return {
            'tier': tier,
            'model': model,
            'confidence': round(confidence, 2),
            'reasoning': reasoning,
            'metrics': {
                'word_count': length,
                'code_ratio': code_ratio,
                'reasoning_depth': reasoning_depth,
                'keywords': keywords
            }
        }

    def _code_ratio(self, query: str) -> float:
        """Calculate ratio of code-related keywords."""
        code_words = [w for w in query.split() if w in self.code_keywords]
        return len(code_words) / max(1, len(query.split()))

    def _reasoning_depth(self, query: str) -> float:
        """Estimate reasoning complexity based on indicators."""
        indicators = [i for i in self.reasoning_indicators if i in query]
        depth = len(indicators)

        # Boost for multi-part questions
        if '?' in query:
            depth += query.count('?') - 1  # First question doesn't count as extra

        # Boost for lists/and-conjunctions
        if ' and ' in query or ' plus ' in query:
            depth += 1

        return min(10, depth * 2)

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract matching keywords for debugging."""
        found = []
        for kw in self.tier1_keywords:
            if kw in query:
                found.append(f"T1:{kw}")
        for kw in self.tier2_keywords:
            if kw in query:
                found.append(f"T2:{kw}")
        for kw in self.tier3_keywords:
            if kw in query:
                found.append(f"T3:{kw}")
        return found[:10]  # Limit to 10

    def _score_tier1(self, query: str, length: int, code_ratio: float, reasoning: float) -> float:
        """Score for Tier 1 (simple)."""
        score = 0

        # Keyword matches
        matches = sum(1 for kw in self.tier1_keywords if kw in query)
        score += matches * 2

        # Short queries favor Tier 1
        if length < 30:
            score += 3
        elif length < 50:
            score += 1

        # Low reasoning favors Tier 1
        if reasoning < 2:
            score += 2

        # Penalize if complex reasoning
        if reasoning >= 4:
            score -= 2

        return max(0, score)

    def _score_tier2(self, query: str, length: int, code_ratio: float, reasoning: float) -> float:
        """Score for Tier 2 (medium)."""
        score = 0

        # Keyword matches
        matches = sum(1 for kw in self.tier2_keywords if kw in query)
        score += matches * 2

        # Medium length
        if 30 <= length < 100:
            score += 3
        elif 100 <= length < 200:
            score += 2

        # Medium reasoning
        if 2 <= reasoning < 5:
            score += 3

        # Some code content
        if 0.1 <= code_ratio < 0.3:
            score += 2

        return max(0, score)

    def _score_tier3(self, query: str, length: int, code_ratio: float, reasoning: float) -> float:
        """Score for Tier 3 (complex)."""
        score = 0

        # Keyword matches (highest weight)
        matches = sum(1 for kw in self.tier3_keywords if kw in query)
        score += matches * 3

        # Long queries
        if length >= 100:
            score += 3
        elif length >= 200:
            score += 5

        # Deep reasoning
        if reasoning >= 5:
            score += 4

        # High code ratio
        if code_ratio >= 0.3:
            score += 3

        return max(0, score)

    def _generate_reasoning(
        self, tier: int, t1: float, t2: float, t3: float,
        length: int, code_ratio: float, reasoning: float, keywords: List[str]
    ) -> str:
        """Generate explanation for the classification."""
        parts = []

        if tier == 1:
            parts.append("Simple task detected")
            if length < 30:
                parts.append("Short query")
            if reasoning < 2:
                parts.append("Low reasoning depth")
        elif tier == 2:
            parts.append("Medium complexity detected")
            if 30 <= length < 100:
                parts.append("Moderate length")
            if 2 <= reasoning < 5:
                parts.append("Multi-step reasoning")
        else:
            parts.append("Complex task detected")
            if length >= 100:
                parts.append(f"Long query ({length} words)")
            if reasoning >= 5:
                parts.append("Deep reasoning required")
            if code_ratio >= 0.3:
                parts.append("High code content")

        if keywords:
            parts.append(f"Keywords: {', '.join(keywords[:5])}")

        return "; ".join(parts)


def main():
    """CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_complexity.py <query>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print('  python analyze_complexity.py "How do I fix this bug?"', file=sys.stderr)
        sys.exit(1)

    query = ' '.join(sys.argv[1:])
    analyzer = ComplexityAnalyzer()
    result = analyzer.analyze(query)

    print(f"Recommended: {result['model'].upper()}")
    print(f"Tier: {result['tier']}/3")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"\nMetrics:")
    print(f"  Words: {result['metrics']['word_count']}")
    print(f"  Code ratio: {result['metrics']['code_ratio']:.2f}")
    print(f"  Reasoning depth: {result['metrics']['reasoning_depth']:.1f}")
    if result['metrics']['keywords']:
        print(f"  Keywords: {result['metrics']['keywords']}")

    # For automation: exit code = tier
    sys.exit(result['tier'])


if __name__ == '__main__':
    main()
