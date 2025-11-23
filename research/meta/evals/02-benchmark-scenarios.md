# Benchmark Scenarios for Mental Model Evaluation

## Overview

**Purpose:** Standard test cases that all mental models must address.

**Philosophy:** Like unit tests for code, we need test cases for mental models.

Each scenario includes:
- **Initial state** - System configuration at t=0
- **Question** - What must the model predict/recommend?
- **Ground truth** - Known outcome (from simulation or historical data)
- **Success criteria** - How to score model performance

**Usage:**
1. Run each model against all scenarios
2. Score on 8 dimensions (from `01-evaluation-dimensions.md`)
3. Compare scores → spider graphs
4. Identify strengths/weaknesses per model

---

## Scenario 1: Incident Prediction

### Description

**Context:** Software system with 20 modules, varying coupling and technical debt.

**Problem:** Predict which module will have an incident in next 10 steps.

### Initial State

```python
modules = {
    'auth': {'complexity': 0.6, 'understanding': 0.8, 'last_modified': 2_steps_ago},
    'payment': {'complexity': 0.9, 'understanding': 0.4, 'last_modified': 1_step_ago},
    'analytics': {'complexity': 0.7, 'understanding': 0.6, 'last_modified': 5_steps_ago},
    'inventory': {'complexity': 0.5, 'understanding': 0.9, 'last_modified': 10_steps_ago},
    # ... 16 more modules
}

coupling_matrix = [
    # auth, payment, analytics, inventory, ...
    [0.0,  0.3,     0.1,       0.2,      ...],  # auth
    [0.3,  0.0,     0.4,       0.5,      ...],  # payment
    [0.1,  0.4,     0.0,       0.3,      ...],  # analytics
    # ...
]

technical_debt = {
    'auth': 0.3,
    'payment': 0.8,  # High debt!
    'analytics': 0.5,
    'inventory': 0.2,
    # ...
}
```

### Question

**Predict:** Which module will have an incident (bug, outage, deadline miss) in next 10 steps?

**Output format:**
```python
predictions = {
    'auth': 0.1,      # 10% probability
    'payment': 0.7,   # 70% probability (highest risk)
    'analytics': 0.4,
    'inventory': 0.05,
    # ...
}
```

### Ground Truth

Run simulation for 10 steps, record actual incidents:

```python
actual_incidents = {
    'payment': 1,     # Had incident at step 3
    'analytics': 1,   # Had incident at step 7
    # All others: 0
}
```

### Success Criteria

**Quantitative:**

```python
from sklearn.metrics import roc_auc_score

auc = roc_auc_score(actual_incidents, predictions)

# Scoring (Predictive Power dimension)
if auc > 0.8: score = 9-10  # Excellent
elif auc > 0.7: score = 7-8  # Good
elif auc > 0.6: score = 5-6  # Mediocre
else: score = 0-4  # Poor
```

**Qualitative:**

- Does model identify non-obvious risks? (e.g., cascading failures from coupling)
- Does model explain WHY module is at risk?
- Can model rank by severity (not just binary prediction)?

---

## Scenario 2: Resource Allocation

### Description

**Context:** 10 AI agents, 20 tasks, limited compute budget.

**Problem:** Assign tasks to agents to maximize throughput and quality.

### Initial State

```python
agents = [
    {'id': 'A1', 'skill': 'backend', 'capacity': 10_compute_units},
    {'id': 'A2', 'skill': 'frontend', 'capacity': 8_compute_units},
    {'id': 'A3', 'skill': 'data', 'capacity': 12_compute_units},
    # ... 7 more agents
]

tasks = [
    {'id': 'T1', 'type': 'backend', 'priority': 9, 'compute_required': 5},
    {'id': 'T2', 'type': 'frontend', 'priority': 7, 'compute_required': 3},
    {'id': 'T3', 'type': 'data', 'priority': 10, 'compute_required': 8},
    # ... 17 more tasks
]

total_compute_budget = 80  # Constrained (not enough for all tasks)
```

