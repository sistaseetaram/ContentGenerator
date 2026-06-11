---
name: loom-to-multipost
description: Turn ONE finished/approved video into review-ready posts for the locked platforms (YouTube + LinkedIn). Derives the right aspect per platform, drafts copy via model_router, titles via youtube-packaging, runs the voice + five-value gate, lands drafts in data/drafts/, emits a JSON report. Never publishes — hands off to publishing-sop.md for human-approved publish. Triggers: "repurpose this video", "draft posts from this video", "loom to multipost", "make the posts for this video", "turn this into posts".
---

# loom-to-multipost — one video → review-ready posts (YouTube + LinkedIn)

Codifies the proven post-009 flow. This skill DRAFTS; a human reviews; `publishing-sop.md` publishes.
Orchestrator never drafts copy directly — this skill dispatches the model via `tools/model_router.py`.
**Platforms locked: YouTube + LinkedIn only.** IG/X excluded (hard rule).

## Inputs

- The approved/edited **video** (16:9 master) — path, or from `data/intake-latest.json` → `source.path`/edit output.
- Its **clean script** (transcript with stumbles corrected) — e.g. `…/edit/transcripts/clean_script.txt`.
  Build it from the mlx-whisper JSON: join word `text` with `' '` (no trailing spaces in tokens),
  collapse space-before-punctuation, apply any audio corrections already made.
- **intent** (`brand` | `neutral`) + **slug** + **date**. Brand = restraint, ICP voice, five-value gate.

## Steps

1. **Derive formats** (per `setu-headless-video-style.md` / `publishing-sop.md`):
   - YouTube = the **16:9 master**.
   - LinkedIn = **1:1 letterbox on paper** (`scale=1080:-2,pad=1080:1080:0:(oh-ih)/2:color=0xf2f2f0`) —
     NOT center-crop (wide diagrams lose labels). Skip 9:16 unless the piece was authored vertical.
2. **Draft LinkedIn post** — dispatch a content sub-agent (or inline) calling `route("long-form", …)`.
   Strong first line, tight body in Setu voice, scannable beat, soft CTA. ~120–220 words. 0–3 hashtags.
   Ground in `clean_script.txt` + wiki voice/values/positioning/target-audience.
3. **Draft YouTube** — `route("long-form", …)` for the description (first 2 lines = the hook before
   "…more"; include the body's key beats + CTA + who-it's-for). Title + tags via the **`youtube-packaging`**
   skill (research-backed, no clickbait, ≤60 chars, lead with the truest specific hook).
4. **Voice + FIVE-VALUE gate** — before writing files, run the copy through the copy test
   (*"respected or sold to?"*) and all five values (work-not-tech · quiet-over-loud · respect-owners ·
   ship-don't-slide · map-before-build). State which were checked. Banned words list applies.
5. **Write drafts** → `data/drafts/<date>-<slug>/`:
   - `linkedin-post.md`, `youtube.md` (3 title options + recommendation, description, tags),
     `report.json` (platforms, drafts[], models_used[], five_values_checked[], notes).
   - For a CTA link: keep the LinkedIn body **link-free**, plan the link for an **auto first-comment**
     (best reach); shorten via **da.gd**, never TinyURL (viglink wrap). See `publishing-sop.md`.
6. **Hand off** — do NOT publish. Point the user to `publishing-sop.md` for review → publish
   (YouTube unlisted-first via `tools/youtube_upload.py`; LinkedIn via Supergrow MCP).
7. **Log** — append the post to `data/posts.json` only after the human publishes (status + URLs).

## Output / report (contract for the executive agent)

Emit `data/reports/YYYY-MM-DD/loom-to-multipost-{unix-ts}.json` per `templates/skill-report.md`.
`run_id` = `l2m-{unix-seconds}`. Populate `model_calls[]` from each `route()` return. `outputs` →
the `data/drafts/<date>-<slug>/` dir + the derived video paths. `status` = success / partial / failure.
File-in / JSON-out so the future executive agent can chain: intake → edit → **loom-to-multipost** → publish.

## Guardrails

- Brand intent: restraint wins — hook + structure come from the brand voice + the video's true content,
  never from trend-chasing. Neutral intent (other projects): visibility engine allowed (separate path).
- Never invent stats/quotes. Numbers come from the script (real hours, real money).
- Drafts only. Human approves. No auto-publish, ever.

## Proven reference

post-009 (2026-06-11) "Why Design Firms Lose a Month a Year to Unpaid Work" — this exact flow:
clean_script → `route("long-form")` LI post + YT desc → `route("short-post")`/youtube-packaging title →
1:1 letterbox derive → YouTube (public) + LinkedIn (native video + first-comment Gem link `da.gd`).
