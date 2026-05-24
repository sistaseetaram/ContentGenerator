# ContentGenerator — Project

## What This Is

Personal-brand content production system for Seetaram (founder face on Setu agency). Posts daily on LinkedIn, X, YouTube, Instagram. Self-improving loop: post → metrics → weekly audit → pillar-mix shift → next week. Extracts into reusable `content-engine-bootstrap` skill by Day 30.

## Core Value

Ship content Day 1 with minimum tooling. Learn what works via metrics. Replace Blotato with owned skills within 30 days. Generalize into `content-engine-bootstrap` for new users (sister, future clients).

---

## Requirements

### Validated (locked — do not change without explicit decision)

- **Platforms:** LinkedIn (primary B2B), X (daily takes), YouTube (long-form), Instagram (separate funny/family feed). No other platforms without explicit decision.
- **Instagram isolation:** funny/sarcasm/roasting ONLY. No Setu mentions, no informative content, no cross-posts from B2B pillars.
- **Model routing:** every model call through `tools/model_router.py`. No direct SDK calls.
- **Voice-first:** every draft passes Setu voice rules. Banned: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses to unlock potential". Short sentences. Real hours, real money. Outcome first.
- **Orchestrator never drafts directly:** always dispatch sub-agent with locked context (pillar + wiki + recent metrics).
- **Skill report emission:** every skill emits JSON report to `data/reports/YYYY-MM-DD/{skill}-{ts}.json`.
- **Wiki ingestion:** every research/scrape output ingests to Obsidian wiki via `llm-wiki-ingest`.
- **Data logging:** every post + metric logs to `data/posts.json` + `data/metrics.json`.
- **Secrets never echo in chat.**

### Active

- Build Receipts pillar: 2/wk LinkedIn, 1/wk X thread, 1/wk YT short, 1/wk Loom
- Plain-English AI Takes: 1/wk LinkedIn, daily X
- Build-in-Public Setu: 1/wk LinkedIn
- Funny/sarcasm IG feed: 2-3/wk Instagram (isolated)

### Out of Scope (held)

- Contrarian pillar: activates Week 3+
- ROI Case Studies: activates when first client metrics land
- TikTok / Threads / Facebook / Reddit / Bluesky — dropped from Blotato scope
- Content Executive Agent: Phase 4 (Day 22-30)

---

## Key Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-23 | Blotato deferred to Day 15 build | Supergrow AI (MCP) used Days 1-15; evaluate Day 15 |
| 2026-05-23 | Platform scope locked: LI + X + IG + YT only | Blotato offers 9 platforms — TikTok/Threads/FB/Reddit/Bluesky dropped |
| 2026-05-23 | Model router required for all calls | Fallback chains: Sonnet→GPT-4o→DeepSeek-V3 for long-form |
| 2026-05-23 | Instagram = separate audience (friends/family) | No informative/promo content — purely personal/funny |
| 2026-05-23 | WAT framework inherited from Nate CLAUDE.md | Workflows / Agents / Tools file layout |

---

## Constraints

- Daily Claude budget: $5/day circuit breaker in `model_router.py`
- Skills self-contained: SKILL.md + scripts + references per skill
- SKILL-REGISTRY.md append required on every new skill creation
- Brand wiki at `/Users/sistaseetaram/Documents/Obsidian Vault/content-wiki/` — read `setu-positioning.md`, `setu-voice.md`, `target-audience.md` every session
- YT transcript summarization: DeepSeek-V3 / GPT-4o-mini ONLY — never Claude (user rule)

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Long-form drafting | Claude Sonnet 4.6 → GPT-4o → DeepSeek-V3 |
| Short posts | GPT-4o-mini → Gemini 2.5 Flash → Haiku 4.5 |
| Multimodal | Gemini 2.5 Flash → GPT-4o vision → Sonnet 4.6 vision |
| Transcription | Whisper → Deepgram Nova-3 → AssemblyAI |
| Lint/dispatch | Haiku 4.5 → GPT-4o-mini → Groq Llama 3.3 |
| Auditor | Sonnet 4.6 → GPT-4o → DeepSeek-V3 |
| Publishing (Days 1-15) | Supergrow AI (MCP) |
| Publishing (Day 15+) | `tools/linkedin_post.py` + direct platform APIs |
| Scheduling/calendar | Blotato (Day 15+ build) |
| Wiki | Obsidian + `llm-wiki-ingest` |
| Carousel | `canvas` skill |
| Brand tokens | `northstar` skill |
