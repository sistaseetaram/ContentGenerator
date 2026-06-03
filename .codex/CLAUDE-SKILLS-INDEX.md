# Claude Skills Index For Codex

This project keeps Claude-authored skills in `.claude/skills/`. Codex should reference those source files directly instead of copying their bodies into Codex memory or this repository.

## Project Skills

| Skill | Source | Use When |
| --- | --- | --- |
| `content-ideator` | `.claude/skills/content-ideator/SKILL.md` | Generate, score, schedule, or tune Setu content ideas. |
| `loom-video-analyzer` | `.claude/skills/loom-video-analyzer/SKILL.md` | Score or review recorded Loom videos against prep packets. |
| `loom-walkthrough-recorder` | `.claude/skills/loom-walkthrough-recorder/SKILL.md` | Prepare Loom walkthrough packets before recording. |

## Codex Usage Rule

When a request matches any skill above:

1. Read that skill's source `SKILL.md`.
2. Follow its workflow.
3. Read only referenced files needed for the active phase.
4. Do not copy skill bodies into prompts, docs, or new Codex skills.
5. If a skill writes visual output, provide browser-previewable HTML and open it per project `AGENTS.md`.

## Trigger Map

### `content-ideator`

Triggers include: `run ideator`, `content ideas`, `idea backlog`, `what should I post`, `score this idea`, `is this a good idea`, `mine my stack for content`, `plan next week`, `weekly schedule`, `Sunday planning`, `what should we post this week`, `tune the ideator`, `auto-develop`, `why are the ideas bad`, `improve the ideator`.

### `loom-video-analyzer`

Triggers include: `analyze loom`, `score my loom`, `review my recording`, `loom video analyzer`, `how did I do`, `score this walkthrough`.

### `loom-walkthrough-recorder`

Triggers include: `prep a loom`, `loom walkthrough`, `record a walkthrough`, `plan a loom`, `loom-walkthrough-recorder`.
