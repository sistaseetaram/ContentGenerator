# ContentGenerator — State

> **RECONCILED 2026-07-03 vs git history.** This file's narrative sections describe the
> state through the 2026-06-06→06-07 session (post-008 published). Git shows one further
> commit since then: `473c28c` (2026-06-11, branch `main`) — "feat: headless-video pipeline
> + publishing + post-009 (Stop Working for Free)" — which shipped the headless-video
> pipeline, the `youtube-packaging` and `loom-to-multipost` skills, three new/updated
> workflows (`setu-headless-video-style.md`, `publishing-sop.md`, `recording-to-published.md`),
> and published post-009. That commit is not reflected in "Current Position," "Pending Todos,"
> or "Session Continuity" below — those sections still show post-008 as the latest and list
> post-009 as a pending blocker. The local branch is also 1 commit ahead of `origin/main`
> (unpushed) and the working tree has further uncommitted changes to `.claude/skills/`,
> `data/*.json`, and `tools/model_router.py`, plus untracked files (`data/ideas-latest.json`,
> `data/skills-status.json`, `tools/dashboard_server.py`, `tools/idea_scorer.py`) — none of
> this is captured in the sections below either. Treat everything past this notice as the
> pre-2026-06-11 narrative, not current state.

## Current Position (git-verified, 2026-07-03)

- **Branch:** `main` (1 commit ahead of `origin/main`, unpushed)
- **Latest commit:** `473c28c` — "feat: headless-video pipeline + publishing + post-009 (Stop Working for Free)" (2026-06-11)
- **Per that commit:** post-009 published (YouTube + LinkedIn); `youtube-packaging` and `loom-to-multipost` skills shipped; headless-video pipeline workflows added.
- **Working tree:** uncommitted modifications (`.claude/skills/content-ideator/*`, `data/content-calendar.json`, `data/ideas-dashboard.html`, `data/ideas.json`, `data/ideator-meta.json`, `data/posts.json`, `tools/model_router.py`) and untracked files (`data/ideas-latest.json`, `data/skills-status.json`, `tools/dashboard_server.py`, `tools/idea_scorer.py`) — not yet committed or described below.

---

## Historical Project Reference (narrative below is current only through post-008 / 2026-06-07)

**Building:** Self-improving personal-brand content engine (Setu)
**Current focus (as of last narrative update):** Phase 1 — Ship first posts, establish baseline metrics

---

## Position as of last narrative update (pre-2026-06-11 commit)

- **Phase:** 1 of 4 — Ship + Sense (Days 1-7)
- **Day:** 15 of 30 (Week 2 complete)

**Progress:** `[███████░░░]` ~50%

Posts published: 8 (post-001 through post-008) — git shows post-009 has since published (commit `473c28c`, 2026-06-11), not reflected in this count.
Skills shipped: 4 (loom-walkthrough-recorder v0.1, loom-video-analyzer v0.1, content-ideator v0.2, linkedin-analyzer v0.1) — git shows 2 more skills shipped since (`youtube-packaging`, `loom-to-multipost`), not reflected in this count.
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
- **Week 1 (May 23–30) DONE** — post-001..004 published. **Week 2 (Jun 1–7) DONE** — already planned manually (`data/ideas.json` week:2 set, status=planned). Ideator does NOT need to schedule Week 1 or 2.
- **Schedule mode = Sundays or manual trigger ONLY.** Never auto-runs on a Generate-mode ideator run. First ideator-built schedule = Week 3 (next Sunday). Generate (ideas) and Schedule (weekly calendar) are separate triggers.

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
- ✅ **linkedin-analyzer v0.1 built (2026-06-03):** measurement + eval engine. Hybrid capture (Supergrow MCP account-trends + manual per-post paste for engagement/demographics — verified Supergrow `get_metrics` is account-level only). 4 modes: ingest · analyze · eval-draft · queue. Tools: `capture_queue.py` (Day3/Day7 due queue from posts.json), `analyzer_rollup.py` (ICP-weighted signals → `data/analyzer-latest.json`, the contract ideator Schedule mode already reads), `post_scorer.py` (SHARED pre-publish scorer, content-creator will reuse). Honesty guard: confidence low until ≥8 posts. Registry row added. Verified: queue math, rollup signals (ICP-weighting ranks correctly), scorer (banned-word + clean paths).
- [ ] **ROUTINE WIRING TODO (user + me):** edit the daily `/schedule` routine prompt → read `data/capture-queue.json`, append due items to Slack DM ("📊 {post_id} Day {day} — View analytics → run linkedin-analyzer ingest"). Run `capture_queue.py` (mode queue) at routine start so queue is fresh. capture-queue.json currently shows 6 overdue captures (post-001/002/003 + post-004 D3 due today).
- [ ] **NEXT skill: content-creator** (consumes data/ideas-latest.json) — the generation engine. Will call `tools/post_scorer.py` for pre-publish eval.
- [ ] After: loom-to-multipost
- [ ] v0.2 of loom-walkthrough-recorder: wire model_router.py calls (long_form for outline, short_post for hook)
- ✅ Idea storage decided: local JSON + HTML dashboard. ClickUp/Airtable dropped (Slack DM covers visibility).
- [ ] Decide brand-identity post slot: Day 5 vs Day 7
- [ ] Confirm volume ramp timing — Sabrina-mode by 2026-06-10 (decide after analyzer ships)
- [ ] Ingest Day 1/2/3 decisions to Obsidian wiki via `llm-wiki-ingest`

