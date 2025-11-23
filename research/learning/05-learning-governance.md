# Learning Governance

## Overview

**Understanding-gated control:** Authority is earned through demonstrated understanding.

This document explains:
1. How understanding scores gate decisions
2. Progressive authority levels
3. Integration with approval workflows
4. Trade-offs and tuning

---

## Core Principle

**You can only govern what you understand.**

Traditional model:
```
Role (senior engineer) → Authority (can approve PRs)
```

Learning governance model:
```
Demonstrated understanding → Authority (can approve PRs on specific modules)
```

**Why this matters:**

- **Safety:** Prevents uninformed decisions
- **Accountability:** Decisions traceable to knowledge
- **Incentive alignment:** Learning unlocks agency

---

## Understanding Gates

### Approval Authority

**Rule:** Can only approve changes to modules you understand above threshold.

```python
def can_approve_pr(engineer_id, pr):
    modules_changed = get_modules(pr)

    for module in modules_changed:
        understanding = get_understanding(engineer_id, module)
        threshold = get_threshold(module)

        if understanding < threshold:
            return False, f"Blocked: {module} requires {threshold:.0%} understanding, you have {understanding:.0%}"

    return True, "Approved: sufficient understanding on all modules"
```

**Example thresholds:**

```python
thresholds = {
    'payment.py': 0.80,    # Critical: 80%
    'auth.py': 0.80,       # Critical: 80%
    'api.py': 0.60,        # Normal: 60%
    'utils.py': 0.40,      # Low-risk: 40%
    'config.py': 0.30,     # Config: 30%
}
```

### Modification Rights

**Tiered access based on understanding:**

```python
access_levels = {
    'read_only': understanding < 0.30,
    'can_submit_pr': understanding >= 0.30,
    'can_approve_others': understanding >= 0.60,
    'can_approve_own': understanding >= 0.80,
    'can_mentor': understanding >= 0.90,
}
```

**Example:**

```
Engineer Alice on payment.py:
  understanding = 0.55

Rights:
  ✓ Read code
  ✓ Submit PRs
  ✗ Approve PRs (need 60%)
  ✗ Self-merge (need 80%)

To unlock approval: Complete 3 more challenges
```

### Scope-Based Gating

**Different thresholds for different change types:**

```python
def get_required_understanding(change_type, module):
    base_threshold = thresholds[module]

    multipliers = {
        'feature_add': 0.9,        # Need 90% of base (e.g., 0.72 for 0.80 base)
        'refactor': 1.1,           # Need 110% (harder)
        'bug_fix': 0.8,            # 80% (easier)
        'config_change': 0.6,      # 60% (easiest)
        'delete_code': 1.2,        # 120% (hardest - must understand to delete safely)
    }

    return base_threshold * multipliers[change_type]
```

**Rationale:**

- **Refactors** require deep understanding (must not break behavior)
- **Deletions** are risky (what depends on this?)
- **Bug fixes** are narrower scope
- **Config changes** are lower risk

---

## Progressive Authority

### Beginner (0-30%)

**Rights:**
- Read code
- File issues
- Ask questions

**Restrictions:**
- Cannot submit PRs
- Cannot approve anything

**Learning path:**
- Complete beginner challenges
- Pair with mentor
- Shadow code reviews

### Contributor (30-60%)

**Rights:**
- Submit PRs
- Comment on PRs
- Work on assigned modules

**Restrictions:**
- Cannot approve PRs (even own)
- Cannot modify critical modules

**Learning path:**
- Active prediction challenges
- Comprehension quizzes
- Sandbox exercises

### Reviewer (60-80%)

**Rights:**
- Approve others' PRs
- Mentor beginners
- Propose architectural changes

**Restrictions:**
- Cannot self-merge
- Need peer review on own PRs

**Learning path:**
- Advanced debugging challenges
- Cross-module understanding
- Review others' PRs

### Expert (80-100%)

**Rights:**
- Self-merge (with understanding)
- Approve critical changes
- Set governance policies

**Responsibilities:**
- Mentor contributors
- Maintain understanding (periodic refresh)
- Design learning challenges

---

## Governance Workflows

### Workflow 1: PR Approval

