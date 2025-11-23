# Mathematical Framework for Model Evaluation

## Overview

**Purpose:** Formalize the evaluation framework with rigorous mathematical foundations.

**Philosophy:** Make the evaluation process reproducible, falsifiable, and statistically sound.

This document provides:
- Formal definitions of evaluation dimensions
- Statistical comparison methods
- Multi-model integration mathematics
- Uncertainty quantification
- Decision theory for model selection

**Cross-references:**
- Uses dimensions from `01-evaluation-dimensions.md`
- Formalizes rubrics from `03-scoring-rubrics.md`
- Provides math for `04-model-comparison.md`
- Underpins decision rules in `05-decision-guide.md`

---

## Notation and Definitions

### Models and Scenarios

**Model space:**

$$\mathcal{M} = \{M_1, M_2, \ldots, M_k\}$$

where $M_i \in \{\text{Physics, Economics, System Dynamics, Ecology, Cognitive, CAS, Organism}\}$

**Scenario space:**

$$\mathcal{S} = \{S_1, S_2, \ldots, S_n\}$$

where $S_j \in \{\text{Incident Prediction, Resource Allocation, ...}\}$ (from `02-benchmark-scenarios.md`)

**Performance metric:**

$$P(M_i, S_j) \in \mathbb{R}$$

Performance of model $M_i$ on scenario $S_j$

### Dimensions

**Dimension vector for model** $M_i$:

$$\mathbf{D}_i = [d_1, d_2, \ldots, d_8]^T \in [0, 10]^8$$

where:
- $d_1$ = Predictive Power
- $d_2$ = Actionability
- $d_3$ = Simplicity
- $d_4$ = Scalability
- $d_5$ = Measurability
- $d_6$ = Generality
- $d_7$ = Learning Curve
- $d_8$ = Computational Cost

---

## Dimension 1: Predictive Power (Formalization)

### Binary Classification (Incident Prediction)

**Setup:**
- Ground truth: $\mathbf{y} \in \{0, 1\}^n$ (0 = no incident, 1 = incident)
- Predictions: $\hat{\mathbf{y}} \in [0, 1]^n$ (predicted probabilities)

**Metric: AUC-ROC**

$$\text{AUC} = \int_0^1 \text{TPR}(\text{FPR}^{-1}(t)) \, dt$$

where:
- $\text{TPR}(\theta) = P(\hat{y} \geq \theta \mid y = 1)$ (True Positive Rate)
- $\text{FPR}(\theta) = P(\hat{y} \geq \theta \mid y = 0)$ (False Positive Rate)

**Scoring function:**

$$d_1(M) = 10 \times \text{AUC}(M)$$

**Thresholds:**
- $\text{AUC} \geq 0.90 \rightarrow d_1 = 10$
- $\text{AUC} \geq 0.80 \rightarrow d_1 = 8$
- $\text{AUC} \geq 0.70 \rightarrow d_1 = 7$
- $\text{AUC} \geq 0.60 \rightarrow d_1 = 5$
- $\text{AUC} < 0.50 \rightarrow d_1 = 0$ (worse than random)

### Regression (Numerical Prediction)

**Setup:**
- Ground truth: $\mathbf{y} \in \mathbb{R}^n$
- Predictions: $\hat{\mathbf{y}} \in \mathbb{R}^n$

**Metric: MAPE (Mean Absolute Percentage Error)**

$$\text{MAPE} = \frac{1}{n} \sum_{i=1}^n \frac{|y_i - \hat{y}_i|}{|y_i|}$$

**Scoring function:**

$$d_1(M) = 10 \times \max(0, 1 - 2 \times \text{MAPE})$$

**Examples:**
- $\text{MAPE} = 0.05 \rightarrow d_1 = 10 \times 0.90 = 9.0$
- $\text{MAPE} = 0.20 \rightarrow d_1 = 10 \times 0.60 = 6.0$
- $\text{MAPE} = 0.50 \rightarrow d_1 = 10 \times 0.00 = 0.0$

### Ranking (Prioritization)

**Setup:**
- Ground truth ranks: $\mathbf{r} \in \mathbb{R}^n$ (true order)
- Predicted ranks: $\hat{\mathbf{r}} \in \mathbb{R}^n$

