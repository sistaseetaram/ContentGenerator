# Tue 2026-09-22 — LinkedIn — Build Receipts

**Slot:** content-calendar.json → Tuesday 2026-09-22 — relaunch opener (RESHAPE verdict: win first; replaces the 09-22 method post and the 09-23 acceptance post as the opening slot)
**Title:** Built for my sister's practice — their architect accepted it, and why that can be trusted
**Format:** text + ONE image (PLAN | RENDER split). Not a carousel.
**Angle:** a system built to help his sister's architecture practice; the practising architect's acceptance is the headline; the method is folded in as the reason the acceptance holds; the eight passes read honestly as finish/furniture/light decisions; the close opens a door to spatial-AI / generative-design / AEC-software teams.
**Body length:** 1,892 characters as written (target 1,400–1,900; hard limit 3,000). 96 of those characters are the two editorial placeholders; with the real practice name and company-page tag in place the body lands at roughly 1,830.
**Status:** DRAFT. Not published. Not logged to posts.json. **Two placeholders must be resolved by Seetaram before publish** — the practice-name spelling and the company-page tag. Nothing else is outstanding.

---

## Post body

I built a render pipeline for my sister's architecture practice. Their designer, a practising architect, accepted its output on a live project.

[PRACTICE NAME — Seetaram to confirm exact spelling] [TAG — @practice LinkedIn page, URL pending] is a three-person practice in Vijayawada and Hyderabad. One government office chamber. Not a mood board — the drawing the site is being built from. That is why I went this deep.

Here is why the yes can be trusted.

The drawing was read into data: rooms, walls, doors, windows, every fixed piece of furniture, with position and angle. That became a plain grey 3D model — shapes where the drawing says shapes go. Five checks ran on it: furniture in the right room, every opening reachable, door clearance, boundary sealed, no dead space. If any fail, nothing renders. Bad geometry is caught before any render runs.

The photoreal render ran off that grey model, not off a paragraph.

Their designer marked it up: eight revision passes across two options.

The notes were about finishes, furniture and light: a walnut feature wall, a woven veneer panel at twice the density, grey velvet seating, blinds sealed, the room lit by its own fixtures.

One note in the first pass fixed a misread: two openings at the edge of frame drawn as windows. The drawing says doors. They became doors.

Not one note, in any pass, asked for a wall, a door or a window to move. What changed was what the designer chose to put in it. Their judgement, their sign-off. That is the bar.

The hard part was never making a good-looking image. It was making a model obey a drawing it cannot read.

That is what I am working on for my MSc in Artificial Intelligence at Southampton, and what I want to keep working on. If your team is anywhere near this — spatial AI, generative design, AEC software — I would like to talk.

I would rather compare notes than keep this to myself.

---

## First comment (no links in the body, nothing that asks the reader to perform for reach)

> One stage does the real work: the grey model. The checks run on it, not on the render — a render is too late to find out that a door cannot open. The gap I have not closed is camera placement: a camera can still end up standing inside a wall. If you test plan-faithfulness a different way, I want to hear it.

Nothing in the body or the comment solicits work, invites drawings, or names terms. That is deliberate — see "The close" in the grounding notes.

---

## Hashtags

#ArchitecturalVisualization #InteriorDesign #DesignStudio

_Advisory, Seetaram's call:_ these three tags aim at practice owners, which was the old CTA's audience. The close now aims at spatial-AI / generative-design / AEC-software teams. Swapping one tag (for example `#DesignStudio` → `#AEC`) would point the reach at the people the ending is addressed to. Left unchanged here because it was not part of the requested revision.

---

## Image (text + ONE image — the PLAN | RENDER split)

**Spec:** 1080x1080 (house LinkedIn spec). Two real artefacts, unmodified, side by side with a hairline divider. Paper theme (`#f2f2f0` / `#111111`), Inter label weight for two small captions — "PLAN" and "RENDER" — nothing else on the canvas. सेtu wordmark in a clear corner margin. No accent colour: Setu is monochrome-per-theme. If the render's 16:9 aspect fights the side-by-side at 1080 wide, stack them (plan above, render below) rather than crop the render's feature wall.

