# Workflow — Tech Stack Revisit

## Objective
Day-7 review: check actual model spend vs plan, identify any routing misfires, recommend adjustments. Prevents cost overrun and keeps model choices calibrated to reality.

## Trigger
Day 7 (+ every 30 days after that). Run before content planning session.

## Required inputs
- `data/model_spend.json` populated with at least 7 days of calls
- Anthropic + OpenAI billing page screenshots or export (manual step by user)

## Sequence

1. Load `data/model_spend.json`. Aggregate:
   - Total spend per model (7-day)
   - Spend per task_type per model
   - Fallback_depth distribution (how often did primary fail?)
   - Average latency per model
   - Any `ModelRouterExhausted` events (all 3 in chain failed)
2. Cross-reference with budget:
   - Claude daily budget guard set at $5/day. Did it trigger? How often?
   - Any model >40% of total 7-day spend → flag for review
3. Dispatch `tech-stack-monitor` sub-agent (Phase 2) OR run analysis in-session (Phase 1).
4. Monitor produces recommendation table:
   ```
   | Task type | Current primary | Actual cost/call | Quality (1-5) | Recommendation |
   |-----------|----------------|-----------------|---------------|----------------|
   | long-form | claude-sonnet-4-6 | $0.03 | 5 | Keep |
   | short-post | gpt-4o-mini | $0.001 | 4 | Keep |
   ...
   ```
5. User reviews. Approves or overrides each recommendation.
6. For approved changes: update routing table in `tools/model_router.py` CHAINS dict.
7. Log decision to `decisions/` (if ContentExecutiveAgent exists) or append to plan file.
8. Ingest findings to wiki: `wiki/syntheses/tech-stack-review-YYYY-MM-DD.md`

## Checks to run manually (supplement automated analysis)
- Is DeepSeek-V3 actually available via API at plan time? (Verify key in `.env`, test call)
- Is Groq Llama 3.3 70B still free-tier adequate for lint/dispatch volume?
- Did any model have a notable outage week? (Check status pages)
- Any new model releases worth adding to a chain?

## Decision criteria for swap
- Cost >40% of total budget AND quality parity with cheaper alternative → swap primary
- Fallback_depth >30% of calls for a task type → primary is unreliable, promote fallback to primary
- Latency consistently >45s for task type → swap to faster model
- Quality score <3 from user assessment → always swap regardless of cost

## Expected outputs
- Recommendation table (in-session or from tech-stack-monitor skill)
- Updated `tools/model_router.py` CHAINS (if changes approved)
- `data/audits/cost/YYYY-MM-DD.json` (spend summary)
- Wiki entry: `wiki/syntheses/tech-stack-review-YYYY-MM-DD.md`
- Plan file note: "Day 7 tech stack: [summary of changes]"

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
