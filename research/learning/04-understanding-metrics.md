# Understanding Metrics

## Overview

To govern with learning force, we must **measure understanding quantitatively**.

This document defines:
1. How to compute understanding scores
2. Decay models (memory fades over time)
3. Aggregation (per-module, per-engineer, team-wide)
4. Correlation with incidents (validation)

---

## Understanding Score Formula

### Base Score

```python
understanding[engineer, module] = weighted_average([
    w_quiz * quiz_accuracy,
    w_pred * prediction_accuracy,
    w_sandbox * sandbox_performance,
    w_code_review * review_quality,
])

# Typical weights
w_quiz = 0.3       # Factual recall
w_pred = 0.4       # Causal reasoning (most important)
w_sandbox = 0.2    # Hands-on practice
w_code_review = 0.1  # Peer feedback
```

**Components:**

1. **Quiz accuracy** - % correct on comprehension challenges
2. **Prediction accuracy** - % correct predictions (before/after testing)
3. **Sandbox performance** - % of exercises completed successfully
4. **Review quality** - How often caught bugs in reviews, gave useful feedback

### Time Decay

**Understanding degrades without practice:**

```python
def understanding_at_time(U_0, t, λ):
    """
    Exponential decay model.

    Args:
        U_0: Initial understanding
        t: Time since last interaction (days)
        λ: Decay rate (per day)

    Returns:
        Current understanding
    """
    return U_0 * np.exp(-λ * t)
```

**Decay rates by complexity:**

```python
λ_simple = 0.01    # 1% per day (simple modules, slow decay)
λ_moderate = 0.05  # 5% per day (moderate complexity)
λ_complex = 0.10   # 10% per day (complex modules, fast decay)
```

**Example:**

```
Module: payment.py (complex, λ = 0.10)
Initial understanding: U_0 = 0.80

After 10 days without touching it:
U = 0.80 × exp(-0.10 × 10) = 0.80 × 0.368 = 0.29

Understanding dropped from 80% to 29%!
```

**Implication:** Critical modules need **periodic refreshers**, not just one-time learning.

### Confidence Intervals

**Track uncertainty:**

```python
# Not all understanding scores are equally reliable
confidence = {
    'n_samples': 20,           # Number of challenges completed
    'recent_variance': 0.05,   # Std dev of recent results
    'time_since_last': 5,      # Days
}

# Higher n_samples → higher confidence
# Higher variance → lower confidence
# Longer time → lower confidence

confidence_score = (
    0.5 * min(n_samples / 20, 1.0) +
    0.3 * (1 - recent_variance) +
    0.2 * exp(-0.1 * time_since_last)
)
```

**Use in governance:**

```python
# Require higher understanding if confidence is low
effective_threshold = base_threshold / confidence_score

# Example:
# base_threshold = 0.8
# confidence = 0.6
# effective_threshold = 0.8 / 0.6 = 1.33 (impossible!)
# → Must complete more challenges to raise confidence
```

---

## Aggregation Levels

### Per-Module, Per-Engineer

**Individual score:**

```python
U[engineer_id, module_id] = decay_adjusted_score(
    base_score=compute_base_score(challenges),
    last_interaction=get_last_interaction_time(engineer_id, module_id),
    decay_rate=get_decay_rate(module_id)
)
```

**Matrix representation:**

```
           payment.py  auth.py  api.py  utils.py
Alice        0.85       0.60     0.40    0.90
Bob          0.50       0.90     0.70    0.30
Carol        0.75       0.75     0.80    0.60
```

### Team-Wide (Per-Module)

**Average understanding for a module:**

```python
U_team[module] = mean([U[engineer, module] for engineer in team])
```

**Weighted by activity:**

```python
# Weight by who actually works on this module
weights = [commits_by[engineer, module] for engineer in team]
U_team[module] = weighted_mean(scores, weights)
```

**Example:**

```
payment.py:
  Alice: 0.85 (50% of commits)
  Bob: 0.50 (40% of commits)
  Carol: 0.75 (10% of commits)

U_team = 0.5 × 0.85 + 0.4 × 0.50 + 0.1 × 0.75 = 0.70
```

