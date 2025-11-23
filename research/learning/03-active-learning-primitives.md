# Active Learning Primitives

## Overview

**Active learning** means learning by doing, not by reading.

Traditional approach:
```
Read docs → Hope you understood → Apply → Discover gaps (when things break)
```

Active learning approach:
```
Predict → Act → Observe outcome → Update mental model → Repeat
```

This document defines the specific learning mechanisms ("primitives") that reduce epistemic gaps.

---

## Primitive 1: Active Prediction

### Concept

**Before** running/changing code, user **predicts** what will happen.

**After** observing the outcome, user updates their mental model.

### Why It Works (Learning Science)

1. **Retrieval practice** - forces user to recall their model
2. **Prediction error** - differences between prediction and reality highlight gaps
3. **Immediate feedback** - tight loop between action and correction

**Research backing:** Math Academy, cognitive science (Roediger & Butler, 2011)

### Implementation

**Flow:**

```
1. System presents scenario:
   "We're about to change function X. What will break?"

2. User predicts:
   [ ] Test A will fail
   [ ] Test B will fail
   [ ] Module Y will need updates
   [ ] No failures expected

3. System runs the change

4. System shows actual outcome:
   "Test A: ✗ Failed (you predicted this ✓)"
   "Test B: ✓ Passed (you predicted failure ✗)"
   "Module Y: ✓ No changes needed (you predicted changes ✗)"

5. System prompts reflection:
   "You missed that Test B would pass. Why?"
   "Update your mental model: Test B only depends on function Z, not X."
```

**Scoring:**

```python
prediction_accuracy = (correct_predictions + correct_non_predictions) / total_items

# Adjust understanding score
understanding[module] = 0.7 * understanding[module] + 0.3 * prediction_accuracy
```

### Example Scenarios

**Scenario A: Dependency change**

```
Prompt: "We're removing the dependency from A → B. Predict impact:"

Options:
  [ ] Tests in A will fail
  [ ] Tests in B will fail
  [ ] Tests in C (which depends on A) will fail
  [ ] No failures

Correct answer: C will fail (transitive dependency)
```

**Scenario B: Refactor**

```
Prompt: "We're extracting function foo() into a new module. What changes are needed?"

User predicts:
  - Import statements in 3 files
  - Update 2 test files

System shows actual:
  - Import statements in 5 files (user missed 2)
  - Update 2 test files (correct)

Feedback: "You missed imports in auth.py and utils.py. Why?"
```

### When to Trigger

**Trigger prediction challenges:**

1. **Before risky changes**
   - High-complexity module
   - Low understanding score
   - Critical path

2. **Periodically for key modules**
   - Once per week for critical modules
   - Spaced retrieval schedule

3. **After incidents**
   - "What should we have predicted?"
   - Post-mortem learning

---

## Primitive 2: Comprehension Sampling

### Concept

**Random quizzes** on codebase, testing factual recall and causal understanding.

**Not** testing "did you read the docs?" but "do you have an accurate mental model?"

### Why It Works

1. **Spaced repetition** - distributed practice beats cramming
2. **Testing effect** - retrieval strengthens memory more than re-reading
3. **Metacognition** - reveals what you don't know

### Implementation

**Quiz types:**

**Type 1: Factual recall**

```
Q: "Which modules depend on database.py?"
A: (multiple choice)
  [ ] auth, users
  [ ] auth, users, payments
  [ ] auth, payments, reports
  [ ] users, payments
```

**Type 2: Causal reasoning**

```
Q: "If database.py connection pool is exhausted, what happens?"
A: (open-ended or multiple choice)
  [ ] API requests timeout after 30s
  [ ] Server crashes
  [ ] Requests queue indefinitely
  [ ] Fallback to SQLite
```

**Type 3: Debugging**

```
Scenario: "Test X is failing with error Y. What's the most likely cause?"

Options:
  [ ] Missing environment variable
  [ ] Database migration not run
  [ ] Network timeout
  [ ] Logic bug in function foo()

Follow-up: "How would you fix it?"
```

### Sampling Strategy

**Where to sample:**

```python
# Weighted sampling by importance
sample_probability[module] = importance[module] / sum(importance)

# Sample more frequently from:
# - High-importance modules
# - Modules with low understanding
# - Recently changed modules
```

**When to sample:**

```python
# Daily active learning session
# - 5-10 minutes per day
# - 3-5 questions
# - Immediate feedback

# Or trigger on events:
# - Before approving a PR touching module X → quiz on X
# - After 2 weeks without touching module Y → refresh quiz on Y
```

### Scoring and Feedback

**Immediate feedback:**

```
Q: "Which function handles user logout?"
Your answer: handle_logout()
Correct answer: logout_user()

Explanation:
  handle_logout() is deprecated as of v2.3.
  New code should use logout_user().
  See: auth/session.py:145
```

**Understanding update:**