**Metric: Spearman's** $\rho$

$$\rho = 1 - \frac{6 \sum_{i=1}^n d_i^2}{n(n^2 - 1)}$$

where $d_i = \text{rank}(r_i) - \text{rank}(\hat{r}_i)$

**Scoring function:**

$$d_1(M) = 10 \times \max(0, \rho)$$

Note: $\rho \in [-1, 1]$, but negative correlation scores 0

---

## Dimension 2: Actionability (Formalization)

### Optimization Problems

**Setup:**
- Decision space: $\mathcal{X}$
- Objective function: $f: \mathcal{X} \to \mathbb{R}$
- Model recommendation: $\hat{x}_M \in \mathcal{X}$
- Optimal solution: $x^* = \arg\max_{x \in \mathcal{X}} f(x)$

**Metric: Efficiency**

$$\eta(M) = \frac{f(\hat{x}_M)}{f(x^*)}$$

where $\eta \in [0, 1]$ (or $[0, \infty)$ if unbounded)

**Scoring function:**

$$d_2(M) = 10 \times \min(1, \eta(M))$$

**Thresholds:**
- $\eta \geq 0.98 \rightarrow d_2 = 10$
- $\eta \geq 0.90 \rightarrow d_2 = 8$
- $\eta \geq 0.75 \rightarrow d_2 = 6$
- $\eta < 0.50 \rightarrow d_2 \leq 3$

### Intervention Effectiveness (A/B Test)

**Setup:**
- Treatment group: Apply model's intervention
- Control group: Baseline (no intervention or alternative)
- Outcomes: $Y_{\text{treatment}}, Y_{\text{control}}$

**Metric: Cohen's d (Effect Size)**

$$d = \frac{\mu_{\text{treatment}} - \mu_{\text{control}}}{\sigma_{\text{pooled}}}$$

where:

$$\sigma_{\text{pooled}} = \sqrt{\frac{\sigma^2_{\text{treatment}} + \sigma^2_{\text{control}}}{2}}$$

**Scoring function:**

$$d_2(M) = \begin{cases}
10 & \text{if } d \geq 0.8 \text{ (large effect)} \\
7 & \text{if } d \geq 0.5 \text{ (medium effect)} \\
4 & \text{if } d \geq 0.2 \text{ (small effect)} \\
1 & \text{otherwise (no effect)}
\end{cases}$$

### Multi-Objective Problems

**Setup:**
- $K$ objectives: $f_1, f_2, \ldots, f_K$
- Weights: $\mathbf{w} = [w_1, \ldots, w_K]^T$, where $\sum_k w_k = 1$

**Metric: Weighted Achievement**

$$a(M) = \sum_{k=1}^K w_k \times \frac{f_k(\hat{x}_M)}{f_k(x^*_k)}$$

where $x^*_k = \arg\max f_k(x)$ (optimal for objective $k$)

**Scoring function:**

$$d_2(M) = 10 \times a(M)$$

---

## Dimension 3: Simplicity (Formalization)

### Code Complexity

**Metric: Kolmogorov Complexity (Approximation)**

$$K(M) \approx \text{LOC} + \lambda_1 \times \text{params} + \lambda_2 \times \text{cyclomatic}$$

where:
- LOC = Lines of code
- params = Number of parameters
- cyclomatic = Cyclomatic complexity
- $\lambda_1, \lambda_2$ = Weighting constants

**Scoring function:**

$$d_3(M) = \frac{10}{1 + \log(K(M) / K_{\text{ref}})}$$

where $K_{\text{ref}} = 100$ (reference complexity)

### Learning Time

**Metric: Time to Proficiency (User Study)**

$$T = \text{median}(\{t_1, t_2, \ldots, t_N\})$$

where $t_i$ = time for user $i$ to reach proficiency threshold

**Scoring function:**

$$d_3(M) = 10 \times e^{-\lambda T}$$

with $\lambda = 0.1 \text{ hr}^{-1}$ (decay constant)

**Examples:**
- $T = 2$ hr $\rightarrow d_3 = 8.2$
- $T = 10$ hr $\rightarrow d_3 = 3.7$
- $T = 40$ hr $\rightarrow d_3 = 0.2$