**Left — the plan.** Source: `/Users/sistaseetaram/Desktop/Claude/claude_projects/Artchitectural_design_automation/references/controlofficeff/01-floor-plan/Screenshot 2026-08-30 at 1.13.48_PM.png`. Crop to the chamber (the 6.0 x 6.0 m room, lower half of the sheet). **Decision for Seetaram:** the room label on the sheet reads "Sr.DEE/TRSO Chamber" — a post designation, which identifies the occupant's office. Clearance covers the plan, not the occupant; mask or crop that label if it reads as identification. Dimension strings and door tags can stay.

**Right — the accepted render (B4). File located:** `/Users/sistaseetaram/Desktop/Claude/claude_projects/Artchitectural_design_automation/references/controlofficeff/05-notes/renders/sr_dee_trso_chamber-photoreal-refine-v1-refine-v1-refine-v1-refine-v1-refine-v1-refine-v1-refine-v1.png` (seven-deep refine suffix, 2,256,887 bytes, saved 2026-09-12 14:31). Identity confirmed three ways: (a) `05-notes/bakeoff-round3/compare.html` lists B4 as the seventh and last pass of the chain; (b) `05-notes/renders/manifest.json` entry 10 — the seventh pass — carries B4's exact revision note (side-wall cabinet section deleted with a keep-boundary, artwork restored, blinds sealed with zero light, weave at the swatch's own density); (c) visual check matches the wiki's B4 decision line (walnut feature wall, lit pleat-weave recessed centre, sealed blinds, grey-velvet seating, off-white officer chair, full-height display, closed low run). Show it **unmodified** — including the warm cast the wiki records by pass seven. Colour-correcting the accepted artefact would misrepresent what was accepted.

**Two flags on the render itself.** (1) The feature wall shows the two portraits and the national emblem. The brief clears the render for showing; the copy never names or describes that arrangement, and it must not in any caption or alt text. Seetaram to confirm that showing the render as-is sits inside the clearance [PRACTICE NAME — Seetaram to confirm exact spelling] gave. (2) The L-desk's return leg is on the end the designer did *not* ask for (see grounding). The post does not claim every note landed, so this is not a copy problem — but it is visible in the image, so know it before someone asks.

**Build note:** this is a composite of two real artefacts plus the logo, so it is the HTML + playwright compositing pass (run from `career-ops/`), not image-gen. Run the mandatory Step 0 pre-flight in `.claude/rules/design-taste.md` first (wiki index → `syntheses/design-pipeline.md` → `setu-tokens.json`).

---

## Five-value check

| Value | Verified | How |
|---|---|---|
| **Work, not tech** | PASS | The headline is a practising architect's decision. The method appears only as the answer to "why can this be trusted" and is told in the language of drawings — read, grey model, checks, passes. No model names, no library names, no pipeline vocabulary, no "control" stage. No commercial framing of any kind: the post says what was built, who judged it, and what the judgement settled. |
| **Quiet over loud** | PASS | No banned words (checked against the list in CLAUDE.md Hard Rule 1; also checked "nothing bad", "clients and vendors", and any commercial or currency figure — all absent). No emoji. No superlatives. The strongest lines are someone else's sign-off and a plain statement of what did not move. The close asks for a conversation; it names no role, no availability and no terms, so it does not read as a job advert or a service pitch. |
| **Respect owners** | PASS | The practice is credited by name and by tag rather than used as an anonymous case, and the designer's judgement is named as theirs, twice. The occupant is never named and the emblem/portrait arrangement is never described. Nothing is sold, nothing is offered, and nothing asks the reader to perform for reach — the only ask is a conversation with teams working on the same problem. **One flag:** tagging the practice puts their page beside a government-office render, so confirm they are happy to be tagged, not only that the render is cleared. |
| **Ship, don't slide** | PASS | A real practice, a real construction drawing, a real accepted render, a real revision chain on disk. Every step in the body ran on this project. The MSc is stated as current work (it starts this month), not as a plan. Nothing in the post is forthcoming. |
| **Map before build** | PASS | The reason-to-trust paragraph *is* the value: read the drawing into data, build it grey, check it, and only then render. "Each stage catches mistakes cheaper than the next" is implied rather than stated, to keep the method from becoming the headline. |

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

