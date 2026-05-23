# Workflow — Wiki Health Check

## Objective
Periodic sweep of the Obsidian wiki for noise, duplicates, stale entries, and contradiction. Keeps the wiki useful as source of truth for agents. Fires monthly OR when entry count grows >20% in a week.

## Trigger conditions
- Monthly (first Sunday of each month)
- Wiki entry count delta >20% in 7 days (threshold alert via macOS notification + plan file note)
- Manually when wiki "feels noisy" after heavy ingest weeks

## Sequence

1. Run `wiki-health-checker` skill (Phase 2) OR manually invoke `llm-wiki-lint` skill (available now).
2. Lint checks:
   - Duplicate detection: entries covering the same concept with conflicting data
   - Stale entries: files not updated in >30 days that reference time-sensitive data (model pricing, API limits, competitor analysis)
   - Orphan entries: files with no `[[links]]` to any other wiki file (isolated, likely noise)
   - Contradiction detection: entries in same concept area that disagree on key facts
   - Format drift: entries missing required frontmatter (title, type, tags, sources)
3. Lint outputs a noise report: `data/audits/wiki/YYYY-WW.json` with fields:
   ```json
   {"duplicates": [...], "stale": [...], "orphans": [...], "contradictions": [...], "format_issues": [...], "noise_score": 0-10}
   ```
4. Review report. For each finding:
   - Duplicate: merge into canonical entry, delete redundant
   - Stale: update from current data, or archive if obsolete
   - Orphan: add `[[link]]` to related entry, or delete if genuinely useless
   - Contradiction: resolve based on most recent source, add `updated` frontmatter
   - Format issue: fix frontmatter
5. After cleanup, re-run lint to confirm noise_score improved.
6. Append cleanup summary to plan file under "Wiki Health Log":
   ```
   YYYY-MM-DD: noise_score N→M. Fixed N duplicates, N stale, N orphans.
   ```

## Phase 1 (before wiki-health-checker skill exists)
Use `llm-wiki-lint` directly in session. Manual review of findings. Same cleanup steps apply.

## Expected outputs
- `data/audits/wiki/YYYY-WW.json` (noise report)
- Cleaned wiki (duplicates merged, stale updated, orphans linked or deleted)
- Plan file append (cleanup summary)

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
