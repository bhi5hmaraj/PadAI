# Learning Force in Software Physics

This folder contains the learning-centric view of the software tensegrity model.

## The Core Insight

**Learning is not a side-effect of development. It's a force that must be balanced.**

In our five-force model:
- **Velocity** (compression) - ship fast
- **Quality** (tension) - correctness, tests
- **Coherence** (tension) - architectural consistency
- **Learning** (tension) - human understanding
- **Scope** (compression/tension) - focus, boundaries

Learning resists epistemic drift. Without it, the system accumulates **knowledge debt**:
- Code evolves faster than mental models update
- Ground truth ≠ AI representation ≠ Human understanding
- Governance fails because decisions are uninformed

## Physics Formulation

Learning contributes to the system's potential energy:

```
V_learning = Σ epistemic_gap[i] × importance[i]
```

Where:
- `epistemic_gap[i]` = distance between human model and ground truth at module i
- `importance[i]` = demand × coupling (critical modules matter more)

High learning energy → system under epistemic tension → governance required.

## Documents in This Folder

| Document | Purpose | Key Concepts |
|----------|---------|--------------|
| `01-learning-as-force.md` | Learning in five-force framework | Force balance, tension dynamics |
| `02-epistemic-energy.md` | Learning as potential energy | V_learning, knowledge debt |
| `03-active-learning-primitives.md` | Specific learning mechanisms | Prediction, comprehension sampling |
| `04-understanding-metrics.md` | Measuring epistemic gap | Understanding scores, decay models |
| `05-learning-governance.md` | Understanding-gated control | Authority = demonstrated understanding |

## Relationship to Other Documentation

**Connects to:**
- `research/meta/` - Learning is ONE mental model among many
- `research/01-motivation-and-core-insight.md` - Two-brain drift problem
- `research/simulation/` - Learning affects dynamics, can be simulated
- `docs/design/` - How learning integrates into Tensegrity governance

## Quick Reference

**Learning primitives:**
1. **Active prediction** - user predicts before running
2. **Comprehension sampling** - random quizzes on codebase
3. **Experimental sandbox** - safe practice environment
4. **Knowledge gap tracking** - per-module understanding scores
5. **Adaptive difficulty** - learning dial adjusts to user behavior

**Key metrics:**
- Understanding score U[i] ∈ [0,1] per module
- Epistemic gap = (1 - U[i])
- Knowledge debt = Σ gap[i] × complexity[i] × demand[i]

**Governance integration:**
- High knowledge debt → require more learning before shipping
- Understanding score gates approval authority
- Learning frequency adjusts based on accuracy + cycle time impact

## Philosophy

Traditional approach:
```
Write code → Document → Hope people read it → Ship
```

Learning-force approach:
```
Write code → Measure understanding gap → Active learning → Gate on demonstrated understanding → Ship
```

Learning is **structural**, not **aspirational**.
