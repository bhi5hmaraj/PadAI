# Software Tensegrity Simulator - MVP Design Document

## Document Status
- **Version**: 0.1.0
- **Date**: 2025-11-22
- **Status**: Draft for Implementation

---

## Executive Summary

We are building an interactive simulator that models software systems as living tensegrity structures—where code modules act as compression elements and constraints (tests, contracts, architectural boundaries) act as tension elements. The goal is to understand how stress distributes through a codebase under various forces: feature pressure, technical debt, agent-driven changes, and market dynamics.

The MVP will demonstrate one core insight: **structural tension at graph hubs (measured via Laplacian-based energy) provides earlier warning signals for system instability than traditional per-node metrics alone.**

---

## 1. Motivation & Context

### 1.1 The Problem

Current software development with AI agents faces a fundamental challenge: agents lack teleology and operate under direct supervision, yet we're asking them to make increasingly autonomous decisions. This creates several issues:

1. **Loss of phase coherence**: The human mental model ("design world") and the actual implementation drift apart when agents make large changes
2. **Blind metrics**: We track churn, coverage, and incidents, but have no structural model of how stress propagates through a system
3. **Ad-hoc governance**: Teams invent rules reactively without understanding the dynamics they're trying to control
4. **No early warnings**: By the time traditional metrics show problems, the system is already in crisis

### 1.2 The Core Insight

Software systems are better understood as **graph-based physical structures under tension** rather than as static artifacts. Just as a tensegrity structure distributes stress through cables and struts:

- **Compression elements**: Code modules, services, infrastructure bearing load
- **Tension elements**: Tests, type systems, contracts, architectural boundaries pulling the system into coherent shape
- **Forces**: Business requirements, user demand, technical debt, agent-driven changes
- **Stress distribution**: Via the graph Laplacian—neighbors under different "strain" create tension in the network

The mathematics of spring networks, electrical circuits, and random walks on graphs all reduce to the same object: **the graph Laplacian and its quadratic energy form**. This gives us a principled way to define "potential energy" (structural stress) and "kinetic energy" (rate of change) for software systems.

### 1.3 Why a Simulator?

We need a controlled environment to:

1. **Test governance strategies** before deploying them on real codebases
2. **Explore phase transitions** between stable and chaotic regimes
3. **Design agent workflows** that keep human-code phase coherence
4. **Validate theories** about structural stress and incident prediction
5. **Build intuition** about multi-actor, multi-timescale dynamics

The simulator is a **conceptual microscope**, not a product. It trades accuracy for structural honesty and interpretability.

---

## 2. Conceptual Model

### 2.1 The Universe

Our simulation universe consists of three coupled layers:

#### **Technical Layer** - The Code Graph G_tech(t)
- **Nodes**: Modules, services, databases, feature areas (e.g., `A_core`, `B_api`, `C_db`, `D_featureX`)
- **Edges**: Dependencies (imports, calls, data flows, deployment coupling)
- **Edge weights** w_ij: Coupling strength—how tightly two components are bound

#### **Actor Layer** - G_actor(t)
- **Nodes**: Human engineers, AI agents, product managers, SREs
- **Edges**: Social/organizational ties (team membership, code review relationships, communication patterns)
- **Attributes**: Expertise, capacity, behavior policies, decision-making rules

#### **Environment Layer** - G_env(t)
- **Nodes**: User cohorts, customer organizations, competitors, market forces, regulators, funders
- **Edges**: Value flows, contracts, competitive pressure, funding relationships
- **Dynamics**: Demand shifts, competitive moves, regulatory changes

**Cross-layer edges** connect these:
- Ownership: Actor → Tech ("engineer owns module")
- Usage: Environment → Tech ("users depend on feature")
- Influence: Environment → Actor ("investor pressures leadership")

### 2.2 Fields Over the Graph

We define **scalar fields** on technical nodes:

```python
health[i] ∈ [0,1]      # Test coverage, code quality, clarity
complexity[i] ∈ [0,1]  # Structural/cognitive complexity
risk[i] ∈ [0,1]        # Emergent from health, complexity, change history
demand[i] ∈ [0,1]      # User/business pressure on this component
```

We define a **vector field** on technical nodes:

```python
flow[i] ∈ ℝ²           # Direction of desired motion
  # x-component: pressure for feature work
  # y-component: pressure for refactor/stabilization
```

We define a **composite "badness" field**:

```
bad[i] = α(1 - health[i]) + β·complexity[i] + γ·risk[i]
```

This aggregates multiple concerns into a single scalar that feeds into energy calculations.

### 2.3 Energies - The Physics

#### **Structural Potential Energy** (Tensegrity Tension)

