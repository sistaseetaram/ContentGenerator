# Pre-publish eval rubric — predict before posting

Used by `eval-draft` mode and `tools/post_scorer.py`. Predicts whether a draft will land and returns the 1–2 highest-leverage fixes. Never posts. The future content-creator calls the same scorer so "what makes a Setu post land" has one definition.

## Dimensions

| # | Dimension | Type | How |
|---|-----------|------|-----|
| 1 | Brand voice gate | hard gate | Banned words present? Sentences too long/hype? Load `setu-voice.md`. Any banned word → FAIL. |
| 2 | Brand values five-filter | hard gate | Work not tech · Quiet over loud · Respect owners · Ship don't slide · Map before build. Clear violation → FAIL. |
| 3 | Supergrow score_post | external | Call `mcp__claude_ai_Supergrow__score_post`. Returns Hook/Clarity/Readability/Completeness/CTA/Originality/Grammar/Content-DNA out of 10. |
| 4 | Proof density | scored | Are there real numbers / receipts / a specific lived moment? Generic = weak. This is the Setu bet. |
| 5 | Learned-pattern match | scored (conditional) | Similarity to winning pillar/hook/format from `analyzer-latest.json`. Only counted when that file's `confidence ≥ med`; else skipped with a note. |

## Hard gates

Dimensions 1–2 are pass/fail. If either fails, `predicted_band = likely-weak` regardless of everything else, and the top fix is the gate failure stated plainly (e.g. "Remove 'game-changing' — banned word" or "This claims a win before it shipped — violates Ship-don't-slide").

## Band logic (when gates pass)

Combine Supergrow score (normalize 0–10 → 0–1), proof density (0–1), and learned-pattern match (0–1, or omitted):
```
score = mean(available components)   # learned-pattern omitted when confidence < med
band  = likely-strong  if score ≥ 0.70
        mixed          if 0.45 ≤ score < 0.70
        likely-weak    if score < 0.45
```

## Output (returned to user or to content-creator)

```json
{
  "predicted_band": "likely-strong | mixed | likely-weak",
  "score": 0.0,
  "gates": {"voice": "pass|fail", "values": "pass|fail"},
  "supergrow": {"hook": 0, "clarity": 0, "cta": 0, "overall": 0},
  "proof_density": 0.0,
  "learned_pattern": {"used": false, "reason": "confidence low (n<8)"},
  "fixes": ["the 1-2 highest-leverage changes"]
}
```

Keep `fixes` to 1–2 items, concrete and rewritable — not "improve the hook" but "open on the $0.06 number, not the backstory."

## Honesty

When `learned_pattern.used = false`, say so in the user-facing output: the prediction is heuristic + brand-gate based, not yet grounded in real performance. Don't oversell the score on n<8 history.
