# ContentGenerator — State

## Project Reference

**Building:** Self-improving personal-brand content engine (Setu)
**Current focus:** Phase 1 — Ship first posts, establish baseline metrics

---

## Current Position

- **Phase:** 1 of 4 — Ship + Sense (Days 1-7)
- **Plan:** Skill-build track (decoupled from posting calendar). Shipped: loom-walkthrough-recorder (05-28), loom-video-analyzer (05-30), content-ideator v0.1 (05-30).
- **Day:** 7 of 30 (in progress)

**Progress:** `[█████░░░░░]` ~30%

Plans complete: 1/6 in Phase 1 (01-01 scaffold done; 01-02 first posts wave 1 done — 3 posts published)
Skills shipped: 3 (loom-walkthrough-recorder v0.1, loom-video-analyzer v0.1, content-ideator v0.1)
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
- ✅ content-ideator v0.1 built (storage=local JSON+dashboard; 7 beats incl own-stack miner; 7-dim rubric; research-summarize chain free-first Groq→Gemini→DeepSeek). Needs first dogfood run + .env keys to exercise router live.
- [ ] **NEXT skill: tech-stack auditor** (unnamed) — task→model→agent spec + cost-cut suggestions; writes report ideator's own-stack miner consumes. Report path TBD by user (local + Drive-latest + Obsidian-ingest).
- [ ] Then: content-creator (consumes data/ideas-latest.json) — the generation engine
- [ ] After: linkedin-analyzer (Supergrow metrics → engagement signal → pillar weights)
- [ ] After analyzer: loom-to-multipost
- [ ] v0.2 of loom-walkthrough-recorder: wire model_router.py calls (long_form for outline, short_post for hook)
- [ ] Decide idea storage (at ideator build start): ClickUp / Airtable / Notion / Google Sheets / local JSON+dashboard
- [ ] Decide brand-identity post slot: Day 5 vs Day 7
- [ ] Confirm volume ramp timing — Sabrina-mode by 2026-06-10 (decide after analyzer ships)
- [ ] Ingest Day 1/2/3 decisions to Obsidian wiki via `llm-wiki-ingest`

---

## Blockers / Concerns

- None active

---

## Session Continuity

Last session: 2026-05-28
Stopped at: Day 6 — post sequencing locked (values post = post-003, fallback chains pushed to week 2). Loom recording imminent using prep packet at `data/loom-preps/2026-05-28-n8n-3-versions.md`.
Resume: 
  1. User posts brand values post manually (post-003) — update data/posts.json with URL when done
  2. User records + posts Loom → capture URL as post-004 in data/posts.json
  3. Run Post-Recording Feedback protocol from SKILL.md (3 questions → skill update if needed)
  4. Next build session = content-ideator (lock storage + beats + eval rubric at session start)
Plan file (this session): /Users/sistaseetaram/.claude/plans/sunny-wandering-melody.md
Session-clear-safe: prep packet + skill files all committed to repo; STATE captures next steps.

---

## Phase 1 Checklist

- [x] 01-01: Day-1 Scaffold (DONE — committed 2026-05-23)
- [ ] 01-02: First Posts — 3 Pillar 1 options, publish 1, log, Week 1 schedule
- [ ] 01-03: content-ideator + loom-walkthrough-recorder skills (Day 3)
- [ ] 01-04: First Loom recording (Day 4)
- [ ] 01-05: loom-to-multipost + metrics_fetch.py (Day 5)
- [ ] 01-06: Day-7 checkpoint — tech-stack revisit + wiki health
