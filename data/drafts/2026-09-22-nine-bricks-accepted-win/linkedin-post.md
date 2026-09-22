# Tue 2026-09-22 — LinkedIn — Build Receipts

**Slot:** content-calendar.json → Tuesday 2026-09-22 — relaunch opener (RESHAPE verdict: win first; replaces the 09-22 method post and the 09-23 acceptance post as the opening slot)
**Title:** Nine Bricks Studio accepted it — and why that can be trusted
**Format:** text + ONE image (PLAN | RENDER split). Not a carousel.
**Angle:** client acceptance is the headline; the method is folded in as the reason the acceptance holds; the eight passes reframed honestly as finish/furniture/light decisions
**Body length:** 1777 characters (target 1,400–1,900; hard limit 3,000)
**Status:** DRAFT. Not published. Not logged to posts.json. Offer line is a placeholder — Seetaram sets terms before publish.

---

## Post body

Nine Bricks Studio accepted the render we built from their construction drawing.

A three-person practice working across Vijayawada and Hyderabad. One government office chamber. Not a mood board — the drawing the site is being built from.

Here is why that acceptance can be trusted.

Before anything was rendered, the drawing was read into data: rooms, walls, doors, windows, every fixed piece of furniture, with its position and angle. That became a plain grey 3D model — shapes where the drawing says shapes go, nothing pretty. Five checks ran on it: furniture in the right room, every door and window reachable, room for each door to swing, boundary sealed, no dead space. If any fail, nothing renders. No bad geometry reaches a paid render.

Only then did the photoreal render run, driven off that grey model rather than off a paragraph describing the room.

Then the designer marked it up. Eight revision passes, across two options.

The notes were about finishes, furniture and light. A walnut feature wall. A woven veneer panel at the centre, its pattern tightened to twice the density. Grey velvet on the seating, off-white leather on the officer's chair. A full-height display unit and a low run of closed cabinets. The blinds sealed, the room lit by its own fixtures.

One note in the first pass fixed a misread: two openings at the edge of frame drawn as windows. The drawing says doors. They became doors.

Not one note, in any pass, asked for a wall, a door or a window to move. The room stayed where the drawing put it. What changed was what the designer chose to put in it.

Their judgement. Their sign-off. That is the bar.

[OFFER — Seetaram to confirm terms before publish]

If you run a practice and want to see this done on one of your own drawings, DM me.

---

## First comment (CTA — no links in the body, no "comment X and I'll send it")

> If you want to try this on a drawing of your own: DM me the plan and tell me which room. That is all I need to start. [Mirror the OFFER line here once the terms are set — same wording as the body, so the offer stands alone in the comment too.]

---

## Hashtags

#ArchitecturalVisualization #InteriorDesign #DesignStudio

---

## Image (text + ONE image — the PLAN | RENDER split)

**Spec:** 1080x1080 (house LinkedIn spec). Two real artefacts, unmodified, side by side with a hairline divider. Paper theme (`#f2f2f0` / `#111111`), Inter label weight for two small captions — "PLAN" and "RENDER" — nothing else on the canvas. सेtu wordmark in a clear corner margin. No accent colour: Setu is monochrome-per-theme. If the render's 16:9 aspect fights the side-by-side at 1080 wide, stack them (plan above, render below) rather than crop the render's feature wall.

**Left — the plan.** Source: `/Users/sistaseetaram/Desktop/Claude/claude_projects/Artchitectural_design_automation/references/controlofficeff/01-floor-plan/Screenshot 2026-08-30 at 1.13.48_PM.png`. Crop to the chamber (the 6.0 x 6.0 m room, lower half of the sheet). **Decision for Seetaram:** the room label on the sheet reads "Sr.DEE/TRSO Chamber" — a post designation, which identifies the occupant's office. Clearance covers the plan, not the occupant; mask or crop that label if it reads as identification. Dimension strings and door tags can stay.

