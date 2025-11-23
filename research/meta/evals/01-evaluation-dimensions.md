# Evaluation Dimensions for Mental Models

## Overview

**Spider graph axes:** What properties matter for evaluating mental models?

Each dimension scored 0-10:
- 0 = Completely fails on this dimension
- 5 = Mediocre, acceptable
- 10 = Exceptional, state-of-the-art

**Purpose:** Enable apples-to-apples comparison across models.

---

## Dimension 1: Predictive Power

**Definition:** Can the model predict future system states, failures, bottlenecks?

**Why it matters:**
- Proactive governance requires seeing problems before they hit
- Models that only explain the past are less useful

**Measurement:**

Quantitative:
```python
# For incident prediction
predictions = model.predict_incidents(current_state, horizon=10_steps)
actual_incidents = run_simulation(10_steps)

# Compute ROC curve, AUC
from sklearn.metrics import roc_auc_score
auc = roc_auc_score(actual_incidents, predictions)

# Score (0-10)
score = auc * 10  # AUC = 1.0 → score = 10
```

Qualitative:
- Expert judgment: "Does model identify non-obvious risks?"
- User feedback: "Did predictions help me avoid problems?"

**Thresholds:**
- 0-3: Poor (random guessing, AUC ≈ 0.5)
- 4-6: Mediocre (some signal, AUC ≈ 0.6-0.7)
- 7-10: Excellent (strong signal, AUC > 0.8)

**Example:**

Physics model:
- Predicts: "Module A will have incident (high E_local)"
- Actual: Module A has incident in 8/10 simulations
- AUC = 0.85 → Score = 8.5

Economics model:
- Predicts: "Module A will be neglected (low ROI)"
- Actual: Module A neglected → incident
- AUC = 0.65 → Score = 6.5

---

## Dimension 2: Actionability

**Definition:** Does the model suggest concrete interventions that actually work?

**Why it matters:**
- A model that predicts but doesn't guide action is less useful
- "What should I do?" is the ultimate question

**Measurement:**

Quantitative (A/B test):
```python
# Group A: Use model's recommended intervention
# Group B: Use baseline intervention (or no intervention)

intervention = model.suggest_intervention(problem)

# Run experiment
outcome_A = apply_intervention(intervention)
outcome_B = apply_baseline()

# Effect size (Cohen's d)
effect_size = (mean_A - mean_B) / pooled_std

# Score
if effect_size > 0.8: score = 10  # Large effect
elif effect_size > 0.5: score = 7  # Medium effect
elif effect_size > 0.2: score = 4  # Small effect
else: score = 1  # No effect
```

Qualitative:
- Specificity: Vague "improve quality" vs concrete "refactor module X"
- Feasibility: Can intervention actually be implemented?
- Cost: Is intervention worth the effort?

