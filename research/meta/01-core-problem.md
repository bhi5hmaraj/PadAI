# The Core Problem: Governance at Agent Velocity

## The Fundamental Challenge

### Execution is Abundant

**AI agents can execute 10-100x faster than humans:**
- Write code in minutes, not hours
- Refactor entire modules in a day
- Explore 20 architectural options in parallel
- Ship 50+ changes per day (vs. 2-3 human PRs)

**This is not speculation—it's happening now:**
- GitHub Copilot writes 46% of code on average
- Claude Code users manage 50+ projects with high velocity
- Agent-assisted development reduces time-to-PR by 55%

**Result**: Execution is no longer the bottleneck.

### Understanding is Scarce

**Humans can't keep pace with agent-generated code:**
- Read/comprehend 10-20 files per day (not 100)
- Build mental models slowly (hours/days, not minutes)
- Need context, patterns, architectural coherence
- Forget details if not actively maintained

**Knowledge representations diverge:**
1. **Ground truth**: The actual codebase (evolving at agent speed)
2. **AI representation**: What agents "know" (RAG, embeddings, context)
3. **Human representation**: What humans understand (mental models, memory)

**The gap widens:**
- After 50 agent changes, human understands ~40% of what was built
- After 200 changes, human understands ~10%
- System becomes a black box maintained by AI, governed by humans who don't understand it

### Governance is Bottlenecked

**Traditional governance assumes human-speed execution:**
- Code review: Humans read every PR
- Architecture decisions: Humans understand the system
- Tech debt management: Humans recognize debt accumulating
- Quality gates: Humans verify correctness

**At agent velocity, this breaks:**
- Can't review 50 PRs/day thoroughly
- Can't understand 100 files that changed
- Can't recognize architectural drift in real-time
- Can't validate AI's assessment of tech debt