### Conceptual Complexity (Entropy)

**Metric: Concept Entropy**

$$H(M) = -\sum_i p(c_i) \log p(c_i)$$

where:
- $c_i$ = concept $i$ in model $M$
- $p(c_i)$ = probability user encounters concept $i$

High entropy = many concepts (complex)
Low entropy = few concepts (simple)

**Scoring function:**

$$d_3(M) = 10 \times e^{-H(M) / H_{\max}}$$

---

## Dimension 4: Scalability (Formalization)

### Performance Degradation

**Setup:**
- Problem sizes: $\mathbf{n} = [n_1, n_2, \ldots, n_K]$
- Performance at each size: $p(n)$

**Metric: Degradation Rate**

$$\delta = \frac{p(n_{\max}) - p(n_{\min})}{p(n_{\min})}$$

Negative $\delta$ = improvement at scale
Positive $\delta$ = degradation at scale

**Scoring function:**

$$d_4(M) = 10 \times \max(0, 1 - \delta)$$

**Examples:**
- $\delta = -0.10 \rightarrow d_4 = 10$ (10% improvement, capped)
- $\delta = 0.05 \rightarrow d_4 = 9.5$
- $\delta = 0.50 \rightarrow d_4 = 5.0$
- $\delta = 1.00 \rightarrow d_4 = 0.0$

### Computational Scaling

**Metric: Asymptotic Complexity**

$$T(n) = O(n^\alpha)$$

Fit runtime to power law: $\log T = \alpha \log n + \beta$

**Scoring function:**

$$d_4(M) = \begin{cases}
10 & \text{if } \alpha \leq 1.2 \text{ (near-linear } O(n)\text{)} \\
8 & \text{if } \alpha \leq 1.5 \text{ (} O(n \log n)\text{)} \\
6 & \text{if } \alpha \leq 2.0 \text{ (} O(n^2)\text{)} \\
3 & \text{if } \alpha \leq 3.0 \text{ (} O(n^3)\text{)} \\
1 & \text{otherwise (worse than cubic)}
\end{cases}$$

---

## Dimension 5: Measurability (Formalization)

### Per-Variable Measurability

For model $M$ with variables $\mathcal{V} = \{v_1, \ldots, v_J\}$:

**Measurability score for variable** $v_j$:

$$m(v_j) = \begin{cases}
10 & \text{if directly observable} \\
8 & \text{if computable from logs} \\
6 & \text{if requires instrumentation} \\
4 & \text{if requires survey/quiz} \\
2 & \text{if requires expert judgment} \\
0 & \text{if unmeasurable}
\end{cases}$$

**Overall measurability:**

$$d_5(M) = \frac{1}{J} \sum_{j=1}^J m(v_j)$$

### Measurement Uncertainty

For measurable variable $v$ with measurement $\hat{v}$:

**Uncertainty:**

$$\sigma(v) = \text{std}(\hat{v} - v)$$

**Signal-to-noise ratio:**

$$\text{SNR}(v) = \frac{\mu(v)}{\sigma(v)}$$

**Adjusted measurability:**

$$m_{\text{adjusted}}(v) = m(v) \times \min\left(1, \frac{\text{SNR}(v)}{3}\right)$$

Interpretation:
- $\text{SNR} \geq 3 \rightarrow$ Full score
- $\text{SNR} < 3 \rightarrow$ Penalized for noise

---

## Dimension 6: Generality (Formalization)

### Context Coverage

**Setup:**
- Context set: $\mathcal{C} = \{c_1, \ldots, c_N\}$
- Model applicability: $a(M, c_i) \in \{0, 1\}$

**Metric: Coverage Ratio**

$$\gamma(M) = \frac{1}{N} \sum_{i=1}^N a(M, c_i)$$

**Scoring function:**

$$d_6(M) = 10 \times \gamma(M)$$

### Transfer Learning

**Setup:**
- Train on domain A: $M_A$
- Test on domain B: Performance $p_B$
- Native performance on A: $p_A$

**Metric: Transfer Ratio**

$$\tau(M) = \frac{p_B}{p_A}$$

**Scoring function:**

