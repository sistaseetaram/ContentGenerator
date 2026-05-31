# Ideas Storage Schema

Ideas live in local JSON — `data/ideas.json` is the source of truth, mirroring the `data/posts.json` house pattern (free, in-repo, version-controlled, zero auth). A cloud mirror (Google Sheet / ClickUp) is a deferred v0.2 option, only if mobile / sister-direct-input proves needed.

## `data/ideas.json`

Top-level object, append-only `ideas[]` array. One record per idea:

```json
{
  "ideas": [
    {
      "id": "idea-001",
      "created_at": "2026-05-30",
      "run_id": "idea-1780200000",
      "title": "Same workflow, 3 rebuilds, $1 → $0.06",
      "angle": "Show the exact line that dropped cost 94%, not the finished workflow.",
      "pillar": "build-receipts",
      "platform": "linkedin",
      "source": "agent",
      "scores": {
        "pillar_fit": 5,
        "value_fit": 5,
        "new_info": 5,
        "lived_exp": 5,
        "proof_level": 5,
        "timeliness": 3,
        "effort": 4
      },
      "total_score": 38.25,
      "proof_plan": "Screen-record the diff + paste real model_spend.json numbers.",
      "supporting_research": [
        {"headline": "...", "source_url": "internal:model_spend.json"}
      ],
      "status": "backlog",
      "strategic_opinion": {
        "verdict": "post_now",
        "reason": "Proof exists (model_spend.json), on-path for Build Receipts, right brand stage.",
        "when_to_post": "now",
        "timing_note": "Screen-record ready → post this week."
      }
    }
  ]
}
```

## Field rules

- `id` — `idea-NNN`, zero-padded, monotonic across the whole file (read max existing, increment).
- `source` ∈ {`agent`, `user`, `sister`}. `agent` = produced by the research fan-out. `user`/`sister` = a human idea submitted for rating.
- `scores` — all seven rubric dimensions, 1–5. See `idea-rubric.md`.
- `total_score` — Σ(score × weight), raw (max 41.25). Don't normalize.
- `proof_plan` — required, one line. An idea with no proof plan is a topic, not a Setu idea — don't store it without one.
- `platform` ∈ {linkedin, x, instagram, youtube} (locked scope). Instagram only for the isolated funny feed — never auto-assign B2B ideas to it.
- `status` ∈ {`backlog`, `drafting`, `posted`} — lifecycle; ideator only ever writes `backlog`.
- `strategic_opinion` — required on every record (agent or user-submitted). Four sub-fields:
  - `verdict` ∈ {`post_now`, `post_later`, `drop`}
  - `reason` — one sentence: why this verdict (on-path, proof-ready, sequencing risk, positioning leak, etc.)
  - `when_to_post` — `"now"` | `"Week N"` | `"after first client"` | `"after N followers"` etc.
  - `timing_note` — what must be true before posting (proof needed, audience size, brand stage)

## `data/ideas-latest.json`

Snapshot of the current run's shortlist (the 3–5 that made the cut). This is the **creator-handoff contract** — see `creator-handoff.md`. Overwritten each run:

```json
{
  "run_id": "idea-1780200000",
  "generated_at": "2026-05-30T09:00:00+05:30",
  "shortlist": [ /* full idea records, same shape as above */ ]
}
```

## Concurrency / safety

Read-modify-write the whole file. Before writing, confirm the JSON parses and `ids` are unique. Never truncate `ideas[]` — it's the historical feed the analyzer and dashboard depend on. If the file is missing, initialize `{"ideas": []}`.
