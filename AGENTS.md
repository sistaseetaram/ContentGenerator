# ContentGenerator — Agent Reference

Model-agnostic companion to CLAUDE.md.

## What this project is

LinkedIn content engine for Setu — ideation, scoring, drafting, and analytics. Feeds into OutreachAutomation via the shared context layer (SharedInfra/shared_context/).

## Skills (project-local)

| Skill | Trigger | What it does |
|---|---|---|
| content-ideator | "run ideator", "content ideas" | Research → score → shortlist 3-5 ideas to data/ideas.json + HTML dashboard |
| linkedin-analyzer | "log analytics", "analyze my posts" | Ingest LinkedIn metrics → steering signals → feeds content-ideator |
| loom-walkthrough-recorder | "prep a loom" | Pre-record prep packet for Loom walkthroughs |
| loom-video-analyzer | "analyze loom" | Post-record scoring against prep packet |

Skills path: `.claude/skills/`

## Shared context integration (Day-3)

Reads/writes to `SharedInfra/shared_context/store.json` via the adapter pattern:
- Reads: `brand_voice`, `icp` (from CNS/atlas)
- Writes: `published_content` (after publishing)

See `.planning/IMPROVEMENTS.md` for 20 improvement items identified Day-3.

## Entry points

```
tools/                ← Python execution scripts
workflows/            ← Markdown SOPs (what to do and how)
data/ideas.json       ← Current idea backlog
data/ideas-dashboard.html  ← Scored idea visual (hub-registered)
```

## No defined agent roles

Operates as a single-agent project (skills handle the routing). No multi-agent orchestration currently.