### Revision 2026-09-26 — what changed in this draft and why

Four changes, all instructed by Seetaram directly. Recorded so nobody re-introduces what was removed.

1. **Reframed: this is a system he built to help his sister's architecture practice.** The practice is his sister's; his CV lists it as a family-run architecture practice. The old opener credited a team and read as commissioned work; it is gone. The relationship is now stated in the first sentence, because it is the reason the engineering went as deep as it did — a practising architect was always going to be the judge. The draft does **not** frame it as a favour or a side project: the acceptance, the pass-by-pass chain and the blocking checks all stay.
2. **Every commercial trace removed from the whole file** — body, first comment, five-value table, claims table, omissions list. The passes are revision passes and are described only as that. The render-gate line now reads "Bad geometry is caught before any render runs" — the sanctioned swap, with the house-safe *scope* (bad geometry, never "nothing bad") unchanged. Every figure of that kind, and the whole offer section that held them, are deleted outright rather than softened. The draft also does **not** advertise that nothing changed hands: saying so would put the commercial frame back in the reader's head and make the work sound like a favour.
3. **First-person plural removed; the post is "I" throughout**, body and first comment. Seetaram is one person; for this audience "I built this" is both stronger and more honest than agency voice. There is now no first-person plural anywhere in the file.
4. **The ending and the CTA replaced entirely.** The old ending solicited work on other people's drawings. **His visa prohibits freelance work, so no version of that ending can ship.** The replacement is the close he chose (option C), integrated rather than pasted — see "The close" below. The first comment was rewritten on the same principle: it now says why the checks run on the grey model rather than on the render, names the one gap that is still open (camera placement is unchecked, and `metrics-and-claims.md` records it as Priority-1 and unbuilt), and asks for other people's methods. It does not invite drawings, does not name terms, and does not promise a build that has not happened.

Two items were deliberately **left unresolved** and must be settled by Seetaram before publish: the practice-name spelling and the company-page tag. Both are marked in place.

**Sources read for this draft:** `data/drafts/2026-09-23-nine-bricks-accepted/linkedin-post.md`; `data/drafts/2026-09-22-method-holds-the-plan/linkedin-post.md`; `.claude/rules/metrics-and-claims.md`; wiki `log.md` entry `[2026-09-12]` in full; `references/controlofficeff/05-notes/bakeoff-round3/compare.html` (the per-pass lineage the log points to); `05-notes/renders/manifest.json` (the full revision note of each of the seven kept passes); the renders folder listing; the plan screenshot and the B4 render viewed directly. Wiki pages `entities/tool-plan-extractor`, `entities/tool-spatial-evals`, `concepts/shift-left-spatial-verification`, `concepts/plan-faithfulness-hard-rule`, `experiments/render-model-ab-nano-field` confirmed to exist and to carry the lines cited below. The 2026-09-26 reframe rests on Seetaram's own instruction plus his CV entry for the practice.

### The two unresolved placeholders

