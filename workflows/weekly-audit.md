# Workflow — Weekly Audit

## Objective
Every Sunday: pull Week N metrics, rank posts, identify what worked, recommend Week N+1 mix, ingest findings to wiki. Self-improving loop.

## Trigger
Sunday (any time after 6pm IST). Run before planning next week's content.

## Required inputs
- Week number (e.g., Week 1 = Days 1-7)
- `data/metrics.json` populated with at least the week's post data
- `data/posts.json` with all published posts

## Sequence

1. Load `data/metrics.json` + `data/posts.json` for the week's posts.
2. Dispatch `weekly-auditor` sub-agent (Phase 2+) with: metrics, posts, week-number.
   - In Phase 1 (before `weekly-auditor` skill exists): run analysis manually in session.
3. Auditor ranks posts by: engagement rate, follow conversion, save rate, comment rate, DM trigger.
4. Auditor identifies:
   - Top performing pillar this week
   - Top performing hook type (outcome-first / vulnerable / story / question)
   - Lowest performing post + why hypothesis
   - Platform delta: which platform drove most engagement per post
5. Auditor produces recommendations for Week N+1:
   - Pillar mix shift (e.g., "Build Receipts at 2/wk → 3/wk; Plain-English Takes at 1/wk → 2/wk")
   - Hook experiment: test one new hook type next week
   - Format experiment: add carousel if text-only dominated, or vice versa
6. Write audit report:
   - `data/audits/engagement/YYYY-WW.json` (raw rankings)
   - `data/audits/synthesis/YYYY-WW.md` (exec summary + recommendations)
7. Ingest synthesis to Obsidian wiki via `llm-wiki-ingest`:
   - Target path: `wiki/syntheses/weekly-content-audit-YYYY-WW.md`
8. User reviews synthesis on Monday morning. Approves or overrides mix recommendations.
9. Update `data/content-calendar.json` with approved Week N+1 mix.

## Output format (synthesis report)

```markdown
# Weekly Content Audit — Week N (YYYY-MM-DD to YYYY-MM-DD)

## Posts published: N
## Platforms: LinkedIn, X, Instagram, YouTube

## Rankings (engagement rate desc)
1. [post-id] "[hook]" — pillar, platform — X% engagement
...

## What worked
- [finding 1]
- [finding 2]

## What didn't
- [finding]

## Recommended Week N+1 mix
- Pillar 1 (Build Receipts): X/wk LI, X/wk X
- Pillar 2 (Plain-English Takes): X/wk LI, X/day X
- Pillar 3 (Build-in-Public): X/wk LI
- Hook experiment: [type to test]
- Format experiment: [carousel / thread / short-form]

## Notes
[Any outliers, external factors, data gaps]
```

## Edge cases
- Week with < 3 posts: note the gap, don't normalize it. Investigate why output dropped.
- Metrics not populated (Phase 1, no `metrics_fetch.py` yet): run metrics pull manually via Blotato dashboard export. Log to `data/metrics.json` before running audit.

## Expected outputs
- `data/audits/engagement/YYYY-WW.json`
- `data/audits/synthesis/YYYY-WW.md`
- Wiki entry: `wiki/syntheses/weekly-content-audit-YYYY-WW.md`
- Updated `data/content-calendar.json` (after user approval)

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
