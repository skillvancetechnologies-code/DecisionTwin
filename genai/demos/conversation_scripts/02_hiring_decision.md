# Demo 2 — Hiring Decision

**Goal:** headcount scenario; surface payroll/ramp risk honestly.

### Turn 1
**User:** Should I hire 5 more engineers?

**simulation_result:**
```json
{
  "predicted_kpis": {"revenue_delta_pct": 2.5, "churn_delta_pct": 0.0, "growth_rate_new": 5.0},
  "risk_level": "Medium", "risk_score": 40, "confidence_score": 82,
  "risk_factors": ["payroll cost", "ramp-up time"]
}
```

**Expected copilot output (shape):**
- Restates as a hiring decision, quotes ~2.5% revenue and ~5% growth.
- Surfaces payroll cost and ramp-up time as the two risks.
- Recommends a staged hire or a checkpoint; ends with a follow-up question.
