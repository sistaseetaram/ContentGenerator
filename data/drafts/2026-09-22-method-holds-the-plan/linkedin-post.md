# Tue 2026-09-22 — LinkedIn — Build Receipts

**Slot:** content-calendar.json → Tuesday 2026-09-22 (idea-008, score 39.5, verdict post_now)
**Title:** How we made the render hold the actual floor plan
**Format:** document carousel
**Angle:** method — the spatial method, told as why you can trust the output
**Status:** DRAFT. Not published. Not logged to posts.json.

---

## Post body

Nine Bricks Studio, a three-person practice working across Vijayawada and Hyderabad, sent us a construction drawing for a government office and asked for one room, rendered.

Not a mood board. The drawing the site is being built from.

So the render had one job: be true to it. Yesterday I showed what happens when that's left to the model. Here's what we do instead.

**We read the drawing before we render it.**
The plan becomes structured data first — rooms, walls, doors, windows, and every fixed piece of furniture, with its position and angle. Now the layout is something you can check, not squint at.

**We build the room in plain grey before anyone sees it pretty.**
A 3D model with no materials, no lighting, no styling. Just shapes where the drawing says shapes go. A designer can look at it for ten seconds and say "that's wrong" — which is exactly when you want them saying it.

**Then five checks run, free, before a single paid render fires.**
Is every piece of furniture inside the room it belongs to. Can you reach every door and window. Does each door have clearance to swing. Is the boundary sealed. Is there dead space with no way into it.

If those fail, nothing renders. No point making a beautiful picture of a floor plan that doesn't work.

Only then does the photoreal render run — driven off that grey model, not off a paragraph describing it.

Each stage catches mistakes more cheaply than the one after it. That's the whole idea — and the only honest answer to "how do I know this matches my drawing?"

Because a render you can't build from isn't a render. It's a nice picture of a building that doesn't exist.

---

## First comment (CTA — no links in the body)

> The drawing and the accepted render, side by side, are the clearest version of this. If you'd like the pair, comment "plan" and I'll send them over.

---

## Hashtags

#ArchitecturalVisualization #AIinArchitecture #DesignStudio

---

## Carousel outline (document carousel, 1080x1080)

| # | Slide | Content |
|---|-------|---------|
| 1 | Cover | "How we made the render hold the actual floor plan." Sub-line: "Nine Bricks Studio · Vijayawada & Hyderabad · a government office." |
| 2 | The input | The real floor plan (cleared to show). Caption: "The drawing they're building from. Not a mood board." |
| 3 | Step 1 — read it | Plan alongside the extracted structure. "Rooms, walls, doors, windows, furniture — with position and angle. Checkable, not squintable." |
| 4 | Step 2 — grey first | The plain grey 3D model. "No materials. No lighting. Just shapes where the drawing says shapes go." |
| 5 | Step 3 — the gate | The five checks, one line each, plain English: furniture in the right room · every door and window reachable · doors have room to swing · boundary sealed · no dead space. Footer: "Runs for $0. If it fails, nothing renders." |
| 6 | Why this order | "Each stage catches mistakes cheaper than the next one. The expensive step goes last." |
| 7 | Step 4 — render | PLAN │ RENDER split. Real drawing left, accepted render right. |
| 8 | The point | "A render you can't build from isn't a render." |
| 9 | Close | "Tomorrow: what it actually took to get this accepted." Setu wordmark, clear corner margin. |

**Visual build note:** do NOT hand-build these slides. Run the mandatory Step 0 pre-flight in `.claude/rules/design-taste.md` first. Slide 7 is the PLAN │ RENDER split — this is the single highest-performing composition found in the packaging research and it must use the two real artefacts, unmodified. No accent colour: Setu is monochrome-per-theme.

---

## Five-value check

| Value | Verified | How |
|---|---|---|
| **Work, not tech** | PASS | Opens with a client and a job, not a stack. The five checks are stated as questions about a room, never as function names. No model names, no library names, no API references anywhere in the body. This is the post most at risk of a positioning leak and it was written specifically to fail that test — a builder can see the whole architecture, but nothing in the copy requires them to. |
| **Quiet over loud** | PASS | No banned words (checked against `setu-voice.md`). No superlatives about the method. The strongest line is a limitation, not a boast. |
| **Respect owners** | PASS | Copy test applied: the reader is a busy studio owner being answered, not taught. It answers the question they'd actually ask — "how do I know it matches my drawing?" — instead of the question we'd enjoy answering. |
| **Ship, don't slide** | PASS | Real client, real drawing, real accepted render. Every step described is one that ran on this project, not a proposed process. |
| **Map before build** | PASS | This is the single clearest expression of the value: the entire post is the diagnosis and verification layer that runs *before* anything gets built. The prep is the product. |

---

## Grounding notes (read before publishing)

- **The calendar's proof_plan pipeline is out of date on one step.** It lists `... → line art → photoreal → refine`. The wiki retired that: `experiments/render-model-ab-nano-field` (2026-07-08) records that **direct whitebox→photoreal in one hop replaced the line-art chain as the primary path**, with line art "retained only as a designer-proof deliverable + drift fallback." The Nine Bricks render files on disk confirm the direct path (`sr_dee_trso_chamber-control.png` → `-photoreal.png` → refine chain; no line-art step in that room's render folder). **The draft uses the direct path.** Publishing the calendar's version would have described a pipeline this project did not use — and would have contradicted Monday's post, which blames the line-art redraw.
- **The five checks are wiki-grounded as the tool's blocking set** (`entities/tool-spatial-evals`: `ffe_in_room`, `opening_reachability`, `door_clearance`, `boundary_sealed`, `no_enclosed_void`) and as a pipeline invariant that runs before any paid image call (`concepts/shift-left-spatial-verification`). **What the wiki does NOT record is a specific catch on the Nine Bricks plan.** The only documented catch — "2 enclosed voids (west + east circulation halls)" — is not attributable to this project (its `plan-coords.json` has three rooms: the chamber, a steno/visitor room, and a toilet). The draft therefore describes the gate as method, and claims no specific save on this plan. **Do not add one.**
- **"$0" appears once, in slide 5, as cost-to-run of the checks — not as client savings.** This is the safe side of the honesty constraint. If it reads at all like ROI in review, cut it to "before any paid render."
- Structured extraction with rotation is grounded in `entities/tool-plan-extractor` ("rooms, walls, openings, and fixtures with `theta_deg` rotation"). The grey 3D model is the Three.js whitebox from `concepts/shift-left-spatial-verification`.
- "A render you can't build is a trap" is a direct paraphrase of `concepts/plan-faithfulness-hard-rule`.
- No time figures. No cost figures. No ROI.
