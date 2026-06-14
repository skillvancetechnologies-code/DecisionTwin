"""Rule-based query parser (Stage 1).

Turns a free-text business question into a validated ParsedQuery. The rules
catch the obvious, unambiguous cases deterministically. Anything the rules
cannot confidently parse is handed to the LLM fallback (Stage 2) via
``llm_parse`` when an LLM client is configured; otherwise it degrades to a
low-confidence ``other`` result that signals "needs clarification".
"""

import re

from .schemas import ParsedQuery

try:  # Stage 2 is optional and only runs when an LLM client is wired up.
    from .llm_parser import llm_parse
except Exception:  # pragma: no cover - llm_parser may be absent/unconfigured
    llm_parse = None


# --- Pattern libraries ---------------------------------------------------

PRICE_UP = re.compile(r"(?:raise|increase|bump|hike).*?price")
PRICE_DOWN = re.compile(r"(?:lower|decrease|cut|drop|reduce).*?price")
HEADCOUNT_UP = re.compile(r"(?:hire|grow|add|expand|recruit)")
HEADCOUNT_DOWN = re.compile(r"(?:lay\s*off|fire|cut|reduce|shrink)")
MARKETING_KW = re.compile(r"(?:marketing|ad\s*spend|advertis|campaign)")

# "10%", "20 percent"
PERCENT = re.compile(r"(\d[\d,]*\.?\d*)\s*(?:%|percent)")
# "$10k", "10000", "5 dollars" -- suffix k/m only when not followed by a letter
# (so the 'm' in "more"/"marketing" is never mistaken for a million suffix).
ABSOLUTE = re.compile(r"\$?(?P<num>\d[\d,]*\.?\d*)(?P<suf>[km])?(?![a-z])")


def _extract_magnitude(text: str):
    """Return (value, magnitude_type) or (None, None) if no number present."""
    m = PERCENT.search(text)
    if m:
        return float(m.group(1).replace(",", "")), "percentage"
    if "double" in text:
        return 100.0, "percentage"
    if "triple" in text:
        return 200.0, "percentage"
    if "halve" in text or "cut in half" in text:
        return 50.0, "percentage"
    m = ABSOLUTE.search(text)
    if m:
        value = float(m.group("num").replace(",", ""))
        suffix = m.group("suf")
        if suffix == "k":
            value *= 1_000
        elif suffix == "m":
            value *= 1_000_000
        return value, "absolute"
    return None, None


def rule_based_parse(text: str):
    raw = text
    text = text.lower().strip()

    # --- Price changes ---
    if PRICE_UP.search(text) or PRICE_DOWN.search(text):
        mag, mtype = _extract_magnitude(text)
        if mag is None:
            # e.g. "bump prices a little" / "drop prices to fight competitor X"
            return ParsedQuery(
                decision_type="price_change", parameter="price_per_unit",
                magnitude=0.0, magnitude_type="percentage",
                target_metric=None, confidence=0.3,
                parser_used="rules", raw_query=raw,
            )
        if PRICE_DOWN.search(text):
            mag = -abs(mag)
        return ParsedQuery(
            decision_type="price_change", parameter="price_per_unit",
            magnitude=mag, magnitude_type=mtype,
            target_metric=None, confidence=0.85,
            parser_used="rules", raw_query=raw,
        )

    # --- Marketing (check before generic headcount verbs like 'cut'/'reduce') ---
    if MARKETING_KW.search(text):
        mag, mtype = _extract_magnitude(text)
        if mag is None:
            return ParsedQuery(
                decision_type="marketing", parameter="marketing_budget",
                magnitude=0.0, magnitude_type="percentage",
                target_metric=None, confidence=0.3,
                parser_used="rules", raw_query=raw,
            )
        if re.search(r"(?:cut|reduce|lower|decrease|drop)", text):
            mag = -abs(mag)
        return ParsedQuery(
            decision_type="marketing", parameter="marketing_budget",
            magnitude=mag, magnitude_type=mtype,
            target_metric=None, confidence=0.88,
            parser_used="rules", raw_query=raw,
        )

    # --- Headcount ---
    team_words = re.search(r"engineer|sales|employee|staff|team|head|ops|rep|worker", text)
    if (HEADCOUNT_UP.search(text) or HEADCOUNT_DOWN.search(text)) and team_words:
        mag, mtype = _extract_magnitude(text)
        if mag is None:
            return ParsedQuery(
                decision_type="headcount", parameter="employee_count",
                magnitude=0.0, magnitude_type="absolute",
                target_metric=None, confidence=0.3,
                parser_used="rules", raw_query=raw,
            )
        if HEADCOUNT_DOWN.search(text) and not HEADCOUNT_UP.search(text):
            mag = -abs(mag)
        return ParsedQuery(
            decision_type="headcount", parameter="employee_count",
            magnitude=mag, magnitude_type=mtype,
            target_metric=None, confidence=0.85,
            parser_used="rules", raw_query=raw,
        )

    return None  # signal: send to LLM / clarification


def parse(text: str) -> ParsedQuery:
    """Public entry point. Tries rules first, then the LLM fallback."""
    parsed = rule_based_parse(text)
    if parsed is not None:
        return parsed

    if llm_parse is not None:
        try:
            llm_result = llm_parse(text)
            if llm_result is not None:
                return llm_result
        except Exception:
            pass  # fall through to clarification result

    return ParsedQuery(
        decision_type="other", parameter="unknown",
        magnitude=0.0, magnitude_type="absolute",
        target_metric=None, confidence=0.0,
        parser_used="rules", raw_query=text,
    )
