# HANDOFF — Setu content restart: full recon + video-kit eval

**Session:** 2026-09-14 → 2026-09-16, ended at token limit (not user-paused).
**Read this before doing anything else in a new session.** It stands on its own — no need to re-read the source conversation.

---

## 1. Where the real output lives

**The full report + locked plan (473 lines):**
`/Users/sistaseetaram/.claude/plans/i-want-you-to-glistening-yao.md`

Read it in full before acting. It has 6 parts:
- Part 1 — everything that exists (repo, posts, skills, tools, credentials, the demo, the exec agent, the video system, the idea backlog) — all verified against disk/live APIs, not assumed.
- Part 2 — verified 2026 research (ViewStats/YouTube tooling, publishing stack, posting-gap evidence, LinkedIn/YouTube format data) — each claim adversarially fact-checked.
- Part 3 — my honest assessment.
- Part 4 — the locked Week 1–4 posting schedule.
- Part 5 — decisions locked vs. still open.
- **Part 6 — session handoff** (added 2026-09-16): the HyperFrames Student Kit evaluation, competitor wiki writes, and exactly what's unread/unfinished. **Start here.**

**This file (the handout)** is the condensed, standalone version of Part 6 for a fresh session.

---

## 2. The one-paragraph state of the world

Setu (India-based solo AI-automation founder) stopped posting 2026-06-26, 80+ days silent, two unfulfilled promises of a render demo. The demo now exists — one room (a government-office "Control Office" chamber) went plan → photoreal → 8 refine passes → **accepted by the client**, with the studio's designer explicitly clearing it for social. Restart is locked: publish the accepted room first (no ROI numbers, just proof the model held the plan), then a 2–3 room **timed** build in Week 2 generates the real number. Cadence: 5 LinkedIn/wk + 2 YouTube/mo. Publishing path is currently **broken** (Supergrow MCP disabled, no LinkedIn credential) — check Supergrow subscription status first thing.

---

## 3. What was verified and committed this session

### A. Full project recon (28 + 18 = 46 subagents, ~4.1M tokens, all adversarially fact-checked)
Everything in Plan Parts 1–2. Key hard facts, re-confirm if >1 week has passed:
- `data/metrics.json` = `{"metrics": []}` — **zero engagement data ever captured** for any of 11 posts.
- Supergrow MCP is **disabled** in `~/.claude.json` (`disabledMcpServers`). No LinkedIn credential anywhere.
- YouTube OAuth token exists at `~/Documents/credentials/.youtube_token.json` (mtime 2026-06-11) — re-auth-test before relying on it.
- Canon plan path cited in `CLAUDE.md`/`README.md` (`~/.claude/plans/this-is-a-workflow-fluttering-hollerith.md`) **does not exist**.
- `CLAUDE.md` self-contradicts on platform scope (4 platforms vs. 2 in Dispatch Rules).

### B. Competitor intelligence → committed to the design-automation wiki
- `Obsidian Vault/design-automation-wiki/wiki/entities/competitor-landscape.md`
- `Obsidian Vault/design-automation-wiki/wiki/syntheses/verification-is-the-unclaimed-wedge.md`
- Committed: `fc67c0a` in the Obsidian Vault repo.
- **Headline finding:** nobody in the market claims verified plan-geometry fidelity. Veras (category leader) ships a "Geometry Override Slider" — the opposite of fidelity. Closest direct YouTube competitor: **Salmaan Mohamed** (103K subs, India, weekly AI-for-architects videos) — but no one films a real project getting the plan wrong and correcting it on camera. That's the open format.

### C. HyperFrames Student Kit — evaluated, sparse-cloned, smoke-tested
Source: `github.com/nateherkai/hyperframes-student-kit` (MIT license, 833 stars, Nate Herk — the same creator flagged in research as the niche's top YouTube channel).

- **Verdict: not 95% adoptable whole.** ~400 of ~405 MB is Nate's own teaching footage (`video-projects/` + `examples/`). Real IP is ~5 MB.
- **Installed via sparse clone** at `/Users/sistaseetaram/Desktop/Claude/claude_projects/VideoEditorHyperframes/student-kit/` — 8 MB, git history intact (`git pull` to update later), footage folders excluded.
- **Smoke-tested working on this machine, zero npm installs needed** (pure `node:` stdlib + ffmpeg shell-out):
  - `cut-silences.mjs` — took an 8s synthetic transcript to 3.96s (50.5% removed), emitted EDL + retimed transcript.
  - `find-cut-candidates.mjs` — correctly flagged a stutter for review.
- **14 skills gained** that we didn't have: `edit-video`, `cut-silences`, `cut-mistakes`, `video-storytelling`, `hyperframes-video-beats`, `short-form-edit`, `short-form-video`, `make-a-video`, `style-library` (+ `gsap`/`hyperframes-cli`/`hyperframes-registry`/`hyperframes`/`website-to-hyperframes`, which we already had).
- **Keep our own `hyperframes` skill** — it's a superset of theirs (31KB vs 20KB, more references). Only worth pulling from theirs: `references/tts.md` (Kokoro voice table) and the **"Visual Identity Gate"** hard-gate (refuses to write composition HTML without a DESIGN.md — would've caught the 3 brand violations already logged in `.claude/rules/design-taste.md`).
- Version gap noted, not resolved: our hyperframes fork is `0.6.61`; kit pins `0.7.109`; npm latest is `0.8.41`.
- Also gained: 410 motion-graphics cards across 2 style packs (`vox-explainer`, `kallaway`) in `style-library/`.

