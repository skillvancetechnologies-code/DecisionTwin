# Demo 5 — Clarification / Fallback

**Goal:** show graceful handling of vague, missing-data, and out-of-scope input.

### Turn 1 — vague (parser low confidence)
**User:** Bump prices a little.

**Expected:** `parse()` returns `decision_type=price_change` with low confidence
(< 0.5). Copilot asks the user to specify a concrete magnitude
("e.g. raise prices by X%") rather than guessing.

### Turn 2 — no simulation yet
**User:** So is that a good idea?  (simulation_result = None)

**Expected (Section 5.4):** "I need a fresh simulation to answer that. Could you
rephrase as a specific change — e.g. raise prices by X% — so I can run the model?"

### Turn 3 — out of scope
**User:** How do I calculate IRR?

**Expected:** polite redirect — "I'm focused on simulating business decisions...
I can help you simulate pricing, hiring, or marketing changes." No invented numbers.

### Turn 4 — low-confidence simulation
**User:** Raise prices by 10%.  (confidence_score = 42)

**Expected:** copilot begins with a directional-not-precise caveat before the analysis.