$$d_6(M) = 10 \times \tau(M)$$

Interpretation:
- $\tau \approx 1 \rightarrow$ Model generalizes perfectly
- $\tau \approx 0 \rightarrow$ Model doesn't transfer

---

## Dimension 7: Learning Curve (Formalization)

### Time to Proficiency

**Learning curve function:**

$$P(t) = P_\infty \times (1 - e^{-\lambda t})$$

where:
- $P(t)$ = proficiency at time $t$
- $P_\infty$ = asymptotic proficiency
- $\lambda$ = learning rate

**Scoring based on** $T_{50}$ (time to 50% proficiency):

$$d_7(M) = 10 \times e^{-\lambda' T_{50}}$$

with $\lambda' = 0.05 \text{ hr}^{-1}$

### Retention Rate

**Setup:**
- Initial proficiency: $P_0$ (after training)
- Proficiency after delay $\Delta t$: $P(\Delta t)$

**Metric: Retention**

$$R(\Delta t) = \frac{P(\Delta t)}{P_0}$$

**Decay model:**

$$R(t) = e^{-\lambda_{\text{decay}} t}$$

**Scoring adjustment:**

$$d_7(M) = d_{7,\text{base}}(M) \times R(4 \text{ weeks})$$

Penalize models with poor retention

---

## Dimension 8: Computational Cost (Formalization)

### Runtime

**Metric: Wall-clock time**

$$T_{\text{compute}} = \text{median}(\{t_1, \ldots, t_K\})$$

($K$ runs)

**Scoring function:**

$$d_8(M) = \begin{cases}
10 & \text{if } T < 1\text{s} \\
9 & \text{if } T < 5\text{s} \\
8 & \text{if } T < 10\text{s} \\
6 & \text{if } T < 30\text{s} \\
4 & \text{if } T < 60\text{s} \\
1 & \text{otherwise}
\end{cases}$$

### Space Complexity

**Metric: Peak memory usage**

$$M_{\text{mem}} = \max \text{ memory during execution}$$

**Scoring function:**

$$d_{8,\text{mem}}(M) = \begin{cases}
10 & \text{if } M_{\text{mem}} < 100 \text{ MB} \\
8 & \text{if } M_{\text{mem}} < 500 \text{ MB} \\
6 & \text{if } M_{\text{mem}} < 1 \text{ GB} \\
3 & \text{if } M_{\text{mem}} < 5 \text{ GB} \\
1 & \text{otherwise}
\end{cases}$$

**Combined score:**

$$d_8(M) = 0.7 \times d_{8,\text{time}}(M) + 0.3 \times d_{8,\text{mem}}(M)$$

---

## Composite Scoring

### Unweighted Average

$$\text{Score}(M) = \frac{1}{8} \sum_{k=1}^8 d_k(M)$$

### Weighted Average

$$\text{Score}_w(M) = \sum_{k=1}^8 w_k \times d_k(M)$$

where $\mathbf{w} \in \Delta^8 = \{\mathbf{w}: \sum w_k = 1, w_k \geq 0\}$

**Default weights (from `03-scoring-rubrics.md`):**

$$\mathbf{w}_{\text{default}} = [0.25, 0.25, 0.10, 0.15, 0.10, 0.05, 0.05, 0.05]^T$$

Emphasizes predictive power and actionability

### Pareto Optimality

**Model** $M_i$ **dominates** $M_j$ ($M_i \succ M_j$) if:

$$\forall k: d_k(M_i) \geq d_k(M_j) \quad \text{AND} \quad \exists k: d_k(M_i) > d_k(M_j)$$

**Pareto frontier:**

$$\mathcal{P} = \{M \in \mathcal{M} : \nexists M' \in \mathcal{M} \text{ such that } M' \succ M\}$$

Non-dominated models are on Pareto frontier

---

## Statistical Comparison

### Hypothesis Testing

**Null hypothesis:**

$$H_0: \text{Score}(M_i) = \text{Score}(M_j)$$

**Test statistic (paired samples):**

$$t = \frac{\mu_i - \mu_j}{\sqrt{\sigma^2_i/n_i + \sigma^2_j/n_j}}$$

Degrees of freedom: $\nu = n_i + n_j - 2$

**Reject** $H_0$ if:

$$p\text{-value} = P(|T| \geq |t|) < \alpha$$

where $\alpha = 0.05$ (significance level)

### Confidence Intervals

**For score estimate:**

$$\text{CI}_{95}(M) = \text{Score}(M) \pm 1.96 \times \text{SE}(M)$$

where $\text{SE}(M) = \sigma(M) / \sqrt{n}$

**Interpretation:**
- If $\text{CI}_{95}(M_i) \cap \text{CI}_{95}(M_j) = \emptyset \rightarrow$ Significantly different
- Otherwise $\rightarrow$ No evidence of difference

### Bayesian Model Comparison

**Prior over models:**

$$P(M_i) = \frac{1}{|\mathcal{M}|}$$

(uniform prior)

**Likelihood (performance on scenarios):**

$$P(\text{Data} \mid M_i) = \prod_j P(S_j \mid M_i)$$

**Posterior:**

$$P(M_i \mid \text{Data}) \propto P(\text{Data} \mid M_i) \times P(M_i)$$

**Model selection via maximum a posteriori:**

$$M^* = \arg\max_{M_i} P(M_i \mid \text{Data})$$

---

## Multi-Model Integration

### Sequential Integration (Pipeline)

**Chain of models:**

$$x_0 \xrightarrow{M_1} x_1 \xrightarrow{M_2} x_2 \xrightarrow{\ldots} x_K$$

Output: $x_K$

**Performance:**

$$P_{\text{seq}} = P(M_1) \times P(M_2 \mid M_1) \times \cdots \times P(M_K \mid M_{K-1}, \ldots, M_1)$$

**Error propagation:**

$$\sigma^2_{\text{total}} \approx \sum_{k=1}^K \left(\frac{\partial f}{\partial x_k}\right)^2 \sigma^2_k$$

where $f$ is final output function

### Ensemble Integration (Parallel)

**Weighted average:**

$$\hat{y}_{\text{ensemble}} = \sum_{i=1}^K w_i \times \hat{y}_i$$

where:
- $\hat{y}_i$ = prediction from model $M_i$
- $w_i$ = weight for model $i$
- $\sum w_i = 1$

**Optimal weights (minimize MSE):**

$$\mathbf{w}^* = \arg\min_\mathbf{w} \mathbb{E}\left[\left(y - \sum_i w_i \hat{y}_i\right)^2\right]$$

**Solution:**

$$\mathbf{w}^* = \frac{\mathbf{\Sigma}^{-1} \mathbf{1}}{\mathbf{1}^T \mathbf{\Sigma}^{-1} \mathbf{1}}$$

where $\Sigma_{ij} = \text{Cov}(\hat{y}_i, \hat{y}_j)$

**Variance reduction:**

$$\text{Var}(\hat{y}_{\text{ensemble}}) = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w} \leq \min_i \text{Var}(\hat{y}_i)$$

