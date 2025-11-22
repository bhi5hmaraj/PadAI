# Experiments as Model Tests

## Purpose

**Experiments are how we evaluate mental models empirically.**

Each experiment tests one or more models' predictions against reality.

---

## Experiment Design Principles

### Principle 1: One Experiment, Multiple Models

**Don't**: Design experiment for ONE model only
**Do**: Test multiple models simultaneously

**Example**:
- Experiment: Predict incidents
- Test simultaneously:
  - Physics: E_local at hubs
  - Ecology: Growth rate imbalance
  - Economics: Negative ROI modules
  - Cognitive: Complexity > 7 chunks

**Compare**: Which predictor has highest AUC?

**Winner**: Use that model for incident prediction.

---

### Principle 2: Comparative Analysis

**Always have baselines**:
- Naive baseline (predict mean, random)
- Simple baseline (single metric like health)
- Alternative models

**Example**:
- Baseline: health < 0.5 predicts incidents (AUC = 0.62)
- Physics: E_local > threshold (AUC = 0.78)
- **Result**: Physics adds 16 points, significant improvement

**No comparison → Can't judge model value.**

---

### Principle 3: Failure is Data

**If model fails (predictions wrong):**
- **Don't**: Ignore and try next model
- **Do**: Document why it failed, what was wrong

**Failure teaches**:
- Which assumptions violated?
- What did we misunderstand?
- Can model be refined?

**Example**:
- Physics predicts E_local warns early
- Test shows: E_local no better than health
- **Learn**: Coupling weights wrong? Laplacian formulation issue?
- **Action**: Revise coupling measurement OR try normalized Laplacian

---

## Mapping Experiments to Models

### Experiment 01: Baseline Validation

**Tests**: All models (sanity check)

**Question**: Does simulation reach equilibrium?

**Models tested**:
- **Physics**: H oscillates, not diverges
- **Ecology**: Population sizes stabilize
- **Economics**: Market clears
- **CAS**: No runaway criticality

**If ANY model's equilibrium violated → Debug before proceeding**

---

### Experiment 02: Incident Prediction

**Tests**: Physics vs. Baselines

**Question**: Does E_local predict incidents better than scalar metrics?

**Models tested**:
- **Physics**: E_local at hubs
- **Baseline**: health, complexity, bad

**Predictions**:
- Physics: AUC > 0.75, lead time ~10 steps
- Baseline: AUC ~0.60-0.65, lead time ~3 steps

**Outcome determines**: Use Laplacian for incident prediction? Or stick with simpler metrics?

**Extension**: Also test
- **Ecology**: Growth rate volatility
- **CAS**: Avalanche precursors

---

### Experiment 03: Governance Effectiveness

**Tests**: Physics governance rules

**Question**: Do H-thresholds and E_local gates reduce incidents?

**Models tested**:
- **Physics**: Governed system recovers faster
- **Economics**: Governance has ROI (cost < benefit)
- **Cognitive**: Constraints reduce load

**Predictions**:
- Physics: H_peak lower, incidents fewer
- Economics: ROI of governance > 3:1
- Cognitive: Comprehension improves

**Outcome determines**: Do governance rules work? Which model best explains why?

---

### Experiment 04: Resource Allocation

**New experiment** (not yet designed)

**Tests**: Economics vs. Ecology

**Question**: How do engineers allocate effort? Optimally (economics) or competitively (ecology)?

**Models tested**:
- **Economics**: Effort ∝ ROI
- **Ecology**: Effort ∝ niche availability

**Predictions**:
- Economics: Correlation(effort, ROI) > 0.7
- Ecology: Lotka-Volterra fits growth rates

**Design**:
- Track effort allocation across modules
- Measure ROI per module
- Test which model predicts allocation better

---

### Experiment 05: Comprehension Limits

**New experiment** (not yet designed)

**Tests**: Cognitive model

**Question**: Is there a ~7 chunk limit for comprehension?

**Model tested**:
- **Cognitive**: Modules with >7 responsibilities hard to understand

**Predictions**:
- Comprehension time spikes at ~7 chunks
- Error rate increases beyond 7

**Design**:
- Measure complexity (responsibilities per module)
- Measure comprehension time (how long to explain)
- Test: Threshold at 7±2?

---

### Experiment 06: Emergence & Criticality

**New experiment** (not yet designed)

**Tests**: CAS model

**Question**: Does coupling follow power law? Is system at critical point?

**Model tested**:
- **CAS**: Degree distribution P(k) ~ k^(-γ)

**Predictions**:
- Power law fit R² > 0.8
- Criticality indicators (susceptibility diverges)

**Design**:
- Measure degree distribution
- Fit power law, test goodness of fit
- Measure avalanche sizes (cascading changes)

---

## Comparative Analysis Protocol

### Step 1: Run Experiment

**Collect data for ALL candidate models simultaneously**:
```python
# Log for physics
log_physics = {
    'E_local': E_local_values,
    'H': H_values,
    'V_struct': V_struct_values,
}

# Log for ecology
log_ecology = {
    'growth_rates': growth_rates,
    'competition': competition_coefficients,
}

# Log for economics
log_economics = {
    'ROI': ROI_values,
    'effort_allocation': effort_allocation,
}

# Ground truth
incidents = incident_log
```

---

### Step 2: Test Each Model's Predictions

