# Confusions: The Lab Notebook of Unresolved Concepts

## Purpose

*[Channeling Feynman's honesty]*

This is where we write down **what we don't understand yet**.

Not the polished equations. Not the beautiful diagrams. The **actual confusions** that arise when trying to implement the theory.

**Every experimentalist keeps this notebook.** When you can't make the apparatus work, when the measurement doesn't make sense, when two formulas contradict—you write it here.

Then you **resolve it**. Update the theory. Test again.

**This is where the real physics happens.**

---

## Status Legend

- **🔴 UNRESOLVED**: Active confusion, needs work
- **🟡 IN PROGRESS**: Working on resolution
- **🟢 RESOLVED**: Clarified, documented, tested

---

## Active Confusions

### 🟢 CONFUSION #1: What exactly is "mass"? [RESOLVED]

**Date raised**: 2025-11-22
**Date resolved**: 2025-11-22
**Raised by**: Implementation of kinetic energy formula

**The problem**:

In `mvp-model.md`, we define kinetic energy as:
```
T = ½ Σ_i m_i (Δbad_i)²
```

But **what is m_i**?

**Resolution: m_i = 1 (uniform mass for MVP)**

**Justification**:
1. **Simplicity**: Start with simplest model (Occam's razor)
2. **Physical analog**: In spring networks, all masses equal unless specified
3. **Testable**: Can compare uniform vs. weighted mass later
4. **MVP goal**: Validate Laplacian predictions first, optimize mass later

**Formula for MVP**:
```python
T = 0.5 * np.sum((bad - bad_prev)**2)
# Equivalent to: m_i = 1 for all i
```

**Post-MVP refinement**:
- If T too small/large, try m_i = demand[i] (business-weighted)
- Sensitivity analysis: vary mass, measure impact on predictions
- Document in `06-future-directions.md` as research question

**Status**: 🟢 RESOLVED (MVP: uniform mass)

---

### 🟢 CONFUSION #2: How to compute "risk" field? [RESOLVED]

**Date raised**: 2025-11-22
**Date resolved**: 2025-11-22
**Raised by**: SimulationState initialization

**The problem**:

We have three primitive fields: health, complexity, demand.
We have one **derived** field: badness = f(health, complexity, risk).

But `risk` appears in the badness formula - circular dependency?

**Resolution: risk is DERIVED, not primitive**

**Formula**:
```python
risk[i] = complexity[i] * (1 - health[i])
```

**Justification**:
1. **Physical meaning**: Risk = "danger of failure" = complexity when unhealthy
2. **No circularity**: risk computed from health & complexity, THEN used in badness
3. **Intuitive**: High complexity + low health = high risk
4. **Measurable**: Both inputs are primitive fields

**Computation order** (breaks circularity):
```python
# Step 1: Update primitive fields (health, complexity, demand)
state.health[i] = ...  # From events
state.complexity[i] = ...

# Step 2: Compute derived risk
state.risk[i] = state.complexity[i] * (1 - state.health[i])

# Step 3: Compute badness using risk
state.bad[i] = α*(1 - state.health[i]) + β*state.complexity[i] + γ*state.risk[i]
```

**Simplified badness** (expand risk):
```python
bad[i] = α*(1 - health[i]) + β*complexity[i] + γ*complexity[i]*(1 - health[i])
       = α*(1 - health[i]) + (β + γ*(1 - health[i]))*complexity[i]
```

**For MVP**, use γ = 0.3 (risk contributes 30% weight).

**Status**: 🟢 RESOLVED (risk = complexity × (1 - health))

---

### 🔴 CONFUSION #3: Edge weight semantics

**Date raised**: 2025-11-22
**Raised by**: Laplacian interpretation

**The problem**:

Edge weight w_ij means "coupling strength." But does that mean:

**Interpretation A**: Tight coupling (high w) → **more tension** when nodes disagree
- L = D - A (standard Laplacian)
- High w_ij amplifies energy when bad[i] ≠ bad[j]
- This is what we use

**Interpretation B**: Loose coupling (low w) → **more freedom** to disagree
- Inverse Laplacian L = D - A^(-1)?
- Or normalize weights differently?

**Why it matters**:
- Affects whether we want high or low w for resilience
- Changes how we interpret V_struct values
- Impacts governance rules (do we add or remove edges to reduce tension?)

**Experiments affected**: Exp02 (Laplacian early warning)

**Status**: 🔴 UNRESOLVED (currently using Interpretation A, but unvalidated)

---

### 🟢 CONFUSION #4: Incident probability function [RESOLVED]

**Date raised**: 2025-11-22
**Date resolved**: 2025-11-22
**Raised by**: Scenario expected outcomes

**The problem**:

We say "incidents occur when health is low and complexity is high," but **what's the exact formula**?

**Resolution: Sigmoid with badness threshold**

**Formula**:
```python
def incident_probability(bad_i, threshold=0.6, steepness=10):
    """
    Smooth transition from 0 to max_prob as badness crosses threshold.

    threshold: badness value where p = max_prob/2 (default 0.6)
    steepness: how sharp the transition (default 10)
    max_prob: maximum incident probability per step (default 0.05)
    """
    from scipy.special import expit  # Logistic sigmoid
    return 0.05 * expit(steepness * (bad_i - threshold))

# Usage per timestep
for node in nodes:
    p = incident_probability(bad[node])
    if random.random() < p:
        trigger_incident(node)
```

**Justification**:
1. **Smooth**: No discontinuities (more realistic than step function)
2. **Tunable**: threshold and steepness control calibration
3. **Physical**: Sigmoid common in failure probability models
4. **Testable**: Can vary threshold to get desired incident rate

**Calibration for MVP**:
- threshold = 0.6 (incidents unlikely below this badness)
- steepness = 10 (fairly sharp transition)
- max_prob = 0.05 (5% per step when very bad)
- **Expected**: ~2-5 incidents per 100 steps in baseline

**If too many/few incidents**: Adjust threshold or max_prob.

**Status**: 🟢 RESOLVED (sigmoid with bad threshold)

---

### 🔴 CONFUSION #5: Flow field interpretation

**Date raised**: 2025-11-22
**Raised by**: Actor decision logic

**The problem**:

Flow field is defined as:
```python
flow[i] = (business_direction, stability_direction)
business_direction = demand[i]
stability_direction = -grad_V[i]
```

But actors choose actions based on flow. **How exactly**?

**Option A**: Sample node with probability ∝ ||flow[i]||
- Actors go where field magnitude is high
- But what's the action type? (Feature vs. Refactor?)

**Option B**: Sample node with probability ∝ flow_x, then choose feature; or ∝ flow_y, choose refactor
- Separates node choice from action choice

**Option C**: Flow is just a **visualization**, actors use raw demand and grad_V directly

**Why it matters**:
- Affects actor behavior
- Changes which nodes get attention
- Impacts simulation dynamics

**Experiments affected**: All (actors in every scenario)

**Status**: 🔴 UNRESOLVED

---

### 🔴 CONFUSION #6: Governance threshold calibration

**Date raised**: 2025-11-22
**Raised by**: Experiment 03 design

**The problem**:

We say "trigger emergency brake if H > 2.0," but **where does 2.0 come from**?

**Possibilities**:
1. Arbitrary (just pick something for MVP)
2. Calibrated from baseline (e.g., 2× mean(H) in baseline)
3. Derived from theory (e.g., when H > T_hot / T_cold...)
4. Learned from data (grid search for optimal threshold)

**Why it matters**:
- If threshold is too high → governance never triggers (useless)
- If threshold is too low → governance always triggers (bureaucracy)
- Need principled approach for real systems

**Experiments affected**: Exp03 (governance effectiveness)

**Status**: 🔴 UNRESOLVED

---

### 🔴 CONFUSION #7: Time units and scales

**Date raised**: 2025-11-22
**Raised by**: "10 steps earlier" prediction claim

**The problem**:

We claim "E_local warns 10 steps before incidents," but **what's a time step**?

**In simulation**:
- 1 step = 1 iteration of loop
- 3 actors act per step
- So 1 step = ~3 actions

**In real systems**:
- 1 step = 1 commit?
- 1 step = 1 day?
- 1 step = 1 PR merge?

**Why it matters**:
- Can't compare simulation to real git history without time mapping
- Affects how we interpret "early warning" (10 commits? 10 days?)

**Experiments affected**: All, especially Exp02

**Status**: 🔴 UNRESOLVED

---

## Resolved Confusions

### 🟢 CONFUSION #R1: Graph Laplacian normalization

**Date raised**: 2025-11-22
**Date resolved**: 2025-11-22
**Resolved by**: Mathematical foundations review

**The problem**:

Should we use:
- Combinatorial Laplacian: L = D - A
- Normalized Laplacian: L_norm = I - D^(-1/2) A D^(-1/2)
- Random walk Laplacian: L_rw = I - D^(-1) A

**Resolution**:

Use **combinatorial Laplacian L = D - A** for MVP.

**Reasons**:
1. Matches physics (spring networks, resistor networks)
2. Energy formula V = ½ f^T L f is exact
3. Simpler implementation (no degree normalization)
4. Post-MVP can compare normalized versions

**Documented in**: `02-mathematical-foundations.md:29-46`

**Status**: 🟢 RESOLVED

---

## Guidelines for Adding Confusions

**When to add**:
- Implementing code and don't know what value to use
- Two doc sections contradict each other
- Formula has undefined variable
- Edge case not handled
- Can't decide between multiple reasonable interpretations

**How to document**:
1. Give it a number (CONFUSION #N)
2. Date raised + who/what raised it
3. State the problem clearly
4. List possible resolutions
5. Explain why it matters
6. Mark status (🔴/🟡/🟢)

**How to resolve**:
1. Try each option experimentally (if fast)
2. Derive from first principles (if possible)
3. Pick simplest for MVP, mark for future testing (if unclear)
4. Update theory docs with the resolution
5. Move confusion to "Resolved" section

---

## Meta-Confusions (Confusions About Confusions)

**None yet. But we're watching for them.**

---

## Next Actions

**Before implementing Phase 1 code**:
1. Review confusions #1-#7
2. For each, pick an MVP resolution (even if temporary)
3. Mark as 🟡 IN PROGRESS
4. Implement, test
5. If it works, mark 🟢 RESOLVED
6. If it doesn't, try alternative, update confusion

**The rule**: Every confusion must be at least 🟡 before claiming "experiment works."

---

*"I would rather have questions that can't be answered than answers that can't be questioned."* — Richard Feynman
