# Workflow — Pillar 2: Plain-English AI Takes

## Objective
Translate AI news and model launches into plain English — what actually changes for a founder running a small firm, not what the press release says.

## Required inputs
- News item or announcement: model launch, tool update, regulation, study
- Relevance angle: how does this touch architecture/interior/construction firm workflow specifically?
- Confidence level: high (will impact them), medium (might), low (probably noise)
- Platform: LinkedIn (1/wk, 200-400 words) or X (daily, thread or single)

## Voice rules (enforce always)
- Banned words: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses to unlock potential"
- Start with what changed for *them* — not what the model can do in benchmarks
- Name the tech only once, early, then drop it. Never repeat model names like marketing copy.
- If it won't change anything they do this week, say so. Don't manufacture relevance.
- Short sentences. No jargon.

## Sequence

1. Load Setu voice + positioning + ICP from `/Users/sistaseetaram/Documents/Obsidian Vault/content-wiki/wiki/concepts/`.
2. Identify relevance tier: high / medium / noise. If noise → skip. Don't post for the sake of posting.
3. Dispatch `content-ideator` sub-agent with: pillar=plain-english-takes, topic, relevance-angle, platform.
4. Sub-agent returns 2-3 draft variants.
5. Dispatch `voice-checker` sub-agent. Reject any that lead with the tech, use jargon, or fake urgency.
6. Present cleaned drafts to user. User picks or skips (skipping is fine — not every launch warrants a post).
7. Publish via `linkedin-publisher` (Phase 1: Blotato) or post to X directly.
8. Append entry to `data/posts.json`:
   ```json
   {"id": "...", "pillar": "plain-english-takes", "platform": "linkedin|x",
    "hook": "...", "body": "...", "scheduled_at": "...", "published_at": "...",
    "topic": "...", "news_source": "..."}
   ```
9. Schedule `metrics_fetch.py` for this post 24h after publish.

## Edge cases
- Breaking news temptation: don't rush. A well-angled take 48h later beats a rushed hot take.
- Topic has no clear angle for ICP → skip. Log it as "skipped — no ICP relevance" in posts.json.
- Multiple launches same week → pick the one most relevant to the ICP. One take, done right.

## Expected outputs
- 1 LinkedIn post/week + 1-5 X posts/week (cycling throughout week)
- `data/posts.json` entry per published post
- JSON report to `data/reports/YYYY-MM-DD/plain-english-takes-{ts}.json`

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
