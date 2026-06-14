# Demo 1 — Pricing Decision

**Goal:** show the copilot turning a price-change simulation into plain English.

### Turn 1
**User:** What if I raise prices by 10%?

**simulation_result:**
```json
{
  "predicted_kpis": {"revenue_delta_pct": 6.8, "churn_delta_pct": 2.1, "growth_rate_new": 4.5},
  "risk_level": "Medium", "risk_score": 54, "confidence_score": 80,
  "risk_factors": ["churn risk", "competitor response"]
}
```

**Expected copilot output (shape):**
- Paragraph 1 quotes ~6.8% revenue and ~2.1% churn in plain English.
- Paragraph 2 names churn risk and competitor response.
- Paragraph 3 gives one concrete next step; ends with a follow-up question.
- No invented numbers; under 300 words; no bullet points.

### Turn 2
**User:** What if I only raise by 5% instead?

**simulation_result:** `revenue_delta_pct 3.4, churn_delta_pct 1.2, confidence 84`

**Expected:** copilot references the prior turn, compares to the 10% case, recommends the lower-risk option.
