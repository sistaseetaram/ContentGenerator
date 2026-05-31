# Idea Scoring Rubric

Every candidate idea is scored 1–5 on seven dimensions. The shortlist is the top 3–5 by weighted total. The rubric encodes the Setu content strategy: in the AI era, information alone is worthless (the viewer can ask ChatGPT). What wins is **new information + lived experience + proof** — the things a competitor and a chatbot cannot fake. The rubric exists to push every idea toward that, not toward generic "good topic" instinct.

## The seven dimensions

| # | Dimension | 1 (low) | 5 (high) | Weight |
|---|-----------|---------|----------|--------|
| 1 | **Pillar fit** | doesn't map to any ACTIVE pillar | maps cleanly to one ACTIVE pillar, on-cadence | 1.0 |
| 2 | **Brand-value fit** | violates a value, or hollow | passes all five values, embodies ≥2 | 1.0 |
| 3 | **New information** | ChatGPT answers it fully | genuine pattern-interrupt / contrarian truth ChatGPT can't produce | 1.5 |
| 4 | **Lived-experience available** | no real receipt to anchor it | user has a concrete build/number/failure to tell | 1.5 |
| 5 | **Proof level** | claim only (proof level ≤2) | can hit proof level 4+ (screen recording, dashboard, real invoice) | 1.5 |
| 6 | **Timeliness** | evergreen, no urgency | rides a current release/trend window closing soon | 1.0 |
| 7 | **Effort** | days of work / needs assets we lack | low effort, assets already exist (5 = easiest) | 0.75 |

`total_score` = Σ(score × weight). Max = 41.25. Carry it raw; don't normalize (keeps deltas legible run-to-run).

## Why dimensions 3–5 are weighted highest

This is the whole strategic bet. A beginner brand with near-zero following cannot win on reach or production polish. It wins on **specificity that can't be faked**: "I built the same n8n workflow three times; v1 was $1/run and broke on a webhook retry at 2am, v3 is $0.06 — here's the exact line that fixed it." That single idea scores 5/5/5 on new-info/lived-exp/proof. A generic "5 tips for n8n automation" scores ~2/1/1 and should never make the shortlist even if pillar fit is perfect.

When in doubt, ask: **would this be impossible for someone who wasn't there to write, and can we show the receipt?** If yes, it's a Setu idea.

## The proof hierarchy (for dimension 5)

From weakest to strongest — score dimension 5 by the highest level this idea can realistically reach:

1. Claim, no evidence (avoid)
2. Anecdotal ("I've seen this work")
3. Self-reported data ("I got these results")
4. **Visual documentation** (screenshot, screen recording, dashboard) ← floor for shortlist
5. Live demonstration (doing it in real time)
6. Third-party results (someone else got results with the method)
7. Auditable public data

## The five brand values (for dimension 2)

Load `setu-values.md` from the wiki to score precisely. Summary:
- **Work, not tech** — outcome and craft over tool worship
- **Quiet over loud** — no hype, no banned words
- **Respect owners** — speak to business owners as peers, never down
- **Ship, don't slide** — bias to shipped, honest, in-progress work
- **Map before build** — thinking shown, not just results

## Voice gate (hard filter, applied after scoring)

Every idea title and angle is checked against the banned-word list before it reaches the shortlist. Banned: *revolutionary, game-changing, disrupt, synergy, cutting-edge, "empowering businesses to unlock potential."* An idea that needs a banned word to sound interesting is a weak idea — reword or drop it. Load `setu-voice.md` from the wiki for the full copy test when a borderline case appears.

## Output

Each scored idea carries its per-dimension scores in `scores{}` plus the `total_score`, so the dashboard and the future creator can sort, filter, and explain *why* an idea ranked where it did. Always include a one-line `proof_plan` — the specific receipt the user would show — because an idea without a proof plan is a topic, not a Setu idea.
