# Setu Headless Video Style — "Architect's Draughting"

The reusable visual style for **headless (no-camera) animated videos, clips, shorts, and
explainers** for Setu. Default for ICP (architecture/design/construction) content and
plain-English takes. NOT for build-in-public camera content (that uses the camera profiles).

Any agent building a headless video/clip MUST load this file + the brand tokens first.

## Concept (why this style is ours)

The visual language is the craft of the ICP itself: **precise architectural drawing**. Lines
**draught themselves in** — an elevation, plan, or section plotting onto paper — mixed with
elegant entourage figures for human moments. It literally embodies the value **map before
build**. Calm, premium, quiet: the craft talks, we don't shout. For an architect scrolling, a
real drawing draughting in is instant recognition — that is the hook.

## Palette — EXACT tokens only (`setu-tokens.json`)

| Context | Background | Line + text |
|---|---|---|
| Paper scenes (default) | `#f2f2f0` | graphite `#1d1d1b` (text may use `#111111`) |
| Signature / close | terracotta `#1e0f09` | cream `#f2ddd3` |

Monochrome per theme. **No other colors, no gradients, no neon, no warm-beige.** (gpt-image
figures come back beige — always recolor to graphite-on-paper.)

## Type

- **Cormorant Garamond** — display, headlines, numbers (wt 300 large / 500 emphasis).
- **Inter** — labels, kickers, captions (wt 400/500; kickers uppercase, tracked).
- **Noto Sans Devanagari** — सेतु wordmark.
- Load via local `@font-face` woff2 (Google Fonts won't load in the sandbox render). Inter:
  `LoomWalkthroughs/edit/fonts/Inter.ttf`. Balanced modular scale — no tiny→huge jumps.

## Semantic relevance — THE FIRST RULE

Every drawing must **literally portray what is being said in that line**, not just be generic
architecture. The art is a depiction, not decoration. If the line says "mood boards," draw a real
material/sample board (swatch tiles), not an abstract grid. "Renders" → a real perspective view.
"First draft" → a loose-but-real floor plan. "Hours of unpaid work" → a growing stack of finished
drawing sheets (+ an unpaid invoice / struck-through payment). "Client disappears" → the figure
leaves AND the drawing-in-progress is abandoned on the board. "It's a pattern" → the loss motif
literally repeated across the frame. Read each line, ask "what exact thing/action is this?", and
draw THAT — accurately. Generic = fail.

The hook (first ~3s) can carry MORE energy than the body — faster, bolder draughting for the
scroll-stop — while the body stays calm/quiet. Energy in the hook is allowed; loudness throughout
is not.

## The two-technique system (one cohesive fine-line-on-paper look)

**1. STRUCTURES** (buildings, plans, elevations, sections, axonometric)
- Author as **exact SVG geometry**; animate **draw-on** via `stroke-dasharray`/`stroke-dashoffset`.
- Conventions: fine consistent stroke (~3px @1080), faint construction grid (`#c5c5c0`),
  dimension lines with 45° architect tick-slashes, title block + scale bar where it fits.
- Precise, confident, **no wobble**. (Do NOT use rough.js — it reads as childish scribble.)
- Reference still: `edit/samples/draught_elevation.png`.

**2. FIGURES / HUMANS / ACTIONS** (arrive, sit, leave, discuss, work)
- Generate elegant single-line **entourage** figures via **gpt-image-1** (transparent bg),
  then **recolor to graphite `#1d1d1b` on paper**; animate with a **drawing-in** left-to-right
  reveal (mask/clip wipe) so it reads as being drawn.
- Prompt register: *"minimal fine single-line architectural entourage, accurate confident
  proportion, faces minimal, no colour, no shading, no clutter, premium and quiet — NOT
  cartoonish, NOT scribbly."*
- Template: `ContentGenerator/.tmp/gen_figure_example.py` (`OPENAI_API_KEY` in
  `ContentGenerator/.env`). Reference still: `edit/samples/figure_example.png`.
- Architectural drawings have always mixed precise linework with looser entourage — the blend
  is authentic to the craft and stays cohesive when both are graphite-on-paper.
- **NEVER a stick figure** (circle head + stick limbs reads childish — rejected on Section 3).
  Humans must be REAL person-type line drawings — accurate proportion, clothed silhouette,
  the kind a skilled architect draws. Generate via gpt-image (entourage prompt), recolor to
  graphite (luminance→alpha tint: dark lines opaque, white→transparent), reveal with a
  clip-path/mask wipe. If the figure performs an action (opening a door, sitting), let gpt-image
  draw the figure AND the prop together in one PNG — cleaner than compositing separately.

## Curation logic — pick ONE treatment per beat (avoid clutter, one focal point)

| Subject of the line | Treatment |
|---|---|
| The words or a number carry it | **Clean type slide** |
| A building / plan / process | **Structure draw-on** |
| A human / action / situation | **Figure reveal** |
| A labeled list, or number + concept | **Both** side-by-side |

## Motion

Confident but calm. Structure draw-on 1.0–1.8s; figure reveal 1.0–1.5s; type fades/slides ≤24px.
Easing easeOut/easeInOut. **No bounce, spin, flash, or kinetic chaos.** Restraint = premium.

## Hook principle (first ~3 seconds)

Open with a precise drawing **draughting itself in fast** → resolve to the first line. Craft +
recognition = the scroll-stop for the ICP. Never bury the hook behind slow text.

## Sign-off

Close on terracotta with the **सेतु wordmark** (typeset cream; the lockup PNG is black-on-white
and breaks on terracotta — typeset it, or recolor the bridge symbol SVG
`setu-symbol-script-span.svg` to cream). Soft CTA only ("the free Gem · link in bio").

**Bridge symbol — do NOT let a builder hand-port the SVG paths** (it drops strokes / renders
lopsided — failed twice on S9). Instead: rasterize the official `setu-symbol-script-span.svg`
(all 4 strokes: deck span + curved left span + right upright + thin diagonal cable) to a CREAM
PNG via playwright/chromium, then **autocrop to the alpha bbox** (the source art is top-biased in
its 256² canvas — uncropped it clips under `object-fit:contain`). The tight PNG is ~624×432;
size by WIDTH (~190px), height auto. Reliable recipe: author the whole terracotta sign-off card
(bridge img + typeset सेtu + cream CTA) as one playwright-rendered 1920×1080 PNG, then composite
it over the section tail via ffmpeg `overlay` with a 0.5s alpha fade-in — far more reliable than
re-authoring the card in the HyperFrames project. Verified card: `edit/samples/signoff_card.png`;
cream bridge: `edit/samples/bridge_cream_tight.png`.

## Five-value gate (must pass before render)

work-not-tech · quiet-over-loud · respect-owners · ship-don't-slide · map-before-build.

## Build + output

- Engine: **HyperFrames** (HTML/CSS/GSAP). Lint + inspect before render.
- Render **1920×1080, 30fps, H.264 (CRF ~16)**; mux the VO; verify stills for brand fidelity.
- Derive **1:1** (LinkedIn) / **9:16** (shorts) from the 16:9 master via
  `VideoEditorHyperframes/video-use/helpers/reframe.py`.
- **Reference render / template:** `edit/samples/v1_hook_draught.mp4` and its project under
  `edit/anim_draught/` — copy that project as the starting point for new pieces.

## Founder split / PIP — BANKED (only with HD footage)

A camera+animation split ("interview + animated b-roll": founder on one side/corner, animation on
the other, shared VO) is a strong format that restores founder presence. **Do NOT use it with
low-res/480p or cluttered footage** — pairing rough camera with high-craft animation drags the
whole piece down (the contrast makes the camera look worse). Reserve for clean HD footage (proper
camera, no tinted glasses, intentional background). Recipe (proven on `section_02_split.mp4`):
ffmpeg composite — left/corner = camera (sharp-center crop), right = animation scaled into its
panel, one shared VO track, thin graphite divider `#1d1d1b`. Corner PIP (~25%) is more forgiving
than a 50/50 half-screen.

## VO / narration

- Founder VO is the spoken track (extract from a recording, or TTS as a fallback).
- Animation timeline syncs to VO beat timestamps (transcribe via `transcribe_local.py`).

### Section VO extraction — TAIL PADDING (learned, S4 clipped "buy")
- When cutting a section's VO from the master, **pad the OUT point ~0.4–0.7s past the last word's
  end** (check the transcript word `end`, not the sentence guess). Cutting exactly at the last word
  clips it. Builders must HOLD the last animation frame to ≥ the VO length (freeze/tpad) so the last
  word stays audible.
- Word `text` fields in the mlx-whisper JSON have **no trailing spaces** — join with `' '` (not raw
  concat) when reconstructing a readable script, then collapse space-before-punctuation.

### Audio correction from a SECOND take (learned, S7/S9 "v2")
When the chosen take has self-corrections (repeats / dropped words), splice clean spans from the
ALT take — **audio-only, video untouched**:
1. Scan the used transcript for adjacent repeats / near-repeat 2-grams (the stumbles). Confirm each
   against the alt take (some "repeats" are intentional rhetoric, e.g. "like you … like you").
2. **Loudness-match first:** normalize the alt take to the master's level (`loudnorm I=-16:TP=-1.5:LRA=11`)
   before cutting, else the splice jumps in volume.
3. **Keep the section's total duration identical** so the locked animation stays synced: replace the
   stumble span with the clean alt span, then **pad the leftover with silence** (if clean span is
   shorter — natural at a sentence boundary) or **mild `atempo` ≤ ~1.08** (if longer). Never let the
   length drift — downstream beats desync.
4. Splice at sample level via wav (`atrim`/`asetpts` + concat), re-mux per section (`-c:v copy`),
   re-concat. Verify by re-transcribing the rebuilt VO. (ASR may still mis-spell spoken words, e.g.
   "Gem"→"germ", "drafts"→"traps" — fix those on-screen / in copy, the audio is correct.)

### Full assembly
- Concat sections with `concat` filter + per-input `aresample=48000,aformat=channel_layouts=stereo`
  (section audio channel counts vary — mono/stereo mix breaks `-c copy` concat).
- Section seams cut from the same master timeline have silence-only overlaps at boundaries — fine.
- Derive **1:1** by **letterbox on paper** (`scale=1080:-2,pad=1080:1080:…:color=0xf2f2f0`), NOT
  center-crop — wide diagrams (OLD/NEW, two-column) lose labels if cropped. **9:16 is awkward** for
  16:9-authored wide layouts (mostly empty bands) — skip unless a piece is authored vertical.
