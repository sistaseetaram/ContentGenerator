# ContentGenerator — Roadmap

**Milestone:** Personal Brand Content Engine v1.0
**Timeline:** Day 1–30 (2026-05-23 start)
**North Star:** Self-improving content engine that posts Day 1, learns weekly, replaces Blotato by Day 30, extracts into `content-engine-bootstrap` skill.

---

## Phase 1 — Days 1-7: Ship + Sense
**Goal:** Post every day on LinkedIn. Capture baseline metrics. Identify Blotato pain points. Record first Loom walkthrough.

**Status:** IN PROGRESS (Day 1 scaffold complete)

Plans:
- [x] 01-01: Day-1 Scaffold — CLAUDE.md, workflow SOPs, model_router.py, data init, git
- [ ] 01-02: First Posts — draft 3 Pillar 1 options, publish 1, log, schedule Week 1 follow-ups
- [ ] 01-03: Core Skills Build — `content-ideator` + `loom-walkthrough-recorder` skills (Day 3)
- [ ] 01-04: First Loom Recording — record 3-5 min n8n workflow walkthrough (Day 4)
- [ ] 01-05: Repurpose Pipeline — `loom-to-multipost` skill + `metrics_fetch.py` (Day 5)
- [ ] 01-06: Day-7 Checkpoint — tech-stack revisit, `wiki-health-checker` skill, Week 1 review

**Phase 1 success:**
- 7 LinkedIn posts published
- `content-ideator`, `wiki-health-checker`, `tech-stack-monitor`, `metrics_fetch.py` built
- First tech-stack review completed
- First wiki health check completed
- Week 1 baseline metrics in `data/metrics.json`

---

## Phase 2 — Days 8-14: Audit + Repurpose
**Goal:** Wire self-improving loop. Add second platform (X).

**Status:** NOT STARTED

Plans:
- [ ] 02-01: Weekly Auditor — `weekly-auditor` skill, run on Week 1 data (Day 8)
- [ ] 02-02: YouTube Pipeline — `youtube-to-multipost`, record + publish first YT long-form (Day 9-10)
- [ ] 02-03: X Publishing — add X to publishing flow, daily X posts begin (Day 11)
- [ ] 02-04: Trend Watcher — `trend-watcher` skill, daily scan → draft queue (Day 12)
- [ ] 02-05: Week-2 Checkpoint — audit, pillar mix shift per data (Day 14)

**Phase 2 success:**
- Weekly auditor running, first audit report in wiki
- X publishing live, 1 YT long-form published
- `youtube-to-multipost` repurposed first YT video → LI post + X thread
- Trend-watcher producing daily draft queue

---

## Phase 3 — Days 15-21: Clone + Sharpen
**Goal:** Replace Blotato with owned skills. Launch Contrarian pillar.

**Status:** NOT STARTED

Plans:
- [ ] 03-01: LinkedIn Publisher — `tools/linkedin_post.py` direct API + Blotato integration (Day 15)
- [ ] 03-02: X + IG Publishers — `tools/x_post.py`, `tools/instagram_post.py`, IG funny feed begins (Day 16-17)
- [ ] 03-03: Contrarian Pillar — `contrarian-drafter` skill, first contrarian post (Day 18)
- [ ] 03-04: Dashboard — `dashboard-builder` skill, web-artifact metrics dashboard (Day 19)
- [ ] 03-05: Day-21 Checkpoint — Blotato cancel/extend decision, owned stack vs Blotato coverage

**Phase 3 success:**
- At least 1 owned publisher (`linkedin_post.py`) running parallel with Blotato
- Contrarian pillar launched
- Instagram funny feed has 4-6 posts
- Dashboard live as web artifact

---

## Phase 4 — Days 22-30: Generalize + Ship Skill + Executive Agent
**Goal:** Package learnings into `content-engine-bootstrap` skill. Build Content Executive Agent.

**Status:** NOT STARTED

Plans:
- [ ] 04-01: Extract Patterns — reusable templates from Setu execution (brand-brief → pillars → calendar → first post) (Day 22-24)
- [ ] 04-02: Bootstrap Skill — `content-engine-bootstrap` skill, test on fake persona (Day 25-27)
- [ ] 04-03: Content Executive Agent scaffold — project init + context files + morning/evening routine skills (Day 26-27)
- [ ] 04-04: ClickUp Integration — authenticate MCP, `tools/clickup_client.py`, dual-write checklist (Day 27-28)
- [ ] 04-05: Dashboard Renderer + Real Test — mobile HTML dashboard, onboard sister/proxy user (Day 28-29)
- [ ] 04-06: Day-30 Milestone — schedule cron/launchd, 30-day retro post, `content-engine-bootstrap` published globally

**Phase 4 success:**
- `content-engine-bootstrap` in `~/.claude/skills/`, tested on 1 new persona
- Blotato cancel/extend decision made on data
- 30-day retro post published
- All learnings ingested to wiki
- Content Executive Agent live (daily routine running)
