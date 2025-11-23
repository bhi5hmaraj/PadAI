# Scoring Rubrics for Mental Model Evaluation

## Overview

**Purpose:** Quantitative and qualitative criteria for scoring models on each dimension.

**Philosophy:** Make evaluation as objective as possible, but accept that some judgment is necessary.

Each dimension scored 0-10:
- **Quantitative thresholds** - Objective metrics (AUC, error rate, runtime)
- **Qualitative rubrics** - Expert judgment (clarity, usability)
- **Composite scoring** - Combine multiple metrics when needed

**Usage:**
1. Run model on benchmark scenarios
2. Measure performance metrics
3. Apply rubrics from this document
4. Generate scores for spider graph

---

## Dimension 1: Predictive Power

### Definition

**Can the model predict future system states, failures, bottlenecks?**

### Quantitative Rubric

**For classification tasks (incident prediction):**

```python
from sklearn.metrics import roc_auc_score, precision_recall_curve

# Primary metric: AUC-ROC
auc = roc_auc_score(y_true, y_pred_proba)

if auc >= 0.90: score = 10
elif auc >= 0.85: score = 9
elif auc >= 0.80: score = 8
elif auc >= 0.75: score = 7
elif auc >= 0.70: score = 6
elif auc >= 0.65: score = 5
elif auc >= 0.60: score = 4
elif auc >= 0.55: score = 3
else: score = 1-2  # Near random guessing
```

**For regression tasks (predict numerical values):**

```python
# Primary metric: MAPE (Mean Absolute Percentage Error)
mape = mean(abs((y_true - y_pred) / y_true))

if mape <= 0.05: score = 10      # <5% error
elif mape <= 0.10: score = 9     # <10% error
elif mape <= 0.15: score = 8
elif mape <= 0.20: score = 7
elif mape <= 0.30: score = 5-6
elif mape <= 0.50: score = 3-4
else: score = 1-2  # >50% error
```

**For ranking tasks (prioritize by risk):**

```python
from scipy.stats import spearmanr

# Rank correlation between predicted and actual
rho, p_value = spearmanr(predicted_ranks, actual_ranks)

if rho >= 0.90 and p_value < 0.05: score = 10
elif rho >= 0.80: score = 8-9
elif rho >= 0.70: score = 6-7
elif rho >= 0.50: score = 4-5
else: score = 1-3
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Exceptional | - Identifies non-obvious risks<br>- Explains causal mechanisms<br>- Confidence intervals provided<br>- Validated on multiple scenarios |
| 7-8 | Strong | - Catches most major risks<br>- Some explanation of why<br>- Works well in-domain |
| 5-6 | Mediocre | - Better than random guessing<br>- Limited explanatory power<br>- Misses some important risks |
| 3-4 | Weak | - Barely better than baseline<br>- Many false positives/negatives<br>- Black box predictions |
| 0-2 | Poor | - No better than random<br>- Misleading predictions<br>- No justification |

### Example Application

**Scenario 1 (Incident Prediction):**

```python
# Physics model
physics_predictions = {
    'payment': 0.85,  # High coupling energy
    'analytics': 0.62,
    'auth': 0.34,
    # ...
}
physics_auc = 0.82
physics_score = 8  # Good predictive power

# Economics model
econ_predictions = {
    'payment': 0.65,  # Low budget allocation
    'analytics': 0.45,
    'auth': 0.30,
    # ...
}
econ_auc = 0.68
econ_score = 6  # Mediocre predictive power
```

**Qualitative assessment:**

- Physics: Explains via coupling energy (clear causal story) → +1 bonus
- Economics: Less direct connection to incidents → No bonus

**Final scores:** Physics = 9, Economics = 6

---

## Dimension 2: Actionability

### Definition

**Does the model suggest concrete interventions that actually work?**

### Quantitative Rubric

**For optimization problems (resource allocation):**

```python
# Compare to optimal solution
efficiency = model_objective_value / optimal_objective_value