### Question

**Recommend:** Which agent should work on which task?

**Constraints:**
- Each agent has skill match requirement (backend agent prefers backend tasks)
- Each agent has compute capacity limit
- Total compute cannot exceed budget
- Maximize: priority-weighted throughput

**Output format:**
```python
allocation = {
    'A1': ['T1', 'T5'],  # Agent A1 assigned to tasks T1 and T5
    'A2': ['T2'],
    'A3': ['T3', 'T7', 'T12'],
    # ...
}
```

### Ground Truth

**Optimal solution (from integer programming solver):**

```python
optimal_allocation = {
    # ... (computed via optimization)
}

optimal_score = sum(priority[task] for task in assigned_tasks) = 142
```

### Success Criteria

**Quantitative:**

```python
model_score = sum(priority[task] for task in model_assigned_tasks)

efficiency = model_score / optimal_score

# Scoring (Actionability dimension)
if efficiency > 0.95: score = 10  # Near-optimal
elif efficiency > 0.85: score = 8
elif efficiency > 0.70: score = 6
else: score = 0-5  # Poor allocation
```

**Qualitative:**

- Does model explain allocation rationale?
- Can model handle constraint changes (e.g., budget cut)?
- Is allocation feasible? (Some models may suggest infeasible allocations)

---

## Scenario 3: Technical Debt Crisis

### Description

**Context:** System with growing technical debt, incidents increasing.

**Problem:** Recommend intervention strategy to stabilize system.

### Initial State

```python
system_state = {
    'total_debt': 0.7,  # High (70% of codebase has debt)
    'incident_rate': 3_per_week,  # Increasing
    'team_capacity': 40_hours_per_week,
    'new_feature_pressure': 'high',  # Stakeholders want features
}

modules_by_debt = [
    {'module': 'auth', 'debt': 0.9, 'criticality': 'high'},
    {'module': 'payment', 'debt': 0.8, 'criticality': 'critical'},
    {'module': 'analytics', 'debt': 0.6, 'criticality': 'medium'},
    {'module': 'notifications', 'debt': 0.5, 'criticality': 'low'},
    # ... more modules
]
```

### Question

**Recommend:** Intervention strategy to reduce incidents and stabilize system.

**Options:**
1. Refactor high-debt modules (costs time, reduces debt)
2. Add tests (costs time, reduces incident probability)
3. Freeze features, focus on quality (political cost)
4. Hire more engineers (monetary cost, delayed effect)
5. Do nothing (debt grows, incidents worsen)

**Output format:**
```python
strategy = {
    'refactor': ['payment', 'auth'],  # Which modules
    'add_tests': ['analytics'],
    'freeze_features': False,
    'hire': 2,  # Number of engineers
    'timeline': '8 weeks',
}
```

### Ground Truth

**Simulate each strategy for 12 weeks:**

```python
outcomes = {
    'refactor_payment_auth': {
        'final_incident_rate': 1_per_week,  # Improved
        'debt_reduction': 0.3,
        'features_delivered': 2,  # Fewer features
        'team_morale': 'high',  # Happy to fix problems
    },
    'do_nothing': {
        'final_incident_rate': 7_per_week,  # Crisis
        'debt_reduction': -0.1,  # Worse
        'features_delivered': 5,  # More features short-term
        'team_morale': 'low',  # Burnout
    },
    # ... other strategies
}
```

### Success Criteria

**Quantitative:**

```python
# Multi-objective scoring
strategy_score = (
    0.4 * incident_reduction +
    0.3 * debt_reduction +
    0.2 * features_delivered +
    0.1 * morale_improvement
)

# Scoring (Actionability dimension)
if strategy_score > 0.8: score = 9-10  # Excellent strategy
elif strategy_score > 0.6: score = 7-8
elif strategy_score > 0.4: score = 5-6
else: score = 0-4  # Poor strategy
```

