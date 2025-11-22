# Catalog of Mental Models for AI Agent Governance

## Overview

Six candidate mental models, each offering different perspectives on the governance problem.

**For each model:**
- Core metaphor
- When it applies best
- Key predictions
- Interventions it suggests
- How to test it
- Limitations

**Remember**: These are tools, not truth. Use whichever predicts reality best.

---

## Model 1: Software as Physical System

### Core Metaphor

**Codebase is a tensegrity structure** with compression (code modules) and tension (tests, constraints) elements.

**Changes are energy injections** that create stress, propagate through coupling, and must be dissipated.

### Key Concepts

**Graph Laplacian** L = D - A
- Nodes = modules
- Edges = dependencies with coupling weight
- Laplacian encodes neighbor disagreement

**Dirichlet Energy**: V_struct = ½ Σ w_ij (bad[i] - bad[j])²
- Measures structural tension
- High when coupled nodes have mismatched health/complexity

**Hamiltonian**: H = T + V
- T = rate of change (kinetic energy)
- V = structural + business tension (potential energy)
- H = total "crisis energy"

**Phase space**: (T, V) coordinates classify regimes
- Healthy flow, chaotic thrash, frozen bureaucracy, stable equilibrium

### When It Applies

**Best for:**
- Structural coupling problems (tight dependencies)
- Stress propagation (failures cascade through graph)
- Early warning signals (tension before breaking)

**Examples:**
- A clean module couples to messy module → tension
- Core service stressed by many unhealthy dependents
- Architectural debt creating "potential energy" that will release as incidents

### Predictions

1. **High E_local at hubs predicts incidents ~10 steps before they occur**
2. Governed systems (H thresholds) recover faster from shocks
3. Phase space trajectory reveals system health
4. Efficiency bounded by Carnot-like limit

### Interventions

**Based on metrics:**
- If E_local[hub] > threshold → Block changes, require refactor
- If H > emergency → Pause features, mandate debt paydown
- If T/V too high → System thrashing, slow down
- If T/V too low → System frozen, relax constraints

### How to Test

**Experiments**:
- Exp02: Does E_local predict incidents better than scalar metrics?
- Compare AUC, lead time vs. health, complexity baselines
- A/B test: Governed vs ungoverned system response to shock

**Success**: AUC(E_local) significantly > AUC(health), p < 0.05

### Limitations

- Ignores semantics (structure only, not correctness)
- Static graph assumption (topology changes are discrete events)
- Unclear how to measure some variables (mass, "temperature")
- May not apply to agent decision-making (not structural)

---

## Model 2: Software as Ecosystem

### Core Metaphor

**Agents and modules are species** competing for resources (engineer time, compute, user attention).

**System is an ecosystem** with niches, carrying capacity, competition, mutualism, predator-prey dynamics.

### Key Concepts

**Lotka-Volterra equations**:
```
dN_i/dt = r_i N_i (1 - Σ_j α_ij N_j / K)

N_i = "population" of module i (LOC, activity, churn)
r_i = growth rate (feature velocity)
α_ij = competition coefficient (coupling, resource overlap)
K = carrying capacity (team bandwidth, complexity budget)
```

**Fitness landscape**: Modules with high value and low cost survive, others die.

**Niches**: Different modules occupy different ecological niches (API layer, data layer, features).

### When It Applies

**Best for:**
- Agent interactions (competition, collaboration)
- Resource allocation (who gets engineering time?)
- System evolution (which modules grow, which die)

**Examples:**
- Two feature teams competing for core API access
- Refactor engineers "prey on" technical debt
- Module extinction (deprecation)

### Predictions

1. **Competitive exclusion**: Tight coupling → one module dominates
2. **Coexistence**: Weak coupling → multiple modules stable
3. **Oscillations**: Predator-prey (features create debt, refactors remove it)
4. **Carrying capacity**: Team can support N modules max

### Interventions

**Based on metrics:**
- If competition too high → Decouple, create separate niches
- If one module dominating → Split, create diversity
- If oscillations wild → Stabilize predator-prey ratio (more refactor engineers)
- If at carrying capacity → Deprecate old modules before adding new

### How to Test

**Experiments**:
- Track module growth rates, competition coefficients
- Test: Do coupled modules compete (negative α_ij)?
- Test: Is there a carrying capacity (growth slows as N increases)?
- Compare predictions to actual module evolution

