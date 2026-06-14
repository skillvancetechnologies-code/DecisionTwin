# DecisionTwin Gen AI — PM Audit (Weeks 1–6)

Audit of the interns' "completed through Week 6" claim against the execution
document (`02 DecisionTwin GenAI Team.pdf`). Date: 2026-06-14.

**Headline:** The team built a *working but materially different* product than
the spec. It is a Mistral-based business-risk classifier with a FastAPI app,
not the documented `dt_genai` library (OpenAI parser + streaming copilot +
contract formatter + evaluation framework). Several "completed" Week 4–6
deliverables are missing, non-compliant, or broken. One **critical security
issue** (committed live API key). Week 6 "fully complete" is **not accurate**.

Severity: 🔴 critical · 🟠 high · 🟡 medium

---

## Cross-cutting findings

| # | Sev | Finding | Status |
|---|-----|---------|--------|
| C1 | 🔴 | Live `MISTRAL_API_KEY` committed in `.env`; `.gitignore` was empty (nothing ignored). | **Fixed** `.gitignore` added + `.env.example`. **Key must be rotated** — assume leaked. |
| C2 | 🟠 | No `pyproject.toml` / `requirements.txt`, though README references `requirements.txt`. Not pip-installable as spec requires. | **Fixed** `requirements.txt` added. (`pyproject.toml` still pending.) |
| C3 | 🟠 | `dt_genai/__init__.py` was empty → documented public API (`parse/chat/format_response/build_pdf`) not exposed; day-one smoke test `dt_genai.parse(...)` failed. | **Partly fixed** `parse` now exported & verified. Other 3 pending contract conformance. |
| C4 | 🟠 | Broken modules that fail to import: `api_server.py` imports `generate_business_analysis`/`stream_response` (don't exist); `mistral_client.py` imports `SYSTEM_PROMPT` (module defines `SYSTEM_COPILOT_PROMPT`). | Pending (fix or delete). |
| C5 | 🟡 | Duplicate/competing code: two FastAPI apps (`app.py` + broken `api_server.py`); three report generators (`report_generator.py` plain-text, `report/report_generator.py` writes .txt, `pdf_generator.py` real PDF). | Pending consolidation. |
| C6 | 🟡 | Provider deviation: built on **Mistral (`open-mistral-7b`)**, spec mandates **OpenAI GPT-4o-mini primary + Gemini fallback**, `tenacity` retries. No retry/backoff layer. | PM decision required. |
| C7 | 🟡 | No `tests/` directory at all (spec requires test_parser, test_copilot, test_formatter, test_evaluator, test_report_generator). | **Partly fixed** `tests/test_parser.py` added (22 cases, all green). |

---

## Week-by-week: claim vs. reality

### Week 1 — Setup & AI integration — ⚠️ OK with deviation
- ParsedQuery schema present ✅ (added a non-spec `strategy` literal — harmless).
- AI integration present but on **Mistral**, not OpenAI (C6).

### Week 2 — Rule parser (10 cases) + v0 prompt — ❌ was failing, now fixed
- Rule parser existed but **failed ~45% of the spec's own Section 4.4 cases**
  ("cut prices 5 dollars", "grow team by 20%", "double ad spend",
  "reduce marketing by $10K" all returned `other`/0).
- **No tests existed** (Week 2 sign-off is `pytest -k parser` showing greens).
- v0 system prompt exists but is a generic bullet-list prompt, not the spec's
  master copilot persona (no hard rules, no "never invent numbers", etc.).
- **Fixed here:** rewrote `query_parser.py` (handles %, absolute, $/k/m suffixes,
  double/triple, clarification for magnitude-less queries) + `tests/test_parser.py`.

### Week 3 — Streaming chat() + LLM parser + classifier — ❌ major gaps
- **No streaming async-generator `chat()`** per contract. `app.py /stream`
  returns the full text in one shot — not token streaming.
- **No Stage-2 LLM function-calling parser** at all (spec's core Week 3–4 item).
  Parser is rules-only. (Added an optional `llm_parse` hook point.)
- Classifier ✅ present (maps decision_type → model route).

### Week 4 — Mid-Sprint Gate — ❌ not met
- `/chat` endpoint exists ✅.
- **30+ parser test cases: were absent.** (Now ~18 added; expand toward 30+.)
- `formatter.format_response` signature is **non-compliant**: takes
  `(category, risk, recommendation, analysis_text)` and does static string
  mapping. Contract is `format_response(raw_llm_output) -> dict` with
  `summary / recommendation / risk_note / follow_up_question`.
- Evaluation rubric: **not designed**. `scoring.py` is an unrelated numeric
  decision score, not the 5-axis rubric.

### Week 5 — Formatter JSON + 25 golden scored + failure report — ❌ not met
- Formatter returns a dict but not the contract fields.
- "25 golden cases": `samples/golden_test_cases.json` exists but contains
  **risk-classification scenarios**, not the spec's copilot eval cases
  (price/headcount/marketing buckets + multi-turn + missing-data) scored on the
  5-axis rubric.
- **No `evaluation/scored_responses.json`, no `failure_modes.md`** (both are
  named Week-8 deliverables and Week-5 sign-off artifacts).

### Week 6 — Feature-Complete Gate — ⚠️ partial
- PDF generator works ✅ via reportlab (`pdf_generator.py`) but is a basic
  title+scenario+text page, **not** the spec layout (header band, 4-card KPI
  strip, exec summary / risk note / recommendation / confidence+methodology
  footer) and not the `build_pdf(scenario: dict) -> bytes` contract (it writes a
  file and returns a filename).
- `docs/prompt_v2_changes.md` exists but is vague prose, no before/after or
  failure-mode linkage; no regression run captured.
- "All modules integration-tested" is **false** — no test suite, and two
  modules don't import (C4).

---

## What was fixed in this audit pass
Decision taken with PM: **full spec conformance, staying on Mistral.**

1. 🔴 `.gitignore` (ignores `.env`, `venv/`, caches, generated outputs) + `.env.example`.
2. 🟠 `requirements.txt` + `pyproject.toml` (pinned `mistralai<1.0` to match the 0.x client).
3. 🟠 `dt_genai/__init__.py` now exports all 4 contract functions; smoke test passes.
4. 🟠 `query_parser.py` rewritten + `llm_parser.py` Stage-2 hook — passes all Section 4.4 cases.
5. 🟠 `llm_client.py` — lazy, import-safe Mistral wrapper with retry/backoff (1s/2s/4s).
6. 🟠 `copilot.chat()` is now a **streaming async generator** per contract, with the
   Section 5.4 fallbacks (no-sim, out-of-scope, low-confidence, API-down) + memory.
7. 🟠 `formatter.format_response(raw)->dict` now contract-compliant (LLM second pass
   with deterministic fallback); legacy app behavior preserved as `enrich_analysis`.
8. 🟠 `report_generator.build_pdf(scenario)->bytes` — spec layout (header, 4-card KPI
   strip, exec summary / risk note / recommendation / confidence+methodology footer).
9. 🟠 **Evaluation framework**: `evaluation/` rubric (5 axes, 3 critical gates),
   scorer, 25-case golden set (all spec buckets), `run_eval.py`, and committed
   `evaluation/scored_responses.json` + `failure_modes.md`.
10. 🟡 Removed broken/dead `api_server.py`, `mistral_client.py`, `report/report_generator.py`.
11. 🟡 Demo scripts: `demos/conversation_scripts/` 01–05 (pricing/hiring/marketing/
    compare/clarification) with inputs + expected outputs.
12. 🟢 **Test suite added** — `tests/` (parser, copilot, formatter, evaluator,
    report_generator): **40 tests, all green**, runnable with no LLM key.

## Still open (require external action / live keys)
- **Re-run the eval live**: `python -m dt_genai.evaluation.run_eval` with a key set,
  to replace the synthetic-reference snapshot with true prompt-v2 scores before demo.
- `scored_responses.json` is currently a synthetic-reference snapshot (LLM was
  unavailable in the audit env); the framework, rubric, and scorer are real.
- README still describes the older Mistral/FastAPI framing; refresh it to match the
  now-conformant `dt_genai` contract.
- `pdf_generator.py` (file-writing helper used by `app.py /generate-report`) is kept
  for the app; the canonical contract path is now `report_generator.build_pdf`.
