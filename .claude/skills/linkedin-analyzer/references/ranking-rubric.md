# Ranking rubric — captures → steering signals

How `tools/analyzer_rollup.py` turns per-post captures into `data/analyzer-latest.json`. Deterministic math here; the skill adds outlier hypotheses on top (report only).

## Inputs

- `data/metrics.json` — per-post captures (use the **latest** capture per post: Day 7 if present, else Day 3).
- `data/posts.json` — content attributes joined by `post_id`.

## Per-post primitives

For each post with at least one capture:
```
engagement_rate   = total ÷ impressions            (0 if impressions missing)
icp_weighted_er   = engagement_rate × (0.5 + icp_match_pct)   (fallback: engagement_rate if icp unknown)
weighted_engage   = reactions×1 + comments×3 + reposts×5      (deep-intent, for tie-breaks)
```

`total` = reactions + comments + reposts.

## Pillar normalization

Map raw `pillar` → canonical:
- `build-in-public-setu` → `build-in-public`
- everything else passes through (`build-receipts`, `plain-english-ai-takes`, `build-in-public`, `contrarian`, `roi-case-studies`)

## Signals

**`pillar_weights`** — for each canonical pillar, mean `icp_weighted_er` of its posts. Then normalize so the mean across pillars = 1.0 (a pillar at 1.3 is 30% above average; ideator nudges toward it). Pillars with no captured posts get weight 1.0 (neutral — no evidence). Round to 2 dp.

**`hook_signals`** — group posts by hook type (read `hook` first line; classify: `question` / `numeric-outcome` / `contrarian` / `story-open` / `other`). For each type with ≥1 post: `{pattern, n, avg_er, avg_icp_weighted_er}`. Sort desc by `avg_icp_weighted_er`.

**`format_signals`** — group by format (text/image/video/carousel from `asset.type`). `{format, n, avg_er}`. Sort desc.

**`icp_reach_leaders`** — post_ids sorted desc by `icp_weighted_er`, top 3. These reached the right people best — the models to copy.

**`underperformers`** — post_ids sorted asc by `icp_weighted_er`, bottom 2 (only if n_posts ≥ 4, else empty — too few to call anything a loser).

**`best_dow_time`** — bucket posts by day-of-week (from `published_at`); pick the day with highest mean ER. Time-of-day only if `published_at` has a time component (currently dates only → return day only, time null).

## Confidence

```
n_posts = number of posts with ≥1 capture
confidence = "low"  if n_posts < 8
             "med"  if 8 ≤ n_posts ≤ 15
             "high" if n_posts > 15
```

`notes` must state n_posts and, when low: "directional only; weights not yet trustworthy."

## What the rollup does NOT do

- Does not compute `icp_match_pct` — that's set at ingest by the auditor model and stored in the capture.
- Does not call any model — pure math, runnable headless by the /schedule routine.
- Does not write outlier hypotheses — the skill's `analyze` mode adds those to the human report.
