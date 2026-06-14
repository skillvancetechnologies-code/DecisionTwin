# Demo 3 — Marketing Cut

**Goal:** a cost-cutting scenario where the downside dominates.

### Turn 1
**User:** Cut marketing by 50%.

**simulation_result:**
```json
{
  "predicted_kpis": {"revenue_delta_pct": -9.0, "churn_delta_pct": 3.0, "growth_rate_new": -11.0},
  "risk_level": "High", "risk_score": 75, "confidence_score": 70,
  "risk_factors": ["lead-gen collapse", "brand decay"]
}
```

**Expected copilot output (shape):**
- Quotes the ~9% revenue drop and ~11% growth decline plainly.
- Names lead-gen collapse and brand decay as the risks.
- Recommends caution / a smaller cut; ends with a follow-up question.
