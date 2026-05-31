# Creator Handoff Contract

The ideator is a **research engine**, not a generation engine. It never drafts finished content (that's the orchestrator hard-rule: sub-agents draft, and a dedicated content-creator agent — built next — does generation). The ideator's job ends when a scored shortlist exists. This file defines the contract the future content-creator reads.

## The contract

`data/ideas-latest.json` is the handoff artifact. The creator agent, when built, reads it and turns each shortlisted idea into platform-specific drafts. Shape (see `ideas-schema.md`):

```json
{
  "run_id": "idea-1780200000",
  "generated_at": "2026-05-30T09:00:00+05:30",
  "shortlist": [ /* 3–5 full idea records */ ]
}
```

## Why this shape

Each idea record already carries everything the creator needs to draft without re-researching:
- `angle` + `title` — the specific take, not a generic topic
- `pillar` + `platform` — which voice/format calibration to load
- `proof_plan` — the receipt to build the post around (the creator should refuse to draft a Setu post with no proof)
- `supporting_research[]` with `source_url` — citations and fact-anchors, so the creator's claims are verifiable
- `scores{}` — lets the creator prioritize (draft the 38-point idea before the 24-point one)

## What the creator must NOT assume

- The shortlist is `backlog` status. The creator advances status to `drafting` when it picks one up — the ideator never writes past `backlog`.
- Instagram ideas (if any) belong to the isolated funny feed only — never cross-post B2B angles there.
- The creator re-runs the brand-voice + five-value filter at draft time. Ideator scoring is a gate, not a substitute for the publish-time compliance check.

## Status of the creator

Not built this session. This contract exists so the ideator writes a stable, forward-compatible artifact today. When the creator skill is built, it consumes `data/ideas-latest.json` as-is — no ideator changes required.