**Qualitative:**

- Does model identify root cause (debt accumulation)?
- Does model consider trade-offs (features vs quality)?
- Is strategy actionable? (Concrete steps, realistic timeline)

---

## Scenario 4: Scaling Challenge

### Description

**Context:** System growing from 10 agents to 100 agents.

**Problem:** Predict what will break, recommend preventive measures.

### Initial State

```python
small_scale = {
    'num_agents': 10,
    'coordination': 'manual',  # Manager assigns tasks
    'communication': 'all-to-all',  # Everyone talks to everyone
    'decision_time': 5_minutes,  # Fast
    'throughput': 50_tasks_per_day,
}

planned_scale = {
    'num_agents': 100,
    'coordination': '?',  # What should it be?
    'communication': '?',
    'decision_time': '?',
    'throughput': '?',  # Goal: 500 tasks/day (10× scale)
}
```

### Question

**Predict:** What bottlenecks will emerge at 100 agents?

**Recommend:** Architecture changes to scale gracefully.

**Output format:**
```python
prediction = {
    'bottlenecks': [
        {'component': 'manager', 'reason': 'serial bottleneck (can\'t assign 100 tasks)', 'severity': 'critical'},
        {'component': 'communication', 'reason': 'O(n²) all-to-all doesn\'t scale', 'severity': 'high'},
    ],
    'recommendations': [
        {'change': 'Hierarchical coordination (manager → team leads → agents)', 'impact': 'high'},
        {'change': 'Event-driven communication (pub/sub)', 'impact': 'medium'},
    ],
}
```

### Ground Truth

**Simulate both architectures at 100 agents:**

```python
baseline_100_agents = {
    'decision_time': 45_minutes,  # 9× slower (manager bottleneck)
    'throughput': 80_tasks_per_day,  # Only 1.6× improvement (should be 10×)
    'communication_overhead': 'high',  # O(n²) messages
}

recommended_100_agents = {
    'decision_time': 8_minutes,  # Still fast
    'throughput': 480_tasks_per_day,  # 9.6× improvement (close to goal)
    'communication_overhead': 'low',  # O(n log n) with hierarchy
}
```

### Success Criteria

**Quantitative:**

```python
# Did model predict bottlenecks correctly?
predicted_bottlenecks = set(['manager', 'communication'])
actual_bottlenecks = set(['manager', 'communication', 'database'])  # Database also bottleneck

recall = len(predicted ∩ actual) / len(actual) = 2/3 = 0.67

# Did recommendations improve performance?
improvement = (recommended_throughput - baseline_throughput) / (goal_throughput - baseline_throughput)
            = (480 - 80) / (500 - 80) = 0.95  # 95% of target achieved

# Scoring (Scalability dimension)
score = 0.5 * recall + 0.5 * improvement = 0.5 * 0.67 + 0.5 * 0.95 = 0.81 → 8/10
```

**Qualitative:**

- Does model identify non-obvious bottlenecks?
- Are recommendations feasible to implement?
- Does model provide migration path (10 → 50 → 100 agents)?

---

## Scenario 5: Human-AI Alignment

### Description

**Context:** AI agents making decisions, humans losing trust.

**Problem:** Diagnose misalignment, restore trust.

### Initial State

```python
ai_agent = {
    'goal': 'maximize_throughput',  # Assigned by engineer
    'policy': 'prioritize_easy_tasks',  # Learned behavior
    'acceptance_rate': 0.25,  # Humans reject 75% of recommendations
}

human_goals = {
    'real_goal': 'maximize_value',  # Not just throughput!
    'constraints': ['quality > 0.8', 'customer_satisfaction > 0.9'],
}

misalignment_observed = {
    'symptom': 'AI recommends easy low-value tasks, humans override',
    'trust_trend': 'decreasing',  # 0.80 → 0.60 → 0.40 → 0.25 (death spiral)
}
```