if efficiency >= 0.98: score = 10    # Near-optimal
elif efficiency >= 0.95: score = 9
elif efficiency >= 0.90: score = 8
elif efficiency >= 0.85: score = 7
elif efficiency >= 0.75: score = 5-6
elif efficiency >= 0.60: score = 3-4
else: score = 1-2  # Worse than simple heuristics
```

**For intervention effectiveness (A/B test):**

```python
# Effect size (Cohen's d)
effect_size = (mean_treatment - mean_control) / pooled_std

if effect_size >= 0.8: score = 10     # Large effect
elif effect_size >= 0.5: score = 7-8  # Medium effect
elif effect_size >= 0.2: score = 4-6  # Small effect
else: score = 1-3  # No meaningful effect
```

**For multi-objective problems:**

```python
# Weighted score across objectives
objectives = {
    'incident_reduction': {'weight': 0.4, 'achieved': 0.75},
    'feature_velocity': {'weight': 0.3, 'achieved': 0.60},
    'team_morale': {'weight': 0.2, 'achieved': 0.85},
    'cost': {'weight': 0.1, 'achieved': 0.90},
}

composite = sum(obj['weight'] * obj['achieved'] for obj in objectives.values())

if composite >= 0.85: score = 9-10
elif composite >= 0.75: score = 7-8
elif composite >= 0.60: score = 5-6
else: score = 0-4
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Highly actionable | - Concrete steps (not vague advice)<br>- Feasible to implement<br>- Cost-effective<br>- Strong empirical validation |
| 7-8 | Actionable | - Specific recommendations<br>- Generally feasible<br>- Some validation |
| 5-6 | Somewhat actionable | - Some specifics, some vagueness<br>- May be expensive or difficult<br>- Limited validation |
| 3-4 | Weakly actionable | - Mostly vague ("improve quality")<br>- Unclear how to implement<br>- No validation |
| 0-2 | Not actionable | - No concrete suggestions<br>- Infeasible or contradictory<br>- Would make things worse |

### Example Application

**Scenario 3 (Technical Debt Crisis):**

```python
# Physics model recommendation
physics_strategy = {
    'refactor': ['payment', 'auth'],  # Specific modules
    'rationale': 'High V_struct (coupling energy)',
    'expected_impact': 'Incidents: 3/week → 1/week',
    'timeline': '6 weeks',
}

# Simulate
physics_actual_impact = {
    'incidents': 1.2_per_week,  # Close to prediction
    'debt_reduction': 0.35,
    'cost': 6.5_weeks,  # Slightly over budget
}
physics_effectiveness = 0.87  # 87% of multi-objective target
physics_score = 8

# System dynamics model recommendation
sysdyn_strategy = {
    'recommendation': 'Address reinforcing feedback loop',
    'rationale': 'Debt → Incidents → Firefighting → More debt',
    'intervention': 'Allocate 30% time to debt paydown (sustained)',
}

# Simulate
sysdyn_actual_impact = {
    'incidents': 1.8_per_week,  # Better, but slower improvement
    'debt_reduction': 0.25,
    'cost': 'ongoing commitment',  # Hard to measure
}
sysdyn_effectiveness = 0.72
sysdyn_score = 6  # Less specific than physics model
```

**Final scores:** Physics = 8, System Dynamics = 6

---

## Dimension 3: Simplicity

### Definition

**How easy is the model to understand and apply?**

### Quantitative Rubric

**Code complexity:**

```python
# Model implementation
loc = count_lines_of_code(model)
num_params = count_parameters(model)
cyclomatic_complexity = calculate_complexity(model)

complexity_index = log(loc / 100 + num_params / 10 + cyclomatic_complexity / 5)

simplicity_score = 10 / (1 + complexity_index)

# Thresholds
if simplicity_score >= 8: score = 9-10  # Very simple
elif simplicity_score >= 6: score = 7-8
elif simplicity_score >= 4: score = 5-6
elif simplicity_score >= 2: score = 3-4
else: score = 1-2  # Very complex
```

**Learning time (user study):**

