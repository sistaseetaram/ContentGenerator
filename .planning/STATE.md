# ContentGenerator — State

## Project Reference

**Building:** Self-improving personal-brand content engine (Setu)
**Current focus:** Phase 1 — Ship first posts, establish baseline metrics

---

## Current Position

- **Phase:** 1 of 4 — Ship + Sense (Days 1-7)
- **Plan:** Skill-build track (decoupled from posting calendar). Shipped: loom-walkthrough-recorder (05-28), loom-video-analyzer (05-30), content-ideator v0.2 (05-31).
- **Day:** 7 of 30 (in progress)

**Progress:** `[█████░░░░░]` ~30%

Plans complete: 1/6 in Phase 1 (01-01 scaffold done; 01-02 first posts wave 1 done — 3 posts published)
Skills shipped: 3 (loom-walkthrough-recorder v0.1, loom-video-analyzer v0.1, content-ideator v0.2)
Total phases complete: 0/4

---

## Recent Decisions

- Supergrow AI (MCP) replaces Blotato for Days 1-15 publishing
- Blotato deferred to Day 15 build (API key obtained)
- Platform scope locked: LinkedIn, X, Instagram, YouTube ONLY
- Instagram = isolated funny/family feed — no B2B content
- Post sequencing locked: values post before fallback-chains post. Post-001 (tech) → Post-002 (visual brand) → Post-003 (values) → Post-004 (Loom). Fallback chains post pushed to week 2.
- Post-003 slot = Setu brand values post (from `setu-brand/03-collateral/linkedin/brand-carousel/setu-brand-values-current-work.png`) — to be drafted + posted manually by user today
- All posts manual for now (user posts directly, not via Supergrow MCP)
- **2026-05-31:** `.env` wired — all 5 keys (ANTHROPIC, OPENAI, GOOGLE, DEEPSEEK, GROQ) confirmed `<set>`. Router live.
- **2026-05-31:** Model stack — Gemini 2.5 Flash now PRIMARY for `long-form` + `auditor` (Sonnet → last-resort fallback). Verified: Gemini Pro sub ≠ API credits; Groq free tier only on direct API (not OpenRouter). Cost table corrected ($0.30/$2.50 per M).
- **2026-05-31:** ClickUp/Airtable DROPPED — Slack DM routine covers live progress visibility.
- **2026-05-31:** New CLAUDE.md "Strategic Advisor Mandate" — never rubber-stamp; honest critique on every idea, brand-stage-aware.

---

## Pending Todos

