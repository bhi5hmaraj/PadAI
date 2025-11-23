# System Dynamics View: Yamaha Showroom

## Overview

**System dynamics** (Sterman, "Business Dynamics") models systems as:
- **Stocks** - accumulations (inventory, customers, cash)
- **Flows** - rates of change (sales, orders, payments)
- **Feedback loops** - circular causality that drives behavior

This document maps the Yamaha showroom as a system dynamics model.

---

## Stock-and-Flow Structure

### Stock 1: Inventory

**Physical inventory on hand:**

```
        New Shipments
              ↓
         [Inventory]
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
  Sales             Returns
    ↓                   ↑
[Customers]      [Inventory]
```

**Sub-categories:**

```python
inventory = {
    'bikes': {
        'model_X': units,
        'model_Y': units,
        # ... per model
    },
    'spare_parts': {
        'part_A': units,
        # ...
    },
    'accessories': {
        'helmets': units,
        'locks': units,
        # ...
    }
}
```

**Key metrics:**
- Inventory level (units)
- Capital tied up (₹)
- Days of inventory (inventory / avg daily sales)
- Stockout frequency (% of days with zero stock)

**Governing equation:**

```
d(Inventory)/dt = New_Shipments - Sales - Obsolescence + Returns
```

---

### Stock 2: Customers

**Customer lifecycle stages:**

```
      Marketing
         ↓
     [Leads] ──→ Drop-off
         ↓
    [Pipeline] ──→ Drop-off
         ↓
   [Purchasers]
         ↓
  [Service Customers] ──→ Churn
         ↓
    [Loyalists] ──→ Referrals → [Leads]
```

**Flow rates:**

```python
# Lead generation
leads_per_day = walk_ins + referrals + advertising_response

# Conversion
pipeline_conversion_rate = 0.30  # 30% of leads enter sales process
purchase_conversion_rate = 0.40  # 40% of pipeline converts to purchase

# Retention
first_service_capture_rate = 0.60  # 60% return for 1st service
loyalist_conversion_rate = 0.30    # 30% of service customers become loyalists

# Referrals
referral_rate_per_loyalist = 0.5 / year  # 0.5 referrals per year per loyalist
```

**Governing equations:**

```
d(Leads)/dt = marketing_efforts + referrals - pipeline_entries - lead_dropoff

d(Pipeline)/dt = pipeline_entries - purchases - pipeline_dropoff

d(Purchasers)/dt = purchases - churn

d(Service_Customers)/dt = first_service_captures - service_churn

d(Loyalists)/dt = service_customer_conversions - loyalist_churn
```

---

### Stock 3: Cash

**Cash flow structure:**

```
      Sales Revenue
            ↓
    [Cash / Working Capital]
            ↓
    ┌───────┴───────┬──────────┬───────────┐
    ↓               ↓          ↓           ↓
Inventory     Salaries    Rent/Utils   Software
Purchases                              Development
```

**Inflows:**
- Sales revenue (bikes, parts, accessories)
- Service revenue (maintenance, repairs)

**Outflows:**
- Inventory purchases (bikes, parts from Yamaha)
- Fixed costs (salaries, rent, utilities)
- Variable costs (commissions, marketing)
- Software development (if outsourced, or opportunity cost if built in-house)

**Governing equation:**

```
d(Cash)/dt = Revenue_Inflows - Cost_Outflows

Where:
  Revenue = Bike_Sales + Parts_Sales + Service_Revenue
  Costs = COGS + Salaries + Rent + Marketing + Software
```

**Key constraint:**

```
Cash >= 0  (cannot go negative)

If Cash < Minimum_Working_Capital:
  → Reduce inventory orders
  → Delay discretionary spending (marketing, software)
  → Risk: Stockouts, lost sales, death spiral
```

---

### Stock 4: Staff & Knowledge

**Staff count:**

```
[Sales Team] - hires/quits → Staff count
[Mechanics]  - hires/quits → Staff count
[Manager]    - you/family
```

**Staff knowledge (intangible stock):**

```
[Product Knowledge]
  ↑
  │ Learning (training, experience)
  │
  └── Decay (turnover, forgetting)

[Customer Relationship Knowledge]
  ↑
  │ Interactions (sales, service)
  │
  └── Decay (staff turnover, customer churn)

[Analytics Understanding]  ← KEY FOR SOFTWARE VALUE
  ↑
  │ Active learning (challenges, prediction)
  │
  └── Decay (disuse, complexity growth)
```

**Governing equation:**

```
d(Knowledge)/dt = Learning_Rate - Decay_Rate - Loss_from_Turnover

# Example: Analytics understanding
d(Analytics_Understanding)/dt =
    Active_Learning_Effort -
    Natural_Decay × Current_Understanding -
    Staff_Turnover_Rate × Avg_Understanding
```

---

### Stock 5: Software System

**Software as a stock (accumulation of features):**

```
    Requirements
         ↓
   [Features Deployed]
         ↑
    Development
         ↓
   (Also accumulates)
         ↓
  [Technical Debt]
```

**Governing equations:**

