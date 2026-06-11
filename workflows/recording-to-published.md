# Recording → Published — the end-to-end automation runbook

The conversational pipeline the project was built for: **drop a recording → say "I dropped X" →
one plain-English checkpoint → published + drafted, with no time sitting in an editor.**

This runbook is the contract. It runs in the **main thread** today (orchestrator + `video-studio`),
and is the exact sequence the future **executive agent** will execute unattended. Every stage is an
existing piece with a file-in / JSON-out contract — nothing here is hand-waved.

Proven manually end-to-end on **post-009** (2026-06-11).

## Trigger

User says **"I dropped a recording in X"** (or drops a file in a known intake folder and says so).
No always-on watcher. The orchestrator runs `tools/intake_dispatch.py dispatch` → finds the newest
unprocessed file by mtime, ffprobes it, resolves `<intent>-<structure>` profile, writes the packet to
`data/intake-latest.json` + `data/reports/`. Intake folders + conventions: `workflows/recording-intake.md`.

## The chain (each arrow = a file/JSON contract)

```
"I dropped X"
  → intake_dispatch.py            → data/intake-latest.json  {source.path, intent, profile, probe, flags}
  → video-studio (edit)           → <footage>/edit/  (master_16x9.mp4, transcript, sections)
        • normalize/enhance: VideoEditorHyperframes/video-use/helpers/{normalize_master,enhance_master}.py
        • brand headless build:  workflows/setu-headless-video-style.md (Architect's Draughting)
        • OR camera profiles:    video-use/profiles/{brand,neutral}-{talking-head,screencast}.json
  → ░░ CHECKPOINT (the ONE human gate) ░░  plain-English cut+style plan → Slack DM → WAIT for "go"
  → render + derive               → edit/final_16x9.mp4 (+ final_1x1.mp4 letterbox for LinkedIn)
  → loom-to-multipost             → data/drafts/<date>-<slug>/ {linkedin-post.md, youtube.md, report.json}
        • copy via tools/model_router.py ; title via youtube-packaging skill ; five-value gate
  → ░░ REVIEW (human) ░░          approve the drafts
  → publish                       → publishing-sop.md  (YouTube unlisted-first; LinkedIn via Supergrow)
  → log                           → data/posts.json  + data/reports/YYYY-MM-DD/
```

## The two human gates (locked decisions — keep them)

1. **Checkpoint** (before render): one plain-English cut+style plan to Slack DM. Never cut/render before "go".
2. **Review** (before publish): human approves the drafts. **No auto-publish, ever.**

Everything between the gates is unattended. The point is zero editor time, not zero judgement.

## Intent gating (brand vs neutral)

- **brand** (Setu / proof / ICP): restraint. Headless = Architect's Draughting; camera = no punch-zooms.
  Hook + structure from brand voice + the video's true content — never trend-chasing. Five-value gate.
- **neutral** (other projects): relaxed brand, zooms OK, founder-tag outro, optional visibility engine
  (research top creators → adapt hooks/retention). Separate path; brand path ignores it.

## Quality rules carried from the manual run (don't relearn)

- Section VO: pad the OUT point past the last word; hold last frame to ≥ VO length (else last word clips).
- Stumbles in the take → splice clean spans from a second take, audio-only, **same section length**
  (loudnorm-match → silence-pad / mild atempo). See `setu-headless-video-style.md` → audio correction.
- Derive 1:1 by **letterbox on paper**, not crop. 9:16 only if authored vertical.
- Concat with `aformat=channel_layouts=stereo` per input. Link in **first comment**, shorten via **da.gd**.

## GATE — executive agent is BLOCKED until every loop is individually tested (user decision 2026-06-11)

Do NOT build the executive agent until each ContentGenerator loop has been run + verified standalone:
`content-ideator`, `linkedin-analyzer`, `loom-to-multipost`, `youtube-packaging`, the video pipeline,
`loom-walkthrough-recorder`, `loom-video-analyzer`. A loop that hasn't run is an untested contract; the
orchestrator must only chain proven loops. Complete + test all loops → THEN build + connect the agent.

## Executive-agent readiness (Phase 6 — build LAST, after the gate above)

Each stage already takes file inputs and emits JSON. The executive agent (in
`/Users/sistaseetaram/Desktop/Claude/Claude Executive Agents/`) will:
read `intake-latest.json` → drive `video-studio` → post the checkpoint → on approve, render →
call `loom-to-multipost` → post the review card → on approve, run `publishing-sop` → log.
It orchestrates; it does not re-implement any stage. **Do not build the executive agent until the
checkpoint + review gates are reliable in the main-thread flow.**

## Status

- ✅ intake_dispatch.py · video-use helpers · profiles · setu-headless-video-style · loom-to-multipost ·
  youtube-packaging · publishing-sop — all exist, all proven on post-009 (manually).
- ⏳ Slack checkpoint + review cards — currently the human is in the chat loop; wire to Slack DM next.
- ⏳ executive agent — last.
