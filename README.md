# ContentGenerator

Personal-brand content production system for Seetaram (building Setu — AI agency for India SMBs).

## What this is

WAT-framework Claude Code project that drafts, publishes, audits, and learns from content across LinkedIn, X, YouTube, Instagram. Powered by a multi-skill swarm under an Executive Agent (Phase 4).

See [the approved 30-day plan](/Users/sistaseetaram/.claude/plans/this-is-a-workflow-fluttering-hollerith.md) for full architecture, pillars, phases, and verification gates.

## Quick start

1. Copy `.env.example` → `.env`, fill keys you have (start with `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `BLOTATO_API_KEY`).
2. Subscribe to Blotato (https://blotato.com) — 7-day trial, $29/mo.
3. Read `CLAUDE.md` for the operating rules.
4. Read the plan file.
5. Ask the orchestrator for a Day-1 LinkedIn draft.

## Layout

```
workflows/       Markdown SOPs (per pillar / platform / recurring task)
tools/           Python execution scripts
data/            posts.json, metrics.json, content-calendar.json, audits/, reports/
.claude/skills/  Project-local skills (built incrementally per plan phases)
.claude/rules/   Per-topic rules (voice, dispatch, reporting)
.tmp/            Disposable intermediates
```

## Content pillars (locked)

| # | Pillar | Status |
|---|--------|--------|
| 1 | Build Receipts | ACTIVE |
| 2 | Plain-English AI Takes | ACTIVE |
| 3 | Build-in-Public Setu | ACTIVE |
| 4 | Contrarian | HOLD → Week 3 |
| 5 | ROI Case Studies | HOLD → first client |
| IG | Funny / sarcasm | ACTIVE on Instagram only |

## Platform scope (locked)

LinkedIn (primary B2B), X (daily takes), YouTube (long-form), Instagram (separate funny feed).