**Result**: Either:
1. **Block agents** (velocity drops, lose the benefit)
2. **Rubber-stamp** (governance theater, quality degrades)
3. **Blind trust** (humans approve what they don't understand)

**All three fail.**

---

## The Stakes

### Without Effective Governance

**Scenario**: Unconstrained agents, human can't keep up

**t=0**: System healthy, human understands it
**t=50**: 50 agent changes, system complexity doubled
- Human understanding: 50%
- Architectural coherence: Degrading
- Technical debt: Accumulating invisibly

**t=200**: 200 agent changes, system incomprehensible
- Human understanding: 10%
- Architecture: Fragmented
- Tech debt: Crushing

**t=300**: **Crisis**
- Incident cascade (humans don't know how to fix)
- System unmaintainable
- Have to slow down or rewrite

**The pattern**: Fast execution → knowledge gap → governance failure → crisis.

### The Temptation: Slow Down

**Response**: "Agents are too risky. Require human review for everything."

**Result**:
- Velocity drops to human speed (lose the 10-100x benefit)
- Agents become expensive prompt-completion tools
- No competitive advantage
- Competitors who solve governance will win

**Can't win by slowing down.**

### What We Need: Scalable Governance

**Requirements**:
1. **Maintain understanding** - Humans keep mental models synchronized
2. **Automated quality gates** - Catch regressions without human review of every line
3. **Predictive metrics** - Early warning before incidents
4. **Adaptive constraints** - Tighten when system stressed, relax when stable
5. **Active learning** - Force human comprehension to keep pace

**Challenge**: How do we reason about such a system? What mental models help us design effective governance?

---

## Why Mental Models Matter

### Governance Requires Prediction

**You can't govern what you can't predict:**
- When will system become unstable?
- Which changes are risky?
- When to tighten constraints?
- When incidents will occur?

**Need models that predict:**
- Failure modes (before they manifest)
- Bottlenecks (before they block)
- Drift (before architecture fragments)
- Debt accumulation (before it crushes velocity)

### Different Problems, Different Models

**Problem 1: Structural tension**
- Tight coupling between mismatched modules
- Stress propagating through dependencies
- Model candidate: Physics (Laplacian energy)

**Problem 2: Resource allocation**
- Which modules get engineering time?
- How to prioritize refactors vs features?
- Model candidate: Economics (ROI, capital allocation)

**Problem 3: Agent interactions**
- Competition for resources
- Collaboration patterns
- Model candidate: Ecology (niches, competition, mutualism)

**Problem 4: Human learning**
- How fast can humans understand new code?
- What's the comprehension ceiling?
- Model candidate: Cognitive science (working memory, chunking)

**Problem 5: Emergent behavior**
- System-level properties from local interactions
- Phase transitions, criticality
- Model candidate: Complex adaptive systems (emergence, self-organization)

**Insight**: We probably need MULTIPLE models, not one universal theory.

---

## The Meta-Framework Approach

### Not: "Which model is TRUE?"

We're not asking: "Is software REALLY a physical system?" or "Is it REALLY an ecosystem?"

**These are metaphors. All models are wrong. Some are useful.**

### Instead: "Which model is USEFUL?"

**Useful = Predicts + Guides Interventions**

**For each problem type:**
1. Try multiple models
2. Test predictions empirically
3. Measure which model predicts better
4. Use whichever works

**Example**:
- Test: Does Laplacian energy predict incidents?
- Test: Does degree centrality predict incidents?
- Test: Does module ROI predict engineer allocation?
- Compare: Which has higher AUC, lower false positive rate?
- Decide: Use the winner for that problem type

### Model Selection Criteria

**Not aesthetics ("physics is elegant")**
**Not familiarity ("we know economics")**

**But empirical performance:**
- Predictive power (AUC, lead time, accuracy)
- Actionability (suggests interventions that work)
- Simplicity (easy enough to use in practice)
- Measurability (can we measure its variables?)

**Let reality choose the model.**

---

## Success Criteria for Governance

### Objective Metrics

**Goal**: System evolves rapidly while remaining stable.

**Metrics**:
1. **Velocity**: Tasks completed per day (want: high)
2. **Quality**: Bug escape rate, test coverage (want: low bugs, high coverage)
3. **Coherence**: Architectural consistency (want: low violations)
4. **Understanding**: Human comprehension score (want: >70% on critical paths)
5. **Incidents**: Production failures (want: <5 per month)
6. **Recovery time**: Time to fix incidents (want: <1 hour)

**Success = All metrics in healthy range simultaneously.**

**Failure modes**:
- High velocity, low quality (thrash, incidents)
- High quality, low velocity (bureaucracy)
- High velocity, low understanding (blind governance → eventual crisis)

### The Equilibrium Test

**Healthy equilibrium:**
- Velocity sustained over months (not just sprints)
- Quality doesn't degrade
- No architectural drift
- Humans understand the system
- Incidents rare and contained

**Mathematically** (if using physics model):
- H oscillates gently (not monotonic increase)
- T and V stay bounded
- E_local at hubs stays below threshold

**Ecologically** (if using ecology model):
- Agent "populations" stable
- No competitive exclusion
- Resources balanced

**Economically** (if using economics model):
- ROI stays positive
- Technical debt "interest rate" < growth rate

**Different models, different equilibrium definitions. All must match observed reality.**

---

## Connection to Tensegrity Vision

### Vision Document Goal

From `../../docs/design/vision_architecture.md`:

**Tensegrity (Layer 2) provides:**
- Invariant enforcement
- Equilibrium monitoring
- Active learning primitives
- Adaptive governance

**Mental models are HOW we:**
1. Define "equilibrium" mathematically
2. Detect when equilibrium breaks
3. Design interventions to restore it
4. Predict which actions will help vs. hurt

### The Five Forces

**Vision describes five forces:**
1. Velocity
2. Quality
3. Coherence
4. Learning
5. Scope

**Different models interpret these differently:**

**Physics view**:
- Forces as compression/tension in tensegrity structure
- Equilibrium = force balance (∑F ≈ 0)
- Imbalance → runaway dynamics

**Ecology view**:
- Forces as selection pressures
- Equilibrium = stable population ratios
- Imbalance → competitive exclusion

**Economics view**:
- Forces as supply/demand
- Equilibrium = market clearing
- Imbalance → price adjustment

**All valid. Which predicts best?**

---

## Open Questions

### Q1: Is there a unified theory?

**Could one model unify all aspects?**
- Maybe: Network theory? Information theory?
- Maybe not: Different scales/aspects need different models
- Empirical question: Test and see

### Q2: How to compose models?

**If we use multiple models:**
- How do they interface?
- Can physics govern structure, ecology govern agents, economics govern resources?
- Need integration framework

### Q3: When to switch models?

**System states may require different models:**
- Startup (high growth) → Ecology?
- Stable (optimization) → Economics?
- Crisis (structural failure) → Physics?

**Decision framework needed.**

### Q4: What about semantics?

**All these models ignore code meaning:**
- Structure (graph, coupling) ✓
- Dynamics (change, flow) ✓
- Semantics (correctness, behavior) ✗

**LLM embeddings? Formal verification? Execution traces?**

**Open problem.**

---

## Next Steps

**Immediate**:
1. Catalog mental models in detail (`02-model-catalog.md`)
2. Define evaluation criteria (`03-evaluation-framework.md`)
3. Design experiments to test models comparatively

**Near-term**:
1. Implement physics model (furthest along)
2. Test predictions (Exp01-02)
3. Based on results, proceed or pivot

**Long-term**:
1. Implement alternative models
2. Comparative analysis
3. Adaptive model selection framework
4. Production governance system

---

## Summary

**The Problem**: Governance at agent velocity (10-100x human speed)

**The Challenge**: Understanding is scarce, execution is abundant

**The Need**: Mental models that predict and guide governance

**The Approach**: Test multiple models empirically, use whichever works

**The Goal**: Sustained high velocity with maintained quality, coherence, and human understanding

**The Test**: Metrics in healthy range over time, equilibrium maintained

**Not forcing physics or any model. Using whatever reality validates.**

---

**Read next**: `02-model-catalog.md` for detailed catalog of candidate models.
