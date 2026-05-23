# Workflow — Pillar 1: Build Receipts

## Objective
Publish concrete proof of automation work — what got built, what it replaced, how many hours/rupees saved.

## Required inputs
- Topic (the build): e.g., n8n stock report 8hrs → 2min
- Before/after numbers: hours saved, money saved, error rate change (if known)
- Workflow screenshot or Loom URL (optional but lifts engagement)
- Target platform(s): LinkedIn / X thread / YouTube short / Loom walkthrough
- Hook angle (pick one): outcome-first, contrarian, story, vulnerable

## Voice rules (enforce always)
- Banned words: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses to unlock potential"
- Real hours, real money — no abstractions
- Short sentences. Plain words.
- Outcome first. Tech named only when reader needs it.
- Apply copy test: would a smart, busy architecture firm owner feel respected — or sold to?

## Sequence

1. Load Setu voice + positioning + ICP from `/Users/sistaseetaram/Documents/Obsidian Vault/content-wiki/wiki/concepts/`.
2. Dispatch `content-ideator` sub-agent with: pillar=build-receipts, topic, numbers, target-platform, hook-angle.
3. Sub-agent returns 3 draft variants (different hooks).
4. Dispatch `voice-checker` sub-agent. Reject any with banned words / abstractions / long sentences.
5. Present 3 cleaned drafts to user. User picks one (or asks for revision).
6. If carousel needed: dispatch `canvas` skill.
7. Publish via `linkedin-publisher` (Phase 1: Blotato schedule) or `tools/linkedin_post.py` (Phase 3+).
8. Append entry to `data/posts.json`:
   ```json
   {"id": "...", "pillar": "build-receipts", "platform": "linkedin",
    "hook": "...", "body": "...", "scheduled_at": "...", "published_at": "...",
    "topic": "...", "numbers": {"hours_saved": ..., "rupees_saved": ...}}
   ```
9. Schedule follow-up: 24h later run `metrics_fetch.py` for this post.

## Edge cases
- No real numbers yet → defer post. Don't fake. Find a different topic with measurable outcome.
- Topic touches a current client → confirm permission before publishing. Use `[Client]` anonymization if needed.
- Screenshot exposes credentials → redact in `.tmp/` first.

## Expected outputs
- 1 post published per call (or 1 batch of 3 drafts for review)
- `data/posts.json` entry appended
- JSON report emitted to `data/reports/YYYY-MM-DD/build-receipts-{ts}.json`

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