Based on the **Dirichlet energy** of the badness field over the graph:

```
V_struct = ½ Σ_(i,j)∈E w_ij · (bad[i] - bad[j])²
         = ½ bad^T · L · bad
```

where L is the **graph Laplacian** (L = D - A).

**Physical interpretation**: High V_struct means neighbors disagree strongly about their state. Like springs stretched between dissimilar masses, or voltage differences in a resistor network.

#### **Business Potential Energy** (Misalignment Cost)

```
V_bus = Σ_i demand[i] · [λ₁(1 - health[i]) + λ₂·complexity[i]]
```

**Interpretation**: Unhealthy or over-complex modules under high demand create business pain.

#### **Total Potential**

```
V(t) = V_struct(t) + V_bus(t)
```

#### **Kinetic Energy** (Rate of Change)

For discrete time steps k:

```
Δbad[i]_k = bad[i]_k - bad[i]_(k-1)
T_k = ½ Σ_i m_i · (Δbad[i]_k)²
```

where m_i is the "mass" of node i (importance weight based on criticality, user impact, etc.).

**Interpretation**: Rapid changes in critical modules carry high kinetic energy; slow changes in peripheral code carry little.

#### **Lagrangian and Hamiltonian**

```
L = T - V    (Lagrangian: prefers motion with constraint)
H = T + V    (Hamiltonian: total system "stress load")
```

**Regimes**:
- **Frozen bureaucracy**: T ≈ 0, V high → no motion, lots of strain
- **Chaotic thrash**: T high, V_struct high → lots of motion, structural tension
- **Healthy flow**: T and V both moderate, well-balanced

### 2.4 Vector Field Dynamics

The flow field guides actor behavior and is computed from:

```python
grad_V[i] ≈ Σ_j w_ij · (bad[i] - bad[j])  # Local gradient via Laplacian
business_dir[i] = demand[i] · x̂          # Push toward features
stability_dir[i] = -normalize(grad_V[i]) · ŷ  # Push toward energy reduction

flow[i] = α·business_dir[i] + β·stability_dir[i]
```

**Key insight**: This field is not static. As demand shifts and energy redistributes, the arrows rotate and change magnitude, creating a dynamic landscape that actors navigate.

---

## 3. Actors and Events

### 3.1 Actor Types (MVP)

We model three simple actor types with distinct policies:

#### **Feature Engineer (FE)**
- **Goal**: Ship features, respond to demand
- **Policy**: High weight on business_dir component of flow[i]
- **Action preference**: FeatureChange > AddEdge > Refactor

#### **Refactor Engineer (RE)**
- **Goal**: Improve structure, reduce technical debt
- **Policy**: High weight on stability_dir component of flow[i]
- **Action preference**: Refactor > RemoveEdge > AddConstraint

#### **AI Agent (LLMA)**
- **Goal**: Maximize local flow magnitude (naive optimizer)
- **Policy**: Follows largest ||flow[i]||, slight bias toward features
- **Action preference**: Whatever flow[i] suggests, but less nuanced

Each actor per time step:
1. Samples a target node i with probability ∝ score[i] = demand[i] + κ·|grad_V[i]| + noise
2. Chooses action type based on personality and flow[i]
3. Applies the action, mutating (G, F)

### 3.2 Event Types

Every actor action is a transformation **(G, F) → (G', F')**.

#### **Field-Only Events** (no topology change)

**FeatureChange(i)**:
- Effect: `complexity[i] ↑`, `health[i] ↓`, `risk[i] ↑`
- Represents: Adding/modifying behavior at node i

**Refactor(i)**:
- Effect: `complexity[i] ↓`, `health[i] ↑`, `risk[i] ↓`
- Represents: Structural cleanup, better tests

**Patch(i)**:
- Effect: Small adjustments to health and risk
- Represents: Bug fixes, minor tweaks

#### **Structural Events** (topology changes)

**AddEdge(i, j)**:
- Effect: Add edge if absent, or increase w_ij
- Side effect: `risk[i] ↑`, `risk[j] ↑` (new coupling)
- Represents: New dependency, tighter coupling

**RemoveEdge(i, j)**:
- Effect: Remove edge or decrease w_ij
- Side effect: May transiently increase complexity (boundaries shifting)
- Represents: Decoupling for modularity

**SplitNode(i → i₁, i₂)**:
- Effect: Create two nodes from one, distribute edges and fields
- Represents: Breaking up a god-object

**MergeNodes(i, j → k)**:
- Effect: Combine two nodes, merge edges
- Represents: Consolidation (sometimes creates god-objects)

#### **Constraint Events** (change tension network)

