# Showroom Experiments: Testing Socio-Technical Dynamics

## Overview

**Experimentalist principle:** Don't theorize - test.

This document provides concrete experiments to validate:
1. System dynamics model (stocks, flows, feedback loops)
2. Software physics (nested within business)
3. AI agent impact
4. Learning as coupling (Impact = Quality × Understanding × Fit)

Each experiment includes: Hypothesis, Method, Measurement, Success criteria.

---

## Experiment 1: Mental Model Audit

### Hypothesis

**Family's mental model of business drivers differs significantly from data.**

### Method

**Week 1: Elicit mental model**

Ask family to rank factors that drive sales (1-10):

```
___ Location (showroom visibility)
___ Price (discounts, promotions)
___ Advertising (social media, local ads)
___ Referrals (word-of-mouth)
___ Test drives offered
___ Service quality
___ Staff knowledge
___ Inventory availability
___ Bike model variety
___ Financing options
```

Family prediction: "Advertising is #1, referrals are #5"

**Week 2-8: Collect data**

Track:
- Sales (weekly)
- Each factor (weekly): ad spend, referrals received, test drives, etc.

**Week 9: Analyze**

Run regression:

```python
from sklearn.linear_model import LinearRegression

X = data[['advertising', 'referrals', 'test_drives', ...]]
y = data['sales']

model = LinearRegression().fit(X, y)
coefficients = model.coef_

# Rank by absolute coefficient (actual importance)
actual_ranking = sorted(zip(features, coefficients), key=lambda x: abs(x[1]), reverse=True)
```

Compare predicted ranking vs actual ranking.

### Measurement

**Rank correlation:**

```python
from scipy.stats import spearmanr

rho, p_value = spearmanr(predicted_ranks, actual_ranks)
```

