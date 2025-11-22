# Model Selection: When to Use Which Model

## Decision Framework

**Goal**: Match model to problem type for maximum effectiveness.

**Approach**: Decision tree based on problem characteristics.

---

## Step 1: Identify Problem Type

### Type A: Structural Tension

**Characteristics**:
- Module coupling issues
- Dependencies creating stress
- Failures propagate through graph
- Clean code adjacent to messy code

**Indicators**:
- Incidents cluster near module boundaries
- High-centrality nodes frequently break
- Refactoring one module affects many others

**Best model**: **Physics** (Graph Laplacian, structural energy)

**Why**: Laplacian explicitly models neighbor disagreement and coupling strength.

**Metrics to use**: E_local, V_struct, H, phase space

---

### Type B: Resource Allocation

**Characteristics**:
- Which modules get engineering time?
- Feature vs. refactor trade-offs
- Tech debt vs. new features
- Portfolio prioritization

**Indicators**:
- Engineers debate where to spend effort
- Some modules over-invested, others neglected
- ROI varies widely across modules

**Best model**: **Economics** (ROI, capital allocation, debt)

**Why**: Economic models explicitly about resource optimization.

**Metrics to use**: ROI per module, tech debt interest rate, allocation efficiency

---

### Type C: Agent Interactions

**Characteristics**:
- Multiple agents competing or collaborating
- Who works on which module?
- Agent specialization vs. generalization
- Coordination patterns

**Indicators**:
- Agents frequently conflict (merge conflicts)
- Some agents dominate certain areas
- Collaboration patterns emerge

**Best model**: **Ecology** (competition, niches, carrying capacity)

**Why**: Ecological models designed for multi-species interactions.

**Metrics to use**: Growth rates, competition coefficients, niche overlap

---

### Type D: Human Understanding

**Characteristics**:
- Complexity overwhelming humans
- Knowledge gap growing
- Onboarding difficult
- Comprehension failures

**Indicators**:
- Humans can't explain recent changes
- Incorrect mental models
- Errors from misunderstanding
- Long learning curves

**Best model**: **Cognitive Science** (working memory, chunking, load)

**Why**: Cognitive models about human learning and comprehension limits.

**Metrics to use**: Chunks per module, cognitive load, comprehension time

---

### Type E: Emergent Behavior

**Characteristics**:
- Unexpected system-level patterns
- No one designed the structure, it emerged
- Self-organization
- Phase transitions

**Indicators**:
- Power law distributions
- Avalanche dynamics
- Spontaneous pattern formation
- Critical phenomena

**Best model**: **Complex Adaptive Systems** (emergence, criticality)

**Why**: CAS models emergence from local rules.

**Metrics to use**: Power law exponents, criticality indicators, avalanche sizes

---

### Type F: System Health & Resilience

**Characteristics**:
- Recovery from failures
- Stress response
- Long-term health trajectory
- Maintenance vs. growth

