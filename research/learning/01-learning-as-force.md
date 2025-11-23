# Learning as Force

## Overview

In the five-force tensegrity model, **learning is a tension force** that resists epistemic drift.

**The five forces:**

```
Compression (drives motion):
├─ Velocity: ship fast, add features, scale
└─ Scope: deadlines, focus, resource constraints

Tension (resists degradation):
├─ Quality: tests, correctness, reliability
├─ Coherence: architecture, coupling, consistency
└─ Learning: human understanding, mental models
```

Like a tensegrity structure, you need **both compression and tension** for stability.

## Learning as Tension

### What Does Learning Resist?

Learning force resists:

1. **Epistemic drift** - divergence between human model and ground truth
2. **Knowledge debt** - accumulated gaps in understanding
3. **Uninformed decisions** - governance without comprehension
4. **Coordination failures** - agents acting on inconsistent mental models

### How Does It Create Tension?

Learning creates tension by:

1. **Slowing velocity** - active learning takes time
2. **Gating decisions** - can't approve what you don't understand
3. **Requiring practice** - deliberate struggle, not passive reading
4. **Challenging assumptions** - prediction → feedback → update

### The Trade-off

```
More learning:
  ✓ Better understanding
  ✓ Safer decisions
  ✓ Lower knowledge debt
  ✗ Slower shipping
  ✗ More cognitive load

Less learning:
  ✓ Faster velocity
  ✓ Lower friction
  ✗ Epistemic risk
  ✗ Knowledge debt accumulates
  ✗ Governance becomes guesswork
```

## Force Balance Regimes

### Regime 1: Learning-Dominated (High Tension)

**Characteristics:**
- Frequent comprehension challenges
- Understanding gates all approvals
- Extensive review/practice required
- Slow but safe

**Example profiles:**
- Medical device firmware
- Financial trading systems
- Safety-critical infrastructure

**Indicators:**
- Low incident rate
- High understanding scores
- Slow cycle time
- Low knowledge debt

**Energy signature:**
- High V_learning (epistemic potential)
- Low T (slow evolution)
- System in controlled equilibrium

### Regime 2: Velocity-Dominated (Low Learning Tension)

**Characteristics:**
- Minimal learning gates
- Ship fast, learn later (or never)
- Sparse comprehension checks
- Fast but risky

**Example profiles:**
- Early-stage startup MVP
- Hackathon prototype
- Exploratory research code

**Indicators:**
- High feature velocity
- Low understanding scores
- Fast cycle time
- Growing knowledge debt

