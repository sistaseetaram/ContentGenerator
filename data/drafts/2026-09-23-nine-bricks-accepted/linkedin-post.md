# Wed 2026-09-23 — LinkedIn — Build Receipts

**Slot:** content-calendar.json → Wednesday 2026-09-23
**Title:** Nine Bricks Studio accepted it
**Format:** document carousel (chosen over video — documents run 1.39x reach vs video 0.86x on personal profiles)
**Angle:** client outcome — third-party validation is the headline, not the render
**Status:** DRAFT. Not published. Not logged to posts.json.

---

## Post body

Nine Bricks Studio accepted the render — after asking for eight rounds of changes.

That second half is the part worth reading.

A three-person practice working across Vijayawada and Hyderabad, a government office chamber, one room off their own construction drawing. They didn't look at the first render and say yes. They marked it up, the way they'd mark up any drawing from any consultant.

A grid ceiling with cassette AC units. Portrait niches on the feature wall. The blinds closed, not open. An L-shaped desk. Specific seating finishes, specific timber on the feature wall.

Eight paid passes later, they took it.

What's worth showing is which of their instructions landed and which didn't. That's the honest shape of this work:

**Finishes, materials and lighting changed every time they were asked for.** Walnut, weave, lighting mood — exactly where the designer put them.

**Moving an existing object did not.** We asked three separate ways for the desk's return leg to move to the window end. It stayed put, three times. Adding a *new* built-in against a wall worked cleanly. Restructuring something already there didn't.

**The closed blinds kept reopening** across five consecutive passes, because an earlier line in the same brief was still asking for daylight through those windows. Two instructions quietly fighting.

None of that is a machine deciding things. Every pass was a designer's note, applied and checked, then handed back. Eight times. The person who knows the building stayed in charge throughout.

That's what accepted looks like here. Not "the AI did it." A practice put their judgement on it and signed off.

---

## First comment (CTA — no links in the body)

> The full chain is the interesting part — eight passes, including the two that made it worse. If you run a studio and want to see it, comment "chain" and I'll send it over.

---

## Hashtags

#ArchitecturalVisualization #InteriorDesign #DesignStudio

---

## Carousel outline (document carousel, 1080x1080)

| # | Slide | Content |
|---|-------|---------|
| 1 | Cover | "Nine Bricks Studio accepted it — after eight rounds of changes." Sub-line: "Vijayawada & Hyderabad · 3-person practice · a government office chamber." |
| 2 | The brief | The designer's actual asks, listed plainly: grid ceiling + cassette AC · portrait niches · blinds closed · L-desk · seating finishes. Caption: "Not our ideas. Theirs." |
| 3–7 | The chain | Five of the eight passes, in order, each captioned with the one instruction that drove it. Use the real filenames' sequence — the chain is legible on disk. Keep one visual language across all five so the progression reads as a progression. |
| 8 | What changed easily | "Finishes, materials, lighting — every time, exactly as asked." |
| 9 | What didn't | "Move the desk's return leg to the window end." Asked three ways. Unchanged three times. Caption: "Adding a built-in worked. Moving an existing object didn't." |
| 10 | The fight in the brief | "The closed blinds reopened five passes running — an earlier line in the same brief was still asking for daylight." |
| 11 | Accepted | The accepted final render, full bleed, no annotation. |
| 12 | Close | "A practice put their judgement on it and signed off. That's the bar." Setu wordmark, clear corner margin. |

**Visual build note:** do NOT hand-build these slides. Run the mandatory Step 0 pre-flight in `.claude/rules/design-taste.md` first. Slide 11 is the payoff — give it the whole canvas and no text on the image. Twelve slides is at the upper end; if the chain slides don't each earn their place, cut to three passes and ship ten.

---

## Five-value check

| Value | Verified | How |
|---|---|---|
| **Work, not tech** | PASS | The headline is a client decision, not an output. No model names, no tooling, no pipeline vocabulary in the body at all — the closest it comes is "passes", which is the language of drawing revisions, not of software. |
| **Quiet over loud** | PASS | No banned words (checked against `setu-voice.md`). The payoff post of the week and it still ends on someone else's judgement rather than on our result. Explicitly refuses the "the AI did it" framing. |
| **Respect owners** | PASS | Copy test applied — and this is the post where it bites hardest. It treats the designer as the expert and us as the consultant being marked up. Two failures are volunteered unprompted. A busy principal reading this is being shown how their own review process would feel, not sold an outcome. |
| **Ship, don't slide** | PASS | The strongest instance in the week: a real practice, a real drawing, eight real paid passes, a real acceptance. Nothing is planned or forthcoming. |
| **Map before build** | PARTIAL — by design | The diagnosis layer sits in Tuesday's post; this one deliberately carries the outcome. What it does carry is the *diagnosis of the edit loop* — which classes of instruction land and which don't — which is the same value applied one layer down. Flagged rather than claimed. |

---

## Grounding notes (read before publishing)

- **"Told us it was good enough to show their own clients and vendors" is NOT wiki-grounded.** That line originates in the already-drafted YouTube opening (`data/drafts/2026-09-16-video-01-control-office/youtube.md`), not in the design-automation wiki. The wiki log (2026-09-12) records only: `OPTION B4 ACCEPTED as the chamber's final render`. The brief for this task states the render is cleared for social by the studio's designer. **The draft claims acceptance and social clearance only, and stops there.** If the clients-and-vendors line is true, get it in writing before it goes on either the post or the video.
- **"Eight passes" is accurate, but it was not one straight chain.** Wiki log 2026-09-12: "EIGHT paid refine passes (v1→v3 on option A, drafts B→B4 on option B)" — two parallel options, eight passes total, ending on the accepted B4. The calendar describes it as a single sequence "ending on the accepted Draft B4". The draft says "eight paid passes" and "eight times" without asserting a single unbroken chain. **The carousel must not fake a straight-line progression across two options.** Present them as two options if slides 3–7 can't be drawn honestly from one.
- **The accepted B4 file is not obviously named on disk.** `05-notes/renders/` holds the control, the photoreal and a seven-deep refine chain; `05-notes/bakeoff-round3/` holds the two round-3 candidates, the texture-swallow failure and `compare.html`. Locate the actual accepted B4 image before building slide 11. `compare.html` reportedly carries the full lineage.
- Grounded claims, all from wiki log 2026-09-12: the designer's brief items (grid ceiling + cassette AC, portrait niches, blinds, L-desk); "edit models re-skin surfaces but will not restructure objects" — the L-desk return leg asked three ways and unchanged each time, while adding wall-hugging built-ins worked; the blinds changing state across five refine passes due to a base-prompt daylight conflict.
- **Omitted deliberately:** the President's name and the emblem/portrait arrangement recorded in the wiki. Cleared permission covers "government office", the firm name and the floor plan — it does not obviously cover naming the office's occupant or its insignia layout. Also omitted: the warm/pink colour cast by pass seven (true, but three volunteered failures in one post tips from honest into self-flagellating; hold it for the Week 2 failure post).
- No time figures. No cost figures. No ROI. The ~$2.55 / ~26-call figure is cost-to-run, not client savings, and is omitted entirely per the honesty constraint.