- **`[PRACTICE NAME — Seetaram to confirm exact spelling]`** — the practice appears three different ways across his files: `Nine Bricks Studio` (every earlier draft in this repo), `9 Brics Studio` (his CV), `9BricksStudio` (the project folder name). Not guessed here. A misspelled company name in a public post, tagged to their page, is the one error this draft must not ship. The placeholder appears twice: once in the body, once in the image note about clearance.
- **`[TAG — @practice LinkedIn page, URL pending]`** — Seetaram wants the practice's LinkedIn company page tagged and has not supplied the URL. The placeholder sits immediately after the name placeholder in the body, because on LinkedIn the tag renders as the name, so the two collapse into one mention when filled. If the practice has no company page, the fallback is the name in plain text and no tag — nothing else in the body depends on it.

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
| The practice is his sister's | Seetaram directly, 2026-09-26; his CV lists the practice as family-run | Caller-stated. The wiki and the project files do not record the relationship. |
| "I built a render pipeline" — one person, not a team | Seetaram directly, 2026-09-26. The pipeline entities in the wiki (`tool-plan-extractor`, `tool-spatial-evals`) carry no other author. | Caller-stated. |
| Their designer, a practising architect, accepted the output | Wiki log 2026-09-12, decision line verbatim: `OPTION B4 ACCEPTED as the chamber's final render` + the task brief stating the studio's designer cleared the render for social; "a practising architect signed off" per Seetaram 2026-09-26 | Recorded decision. The wiki does not quote the designer; acceptance rests on the brief, and the "practising architect" descriptor on Seetaram. The body credits the practice's designer, **not** his sister personally — no source records who drew the markups. |
| Three-person practice, Vijayawada and Hyderabad, "government office" | Task brief (naming cleared). Not in the wiki log entry read. | Caller-cleared. |
| Built from their construction drawing, one chamber | `references/controlofficeff/01-floor-plan/` (the drawing) + `plan-coords.json` (three rooms: chamber, steno/visitor, toilet); log context line | Artefact on disk. |
| Drawing read into data — rooms, walls, doors, windows, fixed furniture with position and angle | `entities/tool-plan-extractor` ("rooms, walls, openings, and fixtures with `theta_deg` rotation") | Wiki entity. |
| Plain grey 3D model | `concepts/shift-left-spatial-verification` (Three.js whitebox for human review) | Wiki concept. |
| Five checks; if any fail, nothing renders | `entities/tool-spatial-evals` line 16: blocking set `ffe_in_room`, `opening_reachability`, `door_clearance`, `boundary_sealed`, `no_enclosed_void`, recorded as running before any render. (The source line states this in commercial terms; paraphrased here per the 2026-09-26 instruction. The blocking set itself is unchanged.) | Wiki entity, stated as the pipeline invariant. **The wiki records no specific catch on this plan; the body claims none.** |
| "Bad geometry is caught before any render runs" | `.claude/rules/metrics-and-claims.md` — the house-approved *scope*: "bad geometry", never "nothing bad". Camera validation is logged Priority-1 and **still unbuilt** (on 2026-09-12 a camera standing inside a wall reached finished renders, pre-round-3), which is why the absolute form is not used. The rule states the safe form with a commercial stage name; the wording here is the sanctioned swap and the scope limit is intact. | Rule-approved scope. |
| Render driven off the grey model, not a paragraph | `experiments/render-model-ab-nano-field` line 12 (direct whitebox→photoreal in one hop is the primary path); renders folder confirms the direct path for this room (`-control.png` → `-photoreal.png` → refine chain, no line-art step) | Wiki experiment + artefact. |
| "Their designer marked it up" | Log context: "the designer's real brief ... applied end-to-end"; refine notes reference "the approved reference" (v3, B2, B3). | Inferred from log context. The wiki does not attribute each note line to the designer, and several note items are the operator undoing model drift (artwork restore, shelf wrapping the corner, blinds re-pinned). The body therefore says the designer marked it up and that "the notes were about" finishes — it does **not** say every note was the designer's. |
| Eight revision passes across two options | Log records eight refine passes (v1→v3 on option A, drafts B→B4 on option B); `metrics-and-claims.md` (two options, not one chain) | Wiki + rule. **Composition:** seven kept passes on disk (v1, v2, v3, B, B2, B3, B4) plus one attempt that failed and was discarded (`FAILED-refine-texture-swallow.png`, between B and B2) = eight passes run. The 2026-09-20 log entry says "B4 = nano-banana-pro + seven refine passes". **2026-09-26:** the original justification for "eight" counted calls made; with commercial framing stripped, the unit is now "passes run, one of which was discarded". Still true, but thinner than it was. If Seetaram prefers the designer-visible count, "seven" is the honest swap and needs no other change. |
| Walnut feature wall; woven veneer at twice the density; grey velvet seating; blinds sealed, room lit by its own fixtures | Log decision line for B4; manifest entries 9 (B3) and 10 (B4) | Recorded, verbatim-level. The off-white officer's chair, the full-height display unit and the low closed cabinets are all equally recorded; they were cut from the list for length, not for doubt. |
| Two openings at the edge of frame drawn as windows; the drawing says doors | Manifest entry 4 item (4) (quoted above); log "DESCRIBE EVERYTHING THE CAMERA SEES"; the plan sheet shows two D1 doors on that side | Recorded. |
| MSc in Artificial Intelligence at Southampton, current work | Seetaram directly, 2026-09-26: University of Southampton, MSc Artificial Intelligence, Sep 2026 – Sep 2027, on an Excellence Scholarship. Today is 2026-09-26, so "what I am working on" is accurate as of publication. | Caller-stated. The scholarship is deliberately not in the post. |

