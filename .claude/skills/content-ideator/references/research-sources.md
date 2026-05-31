# Research Beats

The ideator fans out one subagent per **beat**. A beat is a distinct hunting ground — keeping them distinct prevents 10 agents from returning the same trending headline. Default 7 beats; the user can ask for fewer (5) or more (up to 10). Each beat agent returns 3–8 raw findings, each a `{headline, why_it_matters, source_url, angle_seed}`.

The strategic filter across every beat: hunt for **what ChatGPT can't already answer**. A headline everyone has is table stakes — the value is the pattern-interrupt, the contrarian data point, the thing the user can attach a real receipt to.

## The beats

1. **New releases this week** — n8n, Claude/Anthropic, agent frameworks, LLM pricing changes. What shipped, what it actually changes for a builder. Skip press-release hype; find the practical delta.

2. **Pattern-interrupts** — where popular AI-automation advice fails or is oversold. "Everyone says use an agent for X; here's where the dumb cron wins." This beat is the contrarian goldmine — genuine disagreement backed by evidence is inherently new information.

3. **Competitor content gaps** — what established AI-automation creators publish, and more importantly what they *skip*. The honesty gap (most content oversells "80% time saved") is a wide-open lane. Find the unanswered question in their comments.

4. **Build-in-public angles** — the user's own recent commits, shipped skills, and infra decisions (mem 1121: dev activity is content). Read recent git log + `data/posts.json` for what's already covered, so this doesn't repeat published posts.

5. **Contrarian / honesty angles** — the "I measured 23%, not 80%" lane. Real numbers that contradict the marketing consensus. Needs the user to actually have measured something — flag when it's speculative.

6. **Owner/SMB pain points** — what business owners actually struggle with around AI adoption right now (forums, Reddit, LinkedIn comments). Grounds ideas in audience reality, not builder navel-gazing.

7. **Own-stack content miner** — see below. The highest-value beat.

## Own-stack content miner (beat 7)

The user's real tech stack and cost wins are unfakeable content no competitor or chatbot can produce. This beat turns "what I actually built and optimized" into ideas like *"I cut report cost $1 → $0.06 by doing X."*

**Primary source — the tech-stack auditor report (when it exists):**
A separate, future skill (the tech-stack auditor) maintains a spec of *task → model → handling agent* (crons, embeddings, summarization, daily security checks, website builds, …) plus optimization suggestions ("have you implemented this? this cut my cost"). Each entry and each suggestion is a content angle.

The report path is a **placeholder** — the user will supply it later (it will live locally + a latest copy on Google Drive + likely ingested into the Obsidian wiki JSON). Until then `tech_stack_report_path` is unset.

**Fallback when the report path is unset (works today):** scan, in order, and synthesize what the user has actually built/optimized:
- `/Users/sistaseetaram/Desktop/Claude/claude-datastore/SKILL-REGISTRY.md` — skills shipped
- recent `git log --oneline -30` in the project — what changed lately
- `tools/model_router.py` `CHAINS` + `CLAUDE.md` model-stack table — routing/cost decisions made
- `data/model_spend.json` — real cost numbers (proof-level gold)
- the Obsidian `wiki/index.md`, then specific pages on demand

Wiring the real report path later is a one-line config change (`tech_stack_report_path`) — no restructure. When the user provides it, update this file and `gather-interface.md`.

## Source-quality note

Prefer primary sources (official docs, the user's own repo/spend data, real owner conversations) over aggregator listicles. Every finding carries a `source_url` so the synthesis stage can cite and the proof stage can verify. A finding with no checkable source is a rumor — mark it and down-weight it.
