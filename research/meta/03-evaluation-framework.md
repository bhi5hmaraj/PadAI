# Evaluation Framework: How to Test Mental Models

## Purpose

**Not**: "Which model is elegant?"
**But**: "Which model predicts reality and guides effective interventions?"

**Empirical evaluation framework** with quantitative criteria.

---

## Criterion 1: Predictive Power

### What It Means

**Can the model predict outcomes before they happen?**

**Examples**:
- Physics: E_local spike → incident in 10 steps
- Ecology: High competition → one module will dominate
- Economics: High ROI → will attract more effort
- Cognitive: >7 chunks → comprehension will fail

### How to Measure

**ROC curves** for binary predictions:
- True positive rate vs. false positive rate
- AUC (Area Under Curve): 0.5 = random, 1.0 = perfect
- Compare model AUC vs. baselines

**Lead time** for early warnings:
- Time from prediction signal to actual outcome
- Want: Longer lead time = more actionable

**Accuracy metrics**:
- Precision, recall, F1 score
- Mean absolute error (for continuous predictions)
- R² for regression (how much variance explained?)

### Statistical Tests

**Compare two models**:
```python
# DeLong test for AUC comparison
from scipy.stats import bootstrap

auc_model_a = compute_auc(model_a_predictions, ground_truth)
auc_model_b = compute_auc(model_b_predictions, ground_truth)

p_value = delong_test(auc_model_a, auc_model_b)

# Hypothesis: Model A better than Model B if p < 0.05
```

**Significance threshold**: p < 0.05 (standard)

### Success Criteria

**Strong predictive power**:
- AUC > 0.75
- Significantly better than baselines (p < 0.05)
- Lead time > 5 steps

**Moderate**:
- AUC > 0.65
- Better than baselines (p < 0.10)

**Weak** (model not useful):
- AUC < 0.60
- Not better than baselines

---

## Criterion 2: Actionability

### What It Means

**Does the model suggest interventions that actually work?**

**Not enough to predict**—must guide actions.

**Examples**:
- Physics: "Reduce E_local by refactoring hub" → Does it work?
- Ecology: "Decouple competing modules" → Does competition decrease?
- Economics: "Reallocate to high-ROI" → Does efficiency improve?

### How to Measure

**A/B testing**:
- Intervention group: Apply model-suggested action
- Control group: No intervention (or baseline action)
- Measure outcome

**Effect size**:
```python
# Cohen's d (standardized difference)
d = (mean_intervention - mean_control) / pooled_std

# Interpretation:
# d > 0.8: Large effect
# d > 0.5: Medium effect
# d > 0.2: Small effect
# d < 0.2: Negligible
```

**Cost-benefit**:
- Benefit: Improvement in outcome
- Cost: Effort to implement intervention
- ROI: Benefit / Cost

### Success Criteria

**Highly actionable**:
- Interventions improve outcomes (p < 0.05)
- Effect size d > 0.5
- ROI > 3:1

**Moderately actionable**:
- Some improvement (p < 0.10)
- Effect size d > 0.3

**Not actionable**:
- No improvement, or
- Improvement too small to justify cost

---

## Criterion 3: Simplicity

### What It Means

**Is the model simple enough to use in practice?**

**Occam's Razor**: Prefer simpler models if predictive power is equal.

**Trade-off**: Complexity vs. accuracy.

### How to Measure

**Parameter count**:
- How many variables to measure?
- How many parameters to tune?
- Fewer = simpler

**Conceptual complexity**:
- Can a human understand it in <30 minutes?
- Can it be explained without math PhD?
- Does it require specialized tools?

**Implementation cost**:
- Lines of code to implement
- Engineer-days to build
- Dependencies required

### Success Criteria

**Simple**:
- <10 parameters
- Explainable in 10 minutes
- <1000 LOC to implement

**Moderate**:
- 10-30 parameters
- Requires some technical background
- 1000-5000 LOC

**Complex**:
- >30 parameters
- Requires specialist knowledge
- >5000 LOC

**Decision**: If two models have AUC within 0.05, pick simpler one.

---

## Criterion 4: Generality

### What It Means

**Does the model work across different contexts?**

**Want**: Model that applies to startups, enterprises, open source, different tech stacks.

### How to Measure

**Test across contexts**:
```python
contexts = [
    'startup_mvp',
    'enterprise_java',
    'open_source_python',
    'monolith',
    'microservices',
]

for context in contexts:
    auc = test_model(context)
    print(f"{context}: AUC = {auc:.2f}")

# Check variance
std_auc = np.std(aucs)

# High generality: Low variance across contexts
```

**Transfer learning**:
- Train model on one context
- Test on another
- Does it transfer?

### Success Criteria

**Highly general**:
- Works across all contexts (AUC > 0.65 in each)
- Low variance (std < 0.10)

**Moderately general**:
- Works in most contexts (>75%)
- Moderate variance

**Context-specific**:
- Only works in one context
- High variance