### D. Commits made this session
- ContentGenerator: `2cf6ef3` — session log only (updates.jsonl).
- Obsidian Vault: `fc67c0a` — the two wiki pages above.
- Nothing else in the repo was touched; `.playwright-mcp/*.yml` scratch files are untracked and harmless, left alone.

---

## 4. What's NOT done — pick up here

### Unread research (18-agent fleet already ran and completed — just needs extraction)
Journal file: `/Users/sistaseetaram/.claude/projects/-Users-sistaseetaram-Desktop-Claude-claude-projects-ContentGenerator/255708d5-3411-432b-bd0c-f79b560a12cd/subagents/workflows/wf_9b201964-93d/journal.jsonl`

Only 2 of 9 tracks were extracted and used (`market-definition`, `content-competitors`). **Still sitting in the journal, unread:**
- `outlier-hunt` — real overperforming videos in the niche, with title/thumbnail pattern analysis
- `keyword-research` — actual YouTube/Google autocomplete phrases, winnable long-tail keywords
- `title-thumbnail` — 10 candidate titles + 3 thumbnail concepts for video #1 (no numbers shown, per the user's correction)
- `script-openings` — 3 full 45–60s opening scripts in Setu's voice + a complete beat-sheet
- `tracking-systems` — the $0 outlier-detection + trend-alert implementation spec (YouTube Data API v3 script design)
- `stay-in-lead` — the defensibility/moat strategy question

To pull them: read the journal.jsonl `result` entries the same way the prior session did (`python3` loop over `json.loads(l)` filtering `type=='result'`, match on `topic`). Do NOT re-run the workflow — it already completed, cached results are free.

### Immediate next actions, in order
1. **Check Supergrow subscription status** (user said they'd check). If active → wire it. If not → build `tools/linkedin_post.py` on LinkedIn's free zero-approval Posts API (`w_member_social` scope — verified this session, no partner review needed for personal-profile text/image/video/document posts).
2. **Extract `title-thumbnail` + `script-openings`** from the journal above → draft video #1's actual script and thumbnail.
3. **Extract `outlier-hunt` + `keyword-research`** → sanity-check the title against real winnable keywords.
4. Wire `~/.claude/skills/video-studio/SKILL.md` (global router) to the new student-kit skills — it currently only knows `video-use` + our `hyperframes`. Add a routing row for `edit-video`, `cut-silences`, `cut-mistakes`, `video-storytelling`, `hyperframes-video-beats`, `short-form-edit`, `style-library`.
5. Decide how to bridge transcription: keep `video-use/helpers/transcribe_local.py` (mlx-whisper, free, offline, already proven) feeding into the kit's node-based cutters via `student-kit/scripts/video-use-to-hyperframes-transcript.mjs` (exists for exactly this).
6. Cherry-pick `tts.md` + the Visual Identity Gate block into our `hyperframes` skill.
7. Re-auth-test the YouTube token before the first upload.
8. Execute Phase 0 (plan Part 4) then Week 1.

### Open questions still genuinely unresolved (not blocking, but real)
- Naming permission: designer cleared showing the render; **naming the firm/client publicly** by name is still not explicitly confirmed — default to describing, not naming, until told otherwise.
- Video #2 content is deliberately unplanned (depends on the demo's in-progress visual redesign) — revisit when that's further along.
- hyperframes version upgrade (0.6.61 → 0.8.41) — not evaluated for breaking changes yet.

---

## 5. Standing facts worth not re-deriving
- Today's date at session end: 2026-09-16.
- ContentGenerator has no other git worktrees. `Artchitectural_design_automation/worktrees/demo-consolidation` does exist (separate project) and was already merged to its `main` as of 2026-09-13.
- Content-exec agent (Haiku, cross-project status/routing) exists at `ClaudeExecutiveAgents/.claude/agents/content-exec.md` but is NOT the strategic-advisor "Content Executive Agent" the CLAUDE.md/ROADMAP describes — that one is still gated per a 2026-06-11 decision until all 7 content loops have run standalone (`linkedin-analyzer` never has).
- The demo lives at `Artchitectural_design_automation` (not a separate "architecture" vs "interior" project — one system, three reference projects: `controlofficeff`, `demo-two-bed`, `arial`).
