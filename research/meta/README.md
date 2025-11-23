# Meta-Framework: Mental Models for AI Agent Governance

## Purpose

This directory contains the **meta-framework** for evaluating different mental models that could help govern AI agents at high velocity.

**Philosophy**: We are **not forcing physics** (or any single model) onto the governance problem. Instead, we treat mental models as **tools** to be evaluated empirically. Use whichever model predicts reality and guides decisions most effectively.

---

## The Core Challenge

**Goal**: Build a governance framework where:
- AI agents execute at high velocity (10-100x human speed)
- Humans maintain understanding (no knowledge gap)
- Quality, coherence, alignment stay in balance
- The system scales (10-20 agents working together)

**Problem**: How do we reason about this system? What mental models help us predict, understand, and intervene effectively?

---

## Directory Structure

### 01-core-problem.md
**The Governance Challenge at Agent Velocity**

Articulates the fundamental problem:
- Execution is abundant (agents code fast)
- Understanding is scarce (humans can't keep up)
- Governance is bottlenecked (can't govern what you don't understand)
- Need: Mental models that help predict and guide interventions

### 02-model-catalog.md
**Catalog of Mental Models**

Six candidate mental models, each with:
- Core metaphor
- When it applies
- Predictions it makes
- Interventions it suggests
- How to test it

Models:
1. Software as Physical System (our current exploration)
2. Software as Ecosystem
3. Software as Market
4. Software as Cognitive System
5. Software as Complex Adaptive System
6. Software as Organism

### 03-evaluation-framework.md
**How to Evaluate Mental Models**

Criteria for judging usefulness:
- Predictive power (does it predict failures, bottlenecks?)
- Actionability (does it suggest interventions that work?)
- Simplicity (is it simple enough to use?)
- Generality (works across contexts?)
- Measurability (can we measure its variables?)

Statistical tests, comparative analysis methods.

### 04-model-selection.md
**When to Use Which Model**

Decision framework:
- Which model for which type of problem?
- Can multiple models apply simultaneously?
- How to recognize when a model is failing?
- Adaptive model switching

### 05-experiments-as-tests.md
**Experiments Evaluate Models**

Connection to experiments/:
- Each experiment tests one or more models
- Comparative analysis across models
- Model performance tracking
- When to abandon a model

### 06-economics-and-markets.md
**Economics and Mechanism Design for Agent Coordination**

Markets vs central planning:
- Central planning problems (Soviet-style coordination bottlenecks)
- Market mechanisms (prices, auctions, budgets, trading)
- Mechanism design principles (incentive compatibility, externality pricing)
- Four market structures (task auctions, resource trading, knowledge markets, debt trading)
- Governance via economic incentives (not top-down rules)
- Experimental validation (market vs planning at scale)

### evals/
**Evaluation Framework for Comparing Mental Models**

Comprehensive framework for empirical comparison:
- **01-evaluation-dimensions.md**: Eight dimensions for spider graphs (Predictive Power, Actionability, Simplicity, Scalability, Measurability, Generality, Learning Curve, Computational Cost)
- **02-benchmark-scenarios.md**: Eight standard test cases (incident prediction, resource allocation, technical debt, scaling, alignment, etc.)
- **03-scoring-rubrics.md**: Quantitative and qualitative criteria for scoring models
- **04-model-comparison.md**: Actual scores for Physics (7.0), Economics (8.3), System Dynamics (6.3)
- **05-decision-guide.md**: Decision tree and flowchart for selecting right model for problem

Results:
- Economics wins for: resource allocation, scalability, simplicity
- Physics wins for: incident prediction, structural analysis
- System Dynamics wins for: cross-scale feedback, long-term planning
- Multi-model integration: 42% improvement for complex problems

---

## Key Insight: Model Pluralism

**We don't need THE model. We need A TOOLKIT of models.**

Different aspects of governance may require different models:
- **Structural tension** → Physics (Laplacian)
- **Resource allocation** → Economics
- **Agent interactions** → Ecology or game theory
- **Human learning** → Cognitive science
- **System adaptability** → Complex adaptive systems

**The meta-framework is the discipline of:**
1. Testing models empirically
2. Comparing their predictive power
3. Using whichever works best for each context
4. Recognizing when to switch models

---

## Relationship to Other Docs

**research/01-06-*.md**: Deep dive into ONE model (physics)
- Beautiful theory, needs empirical validation
- May work well, may not—experiments will tell

**research/simulation/**: Implementation of physics model as simulator
- Tests physics predictions
- Could be extended to test other models

**research/experiments/**: Rigorous tests of models
- Exp02 tests: Does Laplacian predict incidents?
- Future: Does ecology predict better? Economics?

**docs/design/vision_architecture.md**: Product vision (Tensegrity governance)
- Agnostic to which model—cares about outcomes
- Wants: effective governance at agent velocity

**This directory (meta/)**: The framework for model evaluation
- How to test multiple models
- How to choose between them
- Intellectual honesty about not forcing any single view

---

## Reading Order

**New reader**:
1. `01-core-problem.md` - Understand the challenge
2. `02-model-catalog.md` - See the options
3. `03-evaluation-framework.md` - How we test
4. `04-model-selection.md` - When to use what

**Implementer**:
1. Pick a model from catalog
2. Design experiment to test it (see `../experiments/`)
3. Compare results across models
4. Use `04-model-selection.md` to guide decisions

**Researcher**:
1. Propose new model (add to catalog)
2. Define testable predictions
3. Design experiment
4. Evaluate against existing models

---

## Status

### Mental Models

| Model | Theory Docs | Simulator | Experiments | Validation |
|-------|-------------|-----------|-------------|------------|
| Physics | ✓ (01-06, learning/) | ✓ (MVP complete) | ⊙ (Exp01 passed) | ⊙ (baseline validated) |
| Economics | ✓ (06-economics-and-markets) | ☐ | ☐ (design pending) | ☐ |
| System Dynamics | ✓ (business/) | ☐ | ⊙ (6 experiments designed) | ☐ |
| Ecology | ⊙ (brief sketch in catalog) | ☐ | ☐ | ☐ |
| Cognitive | ⊙ (brief sketch in catalog, business/04) | ☐ | ☐ | ☐ |
| CAS | ⊙ (brief sketch in catalog) | ☐ | ☐ | ☐ |
| Organism | ⊙ (brief sketch in catalog) | ☐ | ☐ | ☐ |

### Meta-Framework Components

| Component | Status | Description |
|-----------|--------|-------------|
| Core problem definition | ✓ | 01-core-problem.md |
| Model catalog | ✓ | 02-model-catalog.md |
| Evaluation framework | ✓ | 03-evaluation-framework.md |
| Model selection guide | ✓ | 04-model-selection.md |
| Experiments as tests | ✓ | 05-experiments-as-tests.md |
| Economics & markets | ✓ | 06-economics-and-markets.md |
| **Evaluation benchmarks** | **✓** | **evals/ (complete framework)** |

Legend: ✓ = Complete, ⊙ = In progress, ☐ = Not started

---

## The Scientific Method Applied to Models

```
1. Problem: Need governance at agent velocity
2. Hypothesize: Model X might help (e.g., physics, ecology)
3. Predict: Model X says Y will happen
4. Test: Run experiment, measure Y
5. Compare: Does Model X predict better than Model Z?
6. Decide: Use whichever model works best
7. Iterate: Refine or replace models based on data
```

**This is honest science**: Let reality choose the model, not our aesthetic preferences.

---

## Questions This Framework Answers

**Q**: Should we use physics or ecology to model agent interactions?
**A**: Test both. Whichever predicts incidents/bottlenecks better, use that.

**Q**: What if physics works for coupling but ecology works for resource allocation?
**A**: Use both. Different models for different aspects. See `05-experiments-as-tests.md`.

**Q**: What if all models fail?
**A**: Propose new model, add to catalog, test. Or refine existing models.

**Q**: How much complexity is worth it?
**A**: See `03-evaluation-framework.md` - simplicity is a criterion. Trade off against predictive power.

---

## Next Steps

**Immediate**:
1. Complete meta/ docs (this session)
2. Connect to experiments (update exp01-02 to reference meta-framework)
3. Commit and review with user

**Next session**:
1. Implement physics model (it's furthest along)
2. Run Exp01-02, validate
3. Based on results, decide: continue physics, or pivot to alternative model?

**Future**:
1. Sketch other models in catalog
2. Design experiments for ecology, economics
3. Comparative analysis across models
4. Publish findings

---

*"The test of all knowledge is experiment. Experiment is the sole judge of scientific truth."* — Richard Feynman

**But which experiment? That depends on which model you're testing. This meta-framework is how we organize that testing.**
