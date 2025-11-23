# AI Agents as Actors in Socio-Technical Systems

## Overview

**AI agents are not just tools - they're autonomous actors** with:

- **Goals** (maximize sales, minimize inventory costs, predict churn)
- **Policies** (how they decide what to recommend)
- **Mental models** (their "understanding" of the system)
- **Actions** (recommendations, automations, alerts)
- **Learning** (adapt based on outcomes)

This document models AI agents within the showroom system dynamics and software physics framework.

---

## AI Agent Types for Yamaha Showroom

### Agent 1: Sales Assistant

**Goal:** Maximize conversion rate (leads → purchases)

**Inputs:**
- Customer data (demographics, browsing history, test drive requests)
- Inventory levels (what's in stock)
- Historical conversion patterns

**Policy:**

```python
def recommend_next_action(customer, context):
    # Score customer based on purchase likelihood
    score = predict_purchase_probability(customer)

    if score > 0.7:
        return "High-priority: Call immediately"
    elif score > 0.4:
        return "Medium-priority: Send personalized SMS"
    elif score > 0.2:
        return "Low-priority: Add to email nurture campaign"
    else:
        return "Very low: Deprioritize"
```

**Actions:**
- Prioritize leads for sales team
- Suggest personalized messaging
- Recommend which bike model to showcase

**Mental model:**
- Believes: "Customers who test drive are 3× more likely to buy"
- Believes: "Young professionals prefer sporty models"

**Learning:**
- Track recommendations vs actual outcomes
- Update model monthly (re-train on new data)

---

### Agent 2: Inventory Optimizer

**Goal:** Minimize stockouts AND minimize capital tied up

**Inputs:**
- Current inventory levels (by SKU)
- Sales velocity (units/week)
- Lead times (order → delivery)
- Cash flow constraints

**Policy:**

```python
def recommend_order(inventory, sales_velocity, lead_time, cash_available):
    # For each SKU
    for sku in inventory.keys():
        safety_stock = sales_velocity[sku] × lead_time × 1.5  # 50% buffer
        reorder_point = safety_stock + (sales_velocity[sku] × lead_time)

        current_stock = inventory[sku]

        if current_stock < reorder_point:
            order_quantity = safety_stock - current_stock

            # Check cash constraint
            order_cost = order_quantity × unit_cost[sku]
            if order_cost > cash_available:
                order_quantity = cash_available / unit_cost[sku]  # Reduce to fit budget

            return f"Order {order_quantity} units of {sku}"
```

**Actions:**
- Recommend when to order
- Recommend how much to order
- Alert when stockout risk is high

**Mental model:**
- Believes: "Safety stock should be 1.5× lead time demand"
- Believes: "Cash flow constraint is hard limit"

**Learning:**
- Track stockout frequency vs recommendations
- Adjust safety stock multiplier based on actual variability

---

### Agent 3: Service Scheduler

**Goal:** Maximize service revenue + customer retention

**Inputs:**
- Customer purchase dates
- Service history
- Service due dates (based on bike model, usage)

**Policy:**

```python
def recommend_reminder_campaign():
    # Find customers due for service
    customers_due = get_customers_with_service_due(within_days=30)

    for customer in customers_due:
        retention_risk = predict_churn_probability(customer)

        if retention_risk > 0.5:
            # High-risk: Personal call from mechanic
            return f"Call {customer.name} - high churn risk"
        else:
            # Low-risk: Automated SMS
            return f"Send SMS to {customer.name}"
```

**Actions:**
- Schedule reminder campaigns (SMS, email, call)
- Prioritize high-risk customers
- Optimize appointment slots (minimize mechanic idle time)

**Mental model:**
- Believes: "Customers who miss 1st service have 85% churn rate"
- Believes: "Personal calls convert 2× better than SMS"

**Learning:**
- Track service return rate vs reminder type
- A/B test (SMS vs call vs email)

---

### Agent 4: Analytics Copilot

**Goal:** Answer family's questions about the business

**Inputs:**
- Family's natural language question
- Historical business data (sales, inventory, customers)
- Context (what problem are they trying to solve?)

**Policy:**

```python
def answer_question(question, data):
    # Parse question
    intent = classify_intent(question)  # "segment customers", "forecast sales", etc.

    # Retrieve relevant data
    relevant_data = query_database(intent, filters)

    # Generate insight
    if intent == "segment_customers":
        segments = cluster_analysis(data['customers'])
        return f"Found 3 customer segments: {segments.summary()}"

    elif intent == "forecast_sales":
        forecast = time_series_forecast(data['sales'], horizon=3)
        return f"Expected sales next 3 months: {forecast}"

    # ... more intents
```

**Actions:**
- Answer questions ("Which customers are most profitable?")
- Generate visualizations (charts, dashboards)
- Suggest follow-up questions ("Want to see churn risk by segment?")

**Mental model:**
- Believes: "Family cares most about revenue, retention, inventory"
- Believes: "Simple charts > complex tables"

**Learning:**
- Track which questions get asked most (prioritize UX for those)
- Learn family's terminology (map "customers who come back" → "retention")

---

## AI Agent Dynamics

### Agent as Actor in System Dynamics

**AI agents participate in flows and feedback loops:**

```
[Leads]
   ↓
Sales Agent recommends prioritization
   ↓
Sales team focuses on high-score leads
   ↓
Conversion rate increases
   ↓
[Purchases]
```

**System dynamics impact:**

```python
# Baseline conversion rate
baseline_conversion = 0.30  # 30%

# With AI agent lead scoring
ai_enhanced_conversion = 0.40  # 40% (focusing effort on high-probability leads)

# Extra sales per month
extra_sales = (ai_enhanced_conversion - baseline_conversion) × leads_per_month
            = 0.10 × 200 = 20 extra sales/month
```

**AI agent amplifies the flow rate.**

---

### Agent as Software (Software Physics)

**AI agent is also a software system with its own physics:**

```python
# AI agent complexity
complexity['ai_inventory_optimizer'] = 0.7  # High (ML model, data pipeline)

# Technical debt from AI
V_struct_ai = 0.5 × complexity  # Coupling to data sources, model drift

# Understanding requirement
understanding_threshold['ai_optimizer'] = 0.8  # Must trust AI to use it
```

**Software physics impact:**

```python
# AI adds to Hamiltonian
H_total = H_software + H_ai_agents

# If AI is poorly understood, adds to epistemic debt
V_learning_ai = (1 - family_understanding['ai']) × importance['ai']
```

---

### Three-Way Dynamics: Human + AI + Business

```
Business Problem
   ↓
Human recognizes need
   ↓
AI Agent generates recommendation
   ↓
Human evaluates recommendation
   ↓
   ├─ Accept → Execute action → Business outcome
   │             ↓
   │         Feedback to AI (learn)
   │
   └─ Reject → Manual decision → Business outcome
                 ↓
             Feedback to AI (learn from disagreement)
```

**Critical loop: Trust**

```
AI gives good recommendations
  ↓
Human accepts
  ↓
Good outcomes
  ↓
Trust grows
  ↓
More usage
  ↓
More data for training
  ↓
Better recommendations (VIRTUOUS)
```

**Death spiral:**

```
AI gives bad recommendations (or good but misunderstood)
  ↓
Human rejects
  ↓
Manual override
  ↓
Trust erodes
  ↓
Less usage
  ↓
Less training data
  ↓
Worse recommendations (DEATH SPIRAL)
```

---

## AI Agent Governance

### Principle 1: Transparency (Explainable AI)

**Human must understand WHY AI recommends X.**

**Bad (black box):**

```
AI: "Order 50 units of Model X"
Human: "Why?"
AI: "My neural network says so"
Human: "...I don't trust this"
```

**Good (transparent):**

```
AI: "Order 50 units of Model X because:
  - Sales velocity = 10 units/week
  - Lead time = 4 weeks
  - Current stock = 5 units
  - Reorder point = 40 + 15 (safety stock) = 55
  - Shortfall = 55 - 5 = 50 units"