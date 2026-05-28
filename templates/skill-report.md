# Skill Report Schema

Every ContentGenerator skill emits one JSON file on completion to:

```
data/reports/YYYY-MM-DD/{skill-name}-{unix-timestamp}.json
```

## Schema (required keys)

```json
{
  "skill": "loom-walkthrough-recorder",
  "version": "0.1.0",
  "run_id": "lwr-1716912345",
  "started_at": "2026-05-28T21:30:00+05:30",
  "finished_at": "2026-05-28T21:32:14+05:30",
  "duration_s": 134,
  "status": "success",
  "inputs": {
    "topic": "...",
    "target_duration_min": 8,
    "pillar": "build-receipts",
    "repurpose_targets": ["linkedin", "youtube"]
  },
  "outputs": {
    "prep_packet_path": "data/loom-preps/2026-05-28-n8n-3-versions.md",
    "primary_artifact_kind": "loom-prep"
  },
  "model_calls": [
    {
      "task_type": "long_form",
      "model_used": "claude-sonnet-4-6",
      "fallback_depth": 0,
      "tokens_in": 1240,
      "tokens_out": 980,
      "cost_usd": 0.0182,
      "latency_s": 4.3
    }
  ],
  "cost_total_usd": 0.0182,
  "notes": "Optional free text. Reasons for fallback, deviations, etc."
}
```

## Field rules

- `status` ∈ {`success`, `partial`, `failure`}
- `partial` = primary output produced but a non-blocking step failed (e.g. wiki ingest)
- `failure` = primary output not produced
- `model_calls[]` populated from `tools/model_router.py` `route()` return shape (`model_used`, `fallback_depth`, `tokens_in`, `tokens_out`, `cost_usd`, `latency_s`, `task_type`)
- `cost_total_usd` = sum of `model_calls[*].cost_usd`
- Timestamps ISO 8601 with timezone offset (IST `+05:30` for this user)
- `run_id` format: `{skill-short}-{unix-seconds}` (e.g. `lwr-…`, `idea-…`, `lia-…`)

## Why this schema exists

- Cost tracking: feeds `data/model_spend.json` aggregation
- Audit trail: every skill run is reconstructable
- Self-improvement: skill failure patterns are queryable across history
- Analyzer feedback: `linkedin-analyzer` correlates skill runs → published posts → engagement
