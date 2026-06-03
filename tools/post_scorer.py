"""
Shared pre-publish post scorer for ContentGenerator.

Predicts whether a LinkedIn draft will land and returns the 1-2 highest-leverage
fixes. Used by linkedin-analyzer's eval-draft mode AND (later) by content-creator,
so "what makes a Setu post land" has ONE definition.

Design: this module is pure Python + reads analyzer-latest.json. It does NOT call
MCP tools (Supergrow score_post) or models directly — those are passed IN by the
caller (the skill, which has the Supergrow MCP tool and model_router). This keeps
the scorer importable, testable, and runnable headless. Components that aren't
supplied are skipped and noted, never faked.

Usage (from a skill):
    from tools.post_scorer import score_draft
    result = score_draft(text, pillar="build-receipts",
                         supergrow=<score_post result dict>,
                         values_verdict={"pass": True, "reason": ""})
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ANALYZER_FILE = ROOT / "data" / "analyzer-latest.json"

# From CLAUDE.md Hard Rule 1 — banned words.
BANNED_WORDS = [
    "revolutionary", "game-changing", "game changer", "disrupt", "disruptive",
    "synergy", "cutting-edge", "cutting edge",
    "empowering businesses to unlock potential", "unlock potential",
]

LONG_SENTENCE_WORDS = 25  # soft flag, not a hard gate


def _load(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def voice_gate(text: str) -> dict:
    """Hard gate: banned words. Plus a soft sentence-length flag."""
    low = text.lower()
    hits = [w for w in BANNED_WORDS if w in low]

    sentences = [s for s in re.split(r"[.!?\n]+", text) if s.strip()]
    long_sentences = [s.strip() for s in sentences
                      if len(s.split()) > LONG_SENTENCE_WORDS]
    avg_len = (sum(len(s.split()) for s in sentences) / len(sentences)
               if sentences else 0)

    return {
        "pass": len(hits) == 0,
        "banned_hits": hits,
        "avg_sentence_words": round(avg_len, 1),
        "long_sentence_count": len(long_sentences),
    }


def proof_density(text: str) -> dict:
    """Heuristic 0-1: does the draft carry real, specific proof?"""
    low = text.lower()
    has_number = bool(re.search(r"\d", text))
    has_money = bool(re.search(r"[$₹]|(\brs\.?\b)|\busd\b|\bdollar", low))
    has_pct = "%" in text or "percent" in low
    has_time = bool(re.search(r"\b(hour|hours|hrs|min|minute|day|days|week|weeks|night|nights)\b", low))

    types = sum([has_number, has_money, has_pct, has_time])
    score = types / 4.0
    # any concrete number plus a second proof type reads as a real receipt
    if has_number and types >= 2:
        score = max(score, 0.6)
    if not has_number:
        score = 0.0

    return {
        "score": round(score, 2),
        "has_number": has_number, "has_money": has_money,
        "has_pct": has_pct, "has_time": has_time,
    }


def load_learned_patterns() -> dict:
    """Winning pillar/hook/format from analyzer-latest.json, only if confidence >= med."""
    data = _load(ANALYZER_FILE, {})
    confidence = data.get("confidence", "low")
    if confidence not in ("med", "high"):
        return {"used": False, "reason": f"confidence {confidence} (need >= med)"}
    return {
        "used": True,
        "confidence": confidence,
        "pillar_weights": data.get("pillar_weights", {}),
        "top_hook": (data.get("hook_signals") or [{}])[0].get("pattern"),
        "top_format": (data.get("format_signals") or [{}])[0].get("format"),
    }


def _hook_type(text: str) -> str:
    first = text.strip().split("\n", 1)[0].lower()
    if "?" in first:
        return "question"
    if any(t in first for t in ("stop ", "nobody ", "don't ", "everyone ", "unpopular")):
        return "contrarian"
    if any(ch.isdigit() for ch in first) or "$" in first or "%" in first:
        return "numeric-outcome"
    return "story-open"


def score_draft(text, pillar=None, supergrow=None, values_verdict=None) -> dict:
    """
    Combine gates + components into a predicted band + fixes.

    supergrow:      optional dict from Supergrow score_post (caller supplies via MCP).
                    Expected keys like {"hook":, "clarity":, "cta":, "overall":} out of 10.
    values_verdict: optional dict {"pass": bool, "reason": str} from the caller's
                    five-value judgment (model). None => unchecked (noted, not failed).
    """
    voice = voice_gate(text)
    proof = proof_density(text)
    learned = load_learned_patterns()

    values_pass = True if values_verdict is None else bool(values_verdict.get("pass", True))
    values_checked = values_verdict is not None

    # ---- components for the 0-1 score (only those available) ----
    components = {"proof_density": proof["score"]}
    if supergrow and supergrow.get("overall") is not None:
        components["supergrow"] = supergrow["overall"] / 10.0
    if learned["used"]:
        pw = learned.get("pillar_weights", {})
        match = 0.0
        if pillar and pw.get(pillar):
            match = min(1.0, pw[pillar] / 1.5)  # weight 1.5+ => full match
        if learned.get("top_hook") and _hook_type(text) == learned["top_hook"]:
            match = min(1.0, match + 0.3)
        components["learned_pattern"] = round(match, 2)

    score = round(sum(components.values()) / len(components), 2)

    # ---- gates override ----
    gates = {
        "voice": "pass" if voice["pass"] else "fail",
        "values": "pass" if values_pass else ("fail" if values_checked else "unchecked"),
    }
    gate_failed = (not voice["pass"]) or (values_checked and not values_pass)

    if gate_failed:
        band = "likely-weak"
    elif score >= 0.70:
        band = "likely-strong"
    elif score >= 0.45:
        band = "mixed"
    else:
        band = "likely-weak"

    # ---- fixes (top 1-2 by severity) ----
    fixes = []
    if voice["banned_hits"]:
        fixes.append(f"Remove banned word(s): {', '.join(voice['banned_hits'])}.")
    if values_checked and not values_pass:
        fixes.append(f"Brand-values issue: {values_verdict.get('reason', 'violates a core value')}.")
    if proof["score"] < 0.4:
        fixes.append("Add a real receipt — a number, cost, hours saved, or a specific lived moment.")
    if supergrow and supergrow.get("hook") is not None and supergrow["hook"] < 6:
        fixes.append("Strengthen the hook — lead with the concrete outcome, not the backstory.")
    if voice["long_sentence_count"] > 0 and len(fixes) < 2:
        fixes.append(f"Break up long sentences (avg {voice['avg_sentence_words']} words; Setu voice is short).")
    fixes = fixes[:2]

    return {
        "predicted_band": band,
        "score": score,
        "gates": gates,
        "supergrow": supergrow or {"note": "not supplied — call Supergrow score_post and pass it in"},
        "proof_density": proof["score"],
        "voice": voice,
        "learned_pattern": learned if learned["used"] else {"used": False, "reason": learned["reason"]},
        "values_checked": values_checked,
        "fixes": fixes or ["No high-leverage fix found — draft reads solid on available checks."],
    }


if __name__ == "__main__":
    import sys
    sample = sys.stdin.read() if not sys.stdin.isatty() else \
        "This revolutionary tool will disrupt everything. Trust me."
    print(json.dumps(score_draft(sample, pillar="build-receipts"), indent=2))
