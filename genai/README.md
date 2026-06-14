# dt_genai — DecisionTwin Gen AI layer

The natural-language layer of DecisionTwin, shipped as a **pip-installable Python
library** (not a service). The Web backend imports it through
`backend/app/integrations/genai.py`. Provider: **Mistral** (`open-mistral-7b`).

## Public contract (what the backend calls)

```python
from dt_genai.query_parser import parse          # parse(text) -> ParsedQuery
from dt_genai.copilot import chat                 # async generator of str chunks
from dt_genai.formatter import format_response    # see call styles below
from dt_genai.report_generator import build_pdf   # build_pdf(scenario) -> bytes
```

- `chat(user_message, simulation_result, chat_history)` — async generator yielding
  text chunks (the backend wraps these in SSE).
- `format_response(user_message, simulation_result)` — returns a dict with
  `ai_response, summary, recommendation, risk_note` (the shape `chat_service` uses).
  Also accepts the single-arg `format_response(raw_text)` spec form.
- `build_pdf(scenario)` — accepts the backend's scenario dict
  (`name, user_query, decision_type, result, ai_explanation`) and returns PDF bytes.

`simulation_result` shape the copilot expects:
```json
{ "predicted_kpis": {"revenue_delta_pct": 6.8, "churn_delta_pct": 2.1, "growth_rate_new": 4.5},
  "risk_level": "Medium", "risk_score": 54, "confidence_score": 80,
  "risk_factors": ["churn risk", "competitor response"] }
```

## Install (for the backend)

```bash
pip install -e ./genai            # from the repo root, for local dev
# or pin a tagged release:
pip install "dt_genai @ git+https://github.com/skillvancetechnologies-code/DecisionTwin.git@<tag>#subdirectory=genai"
```

Set `MISTRAL_API_KEY` in the backend env. Without it / without `mistralai`
installed, every function degrades gracefully (static fallback) instead of
crashing — the adapter's reference fallback already covers that case too.

## Develop & test

```bash
pip install -e ".[dev]"
pytest -q                              # 42 tests, no API key required
python -m dt_genai.evaluation.run_eval # regenerates evaluation/ artifacts
```

## Layout

| Path | What |
|------|------|
| `dt_genai/` | the package (parser, copilot, formatter, report, llm_client, prompts) |
| `dt_genai/evaluation/` | 5-axis rubric, scorer, 25-case golden set, eval runner |
| `evaluation/` | committed eval outputs: `scored_responses.json`, `failure_modes.md` |
| `demos/conversation_scripts/` | 5 demo scripts (pricing/hiring/marketing/compare/clarification) |
| `tests/` | parser · copilot · formatter · evaluator · report_generator |
| `AUDIT.md` | week-1–6 audit (claim vs reality) and what was fixed |

> **Note:** `scored_responses.json` is a synthetic-reference snapshot (no live key
> in the build env). Re-run `run_eval` with a key set to capture true scores
> before demo day.
