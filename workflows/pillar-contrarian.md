# Workflow — Pillar 4: Contrarian

## STATUS: HOLD — Activates Week 3+

Do not draft or publish Contrarian posts until Week 3. Deploy only after Setu voice is established and at least 15 posts are live on LinkedIn. Contrarian without proof sounds like noise. With proof, it lands.

## Objective (when active)
Challenge a widely-held belief in the AI automation space — with data, not opinion. One post/week LinkedIn. Named entities and real numbers required. Vague contrarianism is banned.

## Required inputs (when active)
- The belief to challenge: state it clearly (e.g., "LangChain is the default for AI agents")
- The counter-evidence: what you actually saw / built / measured
- Real numbers: hours, rupees, error rates, comparison data
- What the nuance is: not "X is wrong" but "X works for Y but not for Z, and here's why"

## Voice rules (when active)
- Banned words: revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses to unlock potential"
- Name the thing you're challenging clearly in line 1. Don't be coy.
- Back every claim with evidence — personal build, client data, or cited study. No vibes.
- End with the nuance, not a hot take. Nuance gets DMs; hot takes get arguments.
- Short sentences. Plain words.

## Sequence (when active)

1. Load Setu voice + positioning + ICP from `/Users/sistaseetaram/Documents/Obsidian Vault/content-wiki/wiki/concepts/`.
2. Confirm: is this backed by data Seetaram personally has? If not, defer until it is.
3. Dispatch `contrarian-drafter` sub-agent with: belief-to-challenge, counter-evidence, numbers, nuance.
4. Sub-agent returns 2 variants.
5. Dispatch `voice-checker`. Reject anything without data or that reads like rage-bait.
6. Present to user. User approves or revises.
7. Publish via `linkedin-publisher`.
8. Append to `data/posts.json` with pillar=contrarian.

## Activation checklist (complete before first use)
- [ ] 15+ LinkedIn posts live
- [ ] Week 3 started (Day 15+)
- [ ] `contrarian-drafter` skill built
- [ ] At least 1 piece of personal evidence/data ready for the first post

## Learnings log
*Append as discovered:*
- (none yet — activates Week 3)
