# Model Evaluation Framework

## Purpose

**How do we compare mental models (physics, economics, ecology, etc.)?**

We need:
1. **Normalized dimensions** - Common axes to evaluate all models
2. **Benchmark scenarios** - Standard test cases every model must address
3. **Scoring rubrics** - Quantitative + qualitative criteria
4. **Visual comparison** - Spider graphs showing model strengths
5. **Decision guide** - When to use which model

**Goal:** Not to find "the best" model, but to know **which model fits which problem**.

---

## Philosophy

**All models are wrong, some are useful** (George Box).

The question is: **Which model is most useful for THIS problem?**

- **Physics** might predict coupling stress perfectly but fail at resource allocation
- **Economics** might optimize task assignment but miss architectural coherence
- **Ecology** might explain agent competition but not human learning

**We need a toolkit, not a hammer.**

---

## Directory Structure

### 01-evaluation-dimensions.md
**The Spider Graph Axes**

Defines dimensions for comparing models:
- Predictive power (does it predict failures?)
- Actionability (does it suggest working interventions?)
- Simplicity (easy to understand and use?)
- Scalability (works at small and large scale?)
- Measurability (can we measure its variables?)
- Generality (works across contexts?)
- Computational cost (expensive to simulate?)
- Learning curve (how long to master?)

Each dimension scored 0-10, visualized as spider graph.

### 02-benchmark-scenarios.md
**Standard Test Cases**

Define scenarios ALL models must address:
- **Scenario 1:** Incident prediction (can model predict failures?)
- **Scenario 2:** Resource allocation (10 agents, 20 tasks, how to assign?)
- **Scenario 3:** Technical debt crisis (debt accumulating, what to do?)
- **Scenario 4:** Scaling challenge (1 → 100 agents, what breaks?)
- **Scenario 5:** Human-AI alignment (agents drift from human intent)
- **Scenario 6:** Market shock (sudden requirement change)

Each scenario has:
- Initial state
- Question to answer
- Ground truth (if known)
- Success criteria

### 03-scoring-rubrics.md
**How to Score Each Dimension**

Quantitative criteria for each dimension:
- Predictive power: AUC > 0.7 (ROC curve for incident prediction)
- Actionability: Effect size > 0.5 (A/B test of interventions)
- Simplicity: LOC < 500, parameters < 20
- Scalability: Performance degradation < 10% from N=10 to N=100
- Etc.

Also qualitative rubrics (expert judgment, user feedback).

### 04-model-comparison.md
**Side-by-Side Analysis**

Actual scores for each model on each dimension.

Includes:
- Spider graphs (visual comparison)
- Strengths/weaknesses table
- When-to-use decision matrix
- Empirical results from experiments

### 05-decision-guide.md
**Model Selection Framework**

Decision tree:
```
Q1: Is the problem about structural stress (coupling, architecture)?
  → Yes: Use Physics
  → No: Continue

Q2: Is the problem about resource allocation (who does what)?
  → Yes: Use Economics
  → No: Continue

Q3: Is the problem about agent competition (scarce resources)?
  → Yes: Use Ecology
  → No: Continue

...
```

Includes:
- Problem type → Model mapping
- Multi-model scenarios (when to combine)
- Red flags (when a model is failing)

### 06-mathematical-framework.md
**Rigorous Mathematical Formalization**

Complete mathematical foundations using MathJax/LaTeX notation:
- Formal definitions of all 8 evaluation dimensions
- Scoring functions: $d_k(M) : \mathcal{M} \to [0, 10]$
- Statistical comparison methods (hypothesis testing, Bayesian)
- Multi-model integration (ensemble, sequential, hierarchical)
- Uncertainty quantification (aleatory + epistemic)
- Decision theory (utility functions, risk-adjustment, multi-armed bandit)
- Information theory (MDL, mutual information)
- Validation metrics (cross-validation, calibration, PAC bounds)

Includes:
- $\text{AUC-ROC}$ for predictive power
- Cohen's $d$ for actionability
- Pareto optimality: $M_i \succ M_j$
- Ensemble optimal weights: $\mathbf{w}^* = \frac{\mathbf{\Sigma}^{-1} \mathbf{1}}{\mathbf{1}^T \mathbf{\Sigma}^{-1} \mathbf{1}}$
- Sample complexity: $n \geq O(1/\epsilon^2 \log(1/\delta))$

### 07-complete-model-scores.md
**All Seven Models Scored and Compared**

Comprehensive scoring of all models from catalog:
1. **Physics** (7.0 avg) - Strong predictive power, structural analysis
2. **Economics** (8.3 avg) - **Best overall**, actionability + scalability
3. **System Dynamics** (6.3 avg) - General, feedback loops
4. **Ecology** (6.6 avg) - Agent interactions, competition
5. **Cognitive** (6.5 avg) - Human factors, understanding
6. **CAS** (6.1 avg) - Emergence, power laws (abstract)
7. **Organism** (6.5 avg) - Resilience, intuitive metaphors

Includes:
- Detailed dimension-by-dimension analysis for each model
- Pareto frontier analysis (simplicity vs predictive power)
- Statistical significance testing (pairwise comparisons)
- Extended decision tree for all 7 models
- Multi-model combinations (11% improvement)
- Best model by problem type table

---

## Evaluation Process

**Step 1: Define dimensions** (spider graph axes)
- What properties matter for a good mental model?
- How do we measure each property?

**Step 2: Create benchmark scenarios**
- Standard test cases every model must handle
- Include diverse problem types (prediction, allocation, coordination, etc.)

**Step 3: Score each model**
- Run experiments (quantitative)
- Expert review (qualitative)
- User feedback (pragmatic)

**Step 4: Visualize comparisons**
- Spider graphs (strengths/weaknesses at a glance)
- Tables (detailed scores)
- Decision trees (when to use what)