**Right — the accepted render (B4). File located:** `/Users/sistaseetaram/Desktop/Claude/claude_projects/Artchitectural_design_automation/references/controlofficeff/05-notes/renders/sr_dee_trso_chamber-photoreal-refine-v1-refine-v1-refine-v1-refine-v1-refine-v1-refine-v1-refine-v1.png` (seven-deep refine suffix, 2,256,887 bytes, saved 2026-09-12 14:31). Identity confirmed three ways: (a) `05-notes/bakeoff-round3/compare.html` lists B4 as the seventh and last pass of the chain; (b) `05-notes/renders/manifest.json` entry 10 — the seventh pass — carries B4's exact revision note (side-wall cabinet section deleted with a keep-boundary, artwork restored, blinds sealed with zero light, weave at the swatch's own density); (c) visual check matches the wiki's B4 decision line (walnut feature wall, lit pleat-weave recessed centre, sealed blinds, grey-velvet seating, off-white officer chair, full-height display, closed low run). Show it **unmodified** — including the warm cast the wiki records by pass seven. Colour-correcting the accepted artefact would misrepresent what was accepted.

**Two flags on the render itself.** (1) The feature wall shows the two portraits and the national emblem. The brief clears the render for showing; the copy never names or describes that arrangement, and it must not in any caption or alt text. Seetaram to confirm that showing the render as-is sits inside the clearance Nine Bricks gave. (2) The L-desk's return leg is on the end the designer did *not* ask for (see grounding). The post does not claim every note landed, so this is not a copy problem — but it is visible in the image, so know it before someone asks.

**Build note:** this is a composite of two real artefacts plus the logo, so it is the HTML + playwright compositing pass (run from `career-ops/`), not image-gen. Run the mandatory Step 0 pre-flight in `.claude/rules/design-taste.md` first (wiki index → `syntheses/design-pipeline.md` → `setu-tokens.json`).

---

## Five-value check

| Value | Verified | How |
|---|---|---|
| **Work, not tech** | PASS | The headline is a client decision. The method appears only as the answer to "why can this be trusted" and is told in the language of drawings — read, grey model, checks, passes. No model names, no library names, no pipeline vocabulary, no "control" stage. "Paid render" is the only nod to cost and it is a stage name, not a figure. |
| **Quiet over loud** | PASS | No banned words (checked against the list in CLAUDE.md Hard Rule 1; also checked "nothing bad", "clients and vendors", any cost or currency figure — all absent). No superlatives. The strongest lines are someone else's sign-off and a plain statement of what did not move. |
| **Respect owners** | PASS | Copy test applied against the Buyer persona: a named practice of his size, in his region, on a real building type, with the drawing he would recognise as his own kind of input. The CTA is "DM me" — nothing asks him to perform for reach. The offer is a placeholder, so nothing is sold that Seetaram has not priced. The one correction volunteered is framed as the drawing winning, not as a render breaking. |
| **Ship, don't slide** | PASS | A real practice, a real drawing, a real accepted render, a real revision chain on disk. Every step in the body ran on this project. Nothing is forthcoming. |
| **Map before build** | PASS | The reason-to-trust paragraph *is* the value: read the drawing into data, build it grey, check it, and only then spend on the render. "Each stage catches mistakes cheaper than the next" is implied rather than stated to keep the method from becoming the headline. |

---

## Image build — BLOCKING constraint (added 2026-09-22, Seetaram)

**Do not publish the plan image until every piece of occupant-designation text is masked or cropped.**
The plan sheet's room label reads `Sr.DEE/TRSO Chamber`, which identifies the occupant's post. Remove or
crop it, and check the same sheet for title-block entries, door/room tags, schedule rows and sheet headers
carrying the same designation. Dimensions, grid lines, generic door/window tags and material callouts may
stay. The render must get the same pass. When in doubt, crop it out.

This is broader than the earlier permission note, which only barred naming the occupant in COPY. It now
covers anything legible in the ARTEFACT.

---

## Grounding notes (read before publishing)

**Sources read for this draft:** `data/drafts/2026-09-23-nine-bricks-accepted/linkedin-post.md`; `data/drafts/2026-09-22-method-holds-the-plan/linkedin-post.md`; `.claude/rules/metrics-and-claims.md`; wiki `log.md` entry `[2026-09-12]` in full; `references/controlofficeff/05-notes/bakeoff-round3/compare.html` (the per-pass lineage the log points to); `05-notes/renders/manifest.json` (the full revision note of each of the seven kept passes); the renders folder listing; the plan screenshot and the B4 render viewed directly. Wiki pages `entities/tool-plan-extractor`, `entities/tool-spatial-evals`, `concepts/shift-left-spatial-verification`, `concepts/plan-faithfulness-hard-rule`, `experiments/render-model-ab-nano-field` confirmed to exist and to carry the lines cited below.

### The eight-rounds verification — result: the line as briefed DIES. A narrower line survives.