### Module Risk Score

**Combine understanding + importance:**

```python
risk[module] = (1 - U_team[module]) × importance[module]

# High risk = low understanding + high importance
```

**Governance:** Prioritize learning for high-risk modules.

---

## Correlation with Incidents

### Hypothesis

**Low understanding predicts incidents:**

```
P(incident at module i) ∝ (1 - U[i]) × complexity[i]
```

### Measurement

**Track incidents and understanding:**

```python
incidents = [
    {'module': 'payment.py', 'timestamp': t1, 'severity': 0.8},
    {'module': 'auth.py', 'timestamp': t2, 'severity': 0.5},
    ...
]

understanding_at_incident = [
    U_team['payment.py'] at t1,
    U_team['auth.py'] at t2,
    ...
]
```

**Compute correlation:**

```python
from scipy.stats import pearsonr

# Do modules with low understanding have more incidents?
r, p_value = pearsonr(
    [1 - U for U in understanding_at_incident],
    [inc['severity'] for inc in incidents]
)

print(f"Correlation: r = {r:.3f}, p = {p_value:.4f}")

# Strong positive correlation (r > 0.6, p < 0.05) validates model
```

### Predictive Power

**Lead time analysis:**

```python
# Does understanding score predict incidents N days in advance?

for lead_time in [1, 3, 5, 10, 20]:
    understanding_before = get_understanding(module, t - lead_time)
    incident_occurred = check_incident(module, t)

    # Compute ROC curve, AUC
    auc = compute_auc(understanding_before, incident_occurred)

    print(f"Lead time {lead_time} days: AUC = {auc:.3f}")
```

**Success criterion:** AUC > 0.7 at lead_time = 10 days

**Interpretation:** Understanding score 10 days before gives 70% prediction accuracy for incidents.

---

## Decay Models (Advanced)

### Simple Exponential

```python
U(t) = U_0 × exp(-λt)
```

**Pros:** Simple, one parameter
**Cons:** Assumes constant decay rate (not realistic)

### Power-Law Decay

```python
U(t) = U_0 / (1 + t/τ)^β

# Typical values
β = 0.5  # Slower decay initially
τ = 10   # Time constant (days)
```

**Pros:** Matches human memory better (fast initial decay, then slower)
**Cons:** More parameters to tune

### Spaced Repetition (Ebbinghaus)

```python
# Review interval grows exponentially
interval[n] = interval[n-1] × ease_factor

# Decay tied to review schedule
U(t) = {
    1.0 if t < next_review,
    U_0 × decay_function(t - last_review) otherwise
}
```

**Pros:** Matches spaced repetition science
**Cons:** Requires scheduling reviews

### Chosen Model for MVP

**Use simple exponential with module-specific λ:**

```python
λ[module] = base_decay × complexity[module]

# Simple modules: λ = 0.01 (1% per day)
# Complex modules: λ = 0.10 (10% per day)
```

**Rationale:** Simple to implement, interpretable, good enough for validation.

---

## Implementation

### Database Schema

```sql
CREATE TABLE understanding_scores (
    engineer_id TEXT,
    module_id TEXT,
    score REAL,                 -- Current understanding [0, 1]
    last_updated TIMESTAMP,
    decay_rate REAL,            -- λ for this module
    n_challenges INT,           -- Total challenges completed
    n_correct INT,              -- Total correct
    PRIMARY KEY (engineer_id, module_id)
);

CREATE TABLE challenge_history (
    challenge_id TEXT PRIMARY KEY,
    engineer_id TEXT,
    module_id TEXT,
    challenge_type TEXT,        -- 'quiz', 'prediction', 'sandbox'
    correct BOOLEAN,
    timestamp TIMESTAMP,
    difficulty TEXT             -- 'easy', 'medium', 'hard'
);
```

### API Endpoints

```python
GET /understanding/{engineer_id}/{module_id}
→ Returns current understanding score (decay-adjusted)

POST /understanding/{engineer_id}/{module_id}/challenge
Body: { "correct": true, "challenge_type": "quiz" }
→ Updates understanding based on challenge result

GET /understanding/team/{module_id}
→ Returns team-wide understanding for module

GET /understanding/engineer/{engineer_id}
→ Returns all modules and scores for engineer

GET /understanding/gaps
→ Returns highest-priority learning gaps (sorted by risk)
```