### Question

**Diagnose:** Why is trust decreasing?

**Recommend:** How to realign AI with human goals?

**Output format:**
```python
diagnosis = {
    'root_cause': 'Goodhart\'s law (optimizing proxy metric, not real goal)',
    'misalignment_type': 'goal_specification_error',
}

realignment_strategy = {
    'change_objective': 'maximize_value, not throughput',
    'add_constraints': ['quality_threshold', 'customer_sat_threshold'],
    'transparency': 'Explain why AI recommends each task (build trust)',
    'human_in_loop': 'AI suggests, human approves (until trust rebuilds)',
}
```

### Ground Truth

**Simulate realignment for 8 weeks:**

```python
week_0 = {'acceptance_rate': 0.25, 'trust': 0.25, 'value_delivered': 100}
week_4 = {'acceptance_rate': 0.55, 'trust': 0.60, 'value_delivered': 180}  # Improving
week_8 = {'acceptance_rate': 0.85, 'trust': 0.85, 'value_delivered': 250}  # Virtuous cycle

# Baseline (no change)
week_8_baseline = {'acceptance_rate': 0.10, 'trust': 0.10, 'value_delivered': 50}  # Death spiral
```

### Success Criteria

**Quantitative:**

```python
# Did strategy restore trust?
trust_improvement = (week_8_trust - week_0_trust) / (1.0 - week_0_trust)
                  = (0.85 - 0.25) / (1.0 - 0.25) = 0.80  # 80% of max possible improvement

# Did value increase?
value_improvement = (week_8_value - week_0_value) / week_0_value
                  = (250 - 100) / 100 = 1.5  # 150% increase

# Scoring (Actionability for alignment problems)
score = 0.6 * trust_improvement + 0.4 * value_improvement
      = 0.6 * 0.80 + 0.4 * 1.5 = 1.08 → capped at 10/10
```

**Qualitative:**

- Does model identify Goodhart's law / misaligned incentives?
- Does model recommend concrete goal changes?
- Does model address transparency (not just goal change)?

---

## Scenario 6: Market Shock

### Description

**Context:** Stable system hit by sudden requirement change.

**Problem:** Adapt quickly to new constraints.

### Initial State

```python
before_shock = {
    'requirement': 'build_features',
    'team_allocation': {
        'new_features': 0.80,
        'maintenance': 0.15,
        'debt_paydown': 0.05,
    },
    'throughput': 10_features_per_quarter,
    'quality': 0.70,  # Mediocre but acceptable
}

shock_event = {
    'type': 'regulatory_compliance',
    'description': 'New data privacy law requires audit trail for all user actions',
    'deadline': '12 weeks',
    'effort_required': '8 person-weeks',
}
```

### Question

**Recommend:** How to reallocate resources to meet compliance deadline while minimizing disruption?

**Output format:**
```python
response_plan = {
    'new_allocation': {
        'compliance': 0.50,  # Half the team on compliance
        'new_features': 0.30,  # Reduce feature work
        'maintenance': 0.15,
        'debt_paydown': 0.05,
    },
    'timeline': {
        'weeks_1-4': 'Build audit trail infrastructure',
        'weeks_5-8': 'Retrofit existing modules',
        'weeks_9-12': 'Testing and certification',
    },
    'trade_offs': {
        'features_delivered': 4,  # Down from 10
        'technical_debt': 0.65,  # Slight increase (deferred maintenance)
        'compliance_deadline': 'met',
    },
}
```

### Ground Truth

**Simulate different response strategies:**