**AddConstraint(i)**:
- Effect: Increase edge weights touching i (stiffer), `health[i] ↑` slightly
- Represents: More tests, contracts, observability

**GovernanceChange(pattern)**:
- Effect: Modify rules about what future actions are allowed
- Represents: New coding standards, review requirements, architectural principles

#### **Environment Events** (external forces)

**DemandShock(i, Δ)**:
- Effect: `demand[i] += Δ`
- Represents: Market shift, user migration, competitive pressure

**NewRequirement(zone)**:
- Effect: Mark graph region as needing new capability, adjust demand
- Represents: Product decision, regulatory mandate, new OKR

---

## 4. MVP Scope

### 4.1 What We Will Build

**Graph**:
- 6–8 technical nodes with meaningful names
- Small hub-and-spoke topology (2–3 core nodes, 3–5 feature leaves)
- No real code, just synthetic events

**Fields**:
- Scalar: health, complexity, risk, demand
- Vector: flow (2D)
- Derived: bad, grad_V

**Energies**:
- V_struct (Laplacian-based)
- V_bus (demand-weighted badness)
- T (finite-difference kinetic)
- H, L (derived)

**Actors**:
- 2 human engineers (feature + refactor focused)
- 1 AI agent (naive flow-follower)
- 1 "product" pseudo-actor (schedules demand shifts)

**Simulation**:
- Discrete time loop, ~100–500 steps
- Simple logging of H, V, T, per-node fields
- Basic graph visualization + time series plots

**Scenarios**:
1. **Baseline**: Stable demand, mixed actor actions
2. **Competitor shock**: Demand drops on one feature, requirement appears for competing feature
3. **Governance experiment**: Compare unconstrained vs. governed agent behavior

### 4.2 What We Will NOT Build (Yet)

- No integration with real repos, VCS, or CI/CD
- No real LLMs in the loop (agents are scripted)
- No calibration to real-world data
- No fancy dashboards (Jupyter + Matplotlib is fine)
- No system dynamics layer (PySD) for macro stocks/flows
- No full agent-based model framework (though Mesa is a natural next step)

### 4.3 Success Criteria

The MVP succeeds if:

1. **Expressiveness**: We can model realistic scenarios (feature rush, competitive pressure, governance) purely as event sequences
2. **Differentiation**: Different governance/actor configs produce qualitatively different trajectories that match intuition
3. **Actionable insight**: At least one concrete diagnostic emerges (e.g., "local Dirichlet energy at hubs predicts problems earlier than global metrics")

---

## 5. Implementation Plan

### 5.1 Technology Stack

**Language**: Python 3.10+

**Core Libraries**:
- `networkx`: Graph structure, Laplacian computation, basic analytics
- `numpy`: Vectorized field operations
- `matplotlib`: Visualization (graphs and time series)
- `scipy`: Sparse linear algebra (if needed for larger graphs later)

**Optional/Future**:
- `mesa`: Agent-based modeling framework with browser visualization
- `pysd`: System dynamics integration
- `streamlit` or `jupyter-widgets`: Interactive parameter tuning

### 5.2 Code Structure

```
tensegrity/research/
├── mvp-design-doc.md          # This document
├── simulation/
│   ├── __init__.py
│   ├── graph_model.py         # Graph, fields, energy computations
│   ├── actors.py              # Actor classes and policies
│   ├── events.py              # Event definitions and business shocks
│   ├── simulation.py          # Main loop, logging
│   └── visualization.py       # Plotting utilities
├── notebooks/
│   └── mvp_demo.ipynb         # Interactive exploration
└── scenarios/
    ├── baseline.py
    ├── competitor_shock.py
    └── governance_experiment.py
```

### 5.3 Development Phases

#### **Phase 1: Core Infrastructure** (Week 1)
- [ ] Implement graph_model.py with NetworkX
- [ ] Define field data structures
- [ ] Implement energy calculations (V_struct, V_bus, T, H)
- [ ] Unit tests for energy computations

#### **Phase 2: Events and Actors** (Week 1-2)
- [ ] Implement event primitives in events.py
- [ ] Create simple actor policies in actors.py
- [ ] Add flow field computation
- [ ] Test actor decision-making in isolation

#### **Phase 3: Simulation Loop** (Week 2)
- [ ] Build discrete-time stepper in simulation.py
- [ ] Add logging infrastructure
- [ ] Implement basic visualization
- [ ] Run smoke test with dummy scenario

#### **Phase 4: Scenarios** (Week 2-3)
- [ ] Baseline scenario
- [ ] Competitor shock scenario
- [ ] Governance experiment
- [ ] Document findings

