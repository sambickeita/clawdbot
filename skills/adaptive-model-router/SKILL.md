---
name: adaptive-model-router
description: Automatic model selection and switching between GLM-4.5-Flash, GLM-4.5, and GLM-4.7 based on task complexity. Use when optimizing for cost/speed vs quality trade-offs, or when explicit model routing is needed. Automatically classifies tasks as simple (fast/cheap), medium (balanced), or complex (high quality) and routes to the optimal model.
---

# Adaptive Model Router

## Core Strategy

**Principle:** Match model capability to task complexity. Don't use a Ferrari for grocery runs.

**Model Tiers (ZAI Working Models Only):**
- **GLM-4.5-Flash** (Tier 1): Simple tasks - speed > quality
- **GLM-4.5** (Tier 2): Medium complexity - balanced
- **GLM-4.7** (Tier 3): Complex tasks - quality > speed

**NOTE:** GLM-4.7-Flash is NOT available via ZAI API.

## Complexity Classification

### Tier 1: Simple Tasks (GLM-4.5-Flash)

**Trigger patterns:**
- Quick Q&A, factual retrieval
- Short text generation (< 100 words)
- Basic classification or categorization
- Code completion or bug fixes (clear scope)
- Summaries of short content
- Translation (non-creative)

**Examples:**
- "What's the capital of France?"
- "Fix this syntax error"
- "Summarize this paragraph"
- "Translate to Spanish"

### Tier 2: Medium Tasks (GLM-4.5)

**Trigger patterns:**
- Multi-step reasoning (3-5 steps)
- Medium-length content (100-500 words)
- Code analysis or refactoring
- Structured outputs (JSON, formats)
- Creative writing with clear constraints
- Research synthesis from few sources

**Examples:**
- "Analyze this code and suggest improvements"
- "Write a blog post about X"
- "Compare these three options"
- "Create a structured report"

### Tier 3: Complex Tasks (GLM-4.7)

**Trigger patterns:**
- Deep reasoning (5+ steps)
- Long-form content (> 500 words)
- Multi-domain synthesis
- Complex decision-making
- High-stakes analysis (finance, security)
- Code architecture design
- Strategic planning

**Examples:**
- "Design a complete trading system"
- "Analyze market conditions and propose strategy"
- "Solve this complex problem with constraints"
- "Design this microservices architecture"

## Automatic Routing Process

When a task comes in:

1. **Analyze complexity** using `scripts/analyze_complexity.py`
2. **Get current model** via `session_status` tool
3. **Compare** recommended vs current
4. **Switch** if needed via `session_status(model="<model-alias>")`

## Manual Override

Opérateur can explicitly request:
- "Use flash model for speed"
- "Use full model for quality"
- "Route this to GLM-4.7"

Explicit requests override automatic classification.

## Model Aliases (WORKING MODELS ONLY)

Use these aliases when switching:
- `glm-4.7` → Full GLM 4.7 (default)
- `glm-4.5` → GLM 4.5 (medium)
- `glm-4.5-flash` → GLM 4.5 Flash (fast)

## Cost Optimization

**Tier 1** ~ 1x cost, **Tier 2** ~ 2x cost, **Tier 3** ~ 4x cost

Target mix for efficiency:
- 60% Tier 1 (simple queries)
- 30% Tier 2 (medium tasks)
- 10% Tier 3 (complex work)

Adjust based on Opérateur's quality tolerance.

## Execution

For model switching, use:
```
session_status(model="<alias>")
```

Example:
```
session_status(model="glm-4.5-flash")
```

This sets the per-session model override.

## WALLACE Integration

**Usage Protocol:**

1. **On task arrival:** Run complexity analysis
   ```
   python skills/adaptive-model-router/scripts/analyze_complexity.py "<query>"
   ```

2. **Check recommended tier:** Output shows tier (1/2/3) and confidence

3. **Get current model:** Use session_status to see current model

4. **Switch if beneficial:**
   - If Tier 1 and current is Tier 2/3 → Switch to GLM-4.5-Flash
   - If Tier 2 and current is Tier 3 → Switch to GLM-4.5
   - If Tier 3 and current is Tier 1/2 → Switch to GLM-4.7
   - If Tier matches → No action needed

5. **Decision logic:** Cost-benefit analysis
   ```
   Tier 1 → 2 or 3: Always switch (wasting resources)
   Tier 2 → 3: Switch if Opérateur tolerates speed > quality
   Tier 3 → 1 or 2: Always switch (quality critical)
   ```

**Behavior:**

- **Proactive routing:** Analyze before complex tasks, suggest switch
- **Opérateur override:** If Opérateur specifies model, respect it
- **Logging:** Track routing decisions in memory for optimization
- **Feedback loop:** Learn from Opérateur's satisfaction ratings

**Cost Impact Tracking:**

Track cumulative savings:
- Tier 1 usage saves ~75% vs Tier 3
- Tier 2 usage saves ~50% vs Tier 3

Target: Reduce average cost per query by 30% while maintaining quality.

**Example Workflow:**

```
Opérateur: "Design a trading bot"

WALLACE:
1. Analyze → Tier 3 detected (confidence: 0.9)
2. Current model: GLM-4.7 (Tier 3)
3. Decision: Already optimal, no switch needed
4. Proceed with task
```

```
Opérateur: "What's the time?"

WALLACE:
1. Analyze → Tier 1 detected (confidence: 0.95)
2. Current model: GLM-4.7 (Tier 3)
3. Decision: Switch to GLM-4.5-Flash (saves 75% cost)
4. session_status(model="glm-4.5-flash")
5. Answer query
```
