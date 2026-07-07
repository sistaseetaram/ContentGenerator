# ContentGenerator — Improvements Note

> Generated: 2026-07-07 (Day-3 connecting-layer sprint, Track C)
> Derived from: brief inspection of commits, STATE.md, ROADMAP.md, CLAUDE.md, data/, tools/, skills/
> Purpose: resume-anchor for whoever picks this project back up. Not a rewrite plan — concrete, actionable items only.

---

## State Drift

- **STATE.md narrative is 26 days stale.** "Current Position" block was reconciled against git on 2026-07-03 but the Pending Todos and Session Continuity sections still describe a world where post-009 was blocked. Git shows post-009 shipped on 2026-06-11. All narrative sections below the header need a truth pass before the next session.
- **ROADMAP.md Phase 1 checkboxes are not in sync with actual commits.** Items 01-02 through 01-06 are unchecked despite the project now being on post-009+. Run a single reconcile pass: check each item against git log and tick/cross it off.
- **Phase tracking has never been advanced.** STATE.md still reads "Phase 1, Day 15 of 30." The real calendar day is Day 45+. Either rebase the plan to the actual date or close Phase 1 and open Phase 2.

---

## Missing Features / Dead Code

- **content-creator skill was never built.** The ideator pipeline produces ideas; nothing consumes them to generate actual post drafts. This is the biggest missing link — every idea in `data/ideas.json` is still waiting for a creator.
- **Ideator Schedule mode (Sunday auto-run) was never wired.** The feature shipped in v0.2 but no cron/routine was created. Either wire it or mark it deferred — a half-shipped feature in a skills file adds confusion.
- **linkedin-analyzer → Slack DM routine wiring was never done.** `data/capture-queue.json` has had overdue captures since at least 2026-06-03. The queue math is right; only the routine-dispatch step is missing.
- **tech-stack auditor skill was listed as "next" three sessions in a row.** It is still not built. The ideator's own-stack-miner beat depends on it. Either build it or remove the dependency from the ideator spec.
- **Model Stack table in CLAUDE.md is marked "revisit Day 7."** Day 7 passed roughly five weeks ago. Run the revisit or remove the note so it does not silently mislead future sessions.

---

## Skill Consolidation

- **Three overlapping loom-* skills should collapse to one.** `loom-walkthrough-recorder`, `loom-video-analyzer`, and `loom-to-multipost` each handle one stage of the same pipeline (record → analyze → repurpose). A single `loom-pipeline` skill with three modes would cut context overhead and prevent drift between the stages. The current three-file setup already has a version-mismatch risk: `loom-walkthrough-recorder v0.2` was listed as a todo but never built.
- **`loom-outreach` in OutreachAutomation vs `loom-video-analyzer`/`loom-to-multipost` here.** The outreach project has its own loom skill for a different purpose (lead personalization from a Loom). Confirm these do not overlap before any consolidation.

---

## Data / Dependency Hygiene

- **Brand voice is duplicated.** `data/gem-instructions/setu-brand-knowledge.md` embeds brand voice inline. `OutreachAutomation/tools/setu_voice.py` embeds the same voice spec independently. The shared context store introduced in this sprint (SharedInfra) is the fix — see `SharedInfra/shared_context/` for the single source of truth.
- **`data/ideas-latest.json` and `data/skills-status.json` are uncommitted and untracked.** Commit them or gitignore them — they are silently missing from every future git clone or fresh session.
- **Obsidian wiki dependency has no fallback.** CLAUDE.md warns that a broken wiki path causes silent off-brand output. Add a health check at session start (one `os.path.exists` call) and surface an explicit warning rather than silently degrading.
- **`data/capture-queue.json` shows 6+ overdue metric captures.** These are post-001 through post-003 Day-3 and Day-7 windows. They are now well past the relevant window (30+ days). Decide: back-fill with whatever data exists, or close them as expired.

---

## Process / Workflow

- **`workflows/tech-stack-revisit.md` exists but has never been run.** It was created as the vehicle for the Day-7 model-stack review. Run it now before resuming content production — the model landscape has shifted since May 2026.
- **`workflows/wiki-health-check.md` has never been run.** The content-wiki index is dated 2026-06-06. If anything was added to the wiki since then, the index is stale.
- **YouTube OAuth token path mismatch.** `tools/youtube_upload.py` saves to `Documents/credentials/.youtube_token.json` but CLAUDE.md mentions `Documents/credentials/YoutubeManagerCreds/`. Verify the canonical path before the next YouTube upload.

---

## On Resume

1. Run the STATE.md truth pass and close Phase 1 in ROADMAP.md.
2. Build content-creator skill (the missing consumer of ideas-latest.json).
3. Wire the Sunday ideator schedule and the Slack capture-queue routine.
4. Run `workflows/tech-stack-revisit.md` — model stack is 6 weeks unreviewed.
5. Register the shared context store adapter (see `shared_context/ADAPTER.md` in this project) to avoid further brand-voice duplication.