#### **Phase 5: Analysis and Iteration** (Week 3)
- [ ] Generate time series plots
- [ ] Compute derived metrics (local Dirichlet energy, centrality × badness)
- [ ] Compare governed vs ungoverned regimes
- [ ] Write up initial insights

---

## 6. Example Scenario: Competitor Shock

### 6.1 Initial Condition

**Graph**: 6 nodes
```
A_core ←→ B_api ←→ D_featureX
   ↕         ↕
C_db      E_featureY
   ↕
F_util
```

**Fields**:
```
health:     A=0.8, B=0.8, C=0.7, D=0.6, E=0.6, F=0.7
complexity: A=0.7, B=0.6, C=0.5, D=0.4, E=0.4, F=0.3
risk:       all 0.3
demand:     D=0.9 (hot feature), E=0.5, others 0.2
```

**Actors**: FE, RE, LLMA, Product

### 6.2 Event Sequence

**t=0–20**: Baseline
- Mixed actions: features, refactors, patches
- System in rough equilibrium: H moderate, V_struct low

**t=20**: Competitor introduces feature
- `DemandShock(D, -0.4)` → demand[D] drops to 0.5
- `NewRequirement(G_featureComp)` → new node G added, demand[G]=0.8
- Vector field rotates: strong business pressure toward G

**t=21–50**: Scramble to respond
- FE and LLMA heavily target G and neighbors
- Many FeatureChange and AddEdge events
- If **unconstrained**: T spikes, V_struct rises at A and B (core under stress)
- If **governed** (rule: "Refactor required when local V_struct > threshold"): RE forced to act on core, T still high but V_struct bounded

**t=50–80**: User re-engagement
- `DemandShock(G, +0.2)` → users return as feature ships
- If G is brittle (high risk, low health): incidents fire with prob ∝ risk[G] × demand[G]
- If G is solid: incidents rare, V_bus drops, system stabilizes

**t=80–100**: Learning
- If incidents occurred: `AddConstraint(G)`, governance tightens
- Actors shift toward refactors around stressed zones
- H gradually relaxes

### 6.3 Expected Outcomes

**Metric**: Local Dirichlet energy at hubs (A, B):
```
E_local[i] = Σ_j w_ij · (bad[i] - bad[j])²
```

**Prediction**: In the unconstrained regime, E_local[A] and E_local[B] spike ~10 steps before global incident metrics show problems. This validates the core insight.

**Phase Space**: Plot H vs. time for both regimes:
- Unconstrained: H rises and stays elevated
- Governed: H spikes briefly then returns to baseline

---

## 7. Physics Analogies and Modeling Choices

### 7.1 Why the Graph Laplacian?

The Laplacian L = D - A appears in:
- **Spring networks**: Elastic potential energy
- **Electrical circuits**: Kirchhoff's laws, power dissipation
- **Random walks**: Generator of diffusion, commute times
- **Spectral clustering**: Finding natural module boundaries

Our Dirichlet energy `½ f^T L f` is the same quadratic that governs all these systems. We're not inventing physics; we're recognizing that **code graphs have the same mathematical structure as physical networks**.

### 7.2 Alternative Modeling Approaches

We considered and may layer in:

- **System Dynamics**: For macro stocks (technical debt, team capacity)
- **Complex Adaptive Systems**: Emphasizes learning and emergence
- **Cybernetics**: Ashby's law of requisite variety for governance design
- **Information Theory**: Shannon entropy for measuring alignment
- **Active Inference**: Free-energy principle for agent teleology
- **Game Theory**: Strategic interactions and incentive alignment

For the MVP, **graph dynamics + thermodynamic intuition** provides the clearest structural skeleton. Other lenses can plug in later as interpretive layers.

### 7.3 What Are We Actually Measuring?

**Kinetic T**: How fast things are changing
**Potential V**: How stressed/misaligned the structure is
**Hamiltonian H = T + V**: Total "crisis energy" in the system
**Lagrangian L = T - V**: Quality of motion (high T with low V is good; high T with high V is thrash)

These are **not** literal Joules or Kelvin. They're dimensionless indices calibrated to the system's own scale. The value is in ratios and trajectories, not absolute numbers.

---

## 8. Open Questions and Future Work

### 8.1 MVP Open Questions

1. **Parameter tuning**: What are good default values for α, β, γ, λ₁, λ₂, m_i?
   - Start with all equal, then tune to get "realistic-feeling" dynamics

2. **Event probabilities**: How often should actors act? How noisy should sampling be?
   - Start deterministic, add noise gradually

3. **Incident modeling**: What's a believable incident probability function?
   - Simple: P(incident at i) = risk[i] × demand[i] × Δt