### Chosen not to use, and why

- **Any commercial framing at all** — removed from the entire file on 2026-09-26, per Seetaram. This was not a commercial engagement, the post does not describe it as one, and no figure of that kind appears anywhere in this file, in any form. Do not re-introduce one "for context".
- **An offer, a service line, or any invitation to send drawings** — removed. Seetaram's visa prohibits freelance work, so the post must not solicit work of any kind. The close asks for a conversation and nothing else. The old body line ("If you run a practice and want to see this done on one of your own drawings, DM me") and the old first comment ("DM me the plan and tell me which room") are both dead; so is the earlier `[OFFER]` placeholder and the section of notes that sat with it.
- **The L-desk return leg** — asked three ways (from-scratch note, refine pin, explicit refine edit in v2), never moved; the accepted B4 still has it on the end the designer did not ask for. Omitted from the body: this is the win post and the roast council's finding on render-failure openers stands. The body is written so nothing it says is contradicted by this (it never claims every note landed). **Seetaram should know it is visible in the image.** Hold for a later "what did not land" post.
- **The blinds reopening across five consecutive passes** (base-prompt daylight conflict) and **the artwork lost to a sibling clause and restored in B4** — both true, both model-drift stories, both held for the same reason.
- **The failed texture-swallow attempt** (the reference swatch returned as the output) — held; it is why the count is eight and not seven, noted above.
- **The warm/pink colour cast by pass seven** — not mentioned; the image shows it honestly.
- **The CV's own parenthetical about the nature of the engagement** — not used, and neither is any wording that announces what did or did not change hands. The instruction is to stop framing this commercially; announcing it would make the work sound like a favour.
- **The Excellence Scholarship, the MSc dates, and anything else CV-shaped** — held out of the body. The post is a working engineer showing work and opening a door, not a CV. One clause naming the degree and the university is the whole of it.
- **The occupant's name and the emblem/portrait layout** — never mentioned, per clearance. The refine notes and the log contain both; nothing from them is in the copy. The word "portrait" does not appear in the body even in the finishes list, on purpose.
- **"Good enough to show their clients and vendors"** — withdrawn line; not used.
- **The five checks as a specific save on this plan** — no such catch is recorded; not claimed.
- **Any "control" / control-image stage in the copy** — not used; the grey model is described as what the render is driven off.
- **A story opener** — the hook is still a concrete fact (what was built, who accepted it), now with the relationship in the same sentence; the analytics note that concrete hooks outperform story hooks on this account (3.9% vs 2.5%).

### The close — Seetaram's decision (option C), recorded here

He chose this ending and it is integrated, not pasted. His text:

> The hard part was never making a good-looking image. It was making a model obey a drawing it cannot read.
>
> That's what I'm working on for my MSc in Artificial Intelligence, and what I want to keep working on. If your team is anywhere near this — spatial AI, generative design, AEC software — I'd like to talk.
>
> I'd rather compare notes than keep this to myself.

What changed in integration, and why:
- Contractions expanded ("That's" → "That is", "I'd" → "I would"). The rest of the body carries none, and the register is the flat, declarative one used throughout.
- "at Southampton" added to the degree clause. It is verified (University of Southampton, MSc Artificial Intelligence, from Sep 2026) and it turns a claim into a checkable fact, which is the whole argument of the post.
- Nothing else. The three paragraph breaks, the sequence and the final line are his.

**What the close is for:** research collaboration, an internship, and conversations with teams building constraint-faithful generative systems. **What it must never become:** a job advert or a service pitch. It names no role, no availability, no notice period, no terms and no deliverable — that restraint is what keeps it reading as an engineer publishing his work. If a future edit adds "open to opportunities" or anything like it, the post changes category and loses the thing that makes it land.

### If the count is dropped altogether

If "eight" still reads as delivery risk, the swap is inside one sentence: replace *"eight revision passes across two options"* with *"two options, and they chose between them"* — everything after it stays true and unchanged. Body length moves to about 1,893 characters, still inside the target.
