# Gather Interface

The research **gather** step is deliberately pluggable. How findings are collected (the expensive, slow part) is separated from how they're synthesized and scored (the cheap, deterministic part), so the collection mechanism can change later without touching the rest of the skill.

## Modes

| Mode | How it gathers | Cost | When |
|------|----------------|------|------|
| `subagents` (v0.1 default) | One Claude Code Task subagent per beat, each with WebSearch + Exa + Firecrawl | session Claude on gather only | best research depth, agentic browsing |
| `router` | Deterministic Python loop calling `route("research-summarize", …)` per beat with a search-results payload | ~$0 (free model first) | cheapest, shallower (no agentic browsing) |
| `hybrid` | Some beats via subagents (deep), some via router (cheap) | mixed | tune after first runs |

v0.1 ships `subagents`. The other modes are documented targets, not built yet — don't implement them now; just don't hard-code assumptions that block them.

## The contract every mode honors

Whatever the mode, gather returns a flat list of findings, each:

```json
{
  "beat": "pattern-interrupts",
  "headline": "short factual claim",
  "why_it_matters": "1-2 sentences",
  "source_url": "https://… (or 'internal:git-log' for own-stack)",
  "angle_seed": "the raw content angle this could become"
}
```

Synthesis and scoring consume only this shape. They never know or care which mode produced it. That's the whole point — it's why swapping modes later is cheap.

## Subagent dispatch (v0.1)

One subagent per beat, all spawned in the same turn (parallel). Each gets:
- the beat definition from `research-sources.md`
- the date window (default: last 7 days for trend beats; all-time for own-stack)
- recent `data/posts.json` topics, so it avoids re-surfacing already-published angles
- instruction to return 3–8 findings in the contract shape above, nothing else

Beat 7 (own-stack miner) is a special subagent: it reads `tech_stack_report_path` if set, else runs the fallback scan from `research-sources.md`.

## Config knobs

- `num_beats` (default 7, range 5–10)
- `gather_mode` (default `subagents`)
- `date_window_days` (default 7)
- `tech_stack_report_path` (default unset → own-stack fallback scan)