```
1. Engineer submits PR touching modules [A, B, C]

2. System checks understanding:
   A: 75% (threshold 60%) ✓
   B: 55% (threshold 60%) ✗
   C: 90% (threshold 80%) ✓

3. PR blocked on module B
   Message: "Complete 2 challenges on module B to unlock approval"

4. Engineer completes challenges:
   Challenge 1 (prediction): ✓ Correct
   Challenge 2 (debugging): ✓ Correct
   New understanding: 65%

5. PR unblocked, can proceed to review
```

### Workflow 2: Emergency Override

**For production incidents:**

```python
def emergency_override(engineer_id, module_id, reason):
    # Allow override if:
    # 1. Incident severity is high
    # 2. No one with sufficient understanding is available
    # 3. Incident commander approves

    if is_incident_critical():
        log_override(engineer_id, module_id, reason)
        return True, "Emergency override granted"

    return False, "Not critical enough for override"
```

**Post-incident:**

```
# After override used
1. Incident resolved
2. System flags: "Alice modified payment.py with override (understanding 45%)"
3. Required: Post-incident learning
   - "What did you learn from this incident?"
   - Comprehension challenges on the modified module
   - Must reach threshold before next change
```

### Workflow 3: Team Coverage

**Ensure team has collective understanding:**

```python
def check_team_coverage(module):
    team_understanding = [
        get_understanding(engineer, module)
        for engineer in team
    ]

    # Need at least 2 people above threshold
    experts = sum(1 for u in team_understanding if u >= threshold[module])

    if experts < 2:
        return False, f"Only {experts} experts on {module}, need 2 minimum"

    return True, "Sufficient team coverage"
```

**Governance:**

- Critical modules require ≥2 experts
- If <2, block new features until knowledge is spread
- Forces knowledge sharing, prevents single point of failure

---

## Integration with Five Forces

### Learning × Velocity

**Trade-off:**

```
More learning gates → Slower velocity (PRs blocked)
Fewer gates → Faster velocity (but more incidents)
```

**Tuning:**

```python
# Adjust thresholds based on velocity goals
if velocity_too_low:
    thresholds *= 0.9  # Reduce by 10%
    log("Lowered learning gates to increase velocity")

if incident_rate_too_high:
    thresholds *= 1.1  # Increase by 10%
    log("Raised learning gates to reduce incidents")
```

### Learning × Quality

**Synergy:**

Learning gates → better-informed decisions → fewer bugs

```python
# Correlation check
correlation = compute_correlation(understanding_scores, bug_density)

# Expected: strong negative correlation (r < -0.5)
# High understanding → low bugs
```

### Learning × Coherence

**Mutual reinforcement:**

- Learning requires coherent mental models
- Understanding coherence requires collective knowledge

**Governance:**

```python
# Block architectural changes unless team understands
def can_change_architecture(module, change_description):
    team_understanding = get_team_understanding(module)

    if team_understanding < 0.70:
        return False, "Team understanding too low for architectural change"

    # Also require majority approval
    return True, "OK if ≥2 experts approve"
```

### Learning × Scope

**Scope as escape valve:**

```
Tight deadline → Reduce scope to modules team already understands

Example:
  Option A: Add feature X (requires learning 3 new modules, 2 weeks)
  Option B: Add feature Y (uses known modules, 3 days)

  Under time pressure → Choose B
```

---

## Tuning Parameters

### 1. Threshold Levels

**Per-module thresholds:**

```python
# Conservative (safety-critical)
thresholds = {
    'critical': 0.90,   # 90% understanding required
    'normal': 0.70,     # 70%
    'low_risk': 0.50,   # 50%
}

# Aggressive (startup velocity)
thresholds = {
    'critical': 0.60,   # 60%
    'normal': 0.40,     # 40%
    'low_risk': 0.20,   # 20%
}
```

### 2. Gate Frequency

**How often to check understanding:**

```python
gate_frequency = {
    'every_pr': 1.0,         # Gate every PR (strict)
    'random_sample': 0.3,    # Gate 30% of PRs (medium)
    'critical_only': 0.1,    # Gate only critical modules (loose)
}
```

### 3. Challenge Difficulty

**Adjust difficulty based on threshold:**

```python
if threshold >= 0.80:
    difficulty = 'hard'     # Advanced debugging, refactoring
elif threshold >= 0.60:
    difficulty = 'medium'   # Prediction, causal reasoning
else:
    difficulty = 'easy'     # Basic recall
```

### 4. Decay Rate

**How fast understanding degrades:**