```python
# Time for new user to achieve proficiency
avg_learning_time_hours = measure_via_user_study()

if avg_learning_time_hours <= 2: score = 10     # Hours to learn
elif avg_learning_time_hours <= 5: score = 8-9
elif avg_learning_time_hours <= 10: score = 6-7
elif avg_learning_time_hours <= 20: score = 4-5
elif avg_learning_time_hours <= 40: score = 2-3
else: score = 1  # Days/weeks to learn
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Very simple | - Explainable in 2 minutes<br>- Minimal prerequisites (high school math)<br>- Intuitive concepts<br>- Visual representations available |
| 7-8 | Simple | - Explainable in 10 minutes<br>- Some prerequisites (linear algebra)<br>- Mostly intuitive<br>- Good documentation |
| 5-6 | Moderate | - Requires 30+ minute intro<br>- College-level prerequisites<br>- Some non-intuitive concepts<br>- Adequate docs |
| 3-4 | Complex | - Requires multi-hour training<br>- Advanced prerequisites<br>- Many non-intuitive parts<br>- Sparse docs |
| 0-2 | Very complex | - Requires days of study<br>- Expert knowledge needed<br>- Opaque/black box<br>- Poor or no docs |

### Example Application

```python
# Physics model
physics_complexity = {
    'loc': 500,
    'params': 15,  # masses, coupling constants
    'prerequisites': ['linear algebra', 'basic physics'],
    'learning_time': 18_hours,
}
physics_score = 5  # Moderate complexity

# Economics model
econ_complexity = {
    'loc': 300,
    'params': 8,  # budgets, prices
    'prerequisites': ['basic economics'],  # Everyone understands markets
    'learning_time': 6_hours,
}
econ_score = 8  # Simple (intuitive concepts)

# Machine learning model
ml_complexity = {
    'loc': 2000,  # Including training pipeline
    'params': 1000+,  # Neural network weights
    'prerequisites': ['ML', 'statistics', 'Python'],
    'learning_time': 40_hours,
}
ml_score = 2  # Very complex (black box)
```

---

## Dimension 4: Scalability

### Definition

**Does the model work at different scales (1 agent vs 1000 agents)?**

### Quantitative Rubric

**Performance degradation:**

```python
# Measure accuracy/effectiveness at different scales
perf_small = run_model(n_agents=10)   # Baseline
perf_medium = run_model(n_agents=50)
perf_large = run_model(n_agents=100)

# Degradation from baseline
degradation = (perf_small - perf_large) / perf_small

if degradation <= 0.05: score = 10     # <5% degradation (or improvement!)
elif degradation <= 0.10: score = 9
elif degradation <= 0.20: score = 7-8
elif degradation <= 0.30: score = 5-6
elif degradation <= 0.50: score = 3-4
else: score = 1-2  # >50% degradation
```

**Computational scaling:**

```python
# Runtime vs problem size
import numpy as np

sizes = [10, 20, 50, 100]
runtimes = [measure_runtime(n) for n in sizes]

# Fit power law: runtime = a * n^b
log_sizes = np.log(sizes)
log_runtimes = np.log(runtimes)
b, log_a = np.polyfit(log_sizes, log_runtimes, 1)

# Score based on exponent
if b <= 1.2: score = 10      # Near-linear O(n)
elif b <= 1.5: score = 8-9   # O(n log n)
elif b <= 2.0: score = 6-7   # O(n²) but acceptable
elif b <= 2.5: score = 3-5   # O(n²) to O(n³)
else: score = 1-2  # Worse than cubic
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Excellent scalability | - Works well 1→1000 agents<br>- May improve at scale<br>- No architecture changes needed |
| 7-8 | Good scalability | - Works well 1→100 agents<br>- Minor degradation at scale<br>- Minimal adjustments needed |
| 5-6 | Moderate scalability | - Works 1→50 agents<br>- Noticeable degradation<br>- Some re-architecture needed |
| 3-4 | Poor scalability | - Struggles beyond 20 agents<br>- Significant degradation<br>- Major changes needed |
| 0-2 | Does not scale | - Breaks beyond 10 agents<br>- Fundamental bottlenecks<br>- Different model needed |

### Example Application

**Scenario 4 (Scaling Challenge):**

