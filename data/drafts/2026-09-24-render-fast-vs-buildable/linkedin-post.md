# Thu 2026-09-24 — LinkedIn — Contrarian

**Slot:** content-calendar.json → Thursday 2026-09-24 (idea-011)
**Title:** An AI render in under a minute is easy. A render you can build from is the hard part.
**Format:** TEXT only — no carousel, no image
**Angle:** contrarian — the whole category, us included, is measuring the wrong thing. Earned by Tue (method) and Wed (client acceptance) landing first.
**Status:** DRAFT. Not published. Not logged to posts.json.
**Body length:** 1,885 characters (LinkedIn limit 3,000; house target 1,400–1,900).

---

## Post body

A photoreal interior out of an AI tool takes under a minute. That part is solved.

Whether you can build from it is another question. The category has quietly answered it.

The leading AI render plugin for Revit and SketchUp ships a Geometry Override Slider — a dial that lets the model move away from your model. That is the headline feature: creative range, not fidelity.

A plan-generation tool sells five human-validated plan uploads a month as its paid tier. The human check is the product.

Nobody here claims your drawing survives the render. They price around the fact that it might not.

I would rather not stop there, because we have the same problem.

We score every render against the plain grey 3D model of the room — the geometry the drawing says is true. Higher score, closer to the plan. Last week we ran it across four renders of a government office chamber for Nine Bricks Studio, a three-person practice in Vijayawada and Hyderabad.

The highest score went to a render that had done nothing: it handed our own grey massing back, re-shaded, every material instruction ignored. It scored 0.79 — the most faithful image of the set, and the worst.

The render the studio actually accepted, after eight rounds of their own changes, scored 0.52. The lowest of the set.

Our number does not rank images the way a designer does. It never did.

What it is good for is a floor. Below a threshold something is structurally wrong — a wall moved, a doorway closed — and the image goes no further. Above it, the number stops having an opinion and a person takes over.

That matters if you are signing off. A fidelity score presented as a ranking does not mean what it looks like. Ask what it blocks, not what it awards.

The whole pilot cost eleven cents. Being wrong cheaply is most of the job.

Fast renders were never the hard part. Knowing which one you can hand to a site is.

---

## First comment (CTA — no links in the body)

> The four-render comparison, scores and all — including the one that scored highest by doing nothing — is more convincing than the summary. If you run a studio and want to see it, comment "score" and I'll send it across.

---

## Hashtags

#ArchitecturalVisualization #AIinArchitecture #DesignStudio

---

## Visual / asset note

**No image on this post. Text only, by choice.**

Thursday follows two consecutive document carousels (Tue method, Wed acceptance). A third visual in a row flattens the week and pushes this one toward looking like promotion. The argument is carried by two numbers in plain sentences — 0.79 for the worst output, 0.52 for the accepted one — and an image would explain less than the sentence does.

If a visual is later judged necessary, it must not be hand-built: run the mandatory Step 0 pre-flight in `.claude/rules/design-taste.md` (load `content-wiki/wiki/index.md` → `syntheses/design-pipeline.md`, then real tokens from `MyPersonalBrand/setu-brand/03-collateral/assets/brand-kit/tokens/setu-tokens.json`) before a single pixel. Setu is monochrome-per-theme; there is no accent colour.

---

## Five-value check