- ✅ Day 1 LinkedIn post published: post-001 (Build Receipts — "Same project. Third version.")
- ✅ Day 3 post-002 (Build-in-Public) published manually by user — URL logged
- ✅ post-003 (Plain-English AI Takes — model fallback chains) drafted, scheduled Day 5
- ✅ content-calendar.json Week 1 locked
- ✅ Major brainstorm reframe captured: ideator = research engine, creator = generation engine (separate)
- ✅ Day 6: loom-walkthrough-recorder v0.1 built + dogfooded (prep packet at `data/loom-preps/2026-05-28-n8n-3-versions.md`)
- ✅ SKILL-REGISTRY.md updated — row: `local:ContentGenerator:loom-walkthrough-recorder`
- ✅ templates/skill-report.md created (JSON schema for all skill reports)
- ✅ post-003 published: Setu brand values post — https://www.linkedin.com/posts/sista-seetaram_aiadoption-workflowautomation-share-7465485954850549760-5YWg/
- [ ] **TODAY:** Record n8n 3-version Loom using prep packet (`data/loom-preps/2026-05-28-n8n-3-versions.md`), post to LinkedIn, capture URL in `data/posts.json` as post-004
- ✅ content-ideator v0.1 built (storage=local JSON+dashboard; 7 beats incl own-stack miner; 7-dim rubric; research-summarize chain free-first Groq→Gemini→DeepSeek).
- ✅ **content-ideator v0.2 (2026-05-31):** `.env` wired (5 keys set, router live). Gemini Flash now primary for long-form+auditor. Added **Schedule mode** (Phase 11 — Sunday weekly calendar from backlog+analyzer+cadence → `data/content-calendar.json`, starts NEXT WEEK) + **Strategic Critique** (every idea gets verdict post_now/post_later/drop + honest reason, shown ON DASHBOARD not chat). New `strategic_opinion` field in ideas-schema; dashboard has verdict column + filter.
- ✅ **Dashboard 2-tab (2026-05-31):** Ideas tab + **Published tab** (reads posts.json status=published → Date · platform · pillar · topic · live link, newest first, platform/pillar/search filters). `build_dashboard.py` now loads posts.json too (`--posts` flag).
- [ ] **DOGFOOD: first `run ideator` (Generate mode)** — router now live; eyeball quality, tune v0.3.
- [ ] **NEXT skill: tech-stack auditor** (unnamed) — task→model→agent spec + cost-cut suggestions; writes report ideator's own-stack miner consumes. Report path TBD by user (local + Drive-latest + Obsidian-ingest).
- [ ] Wire CronCreate: Sunday weekly-schedule auto-run + every-2-day ideator run.
- [ ] NOTE: 7 legacy ideas in ideas.json (from loom-video-analyzer) lack `strategic_opinion` — empty verdict cells until re-scored.
- [ ] Then: content-creator (consumes data/ideas-latest.json) — the generation engine
- [ ] After: linkedin-analyzer (Supergrow metrics → engagement signal → pillar weights)
- [ ] After analyzer: loom-to-multipost
- [ ] v0.2 of loom-walkthrough-recorder: wire model_router.py calls (long_form for outline, short_post for hook)
- ✅ Idea storage decided: local JSON + HTML dashboard. ClickUp/Airtable dropped (Slack DM covers visibility).
- [ ] Decide brand-identity post slot: Day 5 vs Day 7
- [ ] Confirm volume ramp timing — Sabrina-mode by 2026-06-10 (decide after analyzer ships)
- [ ] Ingest Day 1/2/3 decisions to Obsidian wiki via `llm-wiki-ingest`

---

## Blockers / Concerns

- None active

---

## Session Continuity

Last session: 2026-05-31
Stopped at: content-ideator v0.2 shipped — `.env` wired (router live on Gemini Flash primary), Schedule mode + Strategic Critique added. ClickUp dropped.
Resume:
  1. **Dogfood `run ideator`** (Generate mode) — first live router run; eyeball idea quality + costs.
  2. Then build tech-stack auditor skill (own-stack miner consumes its report; path still PLACEHOLDER).
  3. Wire CronCreate for Sunday weekly-schedule + every-2-day ideator runs.
  4. Weekly Schedule mode goes live NEXT WEEK (this week + Week 3 already planned manually).
How the user wants ideator to run (locked 2026-05-31):
  - From next week: ideator picks ideas from backlog using analyzer output + past posts; builds weekly schedule every Sunday.
  - User drops raw ideas into dashboard anytime → ideator scores + critiques (post now/later/drop + why), brand-stage-aware. Critique shown ON dashboard, not pushed to chat.
Plan/save file (this session): /Users/sistaseetaram/.claude/plans/so-prepare-everything-that-floofy-emerson.md
Session-clear-safe: all skill files + router + .env on disk; STATE captures next steps. (`.env` gitignored — keys NOT committed, live only on this machine.)

---

## Phase 1 Checklist

- [x] 01-01: Day-1 Scaffold (DONE — committed 2026-05-23)
- [ ] 01-02: First Posts — 3 Pillar 1 options, publish 1, log, Week 1 schedule
- [ ] 01-03: content-ideator + loom-walkthrough-recorder skills (Day 3)
- [ ] 01-04: First Loom recording (Day 4)
- [ ] 01-05: loom-to-multipost + metrics_fetch.py (Day 5)
- [ ] 01-06: Day-7 checkpoint — tech-stack revisit + wiki health