### Real-Time Updates

```python
# After every challenge
def update_understanding(engineer_id, module_id, challenge_result):
    # Get current score (decay-adjusted)
    U_current = get_understanding(engineer_id, module_id)

    # Compute new score
    if challenge_result['correct']:
        U_new = 0.8 * U_current + 0.2 * 1.0  # Small boost
    else:
        U_new = 0.8 * U_current + 0.2 * 0.0  # Penalty

    # Store updated score
    store_understanding(engineer_id, module_id, U_new, timestamp=now())

    # Recompute V_learning
    recompute_epistemic_energy()
```

---

## Visualization

### Individual Dashboard

**Engineer view:**

```
Your Understanding:

High (>80%):        [payment.py] [utils.py]
Medium (60-80%):    [api.py] [auth.py]
Low (<60%):         [reporting.py] [admin.py]

Recommended learning:
1. reporting.py (risk = 0.45, gap = 0.65)
2. admin.py (risk = 0.30, gap = 0.70)
```

### Team Heatmap

**Module × Engineer matrix:**

```
           payment  auth  api  utils
Alice       ███    ▓▓░   ░░░   ███
Bob         ▓▓░    ███   ▓▓▓   ░░░
Carol       ▓▓▓    ▓▓▓   ███   ▓▓░

Legend: ░░░ Low (<60%), ▓▓▓ Medium (60-80%), ███ High (>80%)
```

### Risk Landscape

**Scatter plot:**

```python
plt.scatter(
    x=importance,
    y=(1 - understanding),
    s=complexity * 100,
    c='red',
    alpha=0.6
)
plt.xlabel('Importance (demand × coupling)')
plt.ylabel('Epistemic Gap (1 - understanding)')
plt.title('Knowledge Debt Landscape')
```

**Quadrants:**

```
High gap, high importance: URGENT (top-right)
High gap, low importance: OK (top-left)
Low gap, high importance: SAFE (bottom-right)
Low gap, low importance: IGNORE (bottom-left)
```

---

## Calibration

**How to set thresholds:**

### Step 1: Baseline Measurement

Run for 2-4 weeks collecting data:
- Understanding scores
- Incident occurrences

### Step 2: Compute Correlation

```python
# Find correlation between understanding and incidents
r, p = pearsonr(understanding_scores, incident_counts)

if r < 0.4:
    print("Warning: Understanding score not predictive of incidents")
    # Need to adjust measurement method
```

### Step 3: Set Thresholds

```python
# Find understanding score that minimizes incidents

thresholds = np.arange(0.5, 0.9, 0.05)
incident_rates = []

for threshold in thresholds:
    # Simulate: what if we required this threshold?
    blocked_changes = count_blocked(understanding, threshold)
    resulting_incidents = count_incidents_after_blocking(blocked_changes)
    incident_rates.append(resulting_incidents)

optimal_threshold = thresholds[np.argmin(incident_rates)]
```

### Step 4: A/B Test

- **Control:** No understanding gates
- **Treatment:** Understanding gates at optimal threshold

**Measure:**
- Incident rate (should decrease 30-50%)
- Cycle time (acceptable increase 10-20%)

---

## Summary

**Key metrics:**

```python
# Individual
understanding[engineer, module] = weighted_avg(quiz, prediction, sandbox)
                                  × exp(-λ × time_since_last)

# Team
U_team[module] = weighted_mean(individual_scores, by=activity)

# Risk
risk[module] = (1 - U_team[module]) × importance[module]

# Knowledge debt
V_learning = sum(risk[module] for module in modules)
```

**Validation:**
- Correlation with incidents (r > 0.6)
- Predictive power (AUC > 0.7, lead time = 10 days)

**Governance:**
- Gate on understanding thresholds
- Prioritize learning by risk
- Adaptive tuning based on outcomes

**Next:** See `05-learning-governance.md` for how understanding gates control.