```python
strategy_A_aggressive_reallocation = {
    'compliance_deadline': 'met (week 11)',
    'features_delivered': 3,
    'team_morale': 'low',  # Overwork
    'debt_increase': 0.10,
}

strategy_B_hire_contractors = {
    'compliance_deadline': 'met (week 10)',
    'features_delivered': 7,  # Less disruption
    'team_morale': 'medium',
    'cost': '$50k',  # Expensive
}

strategy_C_delay_features = {
    'compliance_deadline': 'met (week 12)',
    'features_delivered': 5,
    'team_morale': 'medium',
    'stakeholder_satisfaction': 'low',  # Unhappy about feature delays
}

# Failure mode
strategy_D_ignore_compliance = {
    'compliance_deadline': 'missed',
    'features_delivered': 10,  # Short-term gain
    'regulatory_fine': '$500k',  # Long-term disaster
}
```

### Success Criteria

**Quantitative:**

```python
# Multi-criteria decision
score = (
    1.0 * (1 if compliance_met else 0) +  # Hard constraint
    0.3 * (features_delivered / baseline_features) +
    0.2 * (1 - morale_drop) +
    0.2 * (1 - debt_increase) +
    0.3 * (1 - cost / budget)
)

# Scoring (Actionability under constraints)
if score > 0.8: score_out_of_10 = 9-10
elif score > 0.6: score_out_of_10 = 7-8
else: score_out_of_10 = 0-6
```

**Qualitative:**

- Does model recognize compliance as hard constraint (not negotiable)?
- Does model explore multiple strategies (reallocation, hiring, scope reduction)?
- Does model quantify trade-offs (features vs cost vs morale)?

---

## Scenario 7: Cross-Scale Feedback Loop

### Description

**Context:** Software system nested within business system.

**Problem:** Predict how software change impacts business outcomes.

### Initial State

```python
software_system = {
    'analytics_quality': 0.70,  # Mediocre dashboard
    'understanding': 0.50,  # Family barely uses it
    'usage_frequency': 2_times_per_month,
}

business_system = {
    'revenue': 500_000_per_month,
    'customer_retention': 0.60,  # 60% come back for service
    'decision_quality': 0.65,  # Gut-feel + some data
}

proposed_change = {
    'type': 'improve_analytics',
    'action': 'Add service retention prediction + active learning',
    'cost': 40_hours_development,
}
```

### Question

**Predict:** If we improve analytics quality from 0.70 → 0.90 and add active learning (understanding 0.50 → 0.80), what's the business impact?

**Output format:**
```python
prediction = {
    'software_impact': {
        'analytics_quality': 0.90,
        'understanding': 0.80,  # Active learning helps
        'usage_frequency': 12_times_per_month,  # 6× increase
    },
    'business_impact': {
        'revenue_increase': 150_000_per_month,  # 30% lift
        'retention_increase': 0.15,  # 60% → 75%
        'decision_quality': 0.85,  # Data-driven decisions
    },
    'timeline': 'Impact visible in 8 weeks',
}
```

### Ground Truth

**Run business simulation for 6 months:**

```python
actual_outcomes = {
    'month_1': {
        'usage': 3,  # Slow adoption
        'revenue': 510_000,  # +2% (barely noticeable)
    },
    'month_3': {
        'usage': 8,  # Active learning kicking in
        'revenue': 580_000,  # +16% (trust building)
    },
    'month_6': {
        'usage': 12,  # Regular use
        'revenue': 640_000,  # +28% (close to prediction)
        'retention': 0.73,  # +13% (vs predicted +15%)
    },
}
```

### Success Criteria

**Quantitative:**

```python
# Prediction accuracy
revenue_error = abs(predicted_revenue - actual_revenue) / actual_revenue
              = abs(650_000 - 640_000) / 640_000 = 0.016  # 1.6% error

retention_error = abs(predicted_retention - actual_retention)
                = abs(0.75 - 0.73) = 0.02  # 2 percentage points

# Scoring (Predictive Power for cross-scale dynamics)
if revenue_error < 0.10 and retention_error < 0.05: score = 9-10  # Excellent
elif revenue_error < 0.20 and retention_error < 0.10: score = 7-8
else: score = 0-6
```

**Qualitative:**

