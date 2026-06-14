# Demo 4 — Compare Three Scenarios

**Goal:** show multi-turn memory + the comparison story for the dashboard/PDF.

### Setup
Three saved scenarios are passed in turn:
1. Raise prices 10% — revenue +6.8%, churn +2.1%, risk Medium (54).
2. Add 10 sales reps — revenue +8.0%, churn -0.5%, risk Medium (45).
3. Increase marketing 30% — revenue +5.5%, churn -1.0%, risk Medium (44).

### Turn 1
**User:** Which of these three is the safest way to grow revenue?

**Expected copilot output (shape):**
- References all three by their numbers (no invented figures).
- Calls out that adding sales reps has the highest revenue lift with the lowest
  risk score, while the price rise carries the most churn.
- Gives a single recommendation and a follow-up question.
- `format_response` on this answer should yield a one-line `recommendation`
  suitable for the ComparisonTable tooltip and the PDF.
