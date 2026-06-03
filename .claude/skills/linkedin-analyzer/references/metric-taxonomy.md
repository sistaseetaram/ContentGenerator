# Metric Taxonomy — what we capture and what each steers

Captured per post unless marked *(account-level, Supergrow)*. The "steers" column is why the metric exists — if a metric doesn't steer a decision, don't capture it.

## A. Reach / distribution

| Metric | Source | Steers |
|--------|--------|--------|
| Impressions | paste | Baseline visibility. Context for rates, NOT a goal in itself. |
| Members reached (unique) | paste | True reach vs repeat views. |
| Impression velocity (Day 3 → Day 7 delta) | derived from 2 captures | Fast-peak vs slow-burn → tells whether a format dies in 48h or keeps earning. |
| Profile views | *(Supergrow trend)* | Curiosity signal — did the post send people to the profile? |

## B. Engagement (raw + rate)

| Metric | Source | Steers |
|--------|--------|--------|
| Reactions (total) | paste | Surface approval. Lowest-intent. |
| Reaction breakdown (like/celebrate/support/love/insightful/funny) | paste | "Insightful" on a build-receipt = the proof landed. Tone read. |
| Comments | paste | High-intent. Conversation = the algorithm's strongest signal. Weighted heavier. |
| Reposts / reshares | paste | Highest-intent — someone staked their feed on it. Weighted heaviest. |
| Engagement rate = total ÷ impressions | derived | The core quality metric. Ranks posts fairly across different reach. |
| Comment rate, repost rate | derived | Deep-intent isolated from vanity likes. |

## C. Audience quality — the steering gold (manual paste only)

Supergrow cannot provide any of this. It is the single biggest reason manual paste exists.

| Metric | Source | Steers |
|--------|--------|--------|
| Follower vs non-follower impression split | paste | High non-follower % = the post broke past the network = distribution win. |
| Top job titles | paste | Are owners/principals seeing it, or other automation builders? |
| Top industries | paste | Architecture / interior / construction = on-ICP. Software/marketing = drift. |
| Top seniority | paste | Owner / director / founder = decision-makers = on-ICP. |
| Top company sizes / companies | paste | 3–50 person firms = SMB ICP. |
| Top locations | paste | India-weighted = on-ICP. |
| **ICP-match %** (derived) | `auditor` model | Single number: share of audience matching Setu ICP. The north-star audience metric. |

## D. Conversion / growth

| Metric | Source | Steers |
|--------|--------|--------|
| New followers in window | *(Supergrow get_followers)* | Did content convert viewers to followers? |
| Follower growth rate | *(account-level)* | Trend health. |

## E. Content attributes (joined from posts.json — the X-variables)

These are not measured; they are read from `posts.json` and joined so signals can be attributed.

- `pillar` — build-receipts / plain-english-ai-takes / build-in-public (normalize `build-in-public-setu` → `build-in-public`)
- `format` — derive from `asset.type`: none→text, infographic/image→image, native_video→video, carousel→carousel, loom→video
- hook first-line + hook type (question / numeric-outcome / contrarian / story-open)
- word count
- has-numbers (proof density — does `numbers` exist and is it non-empty?)
- hashtags
- day-of-week + time posted (from `published_at`)
- proof level (if linkable to an ideator idea record)

## F. Derived steering signals → analyzer-latest.json

Computed by `tools/analyzer_rollup.py` + in-skill judgment. This is the output that content-ideator consumes.

| Signal | How | Steers (in ideator) |
|--------|-----|---------------------|
| `pillar_weights` | per-pillar mean of ICP-weighted ER, normalized so mean = 1.0 | Schedule mode weights pillars with room toward winners. |
| `hook_signals` | group posts by hook type, rank by ER | Which opening patterns to favor. |
| `format_signals` | group by format, rank by ER | text vs video vs carousel performance. |
| `icp_reach_leaders` | posts with highest `icp_match_pct × engagement_rate` | The posts that reached the right people — model these. |
| `underperformers` | bottom posts by ICP-weighted ER | What to stop doing. |
| `best_dow_time` | day/time bucket with highest mean ER | When to schedule. |
| velocity profile | per-post Day3→Day7 ER delta | Format longevity (report only, v0.1). |

## ICP-weighted engagement (the ranking primitive)

```
icp_weighted_er = engagement_rate × (0.5 + icp_match_pct)
```

A post with 4% ER reaching 80% ICP (0.5+0.8=1.3 → 5.2%) outranks a 5% ER post reaching 10% ICP (0.5+0.1=0.6 → 3.0%). Reaching the right people beats reaching more people. If `icp_match_pct` is unknown for a post, fall back to plain `engagement_rate` and flag it.

## Deep-intent engagement weighting

For tie-breaks and the "winning hook" call, weight engagement by intent:
```
weighted_engagement = reactions×1 + comments×3 + reposts×5
```
A post that earned 2 reposts and 5 comments is stronger than one with 40 likes, even at lower raw ER.