**Step 5: Validate empirically**
- Do high-scoring models actually work better in practice?
- A/B test: Model X vs Model Y on real problems
- Iterate based on results

---

## Example: Spider Graph for Physics vs Economics

**Dimensions (0-10 scale):**

```
         Predictive Power
              10
               |
    Simplicity|         Actionability
         8    |    6
          \   |   /
           \  |  /
            \ | /
   Scalability-+-Measurability
        7   / | \   9
           /  |  \
          /   |   \
         /    |    \
    Generality    Learning Curve
        6              8

Physics Model (blue line):
  Predictive: 8 (good at predicting coupling failures)
  Actionable: 6 (suggests refactoring, but vague on priorities)
  Simplicity: 5 (requires understanding Laplacian, energy)
  Scalability: 7 (works at different scales)
  Measurability: 9 (can measure coupling, energy)
  Generality: 6 (works for structural problems, not resource allocation)
  Learning Curve: 4 (requires physics background)
  Computational Cost: 6 (matrix operations, manageable)

Economics Model (red line):
  Predictive: 5 (not great at predicting coupling, good at allocation)
  Actionable: 9 (clear interventions: adjust prices, budgets)
  Simplicity: 8 (intuitive: markets, prices)
  Scalability: 9 (excellent at large scale)
  Measurability: 7 (can measure ROI, but "value" is subjective)
  Generality: 7 (works for allocation, not structural stress)
  Learning Curve: 9 (everyone understands markets)
  Computational Cost: 8 (auctions are fast)
```

**Insight from graph:**
- Physics: Strong on prediction and measurement, weak on learning curve
- Economics: Strong on actionability and scalability, weak on structural prediction
- **Use physics for coupling analysis, economics for task allocation**

---

## Normalization Approach

**Problem:** Different models use different units, scales, concepts.

**Solution:** Map everything to normalized dimensions.

**Example:**

| Model | Native Concept | Normalized Dimension |
|-------|----------------|---------------------|
| Physics | V_struct (coupling energy) | Structural stress (0-1) |
| Economics | ROI (return on investment) | Task priority (0-1) |
| Ecology | Fitness (survival probability) | Agent viability (0-1) |
| Cognitive | Working memory load (chunks) | Comprehension difficulty (0-1) |

**Normalization formula:**

```python
normalized_score = (raw_value - min_value) / (max_value - min_value)
```

**This allows apples-to-apples comparison.**

---

## Benchmark Scenarios (Preview)

**Scenario 1: Incident Prediction**

```
Initial state:
  - 50 modules
  - Module A has high coupling (10 dependencies)
  - Module B has low coupling (2 dependencies)
  - Both have complexity = 0.7

Question: Which module will have an incident in next 10 steps?

Physics prediction: Module A (high E_local → incident)
Economics prediction: Depends on ROI (if low ROI, might be neglected → incident)
Ecology prediction: Module A if it's in competition for resources

Ground truth: Run simulation 1000 times, measure actual incident rate

Success: Model with highest AUC (area under ROC curve)
```

**Scenario 2: Resource Allocation**

```
Initial state:
  - 10 agents
  - 20 tasks (varying urgency, complexity)
  - Limited CPU budget

Question: How to assign tasks to minimize total completion time?

Physics prediction: Not its domain (no clear answer from forces/energy)
Economics prediction: Auction (agents bid, highest bids win)
Ecology prediction: Competition (agents fight for tasks, strongest win)

Ground truth: Optimal assignment (solve as linear programming problem)

Success: Model that gets closest to optimal (measured by makespan)
```

**More scenarios in 02-benchmark-scenarios.md**

---

## Success Criteria for Evaluation Framework

**This framework succeeds if:**

1. **Comparative clarity**
   - Can see at a glance which model is best for which problem
   - Spider graphs reveal strengths/weaknesses visually

2. **Actionable guidance**
   - Decision tree leads to right model choice
   - Users report: "I knew which model to use"

3. **Empirical validation**
   - High-scoring models actually perform better in practice
   - A/B tests confirm: right model → better outcomes

4. **Iterative refinement**
   - As we learn, dimensions/rubrics can be updated
   - New models can be added and compared

5. **Intellectual honesty**
   - No "my favorite model always wins" bias
   - Data-driven, not aesthetic-driven

---

## Relationship to Other Docs

**research/meta/02-model-catalog.md**
- Lists available models (physics, economics, etc.)
- evals/ provides the comparison framework for those models

**research/meta/03-evaluation-framework.md**
- High-level criteria (predictive power, actionability, etc.)
- evals/ operationalizes those criteria (specific rubrics, benchmarks)

**research/experiments/**
- Runs experiments that feed data to evals/
- evals/ uses experiment results to score models

**research/simulation/**
- Implements models as simulators
- evals/ compares simulator predictions to ground truth

---

## Next Steps

**Immediate:**
1. Define evaluation dimensions (spider graph axes)
2. Create benchmark scenarios (standard test cases)
3. Develop scoring rubrics (how to measure each dimension)

**Near-term:**
1. Score physics model (use Exp01 results)
2. Score economics model (design experiments)
3. Compare on spider graph

**Future:**
1. Add ecology, cognitive models
2. Expand benchmark scenarios
3. User studies (which model do developers find most useful?)

---

## Philosophy

**We are not looking for THE model. We are building a TOOLKIT.**

Different problems require different tools:
- **Coupling crisis** → Physics (Laplacian predicts stress)
- **Task assignment** → Economics (auction finds efficient allocation)
- **Agent competition** → Ecology (niches, fitness)
- **Human learning** → Cognitive science (working memory, chunking)

**The meta-framework's job:** Help you pick the right tool for the job.

**This evaluation framework is how we do that rigorously.**
