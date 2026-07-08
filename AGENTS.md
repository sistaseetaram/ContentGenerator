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


---

## ⚠ VAULT MIGRATION — one-time, self-removing (added 2026-07-08)

This project's secrets now live in the **AIOS vault** (`~/.config/aios-vault/master.env`),
under the project key **`ContentGenerator`**. Do this ONCE, before other work, then remove this block:

1. **WIRE** (make the entry point load from the vault instead of the local `.env`):
   **Already wired** — the entry point loads from the vault. Just VERIFY + CLEAN below.

2. **VERIFY** the keys resolve, and the project actually runs pulling from the vault:
   ```bash
   python3 ~/Desktop/Claude/SharedInfra/vault/vault_loader.py --audit ContentGenerator
   ```

3. **IF it works** (all required keys `<set>`, project runs):
   a. Overwrite `.env` with ONLY this line — strip every secret value:
      `# Secrets moved to ~/.config/aios-vault/master.env — load via SharedInfra vault_loader`
   b. **Delete this entire "VAULT MIGRATION — one-time, self-removing" block from this file.** Migration done.

4. **IF it fails** (missing keys / load error): leave `.env` untouched, report which
   keys are missing (add them to the vault via `master.env`), and keep this block for next time.

**Never print secret values** during any of this. Confirm with masked `--audit` only.
