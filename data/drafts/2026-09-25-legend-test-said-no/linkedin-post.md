# Fri 2026-09-25 — LinkedIn — Build-in-Public Setu

**Slot:** content-calendar.json → Friday 2026-09-25
**Title:** I thought a symbol legend would help. The test said no.
**Format:** TEXT + one image (single result table)
**Angle:** published negative result — close the week on credibility, not promotion
**Status:** DRAFT. Not published. Not logged to posts.json.
**Body length:** 1,900 characters (LinkedIn limit 3,000; house target 1,400–1,900).
**Revision 2026-09-20:** all F1 figures removed from the post, the table, the value check and the grounding notes, on Seetaram's instruction — F1 on type-multiset detection scores whether the right *kinds* and *counts* of fixtures were found and is blind to *where* they are, which is the only thing a floor plan cares about. The AECV-Bench paragraph is cut. See the grounding notes for what was removed and why.

---

## Post body

I was sure a symbol legend would fix our fixture detection. It made the best model worse.

Before anything is rendered, we have to read your drawing — every door, window and fixture, and where each one sits. Get that wrong and everything after it is wrong, confidently.

We were missing about a third of the fixtures.

The obvious fix: hand the model the symbol legend. This is a WC. This is a wash basin. The way you'd brief a junior.

We tested it. Eight vision models against a verified coordinate file for one plan — 43 fixtures, 15 types. Three conditions: no legend, a 15,000-character text legend, worked examples as images.

Gemini with no legend returned 94 fixture boxes. With the text legend, 33. Ground truth is 43. Fewer guesses, not better ones. Cautious, not accurate.

Qwen did not move. Image examples moved nothing either way. Noise.

Then the finding that mattered.

Pool every model's answers and between them they see almost everything. Ask any two to agree on the same fixture, and it collapses.

They agree something is there. They disagree on where.

So the miss was never a knowledge problem. It is placement and topology — which wall an item belongs to, whether two rooms share a door. Briefing cannot fix that.

It also showed up how we graded ourselves. The score counted whether we found the right kinds of things, in the right numbers. It never asked whether they were in the right place. A decent score and an unusable layout sit together happily.

The conditions: one demo plan, type counts rather than pixel-accurate boxes, the image-example test ran once. Medium confidence, not high. I would not want it quoted harder than that.

What changed: the legend stopped being a prompt and became documentation for the person doing the verification pass.

Published, because the alternative is quietly shipping a fix that does nothing.

That was room 1 of 26 on this floor.

---

## First comment (CTA — no links in the body)

> The full table is eight models across three conditions, including the five I left out of the post. If that's useful to you, comment "legend" and I'll send it across.

---

## Hashtags

#AIinArchitecture #ArchitecturalVisualization #BuildInPublic

---

## Visual / asset note

**One image, two stacked blocks — no scores of any kind.** The table below is rebuilt on raw observables only: how many boxes came back under each condition, and what happens when you ask the models to agree. An honest table *can* be built without a detection score, so the table stays; it just stops reporting grades and starts reporting counts.

**Block 1 — what the legend did to the best model (Gemini)**

| Condition | Fixture boxes returned |
|---|---|
| No legend | 94 |
| 15,000-character text legend | 33 |
| Worked examples as images | — (no box count recorded in the bake-off results) |
| *Ground truth on this plan* | *43* |

**Block 2 — the finding that mattered**

| | Result |
|---|---|
| All eight models pooled | between them, almost every fixture is found |
| Any two models required to agree on the same fixture | collapses |

Caption line under block 2, set small: *They agree something is there. They disagree on where.*

Qwen is not in the table. With the scores gone there is no number for it — "did not move" is a sentence, not a row, and it already lives in the post body. Do not invent a figure to fill the cell.

**Verify before rendering:** the `94 → 33` box counts and the `43 / 15 types` ground truth must be checked against the bake-off's own results file before they go on an artefact. Stating a wrong number on a design is an explicit design-taste failure, and a negative-result post dies if its table is off by a digit.

