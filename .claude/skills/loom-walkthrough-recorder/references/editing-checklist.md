# Post-Record Editing Checklist

After recording, before posting. Editor: Loom built-in, Descript, CapCut, or Premiere.

Thumbnail design deferred to v2 — out of scope for v0.1.

## Trim
- [ ] Cut intro dead air (anything before first word)
- [ ] Cut outro tail (anything after close line + breath)
- [ ] Remove "uhm" / "so" / "like" filler clusters (target: ≤ 1 per 30s)
- [ ] Remove pauses > 2s unless intentional
- [ ] Remove fumbles (wrong tab, dropped train of thought) — keep one for personality

## Audio
- [ ] Normalize audio level to -16 LUFS (LinkedIn/YouTube standard)
- [ ] Remove background hiss if present (noise reduction pass)
- [ ] Confirm no audio drift / sync issues

## Brand overlay
- [ ] Logo placed top-right per `brand-overlay.md` spec
- [ ] Lower-third name tag inserted 0:02–0:06
- [ ] Terracotta accents on number reveals
- [ ] Beat-boundary color sweeps (1s each)
- [ ] Close lower-third with CTA

## Captions
- [ ] Auto-caption pass (Loom AI / Descript / YouTube auto)
- [ ] Manual review pass — fix names ("Setu" often mis-heard), numbers, technical terms
- [ ] Caption style: white text, black drop-shadow, sans-serif, lower-third position
- [ ] Burned-in for LinkedIn / IG (their players don't toggle CC reliably)
- [ ] SRT export for YouTube (their player handles CC)

## Cut points for repurpose (handled by loom-to-multipost in future)
- [ ] Note 2–3 stand-alone "punch moments" (5–15s clips, work as IG reels / X video)
- [ ] Note 1 carousel-able insight (single-frame quotable)
- [ ] Note the strongest 60s segment (LinkedIn native video upload limit-friendly)

## Pre-publish
- [ ] Final review at 1.0x speed (full watch-through)
- [ ] Final review at 1.5x speed (catch dropped audio, jarring cuts)
- [ ] Test view on phone (most LinkedIn / IG views happen there)
- [ ] Title drafted (≤ 60 chars, hook-first, no banned voice words)
- [ ] Description drafted (hook + 2 lines + CTA + relevant tags)
- [ ] Hashtags chosen (2–4 max, match pillar conventions)

## Publish
- [ ] Loom link copied (for LinkedIn post)
- [ ] MP4 exported (for YouTube + IG)
- [ ] Posted to LinkedIn first
- [ ] Posted to YouTube next
- [ ] URL captured for `data/posts.json` log
