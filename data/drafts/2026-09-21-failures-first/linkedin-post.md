# Mon 2026-09-21 — LinkedIn — Build Receipts

**Slot:** content-calendar.json → Monday 2026-09-21
**Title:** The renders that got it wrong first
**Format:** document carousel
**Angle:** fidelity — reopen the problem with real failures before showing any win
**Status:** DRAFT. Not published. Not logged to posts.json.

---

## Post body

An early render out of our own pipeline pushed the dining area back, pulled the sofa forward, and added two console tables that were not in the drawing.

Nothing in the floor plan asked for any of that.

I'm opening this week with the failures, because the wins don't mean much without them. Three things we watched go wrong, on real project files. None of these are staged.

**The redraw invented furniture.**
We compared the plain 3D model of the space against the drawing the model produced from it. The drift was all in one middle step — a line-art redraw that quietly re-composed the room before the final image was ever made. Not the prompt. Not the plan data. One stage in the middle, rearranging someone's home.

**A reference image ate the output.**
On a government office chamber, we attached a texture swatch so the model would match a material. It returned the swatch itself. Full frame, portrait, no room in it at all.

**A clean control image sealed an opening.**
We fed the model a stripped-back grey 3D view of the space, as honest a guide as we could give it. It walled up a doorway the drawing shows open.

Here is the reason all three happen, in plain terms.

Today's image models read a floor plan as a mood board, not as a contract. They optimise for a plausible room, not for your room. And you cannot fix that by writing a better paragraph, because words can't point precisely at *that wall, this side*.

So the fix was never going to sit inside the model. It had to sit around it.

That's what the rest of this week is about.

---

## First comment (CTA — no links in the body)

> Every one of these is from a real project's own history, including the passes that got worse before they got better. If you want the pass-by-pass comparison for this one, comment "failures" and I'll send it across.

---

## Hashtags

#ArchitecturalVisualization #InteriorDesign #AIinArchitecture

---

## Carousel outline (document carousel, 1080x1080)

| # | Slide | Content |
|---|-------|---------|
| 1 | Cover | "The renders that got it wrong first." Sub-line: "Three real failures from our own pipeline." |
| 2 | Failure 1 — the redraw | Side-by-side: the plain grey 3D model (truth) vs the redrawn line art. Callouts: dining pushed back · sofa pulled forward · two consoles added · side entrances blanked. |
| 3 | Why it happened | One line: "The drift lived in one middle step — a redraw between the model and the final image." |
| 4 | Failure 2 — the swallowed reference | The actual `FAILED-refine-texture-swallow.png`. Caption: "We attached a texture swatch. The model returned the swatch." |
| 5 | Why it happened | "With two images attached, the model matched the reference's shape and treated it as the subject — not as a material." |
| 6 | Failure 3 — the sealed opening | The clean grey control view vs the render. Callout on the doorway that became a wall. |
| 7 | The pattern | "A floor plan is being read as a mood board. Not as a contract." |
| 8 | The consequence | "A render you can't build from is a trap. One wrong wall and the drawing is useless to the site." |
| 9 | Close | "Better prompts were never the fix. Tomorrow: what actually worked, on a real client plan." Setu wordmark, clear corner margin. |

**Visual build note:** do NOT hand-build these slides. Run the mandatory Step 0 pre-flight in `.claude/rules/design-taste.md` (load `content-wiki/wiki/syntheses/design-pipeline.md`, then real tokens from `setu-tokens.json`) before a single pixel. Real screenshots only — slides 2, 4 and 6 must use actual project files, never a recreated "example" failure.

---

## Five-value check

| Value | Verified | How |
|---|---|---|
| **Work, not tech** | PASS | Opens on what happened to a room — furniture moved, a doorway sealed — not on model names. The one model behaviour explained (reference-matching) is translated, not named. No API, no model name, no stack in the body. |
| **Quiet over loud** | PASS | No hype words. No banned words (checked against `setu-voice.md`: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses…" — none present). No emoji. Flat declaratives. |
| **Respect owners** | PASS | Copy test applied: the reader is shown evidence and given the reason, not lectured. No "most studios don't realise…". The failures are ours, not theirs. |
| **Ship, don't slide** | PASS | Every failure is a real artefact from a real project's file history (`FAILED-refine-texture-swallow.png`, the whitebox-vs-lineart compare). Nothing hypothetical, nothing staged. |
| **Map before build** | PASS | The whole post is the diagnosis step — it root-causes *where* fidelity breaks before any solution is offered. The solution is deliberately withheld to Tuesday. |

---

## Grounding notes (read before publishing)

- **The furniture-drift failure is from the residential demo plan, not from the Nine Bricks government office.** Wiki source: `concepts/lineart-redraw-is-the-culprit` (main-door look-north spine: living → dining → family-lounge → sit-out). The draft deliberately says "someone's home" and does not attach it to the client project. Do not let the carousel imply otherwise.
- **The calendar says "two extra couches". The wiki says two *consoles*.** Source: `concepts/lineart-redraw-is-the-culprit` — "added 2 consoles". Draft uses consoles. Stating a wrong object on an artefact is an explicit design-taste failure.
- **Texture-swallow failure IS from the Nine Bricks project** (`references/controlofficeff/05-notes/bakeoff-round3/FAILED-refine-texture-swallow.png`, confirmed on disk). Root cause per the 2026-09-12 wiki log: with two images attached the render model matched the reference's aspect ratio and treated it as the subject.
- **Sealed-opening failure** is from `experiments/clean-whitebox-flux-control` — "even clean whitebox V2 sealed the dining opening". Also residential lineage.
- Client is **not named** on this post by choice. The naming permission is granted, but attaching "Nine Bricks Studio" to a failures carousel invites the wrong read. The name lands Tue and Wed, on the method and the acceptance.
- No time figures. No cost figures. No ROI. Per the honesty constraint the ~$2.55 / ~26-call spend figure is omitted entirely.
