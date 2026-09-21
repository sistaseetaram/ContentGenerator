#!/usr/bin/env bash
# Rebuild the content dashboard whenever its inputs have changed.
#
# WHY A STOP HOOK, NOT PostToolUse
#   The dashboard is Seetaram's first surface: he reads the schedule there, not
#   in the JSON. It therefore has to be current without anyone remembering to
#   rebuild it. A PostToolUse hook would only catch Write/Edit calls and would
#   miss writes made through Bash or by a subagent -- which is how most of these
#   files actually get written. Comparing mtimes once per turn catches all of
#   them for the cost of four stat() calls.
#
# Deterministic: no model call, no network, no secrets. Tier 1 of the
# efficiency hierarchy. Exits 0 always -- a dashboard refresh must never be
# able to fail a turn.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$REPO/data/ideas-dashboard.html"
BUILDER="$REPO/.claude/skills/content-ideator/scripts/build_dashboard.py"

[ -f "$BUILDER" ] || exit 0

INPUTS=(
  "$REPO/data/ideas.json"
  "$REPO/data/posts.json"
  "$REPO/data/content-calendar.json"
  "$REPO/data/skills-status.json"
)

# Drafts land as new folders; a slot flipping planned -> drafted must show up.
newest_draft=0
if [ -d "$REPO/data/drafts" ]; then
  while IFS= read -r d; do
    m=$(stat -f %m "$d" 2>/dev/null || stat -c %Y "$d" 2>/dev/null || echo 0)
    [ "$m" -gt "$newest_draft" ] && newest_draft=$m
  done < <(find "$REPO/data/drafts" -maxdepth 1 -mindepth 1 -type d 2>/dev/null)
fi

out_m=0
[ -f "$OUT" ] && out_m=$(stat -f %m "$OUT" 2>/dev/null || stat -c %Y "$OUT" 2>/dev/null || echo 0)

stale=0
[ "$newest_draft" -gt "$out_m" ] && stale=1
for f in "${INPUTS[@]}"; do
  [ -f "$f" ] || continue
  m=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
  [ "$m" -gt "$out_m" ] && stale=1
done

[ "$stale" -eq 1 ] || exit 0

python3 "$BUILDER" >/dev/null 2>&1 \
  && echo "Content dashboard refreshed (inputs changed): data/ideas-dashboard.html"
exit 0