**For each model**:
```python
# Physics
auc_physics = test_predictor(E_local, incidents)

# Ecology
auc_ecology = test_predictor(growth_volatility, incidents)

# Economics
auc_economics = test_predictor(negative_roi, incidents)

# Baselines
auc_health = test_predictor(health, incidents)
```

---

### Step 3: Statistical Comparison

**Pairwise comparisons**:
```python
from scipy.stats import ttest_ind

# Compare physics vs baseline
p_value_physics_vs_health = compare_auc(auc_physics, auc_health)

# Compare ecology vs baseline
p_value_ecology_vs_health = compare_auc(auc_ecology, auc_health)

# Compare physics vs ecology
p_value_physics_vs_ecology = compare_auc(auc_physics, auc_ecology)
```

**Ranking**:
```python
models = {
    'Physics': auc_physics,
    'Ecology': auc_ecology,
    'Economics': auc_economics,
    'Health (baseline)': auc_health,
}

ranked = sorted(models.items(), key=lambda x: x[1], reverse=True)

print("Model ranking:")
for i, (model, auc) in enumerate(ranked, 1):
    print(f"{i}. {model}: AUC = {auc:.3f}")
```

---

### Step 4: Decision

**If one model dominates**:
- Use that model for this problem type
- Document in `04-model-selection.md`

**If multiple models close (within 0.05 AUC)**:
- Consider ensemble (combine predictions)
- Or pick simpler model (Occam's razor)

**If all models fail (no better than baseline)**:
- Re-examine problem
- Try alternative models
- Or improve measurement

---

## Model Performance Tracking

### Scorecard

**Maintain running scorecard**:

| Model | Incident Prediction | Effort Allocation | Comprehension | Average |
|-------|---------------------|-------------------|---------------|---------|
| **Physics** | 0.78 (✓) | - | - | 0.78 |
| **Ecology** | 0.65 | 0.72 (✓) | - | 0.69 |
| **Economics** | 0.62 | 0.75 (✓) | - | 0.69 |
| **Cognitive** | - | - | 0.82 (✓) | 0.82 |
| **Baseline** | 0.60 | 0.55 | 0.60 | 0.58 |

**Interpretation**:
- Physics best for incident prediction
- Economics best for effort allocation (close to Ecology)
- Cognitive best for comprehension
- Each model has domain where it excels

**Use**: Model selection based on problem domain.

---

## When to Abandon a Model

### Criteria for Abandonment

**Abandon if**:
1. **Never outperforms baseline** (across 3+ experiments)
2. **Predictions systematically wrong** (not just noisy, but biased)
3. **Interventions consistently fail** (can predict but can't improve)
4. **Unmeasurable in practice** (can't extract variables from real data)

**Example**:
- If Organism model never predicts better than simple health metric
- And recovery time doesn't correlate with "immune strength"
- And "homeostasis" too vague to measure
- **Then**: Abandon Organism model, remove from catalog

---

### Criteria for Refinement

**Refine if**:
1. **Sometimes works, sometimes doesn't** (context-dependent)
2. **Predictions noisy but unbiased** (measurement issue?)
3. **Close to baseline but not quite** (need parameter tuning?)

**Example**:
- If Physics model AUC = 0.68 (vs. baseline 0.62)
- Better but not by much
- **Then**: Try normalized Laplacian, different coupling weights, etc.
- Re-test after refinement

---

## Experimental Roadmap

### Phase 1: Test Physics Model (Current)

**Experiments**:
- Exp01: Baseline validation
- Exp02: Incident prediction (E_local)
- Exp03: Governance effectiveness

**Timeline**: 3-4 weeks

**Outcome**: Know if physics model is useful

---

### Phase 2: Test Alternative Models

**Experiments**:
- Exp04: Resource allocation (Economics vs. Ecology)
- Exp05: Comprehension limits (Cognitive)
- Exp06: Emergence (CAS)

**Timeline**: 6-8 weeks

**Outcome**: Comparative analysis across models

---

### Phase 3: Production Deployment

**Use validated models**:
- Best model for each problem type
- Ensemble where helpful
- Adaptive switching based on system state

**Timeline**: 3-6 months

**Outcome**: Tensegrity governance in production

---

## Integration with Meta-Framework

**This document connects**:
- `01-core-problem.md` → Defines what we're solving
- `02-model-catalog.md` → Lists candidate models
- `03-evaluation-framework.md` → Criteria for judging models
- `04-model-selection.md` → When to use which model
- **This doc** → How experiments test models
- `../experiments/` → Actual experimental designs

**The loop**:
1. Problem identified (01)
2. Model proposed (02)
3. Experiment designed (../experiments/)
4. Experiment run (this doc)
5. Model evaluated (03)
6. Model selected or rejected (04)
7. Repeat for next problem

---

## Summary

**Experiments are model tests**:
- Each experiment tests multiple models
- Comparative analysis (not just pass/fail)
- Track performance across domains
- Use best model for each problem type
- Abandon models that consistently fail
- Refine models that show promise

**The scientific method**:
- Hypothesize (model predicts X)
- Test (run experiment)
- Analyze (statistics, comparison)
- Decide (use model, refine, or abandon)
- Iterate

**Reality chooses the model, not us.**

---

**Next**: Design and run experiments in `../experiments/` directory.
