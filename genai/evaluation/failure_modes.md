# Failure Modes (Hallucination & Rubric)

_Generated 2026-06-15 from prompt v2 (synthetic-reference (LLM unavailable)). 25/25 cases passed all axes._

## Patterns the rubric watches for

1. **Invented numbers** - any figure in the reply not present in `simulation_result` fails the Hallucination Check (binary gate).
2. **Dropped risk factors** - omitting a `risk_factors` entry lowers Risk Honesty below the 5/5 gate.
3. **Off-topic numbers** - citing business figures on an out-of-scope query is treated as fabrication.
4. **Overconfidence on low data** - not flagging low confidence as 'directional' caps Recommendation Soundness.
5. **Wall-of-text / jargon** - >320 words, bullet dumps, or statistical jargon drop Tone & Clarity.

## Cases failing in the latest run

_None - all golden cases passed every axis in this run._
