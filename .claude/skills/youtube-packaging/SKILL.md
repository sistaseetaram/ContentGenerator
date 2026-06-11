---
name: youtube-packaging
description: Use when titling/packaging a YouTube video for Setu — researches proven title/hook/thumbnail patterns for the niche, adapts them to Setu voice (no clickbait), and recommends one. Triggers: "youtube title", "what should we call this video", "package this for youtube", "thumbnail idea", "youtube hook".
---

# YouTube Packaging — research-backed, Setu-voice-gated

The user is not a content creator and does not want to pick titles blind. This skill
**decides and recommends** — researches what works, adapts it, suggests one. It never
ships clickbait: for a trust-based ICP (architecture/design/construction firm owners),
hype destroys credibility (violates `quiet-over-loud`).

## Process

1. **Read the content.** The video script/transcript (e.g. `…/edit/transcripts/clean_script.txt`)
   + Setu voice/values/positioning from the content-wiki. Find the single strongest, *truest*
   hook beat (usually a specific number or a sharp problem statement).
2. **Research (don't guess).** `WebSearch` proven YouTube title/packaging patterns for the niche
   (educational / B2B / founder / the specific vertical). Optionally look at 2–3 channels actually
   winning in the niche and note their title *structures* (not their words). Verify, cite sources.
3. **Adapt, don't copy.** Map proven *structures* onto the video's true hook, in Setu voice.
4. **Decide + recommend.** Produce 3 titles, recommend ONE with a one-line reason. Plus a thumbnail
   concept (brand-compliant) and the first-2-lines description hook.

## Proven structures that work for trust-based B2B/educational (2026)

- **Problem → outcome:** name the pain + the fix, plainly. "How to [outcome] without [pain]."
- **Specific surprising number:** beats superlatives. "a month a year", "2 hours, not 20" — real, verifiable.
- **System / framework (B2B loves structure):** "The 4 things that…", "The framework we use for…".
- **Authority/credibility lead** where trust is the barrier (finance/law/B2B/design).
- **Specificity over superlatives:** kill "best/ultimate/perfect/insane". Use "the method I used", "the one change".
- Keep ≤ 55–60 chars (mobile), keyword early, optional `[bracket]` for context/tutorial type.
- **2026 reality:** retention ranks more than the title. Title earns the click; the video earns the rank.

## Setu voice gate (mandatory before recommending)

- BANNED: revolutionary, game-changing, disrupt, synergy, cutting-edge, hype, fake urgency, ALL-CAPS bait.
- Copy test: *"Would a smart, busy architecture firm owner feel respected — or sold to?"*
- Five-value filter, esp. `quiet-over-loud` + `respect-owners`. No curiosity-gap lies.

## Thumbnail (brand-compliant)

- Setu tokens only (paper `#f2f2f0`/`#1d1d1b` or terracotta `#1e0f09`/`#f2ddd3`), Cormorant + Inter,
  bridge symbol. No clickbait faces/arrows/neon. Often: pull a strong frame from the video (a
  Cormorant number/line) — e.g. "A month a year. For free." Calm, legible at small size.

## Output

3 titles + 1 recommendation (with reason), thumbnail concept, description first-2-lines hook,
5–8 search tags. Hand to human for the final call (they can override). Log the chosen title with
the post entry in `data/posts.json`.

## Proven example (post-009, 2026-06-11)

Video: "stop working for free in design." Strongest true hook = the rupee math → "a month a year, for free."
Recommended title: **"Why Design Firms Lose a Month a Year to Unpaid Work"** (51 chars) — problem-led +
specific surprising number + zero hype. Chosen over generic "Stop Working for Free".
