# Brainstorm — content-ideator + loom-walkthrough-recorder

**Date:** 2026-05-25 (Day 3)
**Status:** Captured before session clear. Resume tomorrow 9pm IST.

---

## Big Reframe (user input 2026-05-25)

The original plan collapsed two distinct jobs into one skill. They are separate:

### content-ideator = research + ideation engine (NOT content creation)

**Job:** generate, score, and shortlist content ideas. Hand them to `content-creator` (separate, future skill).

**How it works:**
- Runs 5-10 parallel research sub-agents on a schedule (daily or every 2 days — TBD)
- Each agent has a distinct beat:
  - 2-3 agents: trending topics on YouTube (per tool stack)
  - 2-3 agents: new releases / launches in our tool stack (n8n, Claude, Loom, etc.)
  - 2-3 agents: India SMB / architecture-interior-construction AI news
  - 2 agents: other beats (TBD via brainstorming)
- Each returns top 3 candidate ideas
- Aggregator scores ALL candidates against evals (brand fit, voice fit, ICP fit, novelty vs. saturated patterns, hook strength)
- Shortlists to top 3 per cycle
- Stores in ideas dashboard with tags (source: which agent, score, status)
- User can input own ideas → agent rates them, adds opinion, tags **"idea by Sista"**
- After user review/approval → handoff to `content-creator`

**Sources of content (locked):**
1. Daily research agents (above)
2. **User's daily dev work** — commits + summary reports already pushed to GitHub + Drive via existing routine
3. **Brand-building journey** — building Setu agency, executive agents, personal website, brand identity (the meta-content)
4. User's own ideas (manual input)

**Evals (to design):**
- Brand fit (matches Setu positioning)
- Voice fit (no banned words, no jargon, real numbers possible)
- ICP relevance (architecture/interior/construction lens applicable)
- Saturation check (not the 8 competitor patterns — see plan)
- Hook strength
- Pillar slot availability (don't overstuff one pillar)

### content-creator = generation engine (Blotato clone target, future skill)

**Job:** take approved idea → modify/expand prompts → generate full content (post text, video transcript, audio transcript, carousel copy, etc.). This is what runs through `model_router.py` for long-form / short-form / multimodal per task.

**Build target:** clone Blotato's generation flow over ~1 month after we observe it as users.

---

## loom-walkthrough-recorder reframe (user input 2026-05-25)

**Job:** prepare a Loom recording end-to-end — not just outline.

**Inputs:** topic + target duration + repurpose targets

**Outputs:**
- Transcript outline (talking points, beats, hooks)
- Slide deck if needed (presented during walkthrough)
- Brand-aligned tips (mic check, screen setup, brand logo on overlay, video editing cues)
- Post-recording editing checklist
- Video editing guidance (cuts, captions, brand overlay positioning)

**Brainstorm in detail later.**

---

## Volume Target (LOCKED — by 2026-06-10)

| Platform | Daily volume |
|----------|--------------|
| LinkedIn | ≥2 posts |
| YouTube | ≥1 video |
| Instagram | ≥2 reels OR ≥2 posts |
| X | 2-3 tweets (target 3-5 eventually) |

**Mode:** Sabrina-style high-volume (will confirm in plan mode before shift).
**Shift trigger:** This week. Skill-building schedule decoupled from posting schedule — posting continues per current calendar while skills build in parallel starting tomorrow 9pm IST.

---

## Ideas Dashboard / Storage — DECISION PENDING

User asked which platform to store ideas on:
- Google Sheets — simple, mobile, but weak for rich pipeline (tags, status, ratings, AI opinions)
- ClickUp — already in plan (Day 27 build), MCP available, mobile push, custom fields, tags, comments → strong fit for idea pipeline
- Notion / Airtable — also good for structured idea boards

**Tentative recommendation (to discuss tomorrow):**
- **Local-first:** `data/ideas.json` in repo (source of truth, version-controlled)
- **Mirror to ClickUp** once MCP wired (Day 27 in original plan — could pull forward)
- Dashboard view: rendered via `web-artifacts-builder` skill → mobile-viewable HTML, similar to claude-mem dashboard pattern
- Each idea row: `id | source (agent name or "Sista") | topic | hook_angle | pillar_fit | score_brand | score_voice | score_icp | score_novelty | status (new/reviewed/approved/rejected/posted) | claude_opinion | sista_notes | created_at`

**Alternative tools considered:** Airtable (best structured pipeline view), Notion (rich docs).
Decision deferred until tomorrow's brainstorm.

---

## Session State at Save

- **Day 3 of 30** — completed.
- **Day 3 post:** User posting manually today. Skill build skipped today. Will share posted content Day 4.
- **Today todo (marked done):** post-002 published manually.
- **Tomorrow Day 4:** First Loom recording (plan 01-04) + brainstorm continuation for ideator + creator + loom-walkthrough + storage decision. Start 9pm IST.

---

## To Decide Tomorrow

1. Idea storage: ClickUp vs Google Sheets vs Airtable vs Notion vs local JSON + dashboard
2. Research agents — final list of beats, how many agents
3. Cadence — daily vs every-2-days for ideation runs
4. Evals — exact rubric per dimension, scoring thresholds
5. content-creator skill — full design (after ideator scoped)
6. loom-walkthrough-recorder — full design with brand overlay + editing guidance
7. Volume shift timing — when to ramp toward 2-LI-per-day cadence
8. Brand identity content — whether to slot it Day 4 or Day 5 (see below)

---

## Recommendation on Brand-Identity Post (answered in chat 2026-05-25)

See chat thread. Short answer: YES, post brand-identity content as Build-in-Public Setu pillar entry. Strong ICP fit (architecture audience = design-conscious). Strengthens positioning ("diagnose-before-build applied to my own brand"). Slot it Day 5 (post-003 already drafted for Day 5 Plain-English AI Takes — push to Day 7 or shift order).

---

## Pending Todos (carry forward)

- [x] Day 3 post published (manually by user)
- [ ] Day 4: First Loom recording (plan 01-04)
- [ ] Day 4 9pm IST: Resume brainstorm — ideator + creator + loom-recorder
- [ ] Update STATE.md: advance to Day 4, mark post-002 published
- [ ] Update content-calendar.json: mark Day 3 done
- [ ] SKILL-REGISTRY check + Obsidian wiki ingest (still pending from Day 2)
- [ ] Decide idea storage platform
- [ ] Decide brand-identity post slot (Day 5 vs Day 7)