```python
# Central planning model
central_planning = {
    'n=10': {'decision_time': 5_min, 'throughput': 50_tasks_per_day},
    'n=50': {'decision_time': 22_min, 'throughput': 120_tasks_per_day},  # Should be 250
    'n=100': {'decision_time': 45_min, 'throughput': 180_tasks_per_day},  # Should be 500
}
degradation = (500 - 180) / 500 = 0.64  # 64% degradation
central_score = 2  # Does not scale (serial bottleneck)

# Market-based model
market = {
    'n=10': {'decision_time': 8_min, 'throughput': 45_tasks_per_day},  # Overhead for small scale
    'n=50': {'decision_time': 10_min, 'throughput': 230_tasks_per_day},
    'n=100': {'decision_time': 12_min, 'throughput': 480_tasks_per_day},
}
degradation = (500 - 480) / 500 = 0.04  # 4% degradation
market_score = 10  # Excellent scalability (actually improves with scale)
```

---

## Dimension 5: Measurability

### Definition

**Can we actually measure the model's variables in practice?**

### Quantitative Rubric

**Per-variable measurability:**

```python
# For each variable in model
measurability_scores = []

for variable in model.variables:
    if can_measure_directly(variable):
        score = 10  # e.g., LOC, runtime, bug count
    elif can_compute_from_logs(variable):
        score = 8   # e.g., coupling from call graph
    elif requires_instrumentation(variable):
        score = 6   # e.g., code coverage (need tooling)
    elif requires_survey(variable):
        score = 4   # e.g., understanding (subjective)
    elif requires_expert_judgment(variable):
        score = 2   # e.g., code quality (no clear metric)
    else:
        score = 0   # Cannot measure

    measurability_scores.append(score)

# Average across all variables
overall_score = mean(measurability_scores)
```

**Measurement cost:**

```python
# Cost to measure (time + money)
cost_per_measurement = {
    'free': 10,        # Already in logs
    'cheap': 8,        # <1 hour setup
    'moderate': 6,     # 1-8 hours setup
    'expensive': 3,    # 1+ days setup
    'prohibitive': 1,  # Custom infrastructure needed
}
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Easily measurable | - All variables directly observable<br>- Free or cheap to measure<br>- Real-time availability<br>- Low noise |
| 7-8 | Measurable | - Most variables observable<br>- Moderate instrumentation needed<br>- Near real-time<br>- Acceptable noise |
| 5-6 | Somewhat measurable | - Some variables require proxies<br>- Significant instrumentation<br>- Batch processing<br>- Noisy measurements |
| 3-4 | Hard to measure | - Many variables subjective<br>- Expensive measurement<br>- High latency<br>- Very noisy |
| 0-2 | Not measurable | - Variables mostly theoretical<br>- Prohibitively expensive<br>- No reliable method |

### Example Application

```python
# Physics model variables
physics_vars = {
    'V_struct': {'measurable': 'yes', 'method': 'compute from code graph', 'cost': 'cheap', 'score': 9},
    'T (kinetic)': {'measurable': 'yes', 'method': 'track changes over time', 'cost': 'moderate', 'score': 7},
    'Understanding': {'measurable': 'proxy', 'method': 'quizzes', 'cost': 'moderate', 'score': 5},
}
physics_measurability = mean([9, 7, 5]) = 7.0

# Economics model variables
econ_vars = {
    'Budget': {'measurable': 'yes', 'method': 'directly observable', 'cost': 'free', 'score': 10},
    'Market price': {'measurable': 'yes', 'method': 'auction results', 'cost': 'free', 'score': 10},
    'Agent utility': {'measurable': 'proxy', 'method': 'revealed preference', 'cost': 'cheap', 'score': 8},
}
econ_measurability = mean([10, 10, 8]) = 9.3

# Cognitive model variables
cognitive_vars = {
    'Mental model': {'measurable': 'subjective', 'method': 'interviews', 'cost': 'expensive', 'score': 3},
    'Cognitive load': {'measurable': 'proxy', 'method': 'fMRI or reaction time', 'cost': 'prohibitive', 'score': 1},
}
cognitive_measurability = mean([3, 1]) = 2.0
```

---

## Dimension 6: Generality

### Definition

**Does the model apply to many contexts? Or only narrow domains?**

### Quantitative Rubric

**Context coverage:**

```python
# Test model on diverse scenarios
contexts = [
    'web_app', 'ML_pipeline', 'embedded_system',
    'data_warehouse', 'mobile_app', 'API_service',
    'blockchain', 'gaming', 'robotics'
]