**Decision**: Prefer general models for production, specific models for niche cases.

---

## Criterion 5: Measurability

### What It Means

**Can we actually measure the model's variables?**

**No measurement → No validation → Can't use it.**

### How to Measure

**Data availability**:
- Can we extract variables from git history?
- From static analysis?
- From runtime telemetry?
- From surveys?

**Measurement cost**:
- Automatic (free)
- Semi-automatic (some manual work)
- Manual (expensive)

**Measurement reliability**:
- Inter-rater reliability (if manual)
- Test-retest reliability
- Measurement noise

### Success Criteria

**Highly measurable**:
- All variables automatic from existing data
- Low noise, high reliability

**Moderately measurable**:
- Most variables automatic
- Some manual annotation required

**Hard to measure**:
- Requires expensive instrumentation
- High noise, low reliability
- Subjective judgments

**Decision**: Can't validate unmeasurable models. Fix measurement first.

---

## Composite Score

### Weighted Evaluation

**Combine criteria**:
```python
score = (
    0.40 * predictive_power +  # Most important
    0.25 * actionability +
    0.15 * simplicity +
    0.10 * generality +
    0.10 * measurability
)

# Each criterion normalized to [0, 1]
```

**Rankings**:
1. Model with highest composite score wins
2. But check for deal-breakers (e.g., unmeasurable)

### Example Scorecard

| Model | Predictive | Actionable | Simple | General | Measurable | **Composite** |
|-------|-----------|-----------|--------|---------|------------|---------------|
| Physics | 0.85 (AUC) | 0.70 | 0.50 | 0.60 | 0.80 | **0.73** |
| Ecology | 0.65 | 0.60 | 0.80 | 0.70 | 0.60 | **0.66** |
| Economics | 0.70 | 0.75 | 0.70 | 0.80 | 0.70 | **0.72** |

**Interpretation**: Physics slightly better overall, but Economics close. Context matters.

---

## Experimental Protocol

### Step 1: Define Hypothesis

**Specific, testable, falsifiable**:
- "E_local at hubs predicts incidents better than health"
- NOT: "Physics is useful"

### Step 2: Design Experiment

**What to measure**:
- Independent variable (predictor)
- Dependent variable (outcome)
- Controls (baselines)
- Confounds (what to control for)

**Sample size**:
- Power analysis: How many runs for statistical power?
- Typically: 30+ data points minimum

### Step 3: Collect Data

**Run simulation or analyze real data**:
- Log all variables
- Multiple runs (Monte Carlo if stochastic)
- Save raw data (for reanalysis)

### Step 4: Analyze

**Statistical tests**:
- ROC curves, AUC
- t-tests, ANOVA (group comparisons)
- Regression (relationships)
- Effect sizes

**Visualizations**:
- Time series
- Scatter plots
- ROC curves
- Phase space

### Step 5: Interpret

**Accept or reject hypothesis**:
- p < 0.05 → Reject null (model is useful)
- p >= 0.05 → Fail to reject (insufficient evidence)

**Effect size matters**:
- Small p-value but tiny effect = not practical
- Need both statistical significance AND practical significance

### Step 6: Compare Models

**Head-to-head**:
- Same experiment, multiple models
- Compare AUCs, effect sizes
- Statistical test for difference

**Pick winner** or use ensemble.

---

## Pitfalls to Avoid

### Pitfall 1: Confirmation Bias

**Don't**: Only test the model you like.
**Do**: Test multiple models fairly.

### Pitfall 2: P-Hacking

**Don't**: Try 20 tests, report the one that worked.
**Do**: Pre-register hypothesis, report all tests.

### Pitfall 3: Overfitting

**Don't**: Tune model on test data.
**Do**: Train/validation/test split.

### Pitfall 4: Ignoring Effect Size

**Don't**: Celebrate p < 0.05 with tiny effect.
**Do**: Require meaningful effect size.

### Pitfall 5: Forgetting Cost

**Don't**: Pick complex model with 1% better AUC.
**Do**: Consider implementation cost, simplicity.

---

## Decision Framework

### When Model is Useful

**All of**:
1. Predictive power (AUC > 0.65, p < 0.05)
2. Actionability (interventions work, d > 0.3)
3. Measurability (can extract variables)

**Nice to have**:
4. Simplicity
5. Generality

**Use the model** if criteria met.

### When Model is Not Useful

**Any of**:
1. No predictive power (AUC ≈ 0.5)
2. Interventions don't work
3. Can't measure variables

**Don't use the model**—try alternatives.

### When to Revise Model

**If**:
- Moderate predictive power but not strong
- Works in some contexts but not others
- Measurable but noisy

**Then**:
- Refine formulas
- Add parameters
- Better measurement
- Re-test

---

## Next Steps

**Read**: `04-model-selection.md` for how to choose between models.

**Then**: Design experiments (see `../experiments/`) to test models empirically.

**Finally**: Use whichever model passes evaluation framework.
