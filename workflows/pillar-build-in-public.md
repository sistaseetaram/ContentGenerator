# Workflow — Pillar 3: Build-in-Public Setu

## Objective
Founder transparency posts — what Setu the agency built this week, what broke, what I learned, and where we are. Real numbers. No performance. 1/wk LinkedIn.

## Required inputs
- Week's main milestone (shipped, discovered, pivoted, or failed)
- What broke or surprised you (required — no milestone-only posts; that's press release, not build-in-public)
- Metric or evidence: client hours saved, posts published, tools built, revenue if any
- Lesson extracted: one clean learning, not a list of lessons

## Voice rules (enforce always)
- Banned words: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses to unlock potential"
- First sentence = what happened. Not "excited to share" or "big week".
- Include failure or friction. If nothing broke, find the honest friction. No frictionless weeks exist.
- Don't make every post a win. Progress + setback + lesson is the formula.
- Short sentences. Present tense where possible — makes it feel live, not retrospective.

## Sequence

1. Load Setu voice + positioning + ICP from `/Users/sistaseetaram/Documents/Obsidian Vault/content-wiki/wiki/concepts/`.
2. Collect raw inputs from user: milestone, what broke, metric, lesson.
3. Dispatch `content-ideator` sub-agent with: pillar=build-in-public, milestone, friction, metric, lesson, format=linkedin.
4. Sub-agent returns 2 variants (different emphasis — one opens on milestone, one opens on failure/friction).
5. Dispatch `voice-checker` sub-agent. Reject any that lead with hype, skip the friction, or list 5 lessons.
6. Present 2 cleaned drafts. User picks or revises.
7. Publish via `linkedin-publisher` (Phase 1: Blotato).
8. Append to `data/posts.json`:
   ```json
   {"id": "...", "pillar": "build-in-public", "platform": "linkedin",
    "hook": "...", "body": "...", "scheduled_at": "...", "published_at": "...",
    "milestone": "...", "what_broke": "...", "metric": "...", "lesson": "..."}
   ```
9. Schedule `metrics_fetch.py` 24h after publish.

## Edge cases
- Nothing happened this week → still post. Document the stuck feeling, what you tried, what you'll try next. Authentic inertia beats silence.
- Sensitive client detail in the story → anonymize fully. Use "[a firm in Bengaluru]" not client name.
- Post touches a decision you regret → publish it. That's the content. Vulnerability = reach on LinkedIn.

## Expected outputs
- 1 LinkedIn post/week
- `data/posts.json` entry appended
- JSON report to `data/reports/YYYY-MM-DD/build-in-public-{ts}.json`

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