**Success**: Lotka-Volterra fits observed dynamics, R² > 0.7

### Limitations

- Anthropomorphizes modules (they don't "compete" intentionally)
- Assumes gradual evolution (but software has discontinuous jumps)
- Hard to measure fitness, competition coefficients
- May not apply to structural problems

---

## Model 3: Software as Market

### Core Metaphor

**Code is capital**, features are products, technical debt is liabilities.

**Engineers are traders** allocating effort to maximize ROI.

**System is a market** with supply (engineer capacity), demand (features, fixes), prices (effort cost).

### Key Concepts

**ROI**: Return on investment for each module
```
ROI[i] = (Business value) / (Engineering cost)
```

**Technical debt as financial debt**:
```
Debt_payment = Principal × Interest_rate
If unpaid, debt compounds
```

**Efficient market hypothesis**: Engineers allocate effort optimally given available information.

**Price signals**: High-value modules attract investment, low-value modules deprecate.

### When It Applies

**Best for:**
- Resource allocation (which modules to work on?)
- Prioritization (features vs refactors vs tech debt)
- Portfolio management (balance risk/reward)

**Examples:**
- Which feature has highest ROI?
- Is technical debt "interest rate" sustainable?
- Should we "invest" in refactor or "sell" (deprecate)?

### Predictions

1. **Engineers allocate effort to maximize ROI** (not randomly)
2. **High-value modules get more investment** (churn, features)
3. **Tech debt compounds** at measurable interest rate
4. **Market clearing**: Supply = Demand at equilibrium

### Interventions

**Based on metrics:**
- If ROI[i] negative → Deprecate or restructure
- If debt interest > growth → Mandatory paydown
- If misallocation → Reallocate resources to high-ROI modules
- If market inefficient → Improve information flow

### How to Test

**Experiments**:
- Measure actual effort allocation vs. ROI predictions
- Test: Do high-ROI modules get more effort?
- Test: Does debt compound at predictable rate?
- Compare to random allocation baseline

**Success**: Correlation(effort, ROI) > 0.7, p < 0.05

### Limitations

- Hard to measure "value" objectively
- Ignores externalities (coupling, architectural coherence)
- Assumes rational actors (but engineers have biases)
- May not apply to structural stress

---

## Model 4: Software as Cognitive System

### Core Metaphor

**Codebase + team is a distributed cognitive system**.

**Code is externalized memory**, agents are neurons, architecture is mental schema.

### Key Concepts

**Working memory limits** (Miller's 7±2):
```
Comprehensible_complexity ≈ 7 chunks
```

**Cognitive load theory**:
```
Total_load = Intrinsic + Extraneous + Germane

Intrinsic = Problem complexity (unavoidable)
Extraneous = Bad design, poor docs (reducible)
Germane = Learning effort (productive)
```

**Chunking**: Group related concepts to fit in working memory.

**Mental models**: Internal representations of system structure.

### When It Applies

**Best for:**
- Human comprehension problems
- Documentation, naming, abstraction design
- Learning curves, onboarding
- Knowledge gap tracking

**Examples:**
- Module too complex (>7 responsibilities)
- Poor naming increases extraneous load
- Human can't understand refactor → governance fails

### Predictions

1. **Modules with >7 main concepts are hard to understand**
2. **Extraneous load causes errors** (bugs from confusion)
3. **Comprehension degrades with agent velocity** (knowledge gap)
4. **Active retrieval beats passive review** (learning)

### Interventions

**Based on metrics:**
- If complexity > 7 chunks → Split module, better abstractions
- If extraneous load high → Improve docs, naming
- If knowledge gap > threshold → Active learning challenges
- If onboarding slow → Better chunking, mental model diagrams

### How to Test

**Experiments**:
- Measure comprehension time vs. complexity
- Test: Is there a ~7 threshold for understanding?
- Test: Does extraneous load predict bugs?
- A/B test: Active vs passive learning

**Success**: Complexity predicts comprehension, R² > 0.6

### Limitations

- Focuses on individual cognition (not system dynamics)
- Hard to measure "chunks," "load" objectively
- Doesn't address structural coupling
- May not predict incidents directly

---

## Model 5: Software as Complex Adaptive System

### Core Metaphor

**Software is a CAS** with emergent behavior, self-organization, criticality.

**Agents follow local rules**, global properties emerge.

### Key Concepts

**Emergence**: Large-scale patterns from local interactions
- No central control, but system-level order

**Self-organization**: System adapts structure to environment
- Modules form, split, merge based on function

**Criticality**: System operates at phase transition (edge of chaos)
- Power laws (degree distribution, change size)
- Avalanches (small change → cascade)

**Fitness landscape**: System evolves via variation and selection.

### When It Applies

**Best for:**
- Emergent phenomena (architectural patterns arise)
- Phase transitions (order ↔ chaos)
- Scaling behavior (power laws)
- Adaptive systems (self-organizing)

**Examples:**
- Microservices emerge from monolith (self-organization)
- Small refactor cascades through system (criticality)
- Module coupling follows power law (scale-free)

### Predictions

1. **Degree distribution is power law** P(k) ~ k^(-γ)
2. **Change size distribution is power law** (small changes common, large rare)
3. **System operates near critical point** (optimal complexity, creativity)
4. **Avalanches**: Small changes can cause cascades

### Interventions

**Based on metrics:**
- If too ordered → Inject variation, allow experimentation
- If too chaotic → Add constraints, dampen fluctuations
- If not at criticality → Tune coupling to critical point
- If avalanches destructive → Circuit breakers

### How to Test

**Experiments**:
- Measure degree distribution, fit power law
- Measure change size distribution
- Test: Is system at critical point? (susceptibility diverges)
- Induce small changes, measure cascade size

**Success**: Power law fit R² > 0.8, critical exponents match theory

### Limitations

- Abstract (what ARE the local rules?)
- Hard to predict specific outcomes (emergent = unpredictable?)
- Requires large datasets (power laws need statistics)
- May not suggest concrete interventions

---

## Model 6: Software as Organism

### Core Metaphor

**Codebase is an organism** with metabolism, immune system, homeostasis.

**Health as biological health**, stress as disease.

### Key Concepts

**Homeostasis**: System maintains stable internal state despite external changes.

**Immune system**: Tests, linters, CI/CD catch and remove "infections" (bugs).

**Metabolism**: Feature velocity = metabolic rate.

**Stress response**: System adapts to stressors (load, bugs, changes).

**Aging**: Technical debt accumulates like cellular damage.

### When It Applies

**Best for:**
- Resilience, recovery from failures
- Immune response (testing, quality gates)
- Adaptation to stress
- Long-term health trajectory

**Examples:**
- System recovers from bug (immune response)
- High load triggers scaling (stress response)
- Old code accumulates "damage" (tech debt)

### Predictions

1. **Healthy systems recover faster from stress**
2. **Immune strength** (test coverage) predicts bug escape rate
3. **Metabolism** (feature rate) vs. maintenance trade-off
4. **Aging**: Older codebases slower unless maintained

### Interventions

**Based on metrics:**
- If immune weak → Add tests, coverage
- If stressed → Rest (maintenance period)
- If aging → Rejuvenation (refactor, rewrite)
- If sick → Diagnosis, targeted fix

### How to Test

**Experiments**:
- Measure recovery time from failures vs. health
- Test: Does test coverage predict bug escape?
- Test: Is there a metabolism vs. maintenance trade-off?
- Track aging (complexity over time)

**Success**: Health predicts recovery, coverage predicts bugs, R² > 0.6

### Limitations

- Anthropomorphic (organisms have goals, code doesn't)
- Vague metrics (what IS "health" precisely?)
- May not apply to structural coupling
- Limited predictive power

---

## Comparative Summary

| Model | Best For | Key Metric | Test | Limitations |
|-------|----------|------------|------|-------------|
| **Physics** | Structural tension | E_local, H | Incident prediction | Ignores semantics |
| **Ecology** | Agent interactions | Growth rates, α_ij | Module evolution | Anthropomorphic |
| **Economics** | Resource allocation | ROI, debt rate | Effort allocation | Hard to measure value |
| **Cognitive** | Human understanding | Chunks, load | Comprehension | Individual focus |
| **CAS** | Emergence, scaling | Power laws | Criticality | Abstract |
| **Organism** | Resilience, health | Recovery time | Stress response | Vague |

---

## How to Choose?

**See** `04-model-selection.md` for decision framework.

**Short version**:
1. Identify problem type (structural? resource? emergent?)
2. Pick candidate model(s)
3. Test predictions empirically
4. Use whichever works

**Can use multiple models simultaneously** for different aspects.

---

**Read next**: `03-evaluation-framework.md` for how to test models rigorously.