Ensemble reduces variance

### Hierarchical Integration (Nested)

**Outer model parameters depend on inner models:**

$$M_{\text{outer}}(x; \boldsymbol{\theta}_{\text{inner}})$$

where $\boldsymbol{\theta}_{\text{inner}} = f(M_{\text{inner}_1}, M_{\text{inner}_2}, \ldots)$

**Example:**
```
System Dynamics (business level)
  └─ Physics (software level) provides parameters
```

**Performance:**

$$P_{\text{nested}} = P_{\text{outer}} \times \mathbb{E}[P_{\text{inner}} \mid \text{Outer}]$$

---

## Uncertainty Quantification

### Aleatory Uncertainty (Randomness)

**Stochastic scenarios:**

$$P(S_j \mid M_i) \sim \text{Distribution}$$

Multiple runs yield different outcomes

**Estimate via Monte Carlo:**

$$\mathbb{E}[P(M, S)] \approx \frac{1}{N} \sum_{n=1}^N P_n(M, S)$$

### Epistemic Uncertainty (Knowledge)

**Parameter uncertainty:**

$$\boldsymbol{\theta} \sim P(\boldsymbol{\theta} \mid \text{Data})$$

(posterior distribution)

**Prediction uncertainty:**

$$P(y \mid x, \text{Data}) = \int P(y \mid x, \boldsymbol{\theta}) P(\boldsymbol{\theta} \mid \text{Data}) \, d\boldsymbol{\theta}$$