The briefed line was: *every one of the eight passes was a finish, material, lighting or furniture request — and not one asked for a wall, door or window to be corrected.*

Checked against `05-notes/renders/manifest.json`, which stores the complete revision note of every kept pass. **Pass v1 (the first refine pass, manifest entry 4), item (4), verbatim:**

> "(4) The partial openings at the right edge of the frame are DOORS, not windows: render them as plain light-oak door leaves — remove the glazing and blinds there."

That is a door/window correction inside one of the eight passes, so the absolute line is false and is **not used**. Context from the log (2026-09-12, "DESCRIBE EVERYTHING THE CAMERA SEES"): the round-3 base render's camera stood beside the room's own door; its leaf intruded at the frame edge, the scene text said nothing about it, and nano-banana-pro "invented blinds-covered WINDOWS from the unexplained geometry." v1 corrected the render back to what the plan says. Important for how it is framed: the *plan* was never wrong and nothing was asked to *move* — the render's misread was corrected to the drawing. The body says exactly that, in two sentences, and no more.

**What survives, and is used:** *"Not one note, in any pass, asked for a wall, a door or a window to move."* Verified pass by pass — every one of the seven kept notes ends with a pin of the form "the two doors on the right, the window and blinds ... all stay exactly as in the base image", and no note anywhere requests a change of position for any wall, door or window. Two items are worth knowing about so the sentence is not read further than it goes: v2 item (2) removed the recessed portrait niches from the feature wall (surface-mounted instead), and Draft B item (5) recessed the centre panel 3–4 inches with an LED reveal. Both are millwork-depth decisions on a wall's surface, not a wall moving. If Seetaram wants zero exposure on that distinction, the fallback wording is "asked for the room's walls, doors or windows to move" — same meaning, same truth.

**Full classification of the seven kept passes (compare.html order; manifest entries 4–10):**
- v1 — three finish changes (fabric laminate, oak veneer, travertine modules) **+ the door correction above**.
- v2 — finish/millwork depth (centre panel flush, niches removed, ivory laminate, hairline grooves, brass fillets) **+ the L-desk return-leg move** (furniture position; did not land — see omissions).
- v3 — millwork depth + finish (recessed centre, veneer texture per reference, gold creases).
- Draft B (branches from v3) — built-ins added (full-height display unit, low bookshelf), walnut panelling, pale veneer centre, recess with LED reveal.
- Draft B2 — side wall reverted, wrapped shelf section removed, pleat-weave centre per reference.
- Draft B3 — side-wall shelving removed, low run closed, blinds shut, weave densified, grey velvet, off-white officer chair.
- Draft B4 — side-wall cabinet section deleted with keep-boundary, artwork restored, blinds sealed with zero light, weave at swatch density. **Accepted.**

### Every other factual claim → source and grade