successes = sum(1 for ctx in contexts if model_works_well(ctx))
coverage = successes / len(contexts)

if coverage >= 0.80: score = 9-10   # Works in 80%+ of contexts
elif coverage >= 0.60: score = 7-8
elif coverage >= 0.40: score = 5-6
elif coverage >= 0.20: score = 3-4
else: score = 1-2  # Very narrow
```

**Transfer learning:**

```python
# Does model trained on one domain work on another?
model_trained_on_domain_A = train(data_A)
performance_on_domain_B = test(model, data_B)

transfer_ratio = performance_B / performance_A  # How much performance drops

if transfer_ratio >= 0.90: score = 10  # Minimal domain specificity
elif transfer_ratio >= 0.75: score = 8
elif transfer_ratio >= 0.50: score = 6
else: score = 0-4  # Highly domain-specific
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Very general | - Applies to 80%+ of contexts<br>- Core concepts transferable<br>- Minimal customization<br>- Works across scales and domains |
| 7-8 | General | - Applies to 60%+ of contexts<br>- Most concepts transferable<br>- Some customization needed |
| 5-6 | Moderate | - Applies to 40-60% of contexts<br>- Requires significant adaptation<br>- Domain knowledge needed |
| 3-4 | Narrow | - Applies to <40% of contexts<br>- Highly specialized<br>- Hard to transfer |
| 0-2 | Very narrow | - Single domain only<br>- Not transferable<br>- Context-specific assumptions |

### Example Application

```python
# Physics model
physics_contexts = {
    'web_app': True,           # Coupling, architecture
    'ML_pipeline': True,        # DAG structure
    'embedded_system': True,    # Structural problems
    'data_warehouse': True,     # Schema coupling
    'mobile_app': True,
    'API_service': True,
    'blockchain': False,        # Different paradigm (consensus, not structure)
    'gaming': True,             # Engine architecture
    'robotics': True,           # Control systems
}
physics_coverage = 7/9 = 0.78 → score = 7

# Economics model
econ_contexts = {
    'web_app': True,            # Resource allocation
    'ML_pipeline': True,         # Compute resources
    'embedded_system': False,    # No market for embedded resources
    'data_warehouse': True,      # Query optimization
    'mobile_app': True,
    'API_service': True,         # Rate limiting, pricing
    'blockchain': True,          # Native to blockchain!
    'gaming': False,             # Not applicable
    'robotics': False,
}
econ_coverage = 6/9 = 0.67 → score = 7
```

---

## Dimension 7: Learning Curve

### Definition

**How long does it take to learn and apply the model effectively?**

### Quantitative Rubric

**Time to proficiency:**

```python
# User study: Time until user can apply model independently
users = recruit_developers(n=20)
times = [measure_learning_time(user, model) for user in users]
avg_time_hours = mean(times)

if avg_time_hours <= 2: score = 10      # Hours
elif avg_time_hours <= 5: score = 9
elif avg_time_hours <= 10: score = 7-8
elif avg_time_hours <= 20: score = 5-6
elif avg_time_hours <= 40: score = 3-4
else: score = 1-2  # Days or weeks
```

**Retention (after 4 weeks):**

```python
# Do users remember how to use model after 1 month?
retention_score = test_users_after_4_weeks() / initial_proficiency

if retention >= 0.90: score = 10  # Stick well
elif retention >= 0.75: score = 8
elif retention >= 0.60: score = 6
elif retention >= 0.40: score = 4
else: score = 1-3  # Forgotten
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Very gentle | - <5 hours to proficiency<br>- No prerequisites<br>- Intuitive concepts<br>- High retention |
| 7-8 | Gentle | - 5-10 hours to proficiency<br>- Minimal prerequisites<br>- Mostly intuitive<br>- Good retention |
| 5-6 | Moderate | - 10-20 hours<br>- Some prerequisites<br>- Some non-intuitive parts<br>- Moderate retention |
| 3-4 | Steep | - 20-40 hours<br>- Significant prerequisites<br>- Many non-intuitive concepts<br>- Low retention |
| 0-2 | Very steep | - >40 hours<br>- Expert knowledge needed<br>- Opaque<br>- Poor retention |

---

## Dimension 8: Computational Cost

### Definition

**How expensive is it to compute the model's predictions/simulations?**

### Quantitative Rubric

**Runtime:**

```python
# Benchmark on standard problem (100 agents, 1000 steps)
import time