**Do NOT hand-build this.** Run the mandatory Step 0 pre-flight in `.claude/rules/design-taste.md` first: load `content-wiki/wiki/index.md` → `syntheses/design-pipeline.md`, then pull real tokens from `MyPersonalBrand/setu-brand/03-collateral/assets/brand-kit/tokens/setu-tokens.json`. Setu is monochrome-per-theme — **there is no accent colour**, so the "worse" cell cannot be marked in red. Let the number and a hairline rule carry it. One canvas, one colour world, balanced modular type scale — no tiny-label-next-to-huge-number jump.

---

## Five-value check

| Value | Verified | How |
|---|---|---|
| **Work, not tech** | PARTIAL — narrower than before, but still a deviation | Honest call, kept at PARTIAL rather than upgraded. With every score gone, the only tech surface left in the body is two proper nouns (Gemini, Qwen); every number now describes the *drawing* — 43 fixtures, 15 types, 94 boxes down to 33 — not a model's grade. That is a much smaller deviation than the previous pass. It is still a deviation: naming two vendor models is naming tech, and whether those names stay is an open question with Seetaram, not a settled one. Marking it PASS would quietly close a question he has not closed. The containment argument still holds — the post **opens** on the owner's stake ("get that wrong and everything after it is wrong") and **closes** on a judgement call, with no API names, no library names, no pipeline vocabulary anywhere. If the names are cut later, this row becomes a clean PASS with no other edit required. |
| **Quiet over loud** | PASS | No banned words (checked against `setu-voice.md`: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses…" — none present). No emoji. The headline finding is our own mistake, stated in the first line without cushioning. It claims less than the evidence would allow — the confidence hedge and the single-plan condition sit in the body, not in a footnote. The post now also admits that the instrument we were grading ourselves with was the wrong one, which claims less again. |
| **Respect owners** | PASS | Copy test applied. A busy principal is shown a supplier testing their own assumption and publishing the result that cost them the week — which is the behaviour they would want from a consultant. Nothing is sold. There is no offer in the body; the CTA offers the rest of the data, not a pitch. Removing the scores helps here: a principal does not read detection metrics, they read "94 boxes, then 33, against 43 real fixtures". |
| **Ship, don't slide** | PASS | A real bake-off, eight models, a real ground-truth file, and a decision taken off the back of it — the legend was moved to the documentation layer. The post reports a completed test with a verdict, not work in progress. |
| **Map before build** | PASS | The purest instance of the value in the week. The hypothesis was tested against ground truth *before* it was built into the pipeline, and the test killed it. The counterfactual is explicit in the closing line: without the test, a fix that does nothing ships quietly and nobody ever finds out. |

---

## Grounding notes (read before publishing)

- **Core claim and every figure: `syntheses/legend-priming-doesnt-help-detection`** (status **CONFIRMED**, confidence **medium**, created/updated/last-reviewed 2026-06-23) and `experiments/legend-detection-bakeoff` (verdict `failed`). Figures used verbatim in this revision: Gemini text-legend boxes **94 → 33**; Qwen **flat** across conditions; image few-shot **negligible in both directions**; **pooled across models, near-complete coverage; consensus≥2 collapses**; ground truth **"43 fixtures / 15 types"** from a trusted `plan-coords.json`. The synthesis's own verdict — the legend did not help and made the strongest model worse — is what carries the opening line now that no score is shown.
- **ALL DETECTION SCORES CUT (revision 2026-09-20), on Seetaram's instruction.** F1 on type-multiset detection measures whether the right *kinds* and *counts* of fixtures were found; it is blind to *where* they sit. For a floor plan, placement is the whole job, so a respectable score and an unusable layout are perfectly compatible — which is exactly what the bake-off's own headline finding demonstrates (pool the models and coverage is near-complete; require two of them to agree on the same fixture and it collapses). No F1 figure survives anywhere in this file: not in the body, the table, the value check or these notes. **Nothing was substituted for them.** The point is not that a better score belongs here; it is that a detection score is the wrong instrument for this question. Recall figures were dropped with them for the same reason — recall on this bake-off is the same type-multiset measure and would reintroduce the problem under a different name.
- **The measurement beat is deliberately small.** One paragraph ("It also showed up how we graded ourselves…"), placed after the placement/topology conclusion and before the conditions. It is a supporting beat, not the thesis. The thesis stays: *I was sure a legend would help; it did not; here is why; published anyway.* **Do not let a later pass expand this paragraph** — a dedicated post on measuring the wrong thing runs the following week and must not be pre-empted.
- **The "placement and topology" conclusion is the synthesis's own** — "the real miss (~35–37%) and noise come from box PLACEMENT and topology (shared-wall dedupe, corridor-facing doors), which no detector prompt addresses." The body's "about a third of the fixtures" is that ~35–37%, rounded down and stated loosely on purpose.
- **The stated condition is carried, not softened.** Synthesis: "holds for type-multiset detection on a single demo plan with no pixel ground truth; the image few-shot lever is only lightly tested (one plan, one run), so confidence is medium not high." That survives into the body as its own paragraph. **Do not cut it for length.** It is why the post is credible, and the source file's confidence grade is medium — publishing it as settled would misrepresent our own wiki.
- **CUT ENTIRELY: the AECV-Bench paragraph** — the "published benchmark figures I have not reproduced myself… this is where the field is" passage, which set our own detection score against a frontier benchmark figure. Its numbers are deliberately not reproduced here. Three reasons, all of them sufficient on their own. **One:** it compared our number against a benchmark built from the exact class of detection metric this revision rejects — keeping it would have meant arguing "our detection score is respectable" in a post that has just explained why the detection score does not settle anything. **Two:** both source entries (`papers/floorplan-vectorization-model-landscape`, `model-evals/detection-vlms-gemini-qwen`) carry an explicit `_(spot-verify numbers)_` marker, i.e. the wiki itself has not confirmed them. **Three:** the previous pass already flagged this as the paragraph to cut if review was uncomfortable with an unreproduced benchmark on a credibility post — review came back uncomfortable. The post loses only the "this is the field, not us" reassurance and reads tighter without it. **Do not reinstate it without reproducing the benchmark first.**
- **CUT with it: the "our score is at or above the frontier ceiling" corroboration claim.** It was the wiki's own written conclusion in `model-evals/detection-vlms-gemini-qwen`, so it was grounded — but it is a detection score compared to a detection score, and it dies with the paragraph.
- **CUT for insufficient grounding (earlier pass, still cut): the door 39% / window 34% sub-figures.** Same spot-verify marker.
- **CUT for insufficient grounding (earlier pass, still cut): GPT-5.2 (~49%), Claude Opus 4.5 (~42%), and best open-source GLM-4.6V 39%.** All under the same spot-verify marker. Recorded rather than dropped silently.
- **CUT on length: the eighth model that reads a plan as a document.** Grounded (`experiments/legend-detection-bakeoff`: "DeepSeek-OCR unfit (reads plan as a document)") and it was the most vivid line in an earlier pass, but it sits outside the argument's spine and naming it would read as a pile-on. Available if a reviewer wants it back.
- **The "eight vision models" count is grounded** — the bake-off ran Gemini 3.1-pro, Qwen3-VL and DeepSeek-OCR, plus GPT-5.2, GLM and Opus in the extended run. The body names two and says nothing about the rest.
- **Model names Gemini and Qwen are RETAINED.** That question is still open with Seetaram and he has not asked for them to go. With the scores removed they are far less prominent — they now appear as test subjects rather than as leaderboard entries. If the call comes to cut them, the body needs two edits (the Gemini line, the Qwen line) and the `Work, not tech` row upgrades to PASS.
- **"That was room 1 of 26 on this floor" is the week's series line**, carried forward unchanged. **Confirm the 26 against the project's own plan data before publishing** — a stated count that is wrong is worst on a credibility post.
- **NOT described: a ControlNet or control-model stage.** Removed from the codebase 2026-09-20. This post sits upstream of rendering entirely and has no reason to mention it; do not let a rewrite add pipeline scaffolding.
- **NOT stated: "nothing bad reaches a paid render."** Camera validation is logged Priority-1 and still unbuilt; on 2026-09-12 a camera standing inside a wall reached paid renders. Nothing here makes a completeness claim about the gate.
- **No client is named on this post.** The bake-off ran on the demo plan, not on Nine Bricks Studio's drawing. Attaching the client's name to a detection-failure post would be inaccurate and a misuse of the naming clearance. The occupant of the government office and its emblem/portrait layout are not mentioned and must not be added.
- No time figures. No cost figures. No ROI. No client savings of any kind. There is no money in this post at all.