**Interpretation:**
- rho = 1.0: Perfect agreement (family's model is accurate)
- rho = 0.0: No correlation (family's model is wrong)
- rho < 0: Inverse (family believes opposite of reality!)

### Success Criteria

**If rho < 0.5:** Family mental model is significantly wrong → Learning investment is crucial

**If rho > 0.8:** Family already has good intuition → Can trust their judgment, analytics is incremental

---

## Experiment 2: Understanding-Impact Correlation

### Hypothesis

**Software impact correlates with family understanding, controlling for quality.**

```
Impact = Quality × Understanding × Fit
```

### Method

**Build 3 simple analytics features:**

1. **Customer segmentation** (by purchase behavior)
2. **Service retention forecast** (who's likely to return?)
3. **Inventory turnover dashboard** (which bikes are slow-moving?)

**For each feature:**

**Week 1: Deploy with minimal training**

- Give access to dashboard
- Brief explanation (5 minutes)
- Measure initial understanding (quiz score)

**Week 2-4: Measure usage and impact**

- Usage: # times accessed per week
- Impact: Revenue/retention/cash flow change

**Week 5: Intensive active learning**

- Prediction challenges
- Sandbox simulation
- Feedback loops
- Measure understanding (post-training score)

**Week 6-8: Measure usage and impact again**

### Measurement

**Understanding scores:**

```python
understanding_before = [0.3, 0.4, 0.5]  # Feature 1, 2, 3
understanding_after = [0.7, 0.8, 0.9]   # After active learning
```

**Impact metrics:**

```python
impact_before = [₹10k, ₹5k, ₹15k]  # Revenue lift per feature
impact_after = [₹40k, ₹30k, ₹55k]  # After active learning
```

**Regression:**

```python
from sklearn.linear_model import LinearRegression

# Assume quality and fit are constant
X = np.array(understanding_scores).reshape(-1, 1)
y = np.array(impact_values)

model = LinearRegression().fit(X, y)

print(f"Slope: {model.coef_[0]}")  # ₹ per unit of understanding
print(f"R²: {model.score(X, y)}")  # How much variance explained
```

### Success Criteria

**If R² > 0.6:** Understanding significantly predicts impact → Validates coupling hypothesis

**If slope > ₹100k:** 1.0 increase in understanding (e.g., 0.4 → 1.4) yields ₹100k+ revenue

→ Learning ROI is massive, invest heavily

---

## Experiment 3: AI Agent Trust Dynamics

### Hypothesis

**AI recommendation acceptance rate follows trust feedback loop:**

```
Good recommendations → Acceptance → Good outcomes → Trust grows → More acceptance (virtuous)
```

### Method

**Week 1-4: Baseline (no AI)**

- Family makes decisions manually (which leads to prioritize, how much inventory to order)
- Track: Decision quality, outcomes

**Week 5-12: AI recommendations (with transparency)**

Deploy AI agent (e.g., sales assistant, inventory optimizer)

**For each recommendation:**

```python
recommendation = ai_agent.recommend(context)

# Track
log = {
    'timestamp': now(),
    'recommendation': recommendation,
    'explanation': ai_agent.explain_why(),  # Transparent
    'human_decision': family_accepts_or_rejects,
    'outcome': measure_after_1_week(),
}
```

**Week 13: Analyze**

### Measurement

**Acceptance rate over time:**

```python
acceptance_rate_by_week = [
    0.20,  # Week 5 (low initial trust)
    0.35,  # Week 6
    0.50,  # Week 7
    0.70,  # Week 8 (trust building)
    0.85,  # Week 9
    0.90,  # Week 10+ (high trust, virtuous cycle)
]
```

**AI recommendation quality:**

```python
outcomes = {
    'ai_accepted': avg_revenue_when_family_accepted_AI,
    'ai_rejected': avg_revenue_when_family_rejected_AI_and_did_manual,
    'no_ai': avg_revenue_from_baseline_weeks,
}

ai_lift = outcomes['ai_accepted'] - outcomes['no_ai']
```

**Trust dynamics:**

```python
# Fit logistic growth curve to acceptance rate
from scipy.optimize import curve_fit

def logistic(t, L, k, t0):
    return L / (1 + np.exp(-k * (t - t0)))

weeks = [5, 6, 7, 8, 9, 10, 11, 12]
acceptance = [0.20, 0.35, 0.50, 0.70, 0.85, 0.90, 0.92, 0.93]

params, _ = curve_fit(logistic, weeks, acceptance)
L, k, t0 = params

print(f"Asymptotic acceptance: {L:.2f}")
print(f"Growth rate: {k:.2f}")
print(f"Inflection point: Week {t0:.1f}")
```

### Success Criteria

**If asymptotic acceptance > 0.80:** Trust builds to high level → Virtuous cycle confirmed

**If ai_lift > ₹50k/month:** AI recommendations improve outcomes → Worth the investment

**If trust breaks down (acceptance decreases):** Investigate root cause (bad recommendations? Lack of transparency?)

---

## Experiment 4: Active Learning ROI

### Hypothesis

**Active learning (prediction challenges) yields higher ROI than passive documentation.**

### Method

**Build one complex analytics feature** (e.g., dynamic pricing recommendation)

**Group A (Control): Passive learning**

- Provide documentation (10-page guide)
- One-time training session (1 hour)
- No follow-up

**Group B (Treatment): Active learning**

- Brief intro (15 minutes)
- Prediction challenges (weekly, 10 minutes each)
- Sandbox simulation (practice pricing scenarios)
- Feedback loops (compare predictions to actuals)

**Duration:** 8 weeks

### Measurement

**Understanding scores (weekly quiz):**

```python
understanding_A = [0.4, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1]  # Decay without practice
understanding_B = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.9]  # Growth with practice
```

**Usage frequency:**

```python
usage_A = [2, 1, 0, 0, 0, 0, 0, 0]  # Tried once, gave up
usage_B = [3, 5, 7, 8, 10, 12, 12, 12]  # Increasing usage
```

**Business impact:**

```python
revenue_lift_A = ₹10k  # Minimal (didn't really use it)
revenue_lift_B = ₹80k  # High (confident usage)
```

**Effort investment:**

```python
effort_A = 1 hour (training) + 10 hours (doc creation) = 11 hours
effort_B = 0.25 hours intro + 8 weeks × 0.5 hours challenges + 2 hours sandbox = 6.25 hours

# Actually LESS effort than passive approach!
```

### Success Criteria

**If understanding_B > 2× understanding_A:** Active learning significantly more effective

**If revenue_lift_B / effort_B > revenue_lift_A / effort_A:** Active learning has better ROI

→ Active learning is superior, adopt it as standard practice

---

## Experiment 5: Nested Systems Validation

### Hypothesis

**Software impact cascades through business dynamics:**

```
Analytics quality → Decision quality → Business outcome → Feedback to analytics (virtuous cycle)
```

### Method

**Track multi-level metrics for 6 months:**

**Software level (weekly):**

```python
software_metrics = {
    'bugs': count_of_bugs,
    'technical_debt': V_struct,
    'features': feature_count,
    'understanding': avg_understanding_score,
}
```

**Decision level (weekly):**

```python
decision_metrics = {
    'informed_by_analytics': % of decisions using data,
    'prediction_accuracy': % of predictions that were correct,
    'decision_quality': % of decisions that improved outcomes,
}
```

**Business level (weekly):**

```python
business_metrics = {
    'revenue': ₹,
    'customer_retention': %,
    'inventory_turnover': units/week,
    'cash_flow': ₹,
}
```

### Measurement

**Causal chain analysis (lagged correlations):**

```python
# Does software quality predict decision quality 1 week later?
corr_software_decision = correlate(software_metrics['understanding'][t], decision_metrics['quality'][t+1])

# Do good decisions predict business outcomes 2 weeks later?
corr_decision_business = correlate(decision_metrics['quality'][t], business_metrics['revenue'][t+2])

# Does business growth feedback to better analytics 4 weeks later?
corr_business_software = correlate(business_metrics['revenue'][t], software_metrics['features'][t+4])
```

**Mediation analysis:**

```
Software quality → Decision quality → Business outcome

# Test if decision quality mediates the relationship
```

### Success Criteria

**If all correlations > 0.5:** Strong causal chain → Nested systems model validated

**If virtuous cycle confirmed:** Business growth → More data → Better analytics → Better decisions → More growth

→ System is in healthy feedback loop, continue investing

**If death spiral detected:** Bad software → Bad decisions → Business suffers → Less trust → Worse software

→ Emergency intervention needed (fix software quality, rebuild trust)

---

## Experiment 6: AI-Human Collaboration Modes

### Hypothesis

**Optimal collaboration mode depends on task complexity and trust level:**

```
Simple task + Low trust → Human decides, AI observes
Complex task + High trust → AI decides, Human supervises
```

### Method

**Define 4 collaboration modes:**

1. **Human-only** (no AI)
2. **AI suggests, human decides** (low automation)
3. **AI decides, human can override** (high automation)
4. **AI decides autonomously** (full automation)

**Test on 3 task types:**

- **Simple:** Send service reminder SMS (low stakes)
- **Medium:** Prioritize sales leads (medium stakes)
- **Complex:** Dynamic pricing (high stakes)

**For each (task, mode) pair, run for 2 weeks, measure:**

```python
metrics = {
    'outcome_quality': revenue, retention, etc.,
    'human_effort': hours spent,
    'human_satisfaction': survey 1-10,
    'trust_level': % of AI recommendations accepted,
}
```

### Measurement

**Optimal mode by task:**

```python
# Simple task
modes_simple = {
    'human_only': {'quality': 7, 'effort': 5, 'satisfaction': 6},
    'ai_suggests': {'quality': 8, 'effort': 3, 'satisfaction': 8},  # BEST
    'ai_decides': {'quality': 8, 'effort': 1, 'satisfaction': 7},   # Also good
    'autonomous': {'quality': 7, 'effort': 0, 'satisfaction': 5},  # Trust issue
}

# Complex task
modes_complex = {
    'human_only': {'quality': 6, 'effort': 10, 'satisfaction': 4},  # Overwhelmed
    'ai_suggests': {'quality': 9, 'effort': 6, 'satisfaction': 9},  # BEST
    'ai_decides': {'quality': 7, 'effort': 3, 'satisfaction': 5},   # Too risky
    'autonomous': {'quality': 5, 'effort': 0, 'satisfaction': 2},   # Dangerous
}
```

### Success Criteria

**If sweet spot found:** Certain (task, mode) combinations yield 2× better outcomes

**Design principle:** Match automation level to task complexity and trust

- Simple tasks → Automate more (low risk)
- Complex tasks → Keep human in loop (high stakes)
- As trust grows, can increase automation

---

## Summary: Experimental Roadmap

**Phase 1 (Weeks 1-8): Baseline**

- Experiment 1: Mental model audit
  - Understand family's current beliefs
  - Identify largest gaps (highest-leverage learning targets)

**Phase 2 (Weeks 9-16): Build + Learn**

- Build 3 simple analytics features
- Experiment 2: Understanding-impact correlation
  - Validate: Impact = Quality × Understanding × Fit
  - Test active learning vs passive

**Phase 3 (Weeks 17-24): AI Agents**

- Deploy AI sales assistant, inventory optimizer
- Experiment 3: AI trust dynamics
  - Track acceptance rate, outcomes
  - Identify virtuous cycle or death spiral

**Phase 4 (Weeks 25-32): Optimization**

- Experiment 4: Active learning ROI
  - Quantify value of prediction challenges
  - Optimize learning investment

- Experiment 6: AI-human collaboration modes
  - Find optimal automation level per task

**Phase 5 (Months 9-12): Validation**

- Experiment 5: Nested systems validation
  - Confirm causal chain: Software → Decisions → Business
  - Detect feedback loops (virtuous or vicious)

**Expected outcomes:**

- Quantified understanding-impact relationship
- Optimized learning investment (ROI on active learning)
- AI collaboration patterns (when to automate, when to keep human in loop)
- Validated nested systems model (physics + dynamics)

**Cost:** ~2-3 hours/week for data collection, analysis
**Benefit:** Evidence-based decisions (not guesswork)

**Philosophy:** Build → Measure → Learn → Iterate (scientific method for socio-technical systems)
