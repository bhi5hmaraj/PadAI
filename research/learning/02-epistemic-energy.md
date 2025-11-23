# Epistemic Energy: Learning as Potential

## Overview

In the software physics model, **learning contributes a potential energy term** to the Hamiltonian:

```
H = T + V
  = T + V_struct + V_bus + V_learning

Where:
  V_learning = Σ epistemic_gap[i] × importance[i]
```

This document explains how to compute, interpret, and govern using epistemic energy.

---

## The Epistemic Gap

### Definition

The **epistemic gap** at module i measures the distance between:

1. **Ground truth**: actual codebase state
2. **Human mental model**: what the human believes about the code

```
epistemic_gap[i] = (1 - understanding[i])

Where:
  understanding[i] ∈ [0, 1]  - measured via comprehension challenges
```

**Examples:**

```
understanding[i] = 1.0  →  gap = 0.0  (perfect model)
understanding[i] = 0.8  →  gap = 0.2  (mostly accurate)
understanding[i] = 0.3  →  gap = 0.7  (mostly confused)
understanding[i] = 0.0  →  gap = 1.0  (no model at all)
```

### Three-Way Drift

More precisely, there are **three representations**:

1. **Ground truth** G[i] - actual code
2. **AI representation** A[i] - LLM's internal "beliefs"
3. **Human mental model** H[i] - human's understanding

**Full epistemic gap:**

```
gap_total[i] = d(G[i], A[i]) + d(A[i], H[i]) + d(H[i], G[i])

Where d(X, Y) is some distance metric (edit distance, semantic similarity, etc.)
```

**For MVP, simplify to:**

```
gap[i] = d(H[i], G[i]) = (1 - understanding[i])
```

Assume AI is reasonably aligned with ground truth (true for good LLMs with updated context).

---

## Epistemic Potential Energy

### Formula

```
V_learning = Σ_i gap[i] × importance[i]
           = Σ_i (1 - understanding[i]) × (demand[i] × complexity[i])
```

**Interpretation:**

- **High gap in important module** → high potential energy → system under tension
- **High gap in unimportant module** → low energy → ignorable
- **Low gap everywhere** → V_learning ≈ 0 → safe to ship

### Physical Analogy

Think of V_learning as **gravitational potential** in a hilly landscape:

- Modules with high gaps = elevated positions
- Importance = mass of the object at that position
- V = m × g × h (mass × gravity × height)

**Governance goal:** Keep the system in a low-energy valley (minimal epistemic risk).

---

## Computing Understanding

### Measurement Method

**Understanding score U[i] is measured via comprehension challenges:**

1. **Prediction challenges**
   - "If we change X, what breaks?"
   - "What happens if we remove this dependency?"
   - User predicts → run test → compare

2. **Recall challenges**
   - "Which modules depend on this function?"
   - "What invariants does this code maintain?"
   - Multiple choice or open-ended

3. **Debugging challenges**
   - Present a failing test
   - "What caused this failure?"
   - "How would you fix it?"

**Scoring:**

```python
def compute_understanding(challenges, responses):
    correct = sum(1 for r in responses if r.is_correct)
    total = len(challenges)

    # Recency-weighted accuracy
    weights = [decay_function(t) for t in time_since(responses)]

    understanding = sum(w * c for w, c in zip(weights, correct)) / sum(weights)
    return understanding  # ∈ [0, 1]
```

### Time Decay

**Understanding degrades over time:**

```
U[i](t) = U_0 * exp(-λ * t)

Where:
  λ = decay_rate (depends on module complexity)
  t = time since last interaction
```

**Example decay rates:**

```python
λ_simple = 0.01 / day     # 1% decay per day
λ_moderate = 0.05 / day   # 5% decay per day
λ_complex = 0.10 / day    # 10% decay per day
```

**Reason:** Human memory fades. Understanding must be refreshed periodically.

---

## Importance Weighting

### Formula

```
importance[i] = demand[i] × complexity[i] × coupling[i]
```

**Why this formula?**

1. **Demand** - how often is this module used?
   - High-traffic modules matter more
   - User-facing features > internal utilities

2. **Complexity** - how hard is it to understand?
   - Complex modules have bigger blast radius if misunderstood
   - Simple utilities less critical

3. **Coupling** - how connected is this module?
   - High coupling = changes propagate widely
   - Low coupling = changes localized

**Example values:**

```
Module A (core API):
  demand = 0.9      # Very high traffic
  complexity = 0.7  # Moderately complex
  coupling = 0.8    # Many dependencies
  → importance = 0.9 × 0.7 × 0.8 = 0.504

Module B (internal utility):
  demand = 0.2      # Low traffic
  complexity = 0.3  # Simple
  coupling = 0.1    # Isolated
  → importance = 0.2 × 0.3 × 0.1 = 0.006

Epistemic gap matters 80× more for A than B!
```

---

## Knowledge Debt

### Definition

**Knowledge debt** is the total epistemic energy of the system:

```
knowledge_debt = V_learning
               = Σ_i (1 - understanding[i]) × importance[i]
```

**Analogy to technical debt:**

- **Technical debt** = shortcuts in code → future rework
- **Knowledge debt** = shortcuts in learning → future incidents

### Debt Accumulation

**Debt grows when:**

1. **Code changes faster than learning**
   - New features added without understanding old ones
   - Refactors without comprehension

2. **Understanding decays over time**
   - Team doesn't revisit modules
   - Memory fades