**Thresholds:**
- 0-3: Poor (interventions don't work or too vague)
- 4-6: Mediocre (some effect, but weak or expensive)
- 7-10: Excellent (strong effect, concrete, feasible)

**Example:**

Physics model:
- Suggests: "Refactor module A to reduce coupling (V_struct)"
- Effect: V_struct decreases 40%, incidents drop 30%
- Effect size = 0.6 → Score = 7

Economics model:
- Suggests: "Increase budget for module A (raise price/bid)"
- Effect: More agents work on A, quality improves 50%
- Effect size = 0.9 → Score = 10

---

## Dimension 3: Simplicity

**Definition:** How easy is the model to understand and apply?

**Why it matters:**
- Complex models are harder to communicate, harder to trust
- Occam's razor: Simpler is better (all else equal)

**Measurement:**

Quantitative:
```python
# Code complexity
lines_of_code = count_loc(model_implementation)
num_parameters = count_parameters(model)

# Simplicity score (inverse of complexity)
score = 10 / (1 + log(lines_of_code / 100 + num_parameters / 10))
```

Qualitative:
- Conceptual clarity: Can you explain it in 2 minutes?
- Learning curve: How long to master?
- Prerequisites: Requires PhD in physics? Or high school math?

**Thresholds:**
- 0-3: Very complex (requires expert knowledge)
- 4-6: Moderate (some background needed)
- 7-10: Simple (intuitive, minimal prerequisites)

**Example:**

Physics model:
- LOC: 500
- Parameters: 15 (masses, coupling strengths, etc.)
- Prerequisites: Linear algebra, basic physics
- Score = 5 (moderate complexity)

Economics model:
- LOC: 300
- Parameters: 8 (budgets, prices, reserve prices)
- Prerequisites: Basic economics (everyone understands markets)
- Score = 8 (relatively simple)

---

## Dimension 4: Scalability

**Definition:** Does the model work at different scales (1 agent vs 1000 agents)?

**Why it matters:**
- A model that works for 10 agents but breaks at 100 is limited
- Need to scale from prototypes to production

**Measurement:**

Quantitative:
```python
# Measure performance degradation
performance_small = run_model(n_agents=10)
performance_large = run_model(n_agents=100)

degradation = (performance_small - performance_large) / performance_small

# Score (lower degradation = higher score)
score = 10 * (1 - degradation)
```

Qualitative:
- Does model require different formulations at different scales?
- Do intervention strategies change? (Red flag if yes)

**Thresholds:**
- 0-3: Poor (performance drops > 50%)
- 4-6: Mediocre (degrades 20-50%)
- 7-10: Excellent (< 20% degradation)

**Example:**

Physics model:
- Small (10 agents): Accuracy = 85%
- Large (100 agents): Accuracy = 80%
- Degradation = 6% → Score = 9.4

Economics model:
- Small (10 agents): Efficiency = 70% (overhead of auctions not worth it)
- Large (100 agents): Efficiency = 95% (auctions shine at scale)
- Actually IMPROVES at scale → Score = 10

---

## Dimension 5: Measurability

**Definition:** Can we actually measure the model's variables in practice?

**Why it matters:**
- A model with unmeasurable variables is theoretical curiosity, not practical tool
- "If you can't measure it, you can't manage it"

**Measurement:**

Quantitative:
```python
# For each variable in model
measurability_scores = []

for variable in model.variables:
    if variable.can_measure_directly():
        score = 10
    elif variable.can_infer_from_proxy():
        score = 6
    elif variable.requires_subjective_judgment():
        score = 3
    else:
        score = 0

    measurability_scores.append(score)

# Average
overall_score = mean(measurability_scores)
```

Qualitative:
- Cost of measurement: Expensive instrumentation? Or free (in logs)?
- Reliability: Noisy measurements?
- Latency: Real-time? Or requires batch processing?

**Thresholds:**
- 0-3: Hard to measure (subjective, expensive, noisy)
- 4-6: Measurable with effort (proxies, instrumentation)
- 7-10: Easy to measure (directly observable, cheap)

**Example:**

Physics model:
- V_struct (coupling energy): Can compute from code graph → Score = 9
- T (kinetic energy): Requires tracking changes over time → Score = 7
- Understanding: Requires quizzes, subjective → Score = 4
- Average = 6.7

Economics model:
- ROI: Can measure (value / cost), but "value" subjective → Score = 6
- Budget: Directly observable → Score = 10
- Market prices: Directly observable → Score = 10
- Average = 8.7

---

## Dimension 6: Generality

**Definition:** Does the model apply to many contexts? Or only narrow domains?

**Why it matters:**
- A general model is more valuable (can reuse across projects)
- But beware: "General" often means "vague"

**Measurement:**

Quantitative:
```python
# Test model on diverse scenarios
contexts = [
    'web_app', 'ML_pipeline', 'embedded_system',
    'data_warehouse', 'mobile_app', 'API_service'
]

successes = 0
for context in contexts:
    if model.works_well(context):
        successes += 1

score = (successes / len(contexts)) * 10
```

Qualitative:
- Does model require heavy customization per context?
- Are core concepts transferable?

**Thresholds:**
- 0-3: Narrow (works in < 30% of contexts)
- 4-6: Moderate (works in 30-60%)
- 7-10: General (works in > 60%)

**Example:**

Physics model:
- Works for: Structural problems (coupling, architecture)
- Doesn't work for: Resource allocation, business dynamics
- Success: 4/6 contexts → Score = 6.7

Economics model:
- Works for: Resource allocation, task assignment, trading
- Doesn't work for: Structural analysis, human learning
- Success: 4/6 contexts → Score = 6.7

---

## Dimension 7: Learning Curve

**Definition:** How long does it take to learn and apply the model effectively?

**Why it matters:**
- Steep learning curve → fewer users → less adoption
- But sometimes complexity is necessary for accuracy

**Measurement:**

Quantitative:
```python
# User study
users = recruit_developers(n=20)

for user in users:
    time_to_proficiency = measure_training_time(user, model)

avg_time = mean(time_to_proficiency)

# Score (inverse of time)
# 1 hour → 10, 10 hours → 5, 100 hours → 1
score = 10 / log10(avg_time_hours + 1)
```

Qualitative:
- Prerequisites: Do users need domain knowledge?
- Documentation quality: Clear tutorials?
- Intuitiveness: Matches mental models users already have?

**Thresholds:**
- 0-3: Steep (requires weeks of study)
- 4-6: Moderate (few days to learn basics)
- 7-10: Gentle (hours to get started)

**Example:**

Physics model:
- Prerequisites: Linear algebra, physics concepts
- Time to proficiency: ~20 hours
- Score = 10 / log10(21) = 7.6

Economics model:
- Prerequisites: None (everyone understands markets)
- Time to proficiency: ~5 hours
- Score = 10 / log10(6) = 12.9 → capped at 10

---

## Dimension 8: Computational Cost

**Definition:** How expensive is it to compute the model's predictions/simulations?

**Why it matters:**
- Real-time governance needs fast models
- Expensive models limit iteration speed

**Measurement:**

Quantitative:
```python
# Benchmark runtime
import time

start = time.time()
model.run_simulation(n_agents=100, n_steps=1000)
runtime = time.time() - start

# Score (inverse of runtime)
# < 1s → 10, < 10s → 7, < 60s → 4, > 60s → 1
if runtime < 1: score = 10
elif runtime < 10: score = 7
elif runtime < 60: score = 4
else: score = 1
```

Qualitative:
- Parallelizability: Can we speed up with more CPUs?
- Memory usage: Does it fit in RAM?
- Incremental updates: Can we update cheaply? Or recompute from scratch?

**Thresholds:**
- 0-3: Expensive (> 60s for typical problem)
- 4-6: Moderate (10-60s)
- 7-10: Cheap (< 10s)

**Example:**

Physics model:
- Laplacian computation: O(n²) for dense graphs
- For 100 agents: ~5 seconds
- Score = 7

Economics model:
- Auction clearing: O(n log n)
- For 100 agents: ~0.5 seconds
- Score = 10

---

## Composite Score

**How to combine dimensions into single score?**

**Unweighted average:**
```python
composite_score = mean([
    predictive_power,
    actionability,
    simplicity,
    scalability,
    measurability,
    generality,
    learning_curve,
    computational_cost
])
```

**Weighted average (if priorities differ):**
```python
weights = {
    'predictive_power': 0.20,  # Most important
    'actionability': 0.20,     # Most important
    'simplicity': 0.15,
    'scalability': 0.15,
    'measurability': 0.10,
    'generality': 0.10,
    'learning_curve': 0.05,
    'computational_cost': 0.05,
}

composite_score = sum(dimension * weights[name] for dimension, name in ...)
```

**Trade-off analysis:**

Models rarely excel on all dimensions. Look for:
- **Pareto frontier** - Models that aren't dominated on all dimensions
- **Specialization** - Models that excel on specific dimensions (use for specific problems)

**Example:**

```
Model A (Physics):
  High: Predictive (8), Measurable (9)
  Medium: Actionable (6), Scalable (7)
  Low: Simple (5), Learning curve (4)
  → Use for: Prediction tasks where expertise is available

Model B (Economics):
  High: Actionable (9), Scalable (9), Simple (8)
  Medium: Measurable (7), Learning curve (9)
  Low: Predictive (5), Generality (6)
  → Use for: Resource allocation, large scale, non-expert users
```

---

## Dimension Trade-offs

**Common trade-offs:**

1. **Simplicity vs Predictive Power**
   - Simple models (linear regression) are easy but less accurate
   - Complex models (deep learning) are powerful but opaque
   - Sweet spot: Just complex enough to predict well

2. **Generality vs Actionability**
   - General models (CAS, systems theory) apply broadly but give vague advice
   - Specific models (physics for coupling) are narrow but concrete
   - Sweet spot: General framework, specific sub-models

3. **Scalability vs Measurability**
   - Scalable models (market equilibrium) abstract away details
   - Detailed models (agent-based simulations) track everything but slow at scale
   - Sweet spot: Hierarchical models (micro + macro)

**No free lunch:** Every model makes trade-offs. The art is picking the right trade-off for your problem.

---

## Summary

**Eight dimensions for spider graphs:**

1. **Predictive Power** - Does it predict failures?
2. **Actionability** - Does it suggest working interventions?
3. **Simplicity** - Easy to understand?
4. **Scalability** - Works at 1 agent and 1000 agents?
5. **Measurability** - Can we measure its variables?
6. **Generality** - Applies to many contexts?
7. **Learning Curve** - Quick to learn?
8. **Computational Cost** - Fast to compute?

**Each scored 0-10.**

**Visualization:** Spider graph shows strengths/weaknesses at a glance.

**Composite score:** Weighted average, but beware single-number reductionism.

**Trade-offs:** Models rarely excel on all dimensions. Pick the right trade-off.

**Next:** See `02-benchmark-scenarios.md` for standard test cases all models must pass.
