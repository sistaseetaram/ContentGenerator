# Brand Overlay Cues — Setu

Loom records raw. Overlay is applied in post-edit (Descript / CapCut / Premiere). This file is the cue spec.

## Brand tokens

| Token | Hex | Use |
|-------|-----|-----|
| Terracotta | `#1e0f09` | Primary accent — titles, callouts, lower-third bg |
| Forest | `#0e1810` | Secondary accent — alt callouts, "before" cards |
| Anthracite | `#222222` | Neutral dark — base bg, text on light |
| Light | `#ffffff` | Text on dark, slide bg |

Source: `canvas-browser/script.js` themes object.

**Canonical brand assets (wiki):**
- Visual identity poster: `/Users/sistaseetaram/Documents/Obsidian Vault/content-wiki/raw/assets/setu/setu-standard-visual-identity-system.png`
- Brand values poster: `/Users/sistaseetaram/Documents/Obsidian Vault/content-wiki/raw/assets/setu/setu-brand-values-poster.png`
- Full palette + typography spec → `setu-brand-context` skill references
- Values checklist → `wiki/concepts/setu-values.md`

## Logo placement

- **Position:** top-right corner
- **Size:** 6–8% of frame width
- **Opacity:** 85% (subtle, not screaming)
- **Padding:** ≥ 24px from edges
- **Asset:** Setu wordmark (light variant on dark recording, dark variant on light recording)

## Lower-third name tag

- **Trigger:** first 5 seconds of recording
- **Content:** "Sista Seetaram — Founder, Setu"
- **Bg:** Terracotta `#1e0f09` at 90% opacity
- **Text:** Light `#ffffff`, sans-serif
- **Duration on screen:** 4 seconds, fade out
- **Position:** lower-left, 8% padding from edges

## Terracotta accent moments

Apply terracotta overlay accent (background color flash, callout box, or highlight stroke) at:
- Hook end (first 5–10s, after the line lands)
- Each beat boundary (1s color sweep transition)
- Numbers reveals ("$1", "$0.06", "94%", etc.) — number gets a terracotta underline for 2s
- Close (final 3s — terracotta lower-third with CTA)

## Mute / cut markers

Mark in raw recording for editor:
- **Intro dead air:** first 0–3s usually trimmable
- **"Uhm" / "so" / "like" filler:** mark each as cut candidate
- **Long pauses:** > 2s = candidate cut (unless intentional beat break)
- **Tab-switching:** if user fumbles browser tab, mark as cut + redo

## Output in prep packet

Render as bullet list. No paragraphs. Examples:

```
- Logo top-right, 7% width, 85% opacity, light variant (dark recording bg)
- Lower-third at 0:02–0:06 — "Sista Seetaram — Founder, Setu", terracotta bg
- Terracotta accent on numbers: $1, $0.06, 94%, $5/day
- Mark cuts: intro dead air, every "uhm", any pause > 2s
```