**Energy signature:**
- Low V_learning (don't care about gaps)
- High T (rapid change)
- System in chaotic exploration

### Regime 3: Balanced Tensegrity

**Characteristics:**
- Adaptive learning frequency
- Understanding-gated for critical modules
- Light touch for low-risk areas
- Sustainable velocity + safety

**Example profiles:**
- Mature product team
- Enterprise SaaS
- Open-source with governance

**Indicators:**
- Moderate velocity
- High understanding on core modules
- Acceptable cycle time
- Bounded knowledge debt

**Energy signature:**
- Moderate V_learning (selective investment)
- Moderate T (controlled evolution)
- System oscillates near equilibrium

## Physics Interpretation

### Learning as Potential Energy

In our Hamiltonian framework:

```
V_learning = Σ epistemic_gap[i] × importance[i]
```

Where:
- `epistemic_gap[i] = (1 - understanding[i])` - how much is unknown
- `importance[i] = demand[i] × complexity[i]` - how critical the module is

**Interpretation:**
- High gap in critical module → high potential energy
- System under epistemic tension
- Governance should slow velocity until gap closes

### Learning as Constraint

Alternatively, model learning as a **constraint** on motion:

```
Constraint: understanding[i] > threshold  (for critical modules)

If violated:
  → Block changes to module i
  → Trigger active learning
  → Require passing comprehension challenges
```

This is analogous to physical constraints (e.g., rope length in a pendulum).

### Learning as Damping

Learning can also act as **friction/damping**:

```
F_learning = -β × velocity

Where β = learning_intensity
```

**Effect:**
- More learning → higher friction → slower changes
- Less learning → lower friction → faster but riskier

## Force Tuning Parameters

How to adjust learning force in practice:

### 1. Learning Frequency

**Parameter:** `f_learning` - how often to trigger learning events

```python
f_learning = {
  'critical_modules': 0.5,  # 50% of changes trigger learning
  'normal_modules': 0.1,    # 10%
  'low_risk_modules': 0.01, # 1%
}
```

**Effect:** Higher frequency → stronger learning force → more tension

### 2. Understanding Threshold

**Parameter:** `U_min` - minimum understanding score to approve changes

```python
U_min = {
  'critical': 0.8,  # 80% understanding required
  'normal': 0.6,    # 60%
  'low_risk': 0.3,  # 30%
}
```

**Effect:** Higher threshold → stronger gate → more tension

### 3. Learning Difficulty

**Parameter:** `difficulty` - complexity of comprehension challenges

```python
difficulty = {
  'basic': 'recall facts',
  'intermediate': 'explain behavior',
  'advanced': 'predict impact + debug',
}
```

**Effect:** Higher difficulty → deeper understanding required → slower but safer

### 4. Adaptive Dial

**Auto-tune learning force based on:**

```python
# Increase learning if:
if incident_rate > threshold:
    learning_force *= 1.2  # Strengthen

if understanding_scores < target:
    learning_force *= 1.1

# Decrease learning if:
if user_skip_rate > 0.8:
    learning_force *= 0.8  # Weaken

if cycle_time > 2 * baseline:
    learning_force *= 0.9
```

## Integration with Other Forces

Learning interacts with all forces:

### Learning × Velocity

**Tension relationship:**
- Learning slows velocity (time spent understanding)
- But reduces rework (better decisions upfront)
- Net effect depends on knowledge debt level

**Optimization:**
- High debt → invest in learning (pays off long-term)
- Low debt → can reduce learning (ship faster)

### Learning × Quality

**Synergistic relationship:**
- Learning improves quality (informed decisions → fewer bugs)
- Quality tests provide learning feedback (test failures → gaps)

**Combined effect:**
- Both are tension forces
- Reinforce each other
- Create stable, high-quality equilibrium

### Learning × Coherence

**Mutual dependency:**
- Learning requires coherent mental models
- Coherence requires shared understanding

**Effect:**
- Learning force strengthens coherence naturally
- Coherence makes learning more effective

### Learning × Scope

**Trade-off relationship:**
- Scope compression (tight deadlines) → reduce learning
- Scope expansion (add features) → increase learning needs

**Governance:**
- Use scope to modulate learning force
- "We can ship this fast IF we reduce scope to what team already understands"

## Measurement

**How to measure learning force strength:**

1. **Time spent on learning activities**
   - Minutes per week in challenges, reviews, practice
   - As % of total dev time

2. **Gating frequency**
   - % of PRs blocked due to understanding gaps
   - Average time to clear gate

3. **Understanding coverage**
   - % of codebase with U[i] > threshold
   - Weighted by importance

4. **Knowledge debt growth rate**
   - Δ(knowledge_debt) / Δt
   - Positive = accumulating, negative = paying down

**Example metrics:**

```
Weak learning force:
  - 5% time on learning
  - 10% PRs gated
  - 40% coverage
  - +15% debt/month

Strong learning force:
  - 25% time on learning
  - 60% PRs gated
  - 85% coverage
  - -10% debt/month (paying down)
```

## Failure Modes

### Too Strong (Over-Learning)

**Symptoms:**
- Cycle time explodes
- Engineers frustrated by excessive gates
- Velocity near zero
- System "frozen"

**Energy signature:**
- Very low T (no motion)
- High V_learning (over-investing)

**Fix:** Reduce learning force (lower frequency, easier challenges)

### Too Weak (Under-Learning)

**Symptoms:**
- Frequent incidents
- Poor decision quality
- Growing knowledge debt
- Coordination failures

**Energy signature:**
- High T (chaos)
- Low V_learning (ignoring gaps)
- Incidents accumulating

**Fix:** Increase learning force (more challenges, higher gates)

### Misaligned

**Symptoms:**
- Learning on wrong modules
- Low-impact areas over-gated
- Critical areas under-gated

**Fix:** Reweight importance function (focus on high-demand, high-complexity)

## Summary

**Learning is structural tension, not aspirational.**

Key points:

1. Learning force resists epistemic drift
2. Creates tension by slowing velocity, gating decisions
3. Strength tuned via frequency, thresholds, difficulty
4. Interacts with all other forces
5. Balance depends on risk profile, team maturity, domain

**Next:** See `02-epistemic-energy.md` for mathematical formulation of learning as potential energy.