---

## Blockers / Concerns

- post-009 (idea-005 — YouTube drop) needs YouTube video URL embedded before drafting
- idea-007 (public Gem) still blocked on user supplying public Gem URL
- Week 3 calendar not yet generated (trigger: ideator Schedule mode, Sunday)

---

## Session Continuity (historical — see git-verified Current Position above for actual latest state)

Last session (as narrated here): 2026-06-06 → 2026-06-07
Stopped at: post-008 published to LinkedIn via Supergrow MCP (10-slide brand-compliant carousel — "Why I'm not showing you any AI renders yet").

**Superseded by commit `473c28c` (2026-06-11):** post-009 (the item listed as "Resume next session" item 1, below) has since been published per that commit's message ("Stop Working for Free" — YouTube + LinkedIn, headless-video pipeline). The "Resume next session" list below was not updated to reflect this and still shows post-009 as outstanding.

### What shipped this session
- **YouTube upload tool** (`tools/youtube_upload.py`) — OAuth2, scopes: upload + force-ssl + readonly. Token saved to `Documents/credentials/.youtube_token.json`. YT1 (n8n workflow Loom) live: https://www.youtube.com/watch?v=bxjpYUX7xpw
- **post-008 carousel** — 10 slides, paper theme, brand-exact tokens (Cormorant 300/500, Inter 400/500, no invented accent color, bridge symbol + wordmark composited). Generator: `.tmp/visuals/post008/gen_carousel.py`. PDF: `.tmp/visuals/post008/carousel.pdf`.
- **Brand process fix** — `design-taste.md` updated with mandatory Step 0: load wiki index → design-pipeline synthesis → verify tokens before any pixel. Root cause of 3× color violation was skipping the wiki. Documented + locked.
- **posts.json** — post-008 logged (status=published, supergrow_post_id set, 10 slides, spatially-correct copy verified vs plan-coords.json).

### Resume next session
1. **post-009 (idea-005)** — YouTube drop post. Needs YT video URL from user → draft + carousel (n8n walkthrough angle). Already have YT1 URL: https://www.youtube.com/watch?v=bxjpYUX7xpw
2. **post-010 (idea-006)** — "Get the basics right before chasing AI." Text-only or minimal carousel. No blockers.
3. **Record YT2** — shot list drafted (6-min talking head "Before You Automate Anything"). User to record.
4. **Week 3 calendar** — run ideator Schedule mode (Sunday trigger). Week 2 complete, Week 3 unplanned.
5. **idea-007** (public Gem) — blocked on user supplying Gem URL.
6. **linkedin-analyzer routine wiring** — capture-queue.json has overdue captures (post-001→008 Day3/Day7 metrics). Wire Slack DM routine.

### Asset locations
- YT credentials: `Documents/credentials/YoutubeManagerCreds/` + token at `Documents/credentials/.youtube_token.json`
- Brand assets (canonical): `claude_projects/MyPersonalBrand/setu-brand/03-collateral/assets/brand-kit/`
- Post visuals: `.tmp/visuals/post008/`
- Wiki index: `Documents/Obsidian Vault/content-wiki/wiki/index.md` → `syntheses/design-pipeline.md` (brand tokens + pipeline)

Plan/save file: /Users/sistaseetaram/.claude/plans/this-is-a-workflow-fluttering-hollerith.md
Session-clear-safe: all tools + carousel generator + .env on disk. `.env` gitignored — keys NOT committed.

---

## Phase 1 Checklist

- [x] 01-01: Day-1 Scaffold (DONE — committed 2026-05-23)
- [ ] 01-02: First Posts — 3 Pillar 1 options, publish 1, log, Week 1 schedule
- [ ] 01-03: content-ideator + loom-walkthrough-recorder skills (Day 3)
- [ ] 01-04: First Loom recording (Day 4)
- [ ] 01-05: loom-to-multipost + metrics_fetch.py (Day 5)
- [ ] 01-06: Day-7 checkpoint — tech-stack revisit + wiki health