- Does model capture coupling mechanism (understanding × quality × fit)?
- Does model predict delays (not instant impact)?
- Does model identify feedback loops (better decisions → more trust → more usage)?

---

## Scenario 8: Multi-Model Integration

### Description

**Context:** Complex problem requiring multiple mental models.

**Problem:** When to use which model, how to integrate insights.

### Initial State

```python
problem = {
    'description': 'System is slow, buggy, and team is overwhelmed',
    'symptoms': [
        'Incidents: 5 per week',
        'Velocity: 2 features per quarter (down from 8)',
        'Team morale: Low (3/10)',
        'Technical debt: 0.8 (high)',
        'Agent coordination: Manual, slow',
    ],
}
```

### Question

**Which mental model(s) should we apply?**

**Options:**
- Physics (technical debt, coupling energy)
- Economics (resource allocation, markets)
- System Dynamics (feedback loops, delays)
- Cognitive (understanding, learning)

**Output format:**
```python
model_selection = {
    'primary_model': 'physics',
    'reason': 'Root cause is technical debt → structural problem',
    'secondary_models': ['cognitive', 'system_dynamics'],
    'integration_strategy': {
        'physics': 'Identify high-debt modules to refactor',
        'cognitive': 'Measure understanding gaps (why are bugs happening?)',
        'system_dynamics': 'Model debt accumulation feedback loop',
    },
}
```

### Ground Truth

**Expert consensus + empirical validation:**

```python
expert_consensus = {
    'best_model': 'physics',  # 8/10 experts agree
    'reason': 'Structural problems dominate (high V_struct)',
    'multi_model_value': 'Yes - cognitive model explains why debt accumulated (low understanding)',
}

empirical_validation = {
    'physics_only': {
        'intervention': 'Refactor high-debt modules',
        'outcome': 'Incidents drop to 2/week, but velocity still low (didn\'t address team morale)',
        'effectiveness': 0.60,
    },
    'physics_plus_cognitive': {
        'intervention': 'Refactor + active learning (rebuild understanding)',
        'outcome': 'Incidents drop to 1/week, velocity recovers to 6 features/quarter',
        'effectiveness': 0.85,
    },
}
```

### Success Criteria

**Quantitative:**

```python
# Did model selection match expert consensus?
model_match = (primary_model == expert_primary) and (secondary_models ⊆ expert_secondary)

# Did multi-model approach outperform single model?
multi_model_lift = effectiveness_multi / effectiveness_single = 0.85 / 0.60 = 1.42  # 42% better

# Scoring (Generality dimension - knowing when to use which model)
if model_match and multi_model_lift > 1.3: score = 9-10
elif model_match and multi_model_lift > 1.1: score = 7-8
else: score = 0-6
```

**Qualitative:**

- Does meta-framework provide decision tree for model selection?
- Does it explain integration strategy (not just "use all models")?
- Does it identify when single model is sufficient vs multi-model needed?

---

## Summary: Benchmark Test Suite

**Eight scenarios covering different challenges:**

1. **Incident Prediction** - Predictive power
2. **Resource Allocation** - Actionability (optimization)
3. **Technical Debt Crisis** - Actionability (intervention)
4. **Scaling Challenge** - Scalability
5. **Human-AI Alignment** - Generality (non-technical problems)
6. **Market Shock** - Actionability (adaptation)
7. **Cross-Scale Feedback** - Predictive power (nested systems)
8. **Multi-Model Integration** - Generality (meta-framework)

**Usage pattern:**

```python
# For each mental model (physics, economics, cognitive, etc.)
for scenario in benchmark_scenarios:
    # Run model
    prediction = model.predict(scenario)

    # Score on 8 dimensions
    scores = evaluate(prediction, scenario.ground_truth)

    # Accumulate for spider graph
    model_scores[model.name].append(scores)

# Generate spider graph comparison
plot_spider_graph(model_scores)
```

**Next:** See `03-scoring-rubrics.md` for detailed quantitative criteria.