**Indicators**:
- System recovers (or doesn't) from incidents
- Performance under load
- Aging effects
- Health degradation over time

**Best model**: **Organism** (homeostasis, immune system, metabolism)

**Why**: Biological models about health, recovery, resilience.

**Metrics to use**: Recovery time, stress response curve, health trajectory

---

## Step 2: Check Model Applicability

**For chosen model, verify**:

1. **Variables measurable?**
   - Can we extract the model's variables from data?
   - If not, pick different model or improve measurement

2. **Assumptions valid?**
   - Does the model's assumptions match reality?
   - E.g., Physics assumes static graph—is topology stable enough?

3. **Predictions testable?**
   - Can we run experiments to validate?
   - If not, model is not falsifiable

**If all YES → Proceed to testing**

**If any NO → Reconsider model choice**

---

## Step 3: Test Model Empirically

**Follow** `03-evaluation-framework.md`:

1. Define hypothesis
2. Design experiment
3. Collect data
4. Analyze (AUC, p-values, effect sizes)
5. Interpret results

**If model passes** (predictive + actionable) → **Use it**

**If model fails** → **Try alternative from Step 1**

---

## Step 4: Comparative Analysis

### Test Multiple Models

**For same problem, test 2-3 candidate models**:

**Example: Predicting incidents**

Test:
- Model A (Physics): E_local
- Model B (Ecology): Growth rate imbalance
- Model C (Economics): ROI < 0

Compare:
- AUC for each
- Lead time for each
- Simplicity trade-offs

**Pick winner** or use ensemble.

### Ensemble Methods

**If multiple models useful:**

**Voting**: Each model votes, majority wins
**Weighted average**: Combine predictions weighted by AUC
**Staged**: Model A for detection, Model B for intervention

**Example**:
- Physics detects structural stress
- Economics suggests where to allocate refactor effort
- Cognitive limits how much refactoring humans can understand

**Three models, three roles.**

---

## Step 5: Adaptive Model Switching

### Different Models for Different States

**System state may require different models:**

**Startup (rapid growth)**:
- High velocity, low constraints
- **Use**: Ecology (resource competition) or Economics (ROI optimization)
- **Why**: Growth dynamics, allocation matters most

**Stable (optimization)**:
- Moderate velocity, high quality
- **Use**: Economics (efficiency) or Physics (maintain equilibrium)
- **Why**: Incremental improvements, balance forces

**Crisis (structural failure)**:
- High stress, incidents
- **Use**: Physics (structural tension) or Organism (stress response)
- **Why**: Need to detect and fix stress points

**Refactor (tech debt paydown)**:
- Low velocity, high refactor
- **Use**: Economics (debt servicing) or Cognitive (simplify for understanding)
- **Why**: Paying down debt, reducing complexity

### State Detection

**How to know which state?**

**Metrics**:
```python
if incident_rate > threshold:
    state = 'crisis'
    use_model = 'physics'  # Detect structural stress
elif velocity > 2 * baseline and incidents low:
    state = 'growth'
    use_model = 'ecology'  # Manage competition
elif velocity < 0.5 * baseline:
    state = 'refactor'
    use_model = 'economics'  # Optimize debt paydown
else:
    state = 'stable'
    use_model = 'physics'  # Maintain equilibrium
```

**Adaptive**: Switch models based on system state.

---

## Decision Tree Summary

```
START: What problem are we solving?

├─ Structural coupling, stress propagation
│  └─ Use: Physics (Laplacian, H)
│
├─ Resource allocation, prioritization
│  └─ Use: Economics (ROI, debt)
│
├─ Agent interactions, coordination
│  └─ Use: Ecology (competition, niches)
│
├─ Human understanding, complexity
│  └─ Use: Cognitive (working memory, load)
│
├─ Emergent patterns, phase transitions
│  └─ Use: CAS (criticality, power laws)
│
└─ Health, resilience, recovery
   └─ Use: Organism (homeostasis, stress response)

Then:
1. Check if model applicable (measurable? testable?)
2. Test empirically (experiments)
3. Compare to alternatives (if multiple candidates)
4. Use winner (or ensemble)
5. Adapt based on system state
```

---

## Example Scenarios

### Scenario 1: Tight Coupling Causing Incidents

**Problem**: Clean API module tightly coupled to messy data layer. Incidents at boundary.

**Problem type**: Structural tension (Type A)

**Model choice**: Physics (Laplacian)

**Why**: E_local[API] will be high (neighbor disagreement). Predicts stress.

**Intervention**: Refactor data layer OR decouple (reduce w_ij)

**Test**: Does E_local spike before incidents? AUC > 0.70?

---

### Scenario 2: Two Feature Teams Conflicting

**Problem**: Two teams working on same codebase, frequent merge conflicts, duplicated effort.

**Problem type**: Agent interaction (Type C)

**Model choice**: Ecology (competition)

**Why**: Teams competing for same resources (code, time).

**Intervention**: Create separate niches (split into services) OR coordinate allocation

**Test**: Does niche separation reduce conflicts?

---

### Scenario 3: Humans Can't Understand Agent Code

**Problem**: AI agents refactored 50 files, human can't explain changes, governance failing.

**Problem type**: Human understanding (Type D)

**Model choice**: Cognitive (working memory limits)

**Why**: Complexity exceeds human chunking capacity.

**Intervention**: Active learning challenges, better abstractions, comprehension sampling

**Test**: Does chunking improve comprehension time? Working memory limit evident?

---

### Scenario 4: System at Tipping Point

**Problem**: Small changes causing cascading failures. Feels "on edge."

**Problem type**: Emergent behavior (Type E)

**Model choice**: CAS (criticality)

**Why**: System may be at critical point (phase transition).

**Intervention**: Dampen fluctuations OR inject constraints to move away from criticality

**Test**: Measure avalanche size distribution. Power law?

---

## Failure Modes

### When Model Selection Fails

**Symptom 1: Model doesn't predict**
- AUC ≈ 0.5 (no better than random)
- **Solution**: Try different model from catalog

**Symptom 2: Predictions right but interventions fail**
- Can predict but can't fix
- **Solution**: Model predicts but doesn't guide—need different model for interventions

**Symptom 3: Model too complex to use**
- Can't extract variables, takes weeks to compute
- **Solution**: Simplify or pick simpler alternative

**Symptom 4: Model works in one context, fails in another**
- Not general enough
- **Solution**: Use context-specific models, switch based on state

---

## Meta-Model: When to Add New Model

**If none of the 6 models work:**

1. **Identify what's missing**
   - What aspect of problem do existing models ignore?
   - Example: All models ignore code semantics (correctness)

2. **Research candidate models**
   - What field studies this aspect?
   - Example: For semantics, look at formal verification, type theory

3. **Formulate testable predictions**
   - What would this model predict that others don't?

4. **Add to catalog** (`02-model-catalog.md`)

5. **Design experiments**

6. **Test empirically**

**Science progresses by testing AND refining.**

---

## Summary

**Decision process**:
1. Identify problem type (structural? resource? emergent?)
2. Pick candidate model(s) from catalog
3. Check applicability (measurable? testable?)
4. Test empirically (experiments, statistics)
5. Compare alternatives (if multiple)
6. Use winner (or ensemble)
7. Adapt based on system state
8. Iterate

**Key principle**: Let empirical results choose the model, not aesthetic preference.

---

**Read next**: `05-experiments-as-tests.md` for how experiments evaluate models.
