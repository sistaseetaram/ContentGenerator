"""
Deterministic idea scorer for ContentGenerator.

Scores a single content idea against the 7-dimension Setu rubric and applies the
Strategic Advisor critique (post_now / post_later / drop). Used by:
  - the dashboard server (auto-score on submit), and
  - content-ideator Rate mode (when Claude scores a user/sister idea inline).

Every model call goes through tools/model_router.route() — never an SDK directly.
The rubric weights and the five-value filter live here so the score is identical
whether the server or a Claude session produced it.

Usage (CLI, for testing):
    python tools/idea_scorer.py --title "..." --angle "..." --pillar build-receipts \
        --platform linkedin --proof "screen-rec of V1 vs V2"
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from tools.model_router import route  # noqa: E402

# Rubric weights — must match references/idea-rubric.md. Raw max = 41.25.
WEIGHTS = {
    "pillar_fit": 1.0,
    "value_fit": 1.0,
    "new_info": 1.5,
    "lived_exp": 1.5,
    "proof_level": 1.5,
    "timeliness": 1.0,
    "effort": 0.75,
}
SCORE_MAX = 41.25
DIM_ORDER = list(WEIGHTS.keys())

# Hard voice gate — an idea that needs one of these to sound interesting is weak.
BANNED_WORDS = [
    "revolutionary", "game-changing", "game changing", "disrupt", "synergy",
    "cutting-edge", "cutting edge", "empowering businesses to unlock potential",
]

ACTIVE_PILLARS = [
    "build-receipts", "plain-english-ai-takes", "build-in-public-setu",
    "contrarian",  # unlocked once 2-3 Build Receipts shipped (gate met Jun 2026)
]

_SYSTEM = """You are ContentIdeator, the idea-scoring engine for Setu — a personal brand \
of an AI-automation specialist serving interior-design / architecture / construction \
firm owners (the Bridge 01 ICP). The strategic bet: in the AI era, information alone is \
worthless (the audience can ask ChatGPT). Setu wins on specificity that can't be faked — \
new information, lived experience, and real proof (a screen recording, a dashboard, a real \
invoice). An idea ChatGPT could generate is NOT a Setu idea.

Score the idea 1-5 on each of these seven dimensions:
1. pillar_fit       — maps cleanly to one ACTIVE pillar (build-receipts, plain-english-ai-takes, build-in-public-setu, contrarian), on-cadence.
2. value_fit        — passes all five values: work-not-tech, quiet-over-loud, respect-owners, ship-don't-slide, map-before-build. 5 = embodies >=2, violates none.
3. new_info         — 1 = ChatGPT answers it fully; 5 = genuine pattern-interrupt / contrarian truth ChatGPT can't produce.
4. lived_exp        — 1 = no real receipt; 5 = a concrete build / number / failure the author actually lived.
5. proof_level      — 1 = claim only; 5 = can show visual documentation or live demo (screen rec, dashboard, invoice). Floor for a good idea is 4.
6. timeliness       — 1 = evergreen; 5 = rides a current release/trend window closing soon.
7. effort           — 1 = days of work / assets we lack; 5 = low effort, assets already exist.

Then apply the Strategic Advisor critique. Set verdict to exactly one of:
- post_now    — on-ICP, on-positioning, proof exists or is capturable now.
- post_later  — good idea, wrong stage (proof not ready, sequencing risk, announcing before earning).
- drop        — off-ICP, off-positioning (blurs Setu as the design/construction AI specialist), or proof will never exist.

Be honest, never rubber-stamp. Respond with ONLY a JSON object, no prose, no code fence:
{"scores":{"pillar_fit":N,"value_fit":N,"new_info":N,"lived_exp":N,"proof_level":N,"timeliness":N,"effort":N},
 "strategic_opinion":{"verdict":"post_now|post_later|drop","reason":"one sentence","when_to_post":"now|Week N|after first client|...","timing_note":"what must be true before posting"}}"""


def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model response (handles code fences)."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    start = text.find("{")
    if start == -1:
        raise ValueError(f"no JSON object in model output: {text[:200]}")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError(f"unbalanced JSON in model output: {text[:200]}")


def voice_flags(idea: dict) -> list:
    """Deterministic banned-word check on title + angle. Returns list of hits."""
    blob = f"{idea.get('title', '')} {idea.get('angle', '')}".lower()
    return [w for w in BANNED_WORDS if w in blob]


def compute_total(scores: dict) -> float:
    return round(sum(scores.get(k, 0) * w for k, w in WEIGHTS.items()), 2)


def score_idea(idea: dict) -> dict:
    """Score one idea. Returns {scores, total_score, strategic_opinion, voice_flags, model_used, cost_usd}.

    `idea` needs at least: title, angle, pillar, platform, proof_plan.
    Raises ValueError if the model output can't be parsed into the rubric shape.
    """
    prompt = (
        f"Title: {idea.get('title', '')}\n"
        f"Angle: {idea.get('angle', '')}\n"
        f"Pillar (claimed): {idea.get('pillar', '')}\n"
        f"Platform: {idea.get('platform', 'linkedin')}\n"
        f"Proof plan: {idea.get('proof_plan', '')}\n"
    )
    result = route("lint-dispatch", prompt, system=_SYSTEM, max_tokens=600)
    parsed = _extract_json(result["content"])

    scores = {k: int(parsed["scores"][k]) for k in DIM_ORDER}
    op = parsed["strategic_opinion"]
    return {
        "scores": scores,
        "total_score": compute_total(scores),
        "strategic_opinion": {
            "verdict": op.get("verdict", "post_later"),
            "reason": op.get("reason", ""),
            "when_to_post": op.get("when_to_post", "now"),
            "timing_note": op.get("timing_note", ""),
        },
        "voice_flags": voice_flags(idea),
        "model_used": result.get("model_used"),
        "cost_usd": round(result.get("cost_usd", 0.0), 6),
    }


def main():
    ap = argparse.ArgumentParser(description="Score one content idea against the Setu rubric")
    ap.add_argument("--title", required=True)
    ap.add_argument("--angle", default="")
    ap.add_argument("--pillar", default="")
    ap.add_argument("--platform", default="linkedin")
    ap.add_argument("--proof", dest="proof_plan", default="")
    args = ap.parse_args()
    out = score_idea(vars(args))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