```
d(Features)/dt = Development_Rate

d(Technical_Debt)/dt =
    New_Debt_from_Features -
    Refactoring_Effort

# Software physics applies here
H_software = T + V_struct + V_bus + V_learning
```

---

## Feedback Loops

### Loop 1: Inventory-Sales Balance (Balancing)

```
Inventory Low
  ↓
Order More (with delay)
  ↓
Inventory Rises
  ↓
Sales Pressure Drops (already have stock)
  ↓
Inventory Accumulates
  ↓
Cash Tied Up
  ↓
Reduce Orders
  ↓
Inventory Low (loop closes)
```

**Behavior:** Oscillates around target inventory level.

**Delays:**
- Order → Delivery: 2-4 weeks
- Recognition → Decision: 1-3 days
- Decision → Order: 1 day

**Total delay:** ~3-5 weeks (can cause overshoot/undershoot)

**Governance:**
- Target inventory = f(avg daily sales, lead time, stockout cost)
- Analytics can reduce overshoot by better demand forecasting

---

### Loop 2: Customer Acquisition (Reinforcing)

```
Good Service
  ↓
Customer Satisfaction
  ↓
Loyalists Grow
  ↓
More Referrals
  ↓
More Leads
  ↓
More Sales
  ↓
More Revenue
  ↓
Can Hire Better Staff
  ↓
Good Service (loop closes - VIRTUOUS)
```

**Behavior:** Exponential growth until market saturation.

**Limits:**
- Market size (only so many people need bikes)
- Staff capacity (can only handle N customers per day)
- Competition (other dealers)

**Governance:**
- Invest in service quality (long-term compounding)
- Track customer lifetime value (CLV)
- Analytics: Predict which customers become loyalists (focus effort there)

---

### Loop 3: Analytics Value Creation (Reinforcing or Balancing)

**Virtuous cycle:**

```
Analytics Deployed
  ↓
Family Uses It (IF they understand)
  ↓
Better Decisions
  ↓
Business Grows
  ↓
More Data
  ↓
Better Analytics
  ↓
(Loop closes - REINFORCING)
```

**Death spiral:**

```
Analytics Deployed
  ↓
Family Doesn't Understand (black box)
  ↓
Bad Decisions (misuse)
  ↓
Business Suffers
  ↓
Blame Analytics
  ↓
Stop Using
  ↓
No Data
  ↓
Analytics Becomes Stale/Irrelevant
  ↓
(Loop closes - BALANCING, degenerative)
```

**Critical variable:** Family understanding (learning force!)

**Governance:**
- Active learning BEFORE deploying analytics
- Start with simple, transparent features (build trust)
- Prediction challenges (test understanding before decisions)

---

### Loop 4: AI Agent Trust (Reinforcing or Balancing)

**Virtuous cycle:**

```
AI Agent Gives Good Recommendations
  ↓
Family Accepts Them
  ↓
Good Outcomes
  ↓
Trust Grows
  ↓
More Usage of AI
  ↓
More Data for Training
  ↓
Better Recommendations
  ↓
(Loop closes - REINFORCING)
```

**Death spiral:**

```
AI Agent Gives Bad Recommendations (or good but misunderstood)
  ↓
Family Rejects Them
  ↓
Manual Override
  ↓
Trust Erodes
  ↓
Less Usage
  ↓
Less Training Data
  ↓
Worse Recommendations
  ↓
(Loop closes - BALANCING, degenerative)
```

**Governance:**
- Transparency (explain WHY AI recommends X)
- Human-in-the-loop (AI suggests, human decides)
- Override tracking (learn from disagreements)

---

### Loop 5: Cash Flow Crisis (Balancing, Dangerous)

```
Low Cash
  ↓
Delay Inventory Orders
  ↓
Stockouts
  ↓
Lost Sales
  ↓
Even Lower Cash
  ↓
Cannot Pay Salaries
  ↓
Staff Quits
  ↓
Service Quality Drops
  ↓
Customer Churn
  ↓
Lost Sales
  ↓
(Death spiral)
```

**This is a BALANCING loop that drives system to zero** (business failure).

**Prevention:**
- Maintain cash buffer (3-6 months working capital)
- Monitor cash flow weekly (not monthly)
- Analytics: Cash flow forecast (predict crises 1-2 months ahead)

---

## Delays in the System

**Sterman's key insight:** Delays cause oscillation and instability.

### Delay 1: Order → Delivery

**Length:** 2-4 weeks (Yamaha shipment)

**Effect:**
- Can't respond quickly to demand surge
- Risk of stockout OR overstock (if demand changes during delay)

**Mitigation:**
- Safety stock (buffer inventory)
- Better demand forecasting (analytics)

---

### Delay 2: Problem → Recognition

**Length:** Days to weeks

**Example:** Sales dropping, but family doesn't notice until month-end report.

**Effect:**
- Late response, problem worsens

**Mitigation:**
- Real-time dashboards (daily sales tracking)
- Alerts (if sales < threshold, notify immediately)

---

### Delay 3: Software Development → Deployment

**Length:** Weeks to months

**Effect:**
- Business need → software solution takes time
- By the time feature is deployed, business may have changed

