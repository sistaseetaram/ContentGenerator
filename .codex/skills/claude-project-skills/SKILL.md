---
name: claude-project-skills
description: Use when working in the ContentGenerator project and the user asks for content ideation, Setu content scheduling, scoring content ideas, Loom walkthrough prep, Loom recording review, or referencing/importing Claude-authored project skills into Codex without duplicating their bodies. Routes Codex to the canonical Claude skill files under .claude/skills and loads them only on demand. Triggers: "run ideator", "content ideas", "idea backlog", "what should I post", "score this idea", "plan next week", "weekly schedule", "tune the ideator", "prep a loom", "loom walkthrough", "record a walkthrough", "analyze loom", "score my loom", "review my recording", "import Claude skills", "reference Claude skills".
---

# Claude Project Skills Bridge

Use this bridge to keep Codex aligned with project-local Claude skills without copying skill bodies.

## Index

Read `.codex/CLAUDE-SKILLS-INDEX.md` first when routing is unclear.

## Routing

| Request Pattern | Canonical Skill |
| --- | --- |
| Content ideas, idea scoring, backlog refresh, weekly schedule, ideator tuning | `.claude/skills/content-ideator/SKILL.md` |
| Loom prep, walkthrough outline, recording packet | `.claude/skills/loom-walkthrough-recorder/SKILL.md` |
| Loom review, recording score, walkthrough analysis | `.claude/skills/loom-video-analyzer/SKILL.md` |

## Workflow

1. Pick the matching canonical skill from the routing table.
2. Read that source `SKILL.md`.
3. Follow its workflow exactly enough for the user's request.
4. Load referenced `references/`, `scripts/`, or project files only when the active phase needs them.
5. Keep generated outputs in the locations named by the canonical skill.

## Non-Duplication Rule

Do not copy canonical skill bodies into this bridge, prompts, or docs. This bridge stores only route metadata.

## Visual Workflow Rule

Project `AGENTS.md` requires browser-previewable inspection for visual work. If canonical skill creates or updates dashboards, previews, slide plans, visual boards, graphics, diagrams, or similar assets, create/update an HTML preview and open it in the user's browser.
