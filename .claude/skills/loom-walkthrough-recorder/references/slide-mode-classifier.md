# Slide-Mode Classifier

Classify the walkthrough into one of 4 modes. Use signals from the topic + pillar.

## Modes

### `none` — pure screen recording
- Topic is "show me how I did X" with a screen artifact (n8n flow, IDE, dashboard, automation)
- The screen is the evidence
- Slides would slow it down
- Examples: "n8n stock analysis 3-version walkthrough", "live debug of fallback chain", "tour of my Setu repo"

**Slide count:** 0

### `suggested` — light scaffolding (default for most build-receipts)
- Mostly screen, but 1–3 framing slides help (title card, before/after numbers, takeaway)
- User builds slides if mood permits — packet lists what they'd contain
- Examples: "build receipt with cost numbers", "before/after architecture comparison"

**Slide count:** 1–3 (title, optional mid-card, optional close)

### `strongly-recommended` — slides materially raise comprehension
- Concept comparisons, architectures, decision trees
- Audience can't follow without a visual anchor
- Examples: "what is a fallback chain", "how subworkflows changed our cost", "diagram of the agent stack"

**Slide count:** 3–6 (cover key concepts, 1 per beat)

### `slide-dominant` — slides drive, screen recording is supporting
- Strategy talks, frameworks, opinion essays in video form
- No live demo or screen is incidental
- Examples: "why most AI automations fail in week 2", "the 5-pillar content strategy", "build-in-public manifesto"

**Slide count:** every beat = 1 slide minimum; 6–12 total typical

## Decision algorithm

```
if topic mentions ("walkthrough", "live", "tour", "demo", "show how"):
    base = none
elif topic mentions ("explain", "what is", "how does", "framework", "strategy"):
    base = strongly-recommended
elif topic mentions ("manifesto", "opinion", "case for", "why X"):
    base = slide-dominant
else:
    base = suggested

# bump based on pillar
if pillar == "plain-english-ai-takes" and base == none:
    base = suggested  # explainer pillars benefit from at least a title slide

if pillar == "build-receipts" and base == strongly-recommended:
    base = suggested  # receipts should let the screen speak

return base
```

## Output

When classifying, emit:

```
Slide mode: <classification>
Justification: <one sentence — what in the topic triggered this>
```

## Duration → slide count cap

Independent of mode, never exceed:

| Duration | Max slides |
|----------|-----------|
| ≤ 5 min  | 4 |
| 5–10 min | 8 |
| 10–15 min | 12 |
| > 15 min | 16 |

If `slide-dominant` would exceed cap, merge beats.