| Claim in body | Source | Grade |
|---|---|---|
| Nine Bricks Studio accepted the render | Wiki log 2026-09-12, decision line verbatim: `OPTION B4 ACCEPTED as the chamber's final render` + the task brief stating the studio's designer cleared the render for social | Recorded decision. The wiki does not quote the designer; acceptance-by-the-studio rests on the brief. |
| Three-person practice, Vijayawada and Hyderabad, "government office" | Task brief (naming cleared). Not in the wiki log entry read. | Caller-cleared. |
| Built from their construction drawing, one chamber | `references/controlofficeff/01-floor-plan/` (the drawing) + `plan-coords.json` (three rooms: chamber, steno/visitor, toilet); log context line | Artefact on disk. |
| Drawing read into data — rooms, walls, doors, windows, fixed furniture with position and angle | `entities/tool-plan-extractor` ("rooms, walls, openings, and fixtures with `theta_deg` rotation") | Wiki entity. |
| Plain grey 3D model | `concepts/shift-left-spatial-verification` (Three.js whitebox for human review) | Wiki concept. |
| Five checks; if any fail, nothing renders | `entities/tool-spatial-evals` line 16: blocking set `ffe_in_room`, `opening_reachability`, `door_clearance`, `boundary_sealed`, `no_enclosed_void`; "Runs for $0 before any paid render." | Wiki entity, stated as the pipeline invariant. **The wiki records no specific catch on the Nine Bricks plan; the body claims none.** |
| "No bad geometry reaches a paid render" | `.claude/rules/metrics-and-claims.md` — the house-safe form. Camera validation is still unbuilt (a camera inside a wall reached paid renders on 2026-09-12, pre-round-3), which is why the unsafe form "nothing bad" is not used. | Rule-approved wording. |
| Render driven off the grey model, not a paragraph | `experiments/render-model-ab-nano-field` line 12 (direct whitebox→photoreal in one hop is the primary path); renders folder confirms the direct path for this room (`-control.png` → `-photoreal.png` → refine chain, no line-art step) | Wiki experiment + artefact. |
| "Then the designer marked it up" | Log context: "the designer's real brief ... applied end-to-end"; refine notes reference "the approved reference" (v3, B2, B3). | Inferred from log context. The wiki does not attribute each note line to the designer, and several note items are the operator undoing model drift (artwork restore, shelf wrapping the corner, blinds re-pinned). The body therefore says the designer marked it up and that "the notes were about" finishes — it does **not** say every note was the designer's. |
| Eight revision passes, across two options | Log verbatim: "EIGHT paid refine passes (v1→v3 on option A, drafts B→B4 on option B)"; `metrics-and-claims.md` (two options, not one chain) | Wiki + rule. **Composition:** seven kept passes on disk (v1, v2, v3, B, B2, B3, B4) plus one paid attempt that failed (`FAILED-refine-texture-swallow.png`, between B and B2) = eight paid calls. The 2026-09-20 log entry says "B4 = nano-banana-pro + seven refine passes". If Seetaram prefers the designer-visible count, "seven" is the honest swap and needs no other change. |
| Walnut feature wall; woven centre at twice the density; grey velvet seating; off-white officer chair; full-height display; closed low run; blinds sealed, room lit by its own fixtures | Log decision line for B4; manifest entries 9 (B3) and 10 (B4) | Recorded, verbatim-level. |
| Two openings at the edge of frame drawn as windows; the drawing says doors | Manifest entry 4 item (4) (quoted above); log "DESCRIBE EVERYTHING THE CAMERA SEES"; the plan sheet shows two D1 doors on that side | Recorded. |

### Chosen not to use, and why

- **The L-desk return leg** — asked three ways (from-scratch note, refine pin, explicit refine edit in v2), never moved; the accepted B4 still has it on the end the designer did not ask for. Omitted from the body: this is the win post and the roast council's finding on render-failure openers stands. The body is written so nothing it says is contradicted by this (it never claims every note landed). **Seetaram should know it is visible in the image.** Hold for a later "what did not land" post.
- **The blinds reopening across five consecutive passes** (base-prompt daylight conflict) and **the artwork lost to a sibling clause and restored in B4** — both true, both model-drift stories, both held for the same reason.
- **The failed texture-swallow attempt** (the reference swatch returned as the output) — held; it is why the count is eight and not seven, noted above.
- **The warm/pink colour cast by pass seven** — not mentioned; the image shows it honestly.
- **The cost figure** (≈$2.55 across ~26 paid calls) — omitted entirely. Cost-to-run only, never client savings; not needed here.
- **The occupant's name and the emblem/portrait layout** — never mentioned, per clearance. The refine notes and the log contain both; nothing from them is in the copy. The word "portrait" does not appear in the body even in the finishes list, on purpose.
- **"Good enough to show their clients and vendors"** — withdrawn line; not used.
- **The five checks as a specific save on this plan** — no such catch is recorded; not claimed.
- **Any "control" / control-image stage in the copy** — not used; the grey model is described as what the render is driven off.
- **The old CTAs ("comment chain" / "comment plan")** — replaced by DM.
- **A narrative opener** — the hook is the acceptance fact; the analytics note that concrete hooks outperform story hooks on this account (3.9% vs 2.5%).

### The offer — Seetaram's decision, recorded here for reference only

The body carries `[OFFER — Seetaram to confirm terms before publish]`. The roast council's Buyer persona stated his yes-condition as: *"take my plan, send me one render inside 24 hours, free, no call, with the dimension check beside it; if it holds I'll pay for the next five"* — at ₹2,500–4,000 per approved image or ₹15,000–25,000/month retainer. That is his stated condition, not a recommendation from this draft; no price has been written into the post. Whatever terms go in, mirror them in the first comment so the offer stands alone there too.

### If the count is dropped altogether

If "eight" still reads as delivery risk after the reframe, the swap is one sentence: replace *"Eight revision passes, across two options."* with *"The revisions ran as two options, and the designer chose between them."* — everything after it stays true and unchanged. Body length would move to about 1805 characters, still inside the target.