**Credible intervals:**

$$\text{CI}_{95} = [q_{0.025}, q_{0.975}]$$

where $q_p$ = quantile at $p$

### Total Uncertainty

**Law of total variance:**

$$\text{Var}(Y) = \underbrace{\mathbb{E}[\text{Var}(Y \mid \boldsymbol{\theta})]}_{\text{Aleatory}} + \underbrace{\text{Var}(\mathbb{E}[Y \mid \boldsymbol{\theta}])}_{\text{Epistemic}}$$

---

## Decision Theory

### Utility Function

**Define utility for choosing model** $M$:

$$U(M, \text{context}) = \sum_k w_k \times d_k(M) - \text{Cost}(M, \text{context})$$

where Cost includes:
- Learning time $\times$ hourly rate
- Computational cost
- Implementation effort

**Optimal model:**

$$M^* = \arg\max_M U(M, \text{context})$$

### Risk-Adjusted Selection

**For uncertain outcomes:**

$$\text{EU}(M) = \mathbb{E}[U(M, S)]$$

(Expected utility)

- **Risk-averse:** Maximize $\text{EU}(M) - \lambda \times \text{Var}(U(M, S))$
- **Risk-neutral:** Maximize $\text{EU}(M)$
- **Risk-seeking:** Maximize $\text{EU}(M) + \lambda \times \text{Var}(U(M, S))$

### Multi-Armed Bandit (Adaptive Selection)

**Exploration-exploitation trade-off**

**Upper Confidence Bound (UCB):**

$$M_t = \arg\max_i \left[\hat{\mu}_i + \sqrt{\frac{2 \log t}{n_i}}\right]$$

where:
- $\hat{\mu}_i$ = empirical mean performance of model $i$
- $n_i$ = number of times model $i$ has been used
- $t$ = current time step

**Thompson Sampling:**

1. Sample: $\theta_i \sim P(\theta_i \mid \text{Data}_i)$
2. Choose: $M_t = \arg\max_i f(\theta_i)$

---

## Information Theory

### Model Complexity (Description Length)

**Minimum Description Length (MDL):**

$$\text{MDL}(M) = L(M) + L(\text{Data} \mid M)$$

where:
- $L(M)$ = bits to encode model
- $L(\text{Data} \mid M)$ = bits to encode data given model

