#!/usr/bin/env python3
"""
Auto-route task to optimal model based on complexity.

Analyzes the task, checks current model, and switches if needed.
"""

import sys
import subprocess
import json
from pathlib import Path

# Add scripts to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_complexity import ComplexityAnalyzer


class ModelRouter:
    """Routes tasks to optimal models."""

    def __init__(self):
        self.analyzer = ComplexityAnalyzer()
        self.model_aliases = {
            1: "glm-4.5-flash",
            2: "glm-4.7-flash",
            3: "glm-4.7"
        }

    def route(self, query: str, current_model: str = None) -> dict:
        """
        Route query to optimal model.

        Args:
            query: User's task/query
            current_model: Current model (if known)

        Returns:
            Dict with routing decision and action needed
        """
        # Analyze complexity
        analysis = self.analyzer.analyze(query)
        recommended_model = self.model_aliases[analysis['tier']]

        # Determine if switch is needed
        needs_switch = False
        if current_model:
            # Normalize current model name
            current_normalized = self._normalize_model(current_model)
            recommended_normalized = self._normalize_model(recommended_model)
            needs_switch = current_normalized != recommended_normalized

        return {
            'query': query[:100] + '...' if len(query) > 100 else query,
            'recommended_tier': analysis['tier'],
            'recommended_model': recommended_model,
            'current_model': current_model,
            'needs_switch': needs_switch,
            'confidence': analysis['confidence'],
            'reasoning': analysis['reasoning'],
            'metrics': analysis['metrics']
        }

    def _normalize_model(self, model: str) -> str:
        """Normalize model name for comparison."""
        model_lower = model.lower().replace(' ', '-')

        # Map variations to canonical names
        if 'glm-4.7-flash' in model_lower or 'glm4.7flash' in model_lower:
            return 'glm-4.7-flash'
        elif 'glm-4.5-flash' in model_lower or 'glm4.5flash' in model_lower:
            return 'glm-4.5-flash'
        elif 'glm-4.7' in model_lower or 'glm4.7' in model_lower:
            return 'glm-4.7'
        else:
            return model_lower

    def execute_switch(self, model_alias: str) -> bool:
        """
        Execute model switch via session_status tool.

        Note: This should be called from within Moltbot, not as standalone.
        Use the session_status tool directly:
            session_status(model="<model_alias>")
        """
        print(f"ACTION REQUIRED: session_status(model=\"{model_alias}\")")
        return True


def main():
    """CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python auto_route.py <query> [--current-model <model>]", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print('  python auto_route.py "What is the capital of France?"', file=sys.stderr)
        print('  python auto_route.py "Design a microservices architecture" --current-model glm-4.7-flash', file=sys.stderr)
        print("\nOutput: JSON routing decision", file=sys.stderr)
        sys.exit(1)

    # Parse args
    query = ''
    current_model = None
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--current-model' and i + 1 < len(sys.argv):
            current_model = sys.argv[i + 1]
            i += 2
        else:
            query += arg + ' '
            i += 1

    query = query.strip()
    if not query:
        print("ERROR: No query provided", file=sys.stderr)
        sys.exit(1)

    # Route
    router = ModelRouter()
    decision = router.route(query, current_model)

    # Output JSON
    print(json.dumps(decision, indent=2))

    # Exit code indicates action needed
    if decision['needs_switch']:
        sys.exit(1)  # Switch needed
    else:
        sys.exit(0)  # No switch needed


if __name__ == '__main__':
    main()