3. **Team turnover**
   - New engineers lack context
   - Knowledge not transferred

**Growth rate:**

```
d(knowledge_debt)/dt = rate_of_change × (1 - learning_investment)
```

**Example:**

```python
# High velocity, low learning
change_rate = 10 modules/week
learning_rate = 2 modules/week  # Only learning 20%

debt_growth = (10 - 2) × avg_importance = 8 × 0.4 = 3.2/week
```

### Debt Paydown

**Debt decreases when:**

1. **Active learning**
   - Comprehension challenges
   - Deliberate practice
   - Code review with understanding verification

2. **Refactoring for simplicity**
   - Reduce complexity → lower importance
   - Easier to understand

3. **Documentation + shared models**
   - Not a substitute for active learning
   - But helps reduce decay rate

**Paydown rate:**

```
debt_reduction = learning_investment × effectiveness
```

---

## Governance with Epistemic Energy

### Threshold-Based Gates

**Rule:** If V_learning > threshold, trigger learning before shipping

```python
def can_ship(module, V_learning):
    if V_learning[module] > V_max:
        return False, "Knowledge debt too high, complete challenges first"
    return True, "OK to ship"

# Example thresholds
V_max_critical = 0.3  # Max 30% gap × importance for critical modules
V_max_normal = 0.5    # Max 50% for normal modules
```

### Energy-Based Prioritization

**Priority queue for learning:**

```python
learning_priorities = sorted(
    modules,
    key=lambda m: (1 - understanding[m]) × importance[m],
    reverse=True
)

# Focus learning effort on highest-energy modules
```

**Effect:** Reduces V_learning most efficiently.

### Adaptive Learning Intensity

**Adjust learning force based on total knowledge debt:**

```python
def compute_learning_intensity(V_learning_total, V_target):
    if V_learning_total > 2 * V_target:
        return 'high'    # Crisis mode, intensive learning
    elif V_learning_total > V_target:
        return 'medium'  # Moderate learning
    else:
        return 'low'     # Maintain current level
```

---

## Experimental Validation

To test this model, we need to:

### 1. Measure Understanding

**Instrumentation:**

- Track comprehension challenge results
- Compute U[i] per module per engineer
- Store time-series of understanding scores

### 2. Correlate with Incidents

**Hypothesis:** High epistemic gap predicts incidents

```
P(incident at module i) ∝ (1 - understanding[i]) × complexity[i]
```

**Test:**
- Run simulation with varying understanding levels
- Count incidents
- Compute correlation (Pearson's r)

**Success:** Strong correlation (r > 0.6) between gap and incidents

### 3. Test Interventions

**A/B test:**

- **Control group:** No learning gates
- **Treatment group:** Understanding-gated approvals

**Measure:**
- Incident rate
- Cycle time
- Knowledge debt over time

**Expected result:** Treatment group has lower incidents, slightly longer cycle time, decreasing debt.

---

## Implementation Notes

### Storing Understanding Scores

**Data structure:**

```python
understanding_db = {
    'module_id': {
        'engineer_id': {
            'score': 0.75,
            'last_updated': datetime,
            'challenge_history': [
                {'timestamp': ..., 'correct': True, 'difficulty': 'medium'},
                ...
            ],
        },
    },
}
```

### Recomputing V_learning

**Frequency:** Recompute after every event that changes:

1. Understanding scores (challenge results)
2. Importance values (demand, complexity, coupling changes)
3. Module structure (new modules added)

**Efficiency:**

```python
# Incremental update (O(1) per change)
def update_V_learning(module_changed):
    old_contribution = gap[module] × importance[module]
    new_contribution = (1 - understanding_new[module]) × importance[module]

    V_learning += (new_contribution - old_contribution)
```

### Visualizing Epistemic Energy

**Energy landscape plot:**

```python
# 2D heatmap: modules vs engineers
# Color = epistemic_gap[i, j]
# Size = importance[i]

plt.scatter(
    module_complexity,
    epistemic_gap,
    s=importance * 1000,  # Size proportional to importance
    c=epistemic_gap,
    cmap='Reds'
)
plt.xlabel('Module Complexity')
plt.ylabel('Epistemic Gap')
plt.title('Knowledge Debt Landscape')
```

---

## Comparison to Other Debt Metrics

| Metric | What It Measures | How to Pay Down |
|--------|------------------|-----------------|
| **Technical debt** | Code quality shortfall | Refactor, add tests |
| **Design debt** | Architecture inconsistency | Redesign, modularize |
| **Documentation debt** | Missing/outdated docs | Write docs |
| **Knowledge debt** | Understanding gap | Active learning, practice |

**Key difference:**

- Technical/design/doc debt are **code properties**
- Knowledge debt is a **human-code relationship property**

You can have:
- Perfect code + high knowledge debt (nobody understands it)
- Messy code + low knowledge debt (everyone knows the hacks)

---

## Summary

**Epistemic energy (V_learning) is the physics representation of knowledge debt.**

Key formulas:

```
epistemic_gap[i] = (1 - understanding[i])
importance[i] = demand[i] × complexity[i] × coupling[i]
V_learning = Σ_i gap[i] × importance[i]
```

**Governance:**
- High V_learning → trigger learning before shipping
- Prioritize learning on high-energy modules
- Adapt learning intensity to total debt

**Measurement:**
- Understanding via comprehension challenges
- Time decay models
- Correlation with incidents

**Next:** See `03-active-learning-primitives.md` for specific learning mechanisms.