```python
if answer_correct:
    understanding[module] += 0.05  # Small boost
else:
    understanding[module] -= 0.10  # Larger penalty for wrong answer
    flag_for_remediation(module)
```

---

## Primitive 3: Experimental Sandbox

### Concept

**Safe practice environment** where users can:

- Break things deliberately
- Predict failures
- Debug
- Learn without production risk

### Why It Works

1. **Deliberate practice** - focused, challenging work at edge of ability
2. **Safe failure** - learn from mistakes without consequences
3. **Immediate feedback** - see what broke and why

### Implementation

**Sandbox features:**

1. **Isolated environment**
   - Copy of codebase (or subset)
   - Test database, mock services
   - Fast reset (< 5 seconds)

2. **Scenario library**
   - Pre-built exercises
   - "Introduce a bug in module X, debug it"
   - "Refactor function Y without breaking tests"
   - "Optimize query Z for performance"

3. **Challenge ladder**
   - Beginner: simple recall, read code
   - Intermediate: predict behavior, explain why
   - Advanced: debug failing tests, refactor safely

**Example exercise:**

```
Challenge: "Introduce a race condition in payment.py"

Steps:
1. Read payment.py
2. Identify where race condition could occur
3. Write a test that triggers it
4. Verify test fails (race condition exists)
5. Fix the code
6. Verify test passes

Scoring:
  - Correct identification: +10 points
  - Test triggers race condition: +10 points
  - Fix is correct: +10 points
  - Time bonus: +5 if < 15 minutes
```

### Integration with Understanding Scores

**Sandbox exercises count toward understanding:**

```python
understanding[module] = weighted_average([
    0.4 * quiz_accuracy,
    0.4 * prediction_accuracy,
    0.2 * sandbox_performance
])
```

**Progressive unlock:**

```
understanding < 0.4: Beginner exercises only
understanding 0.4-0.7: Intermediate exercises
understanding > 0.7: Advanced exercises + can mentor others
```

---

## Primitive 4: Knowledge Gap Tracking

### Concept

**Explicit tracking** of what each person understands, per module.

### Why It Works

1. **Visibility** - makes ignorance visible, not shameful
2. **Targeted learning** - focus effort where gaps are largest
3. **Governance** - gate decisions on demonstrated understanding

### Data Model

```python
knowledge_graph = {
    'engineer_id': {
        'module_id': {
            'understanding_score': 0.75,
            'last_updated': '2025-11-22',
            'challenges_completed': 15,
            'challenges_passed': 12,
            'decay_rate': 0.05,  # 5% per day
        },
    },
}
```

### Visualization

**Per-engineer heatmap:**

```
           Module A  Module B  Module C  Module D
Engineer 1   0.85      0.60      0.40      0.90
Engineer 2   0.50      0.90      0.70      0.30
Engineer 3   0.75      0.75      0.80      0.60

Color scale: Red (0.0) → Yellow (0.5) → Green (1.0)
```

**Insights:**

- Engineer 1: Strong on A and D, weak on C
- Engineer 2: Strong on B, weak on D
- Module C: Team average 0.63 (needs collective learning)

### Gap-Driven Learning

**Prioritize learning based on gaps:**

```python
def next_learning_task(engineer_id):
    gaps = compute_gaps(engineer_id)

    # Sort by: gap × importance
    priorities = sorted(
        gaps,
        key=lambda m: (1 - understanding[m]) × importance[m],
        reverse=True
    )

    return priorities[0]  # Highest-priority gap
```

---

## Primitive 5: Understanding-Gated Control

### Concept

**Authority is earned through demonstrated understanding.**

You can only approve/modify code you understand.

### Why It Works

1. **Accountability** - decisions made with knowledge, not guesswork
2. **Incentive alignment** - learning is now economically valuable (unlocks agency)
3. **Safety** - prevents uninformed changes

### Implementation

**Approval gates:**

```python
def can_approve(engineer_id, module_id):
    understanding = get_understanding(engineer_id, module_id)
    threshold = get_threshold(module_id)  # Higher for critical modules

    if understanding >= threshold:
        return True, "Approved: sufficient understanding"
    else:
        gap = threshold - understanding
        return False, f"Blocked: need {gap:.0%} more understanding. Complete challenges."
```

**Example thresholds:**

```
Critical modules (payment, auth): 80%
Normal modules (features, utils): 60%
Low-risk modules (docs, config): 30%
```

### Earning Understanding

**How to unlock approval rights:**

1. **Complete comprehension challenges**
   - Pass 10 quizzes on module X → unlock

2. **Pair with expert**
   - Work with someone who has high understanding
   - They vouch for your knowledge

3. **Demonstrate in sandbox**
   - Complete advanced exercises
   - Show you can debug, refactor, predict

### Progressive Authority

**Levels of control:**

```
Understanding 0-30%: Read-only
Understanding 30-60%: Can submit PRs (but not approve own)
Understanding 60-80%: Can approve others' PRs
Understanding 80-100%: Can approve own PRs, mentor others
```

