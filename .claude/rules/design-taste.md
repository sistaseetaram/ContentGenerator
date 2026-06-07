# Design Taste — Seetaram (LEARNED, persistent)

Load this before designing ANY visual artefact (infographic, carousel, thumbnail, banner, post image). These are generic taste rules distilled from real feedback — apply them, never make the user repeat them. Append new lessons here whenever the user reacts to a design (liked / disliked + why).

## Operating principle
Act as a **professional brand designer**, not a layout generator. Before producing, recall what separates pro editorial/brand work: intentional type scale, generous consistent margins, a baseline grid, one focal point, restraint, optical alignment. "Interesting" does NOT mean busy, dynamic, or over-exerted — plain colors done smoothly can be the most attractive. Calm + expensive + legible beats decorated.

## DISLIKED (do not repeat)
- ❌ **Paper-white canvas split with a heavy dark footer band.** The two-block split looks hurried and the color combination reads poorly. Avoid canvas-color + contrasting-block splits.
- ❌ **White (#fff/#f2f2f0) paired with terracotta-dark (#1e0f09)** as the dominant combo — disliked.
- ❌ **Extreme type-scale jumps** — tiny label (e.g. 10–11px) next to a huge title (e.g. 70px) with nothing between. First line too small, next line too big = bad. Text that is "very big, then very small" is a fail.
- ❌ Any text that is **not clearly legible** (too small) or **overpowering** (too big).
- ❌ Anything that "looks made in a hurry."
- ❌ Stating **factually wrong copy** on an artefact (e.g. claiming a task is done a certain way when it isn't). Verify the claim before it goes on a design.
- ❌ Generic SaaS look, gradients, neon, brain/robot/AI cliches (also a hard brand rule).

## LIKED / WANTED
- ✅ **Smooth, cohesive, single-canvas palettes.** One color world, not split blocks.
- ✅ **Balanced modular type scale** — readable label → comfortable steps → headline. No jarring jumps.
- ✅ Editorial restraint (Kinfolk / Aesop / Cereal magazine energy): whitespace, hairline rules, confident serif headline + calm sans body.
- ✅ Plain colors are fine — make them feel intentional and premium, not flat/lazy.
- ✅ Show the user **comparison options** (e.g. Canva vs image-gen vs HTML) before locking, so taste can be expressed by choosing.

## ★ DEFAULT PIPELINE (user-mandated 2026-06-02)
- **Do NOT hand-build designs yourself** (no self-authored HTML layouts, no Canva). User: "you are not doing this very well."
- **Always hand a LOOSE, descriptive prompt to gpt-image** (image-gen) and let IT generate. Loose = describe the idea, audience, message, vibe, and the elements to show — let the model art-direct. Don't over-constrain layout.
- After gpt-image returns, **composite the real सेtu wordmark + bridge symbol via the HTML overlay pass** (compositing the logo is allowed; designing the whole graphic is not).
- **LIKED reference style (the bar to hit):** rich editorial photo-composite — split layout, signature-dark panel with a large light serif headline, a clean data list with small realistic task thumbnails (mood-board swatches, a spreadsheet, an email mock, a chat quote) + time totals per row, a real premium design-studio photo on one side, and a dark summary band at the bottom (total hours lost → "get those hours back for design"). Calm, premium, scroll-stopping — a high-end studio's own brand, NOT a generic tech infographic.

## Process rule
- When the user criticizes a design, treat it as a **generic lesson** and append it here (pattern, not one-off). Never require the same correction twice.
- Default to the all-paper light editorial direction or a single cohesive dark (forest/anthracite) — never the paper+terracotta-dark split — unless the user picks otherwise.

## Engine notes (learned)
- ✅ **gpt-image-1 with a strict palette + editorial-restraint prompt** produced the LIKED result (paper bg, warm near-black type, balanced modular scale, calm magazine feel). This is the go-to for prototyping a layout direction.
- ❌ **Canva generate-design with NO brand kit loaded** is unreliable: it ignored the palette (navy/gold/lavender/pink), defaulted to portrait not 1080×1080, and **fabricated fake statistics and fake quotes** (Peter Drucker, "Creative Leader", invented %). Do NOT use Canva for data/number artefacts until a Setu brand kit exists in the account. Fabricated stats violate the "real hours, real money" rule.
- ✅ **Winning pipeline:** gpt-image-1 for the editorial base → HTML+playwright overlay pass to composite the REAL सेtu wordmark + bridge symbol (image-gen can't draw the logo). Place logo in a clear margin corner; check for collision with existing text.

## ★ MANDATORY PRE-FLIGHT — before any visual (added 2026-06-06, violated 3× without this)

**Step 0 — always, before touching a pixel:**
1. Load `content-wiki/wiki/index.md` → find `syntheses/design-pipeline.md` → read it. This file has the full token table, SVG asset paths, and the exact pipeline. It takes 10 seconds.
2. Token truth lives in `MyPersonalBrand/setu-brand/03-collateral/assets/brand-kit/tokens/setu-tokens.json`. Do NOT guess or invent values.

**Setu brand tokens (snapshot — still verify from source):**
- LinkedIn canvas: `#f2f2f0` bg / `#111111` text (paper theme)
- Premium / signature: `#1e0f09` bg / `#f2ddd3` text (terracotta dark)
- **NO accent color exists in the palette.** Setu is monochrome-per-theme. Never invent a highlight color (e.g. `#c8593a` was wrong — invented, not a brand token).
- Typography: Cormorant Garamond (display wt 300, h1 wt 500), Inter (body wt 400, label wt 500)
- Bridge symbol SVG: `setu-symbol-script-span.svg`; Wordmark: `setu-wordmark-light.svg` (strip white bg rect for transparency)

_Last updated: 2026-06-06 — brand color/weight violation corrected 3× on post-008 carousel. Root cause: skipped wiki index. Fix: mandatory Step 0._