start = time.time()
model.run_simulation(n_agents=100, n_steps=1000)
runtime_seconds = time.time() - start

if runtime_seconds < 1: score = 10       # Sub-second
elif runtime_seconds < 5: score = 9
elif runtime_seconds < 10: score = 8
elif runtime_seconds < 30: score = 6-7
elif runtime_seconds < 60: score = 4-5
else: score = 1-3  # Minutes or more
```

**Space complexity:**

```python
# Memory usage
memory_mb = measure_peak_memory(model)

if memory_mb < 100: score = 10     # <100 MB
elif memory_mb < 500: score = 8
elif memory_mb < 1000: score = 6   # <1 GB
elif memory_mb < 5000: score = 4   # <5 GB
else: score = 1-3  # >5 GB
```

### Qualitative Rubric

| Score | Description | Criteria |
|-------|-------------|----------|
| 9-10 | Very cheap | - Sub-second runtime<br>- <100 MB memory<br>- Real-time capable<br>- Parallelizable |
| 7-8 | Cheap | - <10 seconds<br>- <500 MB<br>- Near real-time<br>- Some parallelism |
| 5-6 | Moderate | - 10-60 seconds<br>- <1 GB<br>- Batch processing OK<br>- Limited parallelism |
| 3-4 | Expensive | - Minutes<br>- >1 GB<br>- Overnight batch<br>- Hard to parallelize |
| 0-2 | Very expensive | - Hours+<br>- >5 GB<br>- Rare re-runs only<br>- Not parallelizable |

---

## Composite Scoring

### Unweighted Average

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

### Weighted Average (Example Weights)

```python
weights = {
    'predictive_power': 0.25,     # Most important
    'actionability': 0.25,        # Most important
    'simplicity': 0.10,
    'scalability': 0.15,
    'measurability': 0.10,
    'generality': 0.05,
    'learning_curve': 0.05,
    'computational_cost': 0.05,
}

composite_score = sum(dimension * weights[name] for dimension, name in ...)
```

**Note:** Weights should be adjusted based on use case.

---

## Statistical Significance

### Hypothesis Testing

**When comparing two models:**

```python
from scipy.stats import ttest_ind

# Scenario: Run each model 30 times, measure performance
model_A_scores = [run_model(A) for _ in range(30)]
model_B_scores = [run_model(B) for _ in range(30)]

t_stat, p_value = ttest_ind(model_A_scores, model_B_scores)

if p_value < 0.05:
    print("Model A is significantly different from Model B")
else:
    print("No significant difference")
```

### Confidence Intervals

```python
import numpy as np

mean_score = np.mean(scores)
std_error = np.std(scores) / np.sqrt(len(scores))
ci_95 = (mean_score - 1.96 * std_error, mean_score + 1.96 * std_error)

print(f"Score: {mean_score:.2f} (95% CI: {ci_95[0]:.2f}-{ci_95[1]:.2f})")
```

---

## Summary: Rubric Application

**For each model:**

1. **Run on all benchmark scenarios** (from `02-benchmark-scenarios.md`)
2. **Measure quantitative metrics** (AUC, MAPE, runtime, etc.)
3. **Apply rubrics** (convert metrics to 0-10 scores)
4. **Assess qualitative criteria** (expert judgment)
5. **Combine** (average or weighted)
6. **Visualize** (spider graph)

**Example workflow:**

```python
# Evaluate physics model
physics_scores = {
    'predictive_power': 8,      # AUC = 0.82
    'actionability': 7,         # Efficiency = 0.87
    'simplicity': 5,            # LOC = 500, params = 15
    'scalability': 9,           # <10% degradation
    'measurability': 7,         # Some variables need instrumentation
    'generality': 7,            # 78% context coverage
    'learning_curve': 5,        # 18 hours to proficiency
    'computational_cost': 8,    # 5 seconds runtime
}

# Plot spider graph
plot_spider(physics_scores)
```

**Next:** See `04-model-comparison.md` for actual model scores and comparisons.
