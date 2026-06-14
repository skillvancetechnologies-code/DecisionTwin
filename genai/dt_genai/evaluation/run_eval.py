"""Run the golden set through the copilot and score every response.

Usage:
    python -m dt_genai.evaluation.run_eval

If a live LLM (MISTRAL_API_KEY + mistralai) is available it scores real copilot
output. Otherwise it scores synthetic *reference* responses so the pipeline and
artifacts (scored_responses.json, failure_modes.md) can be produced and the
rubric exercised end-to-end. Re-run live before any demo to capture true scores.
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import date

from .golden_set import GOLDEN_SET
from .scorer import score_response
from .rubric import AXES

OUT_DIR = Path(__file__).resolve().parents[2] / "evaluation"
SCORED_JSON = OUT_DIR / "scored_responses.json"
FAILURE_MD = OUT_DIR / "failure_modes.md"


def _reference_response(case: dict) -> str:
    """A spec-shaped, well-behaved response, used when no live LLM is present."""
    sim = case.get("simulation_result")
    if case.get("out_of_scope") or sim is None:
        return ("I'm focused on simulating business decisions, so I can't help "
                "with that. I can simulate pricing, hiring, or marketing changes "
                "instead. Would you like to model one of those?")

    kpis = sim.get("predicted_kpis", {})
    rev, churn, growth = (kpis.get("revenue_delta_pct"),
                          kpis.get("churn_delta_pct"), kpis.get("growth_rate_new"))
    factors = ", ".join(sim.get("risk_factors", []) or [])
    parts = []
    nums = []
    if rev is not None:
        nums.append(f"revenue would move about {abs(rev)}%")
    if churn is not None:
        nums.append(f"churn about {abs(churn)}%")
    if growth is not None:
        nums.append(f"growth around {abs(growth)}%")
    parts.append("Based on the simulation, " + ", and ".join(nums) + ".")
    parts.append(f"The key risks are {factors}, which could pressure the business "
                 "if they materialise.")
    rec = "I recommend running a small pilot and monitoring the numbers before a full rollout."
    if case.get("low_confidence") or (sim.get("confidence_score") or 100) < 60:
        rec = ("Because confidence is low, treat these numbers as directional, not "
               "precise, and proceed with caution via a limited pilot.")
    if case.get("null_fields"):
        parts.append("Some fields (churn, growth) are missing, so I've left those out "
                     "rather than guessing.")
    parts.append(rec)
    parts.append("Would you like to compare this against a smaller change?")
    return " ".join(parts)


async def _live_response(case: dict) -> str:
    from .. import copilot
    return await copilot.chat_complete(
        case["user_query"], case.get("simulation_result"), case.get("history"))


def _llm_available() -> bool:
    if not os.getenv("MISTRAL_API_KEY"):
        return False
    try:
        import mistralai  # noqa: F401
        return True
    except Exception:
        return False


def run() -> dict:
    live = _llm_available()
    records = []
    for case in GOLDEN_SET:
        if live:
            response = asyncio.run(_live_response(case))
        else:
            response = _reference_response(case)
        result = score_response(case, response)
        records.append({
            "id": case["id"],
            "bucket": case["bucket"],
            "user_query": case["user_query"],
            "response": response,
            "scores": result["scores"],
            "passed": result["passed"],
            "critical_passed": result["critical_passed"],
            "failed_axes": result["failed_axes"],
        })

    passed = sum(1 for r in records if r["passed"])
    payload = {
        "generated_on": date.today().isoformat(),
        "prompt_version": "v2",
        "source": "live-llm" if live else "synthetic-reference (LLM unavailable)",
        "total": len(records),
        "passed": passed,
        "failed": len(records) - passed,
        "axes": [a.name for a in AXES],
        "results": records,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SCORED_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _write_failure_modes(payload)
    return payload


def _write_failure_modes(payload: dict):
    fails = [r for r in payload["results"] if not r["passed"]]
    lines = [
        "# Failure Modes (Hallucination & Rubric)",
        "",
        f"_Generated {payload['generated_on']} from prompt {payload['prompt_version']} "
        f"({payload['source']}). {payload['passed']}/{payload['total']} cases passed all axes._",
        "",
        "## Patterns the rubric watches for",
        "",
        "1. **Invented numbers** - any figure in the reply not present in "
        "`simulation_result` fails the Hallucination Check (binary gate).",
        "2. **Dropped risk factors** - omitting a `risk_factors` entry lowers Risk "
        "Honesty below the 5/5 gate.",
        "3. **Off-topic numbers** - citing business figures on an out-of-scope query "
        "is treated as fabrication.",
        "4. **Overconfidence on low data** - not flagging low confidence as "
        "'directional' caps Recommendation Soundness.",
        "5. **Wall-of-text / jargon** - >320 words, bullet dumps, or statistical "
        "jargon drop Tone & Clarity.",
        "",
        "## Cases failing in the latest run",
        "",
    ]
    if not fails:
        lines.append("_None - all golden cases passed every axis in this run._")
    else:
        for r in fails:
            lines.append(f"- **Case {r['id']} ({r['bucket']})** "
                         f"\"{r['user_query']}\" - failed: {', '.join(r['failed_axes'])}")
    FAILURE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    out = run()
    print(f"Scored {out['total']} cases: {out['passed']} passed, {out['failed']} failed")
    print(f"-> {SCORED_JSON}")
    print(f"-> {FAILURE_MD}")