**Effect:**

- Learning becomes **structurally necessary**, not optional
- Engineers invest time in understanding because it unlocks agency
- System naturally balances velocity (ship fast) with safety (informed decisions)

---

## Primitive 6: Adaptive Learning Dial

### Concept

**Auto-tune learning intensity** based on:

1. User behavior (skipping challenges)
2. Accuracy (passing/failing)
3. System state (cycle time, incidents)

### Why It Works

1. **Efficiency** - don't over-burden if understanding is high
2. **Responsiveness** - increase learning if gaps cause problems
3. **Engagement** - reduce learning if user burnout

### Tuning Algorithm

**Inputs:**

```python
skip_rate = challenges_skipped / challenges_presented
accuracy = challenges_correct / challenges_attempted
cycle_time = current_cycle_time / baseline_cycle_time
incident_rate = current_incidents / baseline_incidents
```

**Tuning rules:**

```python
def adjust_learning_intensity(metrics):
    intensity = 1.0  # Baseline

    # Reduce if user is skipping
    if metrics['skip_rate'] > 0.8:
        intensity *= 0.7  # 30% reduction

    # Reduce if cycle time too long
    if metrics['cycle_time'] > 2.0:
        intensity *= 0.8

    # Increase if accuracy is low
    if metrics['accuracy'] < 0.5:
        intensity *= 1.3

    # Increase if incidents are high
    if metrics['incident_rate'] > 1.5:
        intensity *= 1.5

    return np.clip(intensity, 0.3, 2.0)  # Bound to [0.3, 2.0]
```

**Effect on behavior:**

```
High intensity (2.0):
  - 50% of changes trigger challenges
  - Higher difficulty
  - Stricter gates

Low intensity (0.3):
  - 5% of changes trigger challenges
  - Easier challenges
  - Looser gates
```

### Feedback Loop

**Closed-loop control:**

```
1. Measure current state (understanding, incidents, cycle time)
2. Compute desired learning intensity
3. Apply intensity → adjust challenge frequency, difficulty, gates
4. Observe outcomes → update metrics
5. Repeat
```

**Goal:** Maintain equilibrium where:

- Understanding scores stay above threshold
- Incident rate is low
- Cycle time is acceptable
- User engagement is high (not skipping)

---

## Combining Primitives

**How they work together:**

1. **Prediction** + **Comprehension Sampling** → measure understanding
2. **Sandbox** → deliberate practice to raise understanding
3. **Gap Tracking** → visibility into who knows what
4. **Understanding-Gated Control** → incentivize learning
5. **Adaptive Dial** → auto-tune intensity for efficiency

**Example workflow:**

```
Engineer Alice wants to modify payment.py

Step 1: Check understanding
  Alice's score on payment.py: 45%
  Required threshold: 80%
  Gap: 35%

Step 2: Blocked, trigger learning
  System: "Complete 5 challenges to unlock approval"

Step 3: Active learning
  - Prediction: "If we change refund logic, what breaks?"
  - Quiz: "Which function handles partial refunds?"
  - Sandbox: "Debug the failing test in payment_test.py"

Step 4: Measure progress
  After completing challenges: 75%
  Still below threshold, need 1 more challenge

Step 5: Final challenge (harder)
  Advanced debugging scenario
  Pass → understanding = 82%

Step 6: Gate opens
  Alice can now approve changes to payment.py
```

---

## Measurement and Validation

**How to test if these primitives work:**

### Experiment: A/B Test

**Control group:** No active learning, traditional code review

**Treatment group:** Active learning primitives enabled

**Measure:**

1. **Incident rate** (should decrease)
2. **Time to first incident** (should increase)
3. **Rework rate** (should decrease - fewer uninformed decisions)
4. **Understanding scores** (should increase)
5. **Cycle time** (acceptable trade-off)

**Hypothesis:**

- Treatment group has 30-50% fewer incidents
- Cycle time increases by 10-20% (acceptable)
- Understanding scores rise from 40% → 75%

### Leading Indicators

**Early signals that primitives are working:**

1. **Challenge completion rate > 70%**
   - Users engaging, not skipping

2. **Accuracy improving over time**
   - 50% → 70% → 85% (learning is effective)

3. **Knowledge debt decreasing**
   - V_learning going down

4. **High-understanding engineers correlate with low incident rates**
   - Validates understanding → safety link

---

## Summary

**Six active learning primitives:**

1. **Active Prediction** - predict before acting
2. **Comprehension Sampling** - random quizzes on codebase
3. **Experimental Sandbox** - safe practice environment
4. **Knowledge Gap Tracking** - explicit per-module understanding
5. **Understanding-Gated Control** - earn authority via demonstrated knowledge
6. **Adaptive Learning Dial** - auto-tune intensity

**Key insight:** Learning is not passive (read docs). It's active (predict, test, update model).

**Next:** See `04-understanding-metrics.md` for detailed measurement.