4. **Vector field**: Should we use gradients, or more sophisticated "policy fields"?
   - Start simple (linear combo of demand and -grad_V), iterate

### 8.2 Future Enhancements

**Immediate Next Steps**:
- Integrate Mesa for proper ABM with interactive visualization
- Add LLM-in-the-loop for AI agent policy (call real API)
- Calibrate against one real project's history

**Medium-Term**:
- Multi-layer graphs: technical, social, environment explicitly modeled
- System dynamics layer (PySD) for long-term stocks
- Richer governance: finite-state machines for process flows
- Thermodynamic analysis: define efficiency, entropy production

**Long-Term**:
- Active inference agents with internal generative models
- Game-theoretic incentive analysis
- Information-theoretic alignment metrics
- Real-time dashboard for production systems

---

## 9. Relation to Broader "Software Physics" Vision

This MVP is a stepping stone toward the full Tensegrity governance layer you're envisioning.

**What we're learning**:
- Can graph-based energy metrics actually predict problems?
- Do different agent workflows produce different "phase space" trajectories?
- Is there a principled way to define "good motion" vs "thrash"?

**What comes next**:
- If MVP validates core ideas → build real integration with codebases
- Design actual "governor" processes that use H, V, local Dirichlet energy as gates
- Develop agent workflows that operate on "potential layer" (docs, specs, tests) separate from "code layer"
- Ship it as tooling that teams can actually use

The ultimate vision: **A development environment that treats software as a living physical system, gives teams real-time structural diagnostics, and guides agents to act in ways that preserve coherence and stability—just like a cell's cytoskeleton or a well-designed tensegrity tower.**

---

## 10. References and Further Reading

### Graph Theory and Spectral Methods
- Spielman, "Spectral Graph Theory" (Yale lecture notes)
- Aldous & Fill, "Reversible Markov Chains and Random Walks on Graphs"
- Chung, "Spectral Graph Theory"

### Physics and Dynamics
- Goldstein, "Classical Mechanics" (Lagrangian/Hamiltonian formalism)
- Strogatz, "Nonlinear Dynamics and Chaos"

### Complex Systems
- Mitchell, "Complexity: A Guided Tour"
- Holland, "Hidden Order: How Adaptation Builds Complexity"

### Cybernetics and Control
- Ashby, "An Introduction to Cybernetics" (requisite variety)
- Beer, "Brain of the Firm" (viable system model)

### Software Engineering
- Sommerville & Baxter, "Socio-Technical Systems"
- Cataldo et al., "Sociotechnical Congruence" (empirical studies)
- Conway's Law and organizational structure

### Active Inference
- Friston, "The Free-Energy Principle" (generative models)
- Parr & Pezzulo, "Active Inference: The Free Energy Principle in Mind, Brain, and Behavior"

---

## Appendix A: Mathematical Notation Summary

| Symbol | Meaning |
|--------|---------|
| G(t) | Technical graph at time t |
| V, E | Vertices (nodes), Edges |
| w_ij | Edge weight between i and j |
| L | Graph Laplacian (L = D - A) |
| f[i] | Generic scalar field value at node i |
| health[i], complexity[i], risk[i], demand[i] | Specific field values |
| bad[i] | Composite badness: α(1-health) + β·complexity + γ·risk |
| V_struct | Structural potential: ½ Σ w_ij(bad[i]-bad[j])² |
| V_bus | Business potential: Σ demand[i]·(λ₁(1-health[i]) + λ₂·complexity[i]) |
| V | Total potential: V_struct + V_bus |
| T | Kinetic energy: ½ Σ m_i(Δbad[i])² |
| L | Lagrangian: T - V |
| H | Hamiltonian: T + V |
| flow[i] | 2D vector field: (feature pressure, refactor pressure) |
| m_i | Mass (importance weight) of node i |

---

## Appendix B: Quick Start Guide

### Running the Simulation

```python
# Install dependencies
pip install networkx numpy matplotlib scipy

# Run baseline scenario
cd tensegrity/research/simulation
python scenarios/baseline.py

# Run competitor shock
python scenarios/competitor_shock.py

# Interactive exploration
jupyter notebook notebooks/mvp_demo.ipynb
```

### Key Outputs

1. **Time series plots**: H(t), V(t), T(t), T/V ratio
2. **Graph snapshots**: Node colors = badness, arrows = flow field, edge thickness = coupling
3. **Metrics CSV**: All fields and energies per time step
4. **Summary report**: Key events, incidents, regime transitions

---

**Document End**

*This design document is a living artifact. As we learn from the MVP, we will update motivations, refine the model, and extend the scope.*