Prefer models with low MDL (Occam's razor)

### Mutual Information

**How much does model** $M$ **tell us about scenario** $S$?

$$I(M; S) = H(S) - H(S \mid M)$$

where:
- $H(S)$ = entropy of scenarios
- $H(S \mid M)$ = conditional entropy

High $I(M; S) \rightarrow$ Model captures scenario structure

---

## Validation Metrics

### Cross-Validation

**K-fold cross-validation:**

$$\text{CV}_{\text{score}}(M) = \frac{1}{K} \sum_{k=1}^K P(M_{\text{train}}^{-k}, S_{\text{test}}^k)$$

where:
- $M_{\text{train}}^{-k}$ = model trained on all scenarios except fold $k$
- $S_{\text{test}}^k$ = scenarios in fold $k$

### Bootstrapping

**Bootstrap estimate of variance:**

1. Sample scenarios with replacement: $\mathcal{S}^* = \{S_1^*, \ldots, S_n^*\}$
2. Compute: $\text{Score}_b(M)$ on $\mathcal{S}^*$
3. Repeat $B$ times
4. $\text{Var}(\text{Score}) \approx \text{Var}(\{\text{Score}_1, \ldots, \text{Score}_B\})$

### Calibration

**For probabilistic predictions:**

**Expected Calibration Error (ECE):**

$$\text{ECE} = \sum_b \frac{n_b}{n} |\text{acc}(b) - \text{conf}(b)|$$

where:
- $b$ = bins $[0, 0.1), [0.1, 0.2), \ldots, [0.9, 1.0]$
- $\text{acc}(b)$ = accuracy in bin $b$
- $\text{conf}(b)$ = average confidence in bin $b$

Well-calibrated model: $\text{ECE} \approx 0$

---

## Sensitivity Analysis

### Weight Sensitivity

**How does composite score change with weights?**

**Gradient:**

$$\frac{\partial \text{Score}_w}{\partial w_k} = d_k(M) - \frac{1}{8} \sum_j d_j(M)$$

If $d_k >$ avg $\rightarrow$ increasing $w_k$ increases score

**Robustness:**

$$R(M) = \min_{\mathbf{w} \in \Delta^8} \text{Score}_w(M)$$

Robust model scores well under any weighting

### Parameter Sensitivity

**For model with parameters** $\boldsymbol{\theta}$:

**Sensitivity coefficient:**

$$S(\theta_i) = \frac{\theta_i}{\text{Score}} \times \frac{\partial \text{Score}}{\partial \theta_i}$$

Measures % change in score per % change in parameter

---

## Formal Guarantees

### Sample Complexity

**How many scenarios needed to estimate score accurately?**

**Hoeffding's inequality:**

$$P(|\text{Score}_{\text{empirical}} - \text{Score}_{\text{true}}| \geq \epsilon) \leq 2 \exp(-2n\epsilon^2)$$

where $n$ = number of scenarios

**For** $\epsilon = 0.5$ (half-point accuracy), $\delta = 0.05$ (95% confidence):

$$n \geq \frac{\log(2/\delta)}{2\epsilon^2} \approx 15 \text{ scenarios}$$

### PAC Learning Bound

**Probably Approximately Correct:**

$$P(\text{Score}_{\text{empirical}} \text{ within } \epsilon \text{ of } \text{Score}_{\text{true}}) \geq 1 - \delta$$

requires $n \geq O(1/\epsilon^2 \log(1/\delta))$

---

## Example Application

### Compare Physics vs Economics

**Dimension scores:**

$$\mathbf{D}_{\text{physics}} = [8, 7, 5, 9, 7, 7, 5, 8]^T$$
$$\mathbf{D}_{\text{econ}} = [6, 9, 8, 10, 9, 7, 9, 10]^T$$

**Composite scores:**

$$\text{Score}_{\text{unweighted}}(\text{Physics}) = \frac{1}{8} \sum d_k = 7.00$$
$$\text{Score}_{\text{unweighted}}(\text{Econ}) = \frac{1}{8} \sum d_k = 8.25$$

**Hypothesis test:**

$$H_0: \text{Score}(\text{Physics}) = \text{Score}(\text{Econ})$$

$t$-statistic (from bootstrap): $t = -2.3$
$p$-value $= 0.032 < 0.05$

**Reject** $H_0$: Economics significantly better (overall)

**But on Predictive Power dimension:**

$$d_1(\text{Physics}) = 8 > d_1(\text{Econ}) = 6$$

$t = 2.1$, $p = 0.048 < 0.05$

Physics significantly better for prediction

**Decision rule:**
- If task = prediction: Choose Physics
- If task = resource allocation: Choose Economics

---

## Summary

**This mathematical framework provides:**

1. **Formal definitions** of all 8 evaluation dimensions
2. **Scoring functions** mapping measurements to $[0, 10]$
3. **Statistical tests** for model comparison ($t$-test, Bayesian)
4. **Multi-model integration** mathematics (ensemble, sequential, hierarchical)
5. **Decision theory** for optimal model selection
6. **Uncertainty quantification** (aleatory + epistemic)
7. **Validation metrics** (cross-validation, calibration)
8. **Formal guarantees** (sample complexity, PAC bounds)

**All formulas are:**
- Reproducible (clear procedures)
- Falsifiable (testable hypotheses)
- Statistically rigorous (confidence intervals, $p$-values)

**Cross-references:**
- See `01-evaluation-dimensions.md` for conceptual definitions
- See `02-benchmark-scenarios.md` for test cases
- See `03-scoring-rubrics.md` for practical implementation
- See `04-model-comparison.md` for actual scores
- See `05-decision-guide.md` for decision rules
- See `07-complete-model-scores.md` for all 7 models

**Next:** Apply this framework to score all models (Physics, Economics, System Dynamics, Ecology, Cognitive, CAS, Organism).