| Value | Verified | How |
|---|---|---|
| **Work, not tech** | PASS | No model names, no library names, no API references in the body. The competitor products are described by what they do for a studio — a dial, a paid human check — not by their stack. The one technical object in the post, the fidelity score, is explained entirely as "how close to the drawing", which is all an owner needs from it. |
| **Quiet over loud** | PASS | No banned words (checked against `setu-voice.md`: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses…" — none present). No emoji. The contrarian pillar's standing risk is smugness; the post defuses it by turning the same criticism on our own metric four lines after raising it, and never claims we solved what the category hasn't. |
| **Respect owners** | PASS | Copy test applied. The reader is handed a test they can run on any vendor — "ask what it blocks, not what it awards" — and then left to use it. No "most studios don't realise". The competitors are described accurately and without contempt; one is explicitly credited for being honest about what it sells. |
| **Ship, don't slide** | PASS | Every number is from a paid pilot that ran on a real client's room, including the number that makes us look worst. Competitor claims were read off live pages on a dated verification pass, not recalled. |
| **Map before build** | PASS | The post is a measurement audit — it checks whether our own instrument means what we assumed, before anyone relies on it. Finding that the metric is a floor and not a ranking *is* the map step, performed on ourselves in public. |

---

## Grounding notes (read before publishing)

- **The core claim — a fidelity score that ranks backwards — is from `experiments/fallback-render-tier-pilot`** (type: experiment, verdict `failed`, created/updated 2026-09-20). Exact figures: highest arm **0.7885** ("Pass-through — the massing re-shaded, every material instruction ignored"); **accepted B4 final 0.5216**. The wiki's own first finding is paraphrased closely: "`covered_ratio` does not rank images the way the designer does… Coverage is a floor to clear, never a ranking." Rounded to 0.79 and 0.52 in the body for readability — give the full figures if anyone asks in comments.
- **"The whole pilot cost eleven cents" is grounded** — same file: "Total spend: ~$0.11 across four renders." This is **cost-to-run, on our side, on our own test**. It is not a client saving and must not be re-framed as one in any reply.
- **The unstated premise is `syntheses/image-models-treat-plan-as-mood`** (status CONFIRMED, confidence **high**, last reviewed 2026-06-23): "No amount of prompt engineering or whitebox conditioning makes today's text-to-image / image-edit models preserve a floor plan's geometry well enough to present." Supporting failure set: `experiments/render-faithfulness-sweep` — seven escalating tests, all seven failed the trust bar ("mirrored sides, dropped pooja, invented doors, sealed dining opening"). **Neither is asserted in this draft.** Monday's post already carries the failures; repeating them would make Thursday a rerun.
- **Competitor claims are from `entities/competitor-landscape`** (created 2026-09-16, "verified against live pages on 2026-09-16"): Veras "Geometry Override Slider… explicitly lets the AI diverge from the source model"; Maket.ai "$100/mo Pro… 5 human-validated plan uploads monthly". **Named brands are deliberately not used in the body** — "the leading AI render plugin for Revit and SketchUp", "a plan-generation tool". A named list reads as a hit-piece and the brief rules that angle out. The descriptions stay specific enough to be checkable.
- **CUT on length and tone: the Enscape seat price** ($574.80–$730.80 per seat/year, same source, grounded and public). It was in an earlier pass. Two market examples make the pattern; a third plus a second dollar figure tipped the opening into a pricing comparison and pushed the body over the 1,900 ceiling. Recorded rather than dropped silently — it is available if a reviewer wants the third example back, at the cost of another trim elsewhere.
- **CUT on the same grounds: Maket's $100/mo price.** The persuasive content is "they charge for the human check", not the number.
- **CUT for lack of grounding — Higharc's funding.** The ~$169M figure is unverified and contradicted by the company's own About page ($78M). Not used in any form, not even as "well-funded", because the sentence it would have supported was doing no work.
- **CUT for lack of grounding — the "$300–2,500 per image US/EU" market rate.** Sourced from a search-engine AI summary and flagged do-not-publish in the research pass. Dropped entirely. It would have been the strongest hook available and it is not usable; the metric finding replaces it and is better evidence anyway.
- **NOT described anywhere: a ControlNet or control-model stage.** Removed from the codebase 2026-09-20. The flat-shaded whitebox IS the control image — which is why the body says the score is taken "against the plain grey 3D model of the room" and stops there.
- **NOT repeated: the flux-canny-pro deprecation/licence story.** Retracted on 2026-09-20 as a misread deprecation notice (`model-evals/flux-canny-pro`). Both pilot candidates were rejected by the designer on quality, not licensing, and neither model is named in the body.
- **OMITTED deliberately: the state-emblem failure** recorded in the same pilot (a condensed prompt caused a foreign state emblem and foreign officials' portraits to be rendered into the chamber). It is the most vivid finding in the file. The naming clearance explicitly does **not** cover the office's occupant or its emblem/portrait layout, so it cannot be used. Do not add it back under any rewrite.
- **Nine Bricks Studio, Vijayawada and Hyderabad, "government office chamber", and the eight rounds of changes** are all inside the cleared naming set and consistent with Wednesday's post. The eight passes are described as "eight rounds of their own changes" and are **not** presented as one straight chain — they were two parallel options (A: v1–v3, B: drafts B→B4), per the 2026-09-12 log.
- **Not claimed: "nothing bad reaches a paid render."** The body says only that a below-threshold image "goes no further". Camera validation is logged Priority-1 and still unbuilt; on 2026-09-12 a camera standing inside a wall reached paid renders. If this needs strengthening in a comment, the safe form is "no bad *geometry* reaches a paid render" — nothing wider.
- **Not claimed: that Nine Bricks showed the render to their own clients or vendors.** That line is withdrawn and unverified. The body says only that they accepted it after eight rounds of changes.
- No time figures. No client cost figures. No ROI. The only money in the post is our own eleven-cent test spend.
