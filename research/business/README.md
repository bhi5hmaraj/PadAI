# Business Systems: Software + AI + Human Co-Evolution

This folder applies tensegrity and system dynamics concepts to **socio-technical systems** where software, AI agents, and humans co-evolve.

## The Core Problem

**Software physics is too narrow for real businesses.**

Software is not the primary system - it's a **tool** embedded in a larger socio-technical system:

```
Business System
├─ Humans (family, staff, customers)
├─ Physical operations (inventory, showroom, service)
├─ Software (analytics, automation)
└─ AI Agents (assistants, decision support)
```

All four co-evolve. Software physics governs the software subsystem, but **system dynamics** governs the whole.

## Use Case: Yamaha 2-Wheeler Showroom

**Context:**
- Family business selling Yamaha bikes
- Building analytics software to help operations
- Exploring AI agents for sales, service, inventory management

**Key insight:** Software impact = Quality × Understanding × Business Fit

Perfect analytics are worthless if the family doesn't understand them.

## Mental Models Hierarchy

| Scope | Model | When to Use |
|-------|-------|-------------|
| Software codebase | **Software Physics** | Managing technical debt, velocity vs quality |
| Business operations | **System Dynamics** | Cash flow, inventory, customers, feedback loops |
| Software + Business | **Nested Systems** | Strategic decisions about software investment |
| Humans learning | **Active Learning** | Ensuring family understands analytics |
| AI agents acting | **Multi-Agent Systems** | Coordinating AI + human decision-making |

**Meta-principle:** Switch models based on the question, not ideology.

## Documents in This Folder

| Document | Purpose | Key Concepts |
|----------|---------|--------------|
| `01-system-dynamics-view.md` | Business as stocks, flows, feedback | Inventory, customers, cash, delays |
| `02-nested-systems.md` | Software physics within business dynamics | Coupling mechanisms, leverage points |
| `03-ai-agents-as-actors.md` | AI agents interacting with business + software | Agent types, policies, governance |
| `04-learning-as-coupling.md` | Understanding bridges software and business | Impact = Quality × Understanding × Fit |
| `05-showroom-experiments.md` | Practical experiments to run | Hypotheses, measurements, validation |

## Key Insights

### 1. Nested Dynamics

**Software physics (inner loop):**
- Velocity, Quality, Coherence, Learning forces
- Technical debt, refactoring, incidents
- Developer mental models

**Business dynamics (outer loop):**
- Cash flow, inventory turnover, customer acquisition
- Sales cycles, service revenue, margins
- Family/staff mental models

**Coupling:** Software enables business decisions → business outcomes validate software

### 2. AI Agents as Actors

AI agents are not just tools - they're **autonomous actors** with:

- **Goals** (maximize sales, minimize inventory costs, etc.)
- **Policies** (how they decide what to do)
- **Mental models** (their "understanding" of the system)
- **Actions** (recommendations, automations, alerts)

**Three-way dynamics:**
- Human decisions ⇄ AI recommendations ⇄ Software capabilities

### 3. Learning Is the Bottleneck

**Hypothesis:** Understanding is the coupling strength between software and business value.

```python
Business_Impact = Software_Quality × Family_Understanding × Business_Fit

# Even perfect software (Quality = 1.0) has zero impact if Understanding = 0
```

**Implication:** Invest as much in active learning (building understanding) as in building features.

### 4. Feedback Dominates

**Virtuous cycle:**
```
Good decisions → Business grows → More data → Better analytics
→ Even better decisions (reinforcing)
```

**Death spiral:**
```
Bad decisions (from misunderstanding) → Business suffers
→ Blame software → Stop using → No data → Worse decisions (balancing, degenerative)
```

**Governance goal:** Ensure virtuous cycle, prevent death spiral.

## Practical Philosophy

### Start Simple

1. **Week 1-2:** Pencil-and-paper system dynamics model with family
   - Identify stocks (inventory, customers, cash)
   - Map flows (sales, orders, payments)
   - Find leverage points (what drives profit?)

2. **Week 3-4:** Build ONE simple analytics feature
   - High-value (addresses a real pain point)
   - Obviously correct (family can validate by hand)
   - Fast feedback (see results in days, not months)

3. **Week 5+:** Run active learning experiments
   - Predict impact before deploying
   - Measure actual outcomes
   - Update mental models

### Experimentalist Mindset

**Don't build software until you know what question to answer.**

**Every feature is a hypothesis:**
- Hypothesis: "Segmenting customers by purchase history will increase retention"
- Test: Build segmentation, run A/B test (personalized follow-up vs standard)
- Measure: Retention rate, service revenue, referrals
- Learn: Update model (was hypothesis correct?)

**Every AI agent is a hypothesis:**
- Hypothesis: "AI-recommended inventory levels reduce stockouts without increasing capital tied up"
- Test: AI agent vs human judgment for 3 months
- Measure: Stockout frequency, inventory turnover, cash flow
- Learn: Where does AI help? Where does it fail?

### Governance Principles

**From software physics:**
- Understanding-gated control (can't approve what you don't understand)
- Force balance (velocity vs learning vs quality)
- Technical debt as epistemic debt

**From system dynamics:**
- Respect delays (software impact takes time to materialize)
- Watch for unintended consequences (optimization in one area creates problems elsewhere)
- Feedback loops dominate (small changes amplify over time)

**From multi-agent systems:**
- Human-AI collaboration (not replacement)
- Transparency (family must understand what AI is doing)
- Override capability (human can always veto AI recommendations)

## Connection to Other Research

**Links to:**
- `research/meta/` - Multiple mental models, empirical validation
- `research/learning/` - Active learning primitives, understanding metrics
- `research/simulation/` - Can simulate business + software dynamics
- `research/01-motivation-and-core-insight.md` - Epistemic drift applies to business too

## Quick Reference

**System dynamics stocks:**
- Inventory (bikes, parts)
- Customers (leads, pipeline, owners, loyalists)
- Cash (working capital, receivables, payables)
- Knowledge (family understanding, AI training data)

**Key feedback loops:**
1. Analytics → Better decisions → Growth → More data → Better analytics (virtuous)
2. Misunderstanding → Bad decisions → Blame software → Stop using → Worse decisions (death spiral)
3. AI recommendations → Trust → More usage → Better training → Better recommendations (virtuous)
4. AI errors → Distrust → Manual override → Less data → Worse AI (death spiral)

**AI agent types:**
- Sales assistant (lead scoring, personalized outreach)
- Inventory optimizer (order timing, stock levels)
- Service scheduler (reminder campaigns, appointment optimization)
- Analytics copilot (answer questions, generate insights)

**Critical measurements:**
- Family understanding scores (per analytics feature)
- Software impact = Quality × Understanding × Fit
- AI recommendation acceptance rate
- Business outcomes (sales, margins, cash flow, customer satisfaction)

## Philosophy

**Traditional approach:**
```
Build software → Hope family uses it → Ship features → Measure adoption
```

**Socio-technical approach:**
```
Understand business dynamics → Build mental model with family
→ Identify leverage points → Build software to address them
→ Active learning (prediction challenges)
→ Measure impact (business outcomes, not just usage)
→ Update mental model → Repeat
```

**Software and AI are not solutions. They're amplifiers of understanding.**

Good mental model + mediocre software > Perfect software + wrong mental model