```python
# Faster decay → more frequent refreshers
# Slower decay → longer intervals between challenges

decay_multiplier = {
    'aggressive_refresh': 2.0,   # 2× baseline decay
    'normal': 1.0,
    'relaxed': 0.5,              # 0.5× decay (longer retention)
}
```

---

## Failure Modes and Mitigations

### Failure Mode 1: Learning Gridlock

**Symptom:** All PRs blocked, nobody can approve, velocity = 0

**Causes:**
- Thresholds too high
- Team understanding too low
- New team members

**Mitigation:**

```python
if prs_blocked / total_prs > 0.7:
    # Emergency: Lower thresholds temporarily
    thresholds *= 0.8
    log("Temporary threshold reduction due to gridlock")

    # Schedule team learning sessions
    schedule_team_workshops(blocked_modules)
```

### Failure Mode 2: Gaming the System

**Symptom:** Engineers memorize quiz answers without real understanding

**Detection:**

```python
# Check for suspicious patterns
if challenge_accuracy > 0.95 and incident_rate_on_module > baseline:
    flag_for_review(engineer, module)
    log("High quiz accuracy but high incidents - possible gaming")
```

**Mitigation:**

- Randomize challenge variants
- Include practical debugging (can't fake)
- Correlation checks (understanding should predict incident reduction)

### Failure Mode 3: Knowledge Hoarding

**Symptom:** Experts gatekeep, don't share knowledge

**Detection:**

```python
# Check if expert is only approver for critical module
expert_count = count_experts(module, threshold=0.80)

if expert_count == 1:
    log(f"Single point of failure: {module} has only 1 expert")
```

**Mitigation:**

```python
# Require knowledge sharing
if expert_count < 2:
    block_new_features(module)
    require_pairing(expert, learner)
    incentivize_mentorship(expert)
```

### Failure Mode 4: Stale Understanding

**Symptom:** Module changed but understanding scores not updated

**Detection:**

```python
# If module changes significantly, invalidate understanding
if code_churn[module] > threshold:
    decay_understanding(module, factor=0.5)  # 50% reduction
    log(f"{module} changed significantly, understanding scores adjusted")
```

---

## Metrics and Validation

### Leading Indicators

**Metrics to track:**

```python
metrics = {
    # Coverage
    'pct_modules_above_threshold': 0.75,  # 75% of modules well-understood

    # Gating
    'pct_prs_blocked': 0.20,  # 20% blocked (healthy friction)

    # Learning activity
    'challenges_completed_per_week': 15,  # Active engagement

    # Knowledge debt
    'V_learning': 0.45,  # Total epistemic energy

    # Team coverage
    'modules_with_single_expert': 2,  # Low bus factor
}
```

### Lagging Indicators

**Outcomes to measure:**

```python
outcomes = {
    'incident_rate': 0.05,            # 5% of deploys have incidents
    'rework_rate': 0.10,              # 10% of PRs need rework
    'time_to_understand': 3.5,        # Days to reach understanding on new module
    'knowledge_debt_trend': -0.05,    # -5% per month (paying down)
}
```

### Correlation Checks

**Validate that understanding predicts outcomes:**

```python
# Understanding should negatively correlate with incidents
r_incidents = correlate(understanding, incident_rate)  # Expect r < -0.5

# Understanding should negatively correlate with rework
r_rework = correlate(understanding, rework_rate)  # Expect r < -0.4

if r_incidents > -0.3:
    log("Warning: Understanding not predictive of incidents")
    log("Check: Are challenges measuring the right things?")
```

---

## Summary

**Learning governance = understanding-gated control**

**Key mechanisms:**

1. **Approval gates** - can only approve what you understand
2. **Progressive authority** - unlock rights by demonstrating knowledge
3. **Team coverage** - critical modules need ≥2 experts
4. **Emergency overrides** - with post-incident learning
5. **Adaptive thresholds** - tune based on velocity / incidents

**Integration:**

- Learning force balances with velocity
- Synergizes with quality, coherence
- Scope adjusts based on team understanding

**Validation:**

- Track gating metrics (% blocked, learning activity)
- Measure outcomes (incident rate, rework rate)
- Correlation checks (understanding → safety)

**Tuning:**

- Adjust thresholds based on risk profile
- Adaptive based on team maturity
- Emergency escape valves for gridlock

**Philosophy:**

Learning is not aspirational. It's **structural governance**.

Authority = demonstrated understanding, not seniority.
