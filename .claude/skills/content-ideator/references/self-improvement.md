# Self-Improvement and Auto-Development Loops

Two distinct loops keep the ideator getting better through use. The first (Phase 9) fires after every run and captures immediate human signal. The second (Phase 10) fires periodically and applies evidence-based changes — it's what makes the skill genuinely autonomous over time rather than just static.

---

## Loop 1: Post-Run Feedback (Phase 9 — fires after every Generate run)

**Trigger:** immediately after Phase 8 (Slack delivery), before closing the session.

Ask exactly three questions — don't merge them, don't skip them:

1. **Idea quality:** "Looking at the shortlist — any ideas that felt weak or off-brand? Any that felt obviously right? One line each."
2. **Beat signal:** "Which research beat seemed most useful? Was anything in the shortlist clearly from a weak source?"
3. **Rubric miss:** "Any idea that scored high but felt wrong (overscored), or scored low but felt strong (underscored)?"

**What each answer changes:**

| Signal | What to update |
|--------|----------------|
| An idea felt weak despite high score → specific dimension was wrong | Add Applied Learning bullet; if same dimension misfires 2+ runs, propose weight change in Phase 10 |
| A beat was clearly useless this run | Increment `beat_performance[beat].low_signal_count` in `ideator-meta.json` (track silently) |
| A beat was clearly the best source | Note it; if consistent for 3+ runs, propose reallocating agents toward it in Phase 10 |
| An idea angle felt wrong despite passing the rubric | Update `references/idea-rubric.md` with a new "watch-out" note under the relevant dimension — don't change weights yet, document the pattern |
| Voice gate missed a weak angle | Add the specific pattern to `references/idea-rubric.md` under "Voice gate watch-outs" |

**If any answer is non-trivial:**
- Update the relevant reference file immediately
- Append one Applied Learning bullet (≤15 words) to SKILL.md
- If the change is structural (new dimension, new beat, scoring logic change), bump SKILL.md frontmatter version to next minor (v0.1 → v0.2)

**If all answers are empty or "looks fine":** note it silently in `ideator-meta.json` run record — the run produced ideas that felt right. No action needed.

**Trigger words for immediate skill update:** "that scored wrong", "the beat was useless", "that idea was weak", "that's not what I post", "the angle was off", "none of these are real ideas".

---

## Loop 2: Auto-Development (Phase 10 — evidence-based, periodic)

**Trigger conditions (check at start of every Phase 9):**

- `auto_dev_triggers.runs_since_last_beat_analysis >= beat_analysis_every_n_runs` → run beat analysis
- `auto_dev_triggers.posts_since_last_weight_tune >= weight_tune_every_n_posts` → run weight calibration
- User explicitly says "tune the ideator", "auto-develop", "why are the ideas bad", "the rubric is off"

**If no trigger condition is met:** skip Phase 10 entirely. Don't analyze for the sake of analyzing.

---

### Sub-loop A: Beat Performance Analysis (every 5 runs)

Read `data/ideator-meta.json` → `beat_performance`. For each beat compute:

```
shortlist_rate = shortlisted / candidates_generated   (0–1)
post_rate      = posted / shortlisted                  (0–1, once data exists)
```

**Action thresholds:**

| Condition | Proposed change |
|-----------|----------------|
| `shortlist_rate < 0.05` over 5+ runs | Propose removing/replacing that beat |
| `shortlist_rate > 0.60` over 5+ runs | Propose allocating 2 agents to this beat instead of 1 |
| `own-stack-miner` shortlist_rate < 0.20 | Warn: own-stack fallback scan may be stale; suggest user provide `tech_stack_report_path` |
| A beat shows 0 candidates for 3+ consecutive runs | The beat definition may be too narrow — propose broadening its query |

**Present proposed changes to the user.** Wait for "yes" before updating `references/research-sources.md`. Append an `applied_changes` record to `ideator-meta.json` when applied.

---

### Sub-loop B: Rubric Weight Calibration (every 10 posted ideas)

Requires `data/ideas.json` to have ≥10 ideas with `status="posted"`.

Cross-reference posted ideas against their stored `scores{}`. For each dimension, compute:
- `mean_score_for_posted` — average dimension score among ideas that reached `posted`
- `mean_score_for_backlog` — average dimension score among ideas still in `backlog`
- `discriminating_power = mean_posted - mean_backlog` (positive = this dimension predicted posting; near-zero = dimension doesn't differentiate)

**Action thresholds:**

| Condition | Proposed change |
|-----------|----------------|
| A dimension's `discriminating_power < 0.2` for 10+ posted ideas | Propose reducing its weight by 0.25 |
| A dimension's `discriminating_power > 1.5` | Propose increasing its weight by 0.25 |
| `lived_exp` or `proof_level` ever show `discriminating_power < 0.3` | Flag explicitly — this contradicts the core strategic bet; do not silently reduce these weights, ask the user to review the strategy |

**Present the before/after weight table.** Example:

```
Proposed rubric weight change (based on 12 posted ideas):

Dimension    | Current | Proposed | Evidence
-------------|---------|----------|----------
new_info     |   1.5   |   1.75   | highest discriminating power (2.1)
timeliness   |   1.0   |   0.75   | near-zero discriminating power (0.15)
effort       |   0.75  | unchanged| no signal yet (n=3 only)
```

Wait for user confirmation. On apply: update `references/idea-rubric.md` weights table, append to `rubric_weight_history[]` in meta with reason, bump SKILL.md version.

---

### Sub-loop C: Trigger-Phrase Freshness (every 10 runs)

Read last 10 run records from `ideator-meta.json`. Look for entry modes or phrasings that triggered the skill but weren't in the description. Example: if the user said "mine my recent builds" three times and it's not in the description triggers, add it.

Also: if Rate mode is being used significantly more than Generate mode, consider whether a dedicated `rate-idea` trigger phrase should be added.

This sub-loop auto-updates the SKILL.md `description` field without asking (trigger phrases only — never the substance). Log the change in `applied_changes`.

---

## Meta-tracking: what to log every run

At the end of Phase 7 (JSON report), update `data/ideator-meta.json`:

```json
{
  "runs": [
    {
      "run_id": "idea-1780200000",
      "ts": "2026-05-30",
      "mode": "generate",
      "num_beats": 7,
      "candidates_generated": 14,
      "shortlisted": 4,
      "cost_usd": 0.012,
      "beat_breakdown": {
        "own-stack-miner": {"candidates": 3, "shortlisted": 2},
        "pattern-interrupts": {"candidates": 2, "shortlisted": 1},
        "new-releases": {"candidates": 4, "shortlisted": 1},
        "competitor-gaps": {"candidates": 2, "shortlisted": 0},
        "build-in-public": {"candidates": 1, "shortlisted": 0},
        "contrarian-honesty": {"candidates": 1, "shortlisted": 0},
        "owner-pain-points": {"candidates": 1, "shortlisted": 0}
      },
      "feedback_quality": "non-trivial"
    }
  ]
}
```

Aggregate `beat_breakdown` into `beat_performance` cumulative totals. Increment `runs_since_last_beat_analysis`. Read `data/posts.json` → count ideas with `status=posted` that weren't counted before → increment `posts_since_last_weight_tune`.

---

## Version discipline

- **Applied Learning bullet only** → no version bump (just a note for future runs)
- **Reference file update (rubric note, beat watch-out)** → no version bump
- **Rubric weight change or beat definition change** → bump minor (v0.1 → v0.2)
- **New phase, new dimension, new beat** → bump minor
- **Gather mode change, storage contract change** → bump minor

Never bump to v1.0 without the user explicitly deciding the skill has been validated across 20+ posts.