**Mitigation:**
- Start simple (MVP)
- Iterative development (ship small features fast)

---

### Delay 4: Deployment → Adoption

**Length:** Weeks to months (LONGEST DELAY)

**Example:**
- Week 1: Deploy analytics
- Week 2-4: Family learning to use it
- Week 5-8: Family building trust
- Week 9+: Regular usage

**Effect:**
- ROI delayed significantly
- Risk: Family gives up before seeing value

**Mitigation:**
- Active learning (reduce learning time)
- Quick wins (show value in week 1)
- Ongoing support (not just "here's the tool, good luck")

---

### Delay 5: Action → Business Impact

**Length:** Weeks to months

**Example:**
- Improve service reminder campaign
- Takes 3-6 months to see impact on retention

**Effect:**
- Hard to attribute causality (was it the reminders? Or something else?)
- Impatience (family expects immediate results)

**Mitigation:**
- Set expectations (explain delays upfront)
- Leading indicators (track intermediate metrics: reminder open rate, appointment bookings)
- A/B testing (isolate causal effect)

---

## Leverage Points (Where to Intervene)

**Sterman's hierarchy of leverage (low to high):**

### Low Leverage: Parameters

**Example:** Change discount from 10% → 15%

**Effect:** Small, linear impact

**When to use:** Fine-tuning existing processes

---

### Medium Leverage: Buffers/Stocks

**Example:** Increase cash buffer from 1 month → 3 months

**Effect:** Resilience against shocks

**When to use:** Reduce vulnerability to delays, variability

---

### Medium-High Leverage: Delays

**Example:** Reduce order → delivery delay from 4 weeks → 2 weeks

**Effect:** Faster response, less oscillation

**When to use:** System is oscillating or unstable

---

### High Leverage: Feedback Loop Strength

**Example:** Improve referral rate (loyalists → new leads)

**Effect:** Amplifies over time (compounding)

**When to use:** Long-term growth (but watch for limits)

---

### Highest Leverage: Mental Models

**Example:** Change family's belief from "More inventory = More sales" to "Right inventory at right time = More sales"

**Effect:** Changes all decisions downstream

**When to use:** Fundamental misunderstanding causing persistent problems

**This is where active learning has massive leverage.**

---

## Software & AI Impact on System Dynamics

### Software as Flow Accelerator

**Analytics can:**

1. **Speed up flows:**
   - Lead → Pipeline (better lead scoring)
   - Pipeline → Purchase (personalized sales approach)

2. **Reduce delays:**
   - Faster problem recognition (real-time dashboards)
   - Faster decision-making (data at hand, not manual lookup)

3. **Improve conversion rates:**
   - Better targeting (customer segmentation)
   - Better timing (reminder campaigns)

### AI Agents as Autonomous Actors

**AI can:**

1. **Automate flows:**
   - Auto-send service reminders (no human intervention)
   - Auto-order inventory (when below threshold)

2. **Optimize policies:**
   - Dynamic pricing (adjust based on demand, inventory)
   - Smart scheduling (maximize mechanic utilization)

3. **Augment decisions:**
   - Recommend which leads to prioritize
   - Predict which customers will churn (proactive retention)

**BUT: AI is also a stock with its own dynamics:**

```
d(AI_Capability)/dt = Training_Data + Algorithm_Improvements - Model_Decay

Where:
  Training_Data ∝ Business_Activity × Data_Collection_Rate
  Model_Decay = drift as business changes
```

---

## Model Calibration: What to Measure

**To validate this model, measure:**

### Stock levels (weekly)

```python
inventory_count = { 'model_X': units, ... }
customer_counts = {
    'leads': count,
    'pipeline': count,
    'purchasers': count,
    'service_customers': count,
    'loyalists': count
}
cash_balance = ₹
staff_count = people
```

### Flow rates (weekly)

```python
flows = {
    'new_leads': count / week,
    'pipeline_entries': count / week,
    'sales': count / week,
    'first_service_captures': count / week,
    'referrals': count / week,
    'revenue': ₹ / week,
    'costs': ₹ / week,
}
```

### Delays (one-time measurement)

```python
delays = {
    'order_to_delivery': days,
    'lead_to_purchase': days,
    'problem_to_recognition': days,
    'feature_request_to_deployment': days,
    'deployment_to_adoption': days,
}
```

### Feedback loop strengths (correlation)

```python
# Measure correlations
correlation(service_quality, customer_retention)
correlation(analytics_usage, decision_quality)
correlation(AI_recommendation_acceptance, business_outcomes)
```

---

## Summary

**System dynamics view provides:**

1. **Structure:** Stocks, flows, feedback loops
2. **Delays:** Recognition → decision → action → impact
3. **Leverage points:** Where to intervene for maximum effect
4. **Feedback dominance:** Small changes amplify over time

**Key insights for software + AI:**

- Software/AI impact depends on **understanding** (learning force)
- Delays mean **quick wins** are crucial (build trust before impact materializes)
- **Feedback loops** dominate (virtuous cycles or death spirals)
- **Mental models** are highest leverage (active learning targets this)

**Next:** See `02-nested-systems.md` for how software physics sits within this business model.
