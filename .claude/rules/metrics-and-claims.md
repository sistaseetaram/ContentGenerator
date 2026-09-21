# Metrics & Claims — what may go in a post, and what may not

Load before writing any post, script, or carousel that cites a number.
Per-topic rule under CLAUDE.md's `.claude/rules/` layout. Append to this file whenever a
number turns out to be unpublishable — same pattern as `design-taste.md`.

## The rule

**A metric is a floor to clear, never a ranking — and never the parameter that decides publicly
whether a model or a method works.**

This project has now caught its own metrics ranking wrongly twice:

| Metric | How it failed | Source |
|---|---|---|
| `covered_ratio` (render fidelity) | Scored a pass-through render — the model handing the control image back untouched, the worst output of the set — **highest at 0.7885**. Scored the render the client actually **accepted lowest at 0.5216**. | `experiments/fallback-render-tier-pilot`, 2026-09-20 |
| Detection **F1 / precision / recall** | Scores whether the right *kinds and counts* of fixtures were found. **Blind to placement.** For a floor plan, placement is the only thing that matters — so a respectable score and an unusable layout are perfectly compatible. The bake-off proves it: pooled across models recall is high, but require any two models to agree on the same fixture and it collapses. They agree something is there and disagree on *where*. | `syntheses/legend-priming-doesnt-help-detection`; Seetaram's instruction 2026-09-20 |

**Consequence:** do not publish either as the deciding number. Prefer, in order:

1. **Raw observables** — counts, before/after states, artefacts. "Detected boxes collapsed 94 to 33"
   needs no metric and cannot be argued with.
2. **Hand-computed truth** — a measured value against an independently derived one
   (px/ft 47.82 → 40.31 against a hand-computed 40.30).
3. **The designer's judgement** — acceptance, sign-off, a marked-up revision. This is what the
   client actually pays for.

## Numbers that are banned outright

| Figure | Why |
|---|---|
| Higharc funding ≈$169M | Unverified and contradicted by their own About page ($78M). Say "well-funded" or nothing. |
| "$300–2,500/image" US/EU render pricing | Sourced from a search-engine AI summary. Wiki-flagged do-not-publish. |
| AECV-Bench per-category figures (door 39%, window 34%, GPT-5.2 ~49%, Opus 4.5 ~42%, GLM-4.6V ~39%) | All carry a `spot-verify` marker in-wiki. Also the rejected metric class. |
| Any single-day arXiv listing as evidence of research volume | One day's listing is not a literature search. Wiki-flagged must-not-repeat. |
| "Nobody is researching this" | Same reason. |

## Claims that need a scope limit attached, every time

- **"Five $0 spatial checks"** — accurate as the *blocking* set, but two more evals exist and camera
  validation is logged Priority-1 and **still unbuilt**. On 2026-09-12 a camera standing inside a wall
  reached paid renders. Safe: *"no bad geometry reaches a paid render."* Unsafe: *"nothing bad reaches
  a paid render."*
- **The phantom-walls result** — 31 segments, zero phantom walls, 99 tests green, and a strong
  designer quote. The segments are **bands, not a graph**, and are **derived from the already-corrected
  model, not acquired from a semantic mask**. Phantom walls had three causes; this fixed one. Never
  publish the quote without the caveat.
- **The eight refine passes** — two parallel options (A: v1–v3, B: drafts B→B4), not one chain.

## Cost figures

`~$2.55` for one client-accepted render across ~26 paid calls is **cost-to-run** and may be stated as
such. It is **not** client savings and must never be framed as ROI. No ROI figure ships until a real
measured one exists.

_Last updated 2026-09-20 — created after F1 was removed from the Friday 2026-09-25 post._
