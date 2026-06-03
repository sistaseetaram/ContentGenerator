# Ingest parsing — pasted LinkedIn analytics → structured capture

The user opens their own post → "View analytics" → copies what they see → pastes into a Claude session. LinkedIn's layout varies (mobile vs desktop, creator vs basic). Parse defensively.

## What the paste usually contains

LinkedIn's post analytics surface (in rough order):
- **Impressions** / "X impressions"
- **Members reached** (sometimes "X members reached" or "unique views")
- **Reactions** total, often with a breakdown popover (Like, Celebrate, Support, Love, Insightful, Funny)
- **Comments** count
- **Reposts** count
- **Discovery / audience** section: "Top job titles", "Top industries", "Top locations", "Top companies", "Seniority" — each a short ranked list, sometimes with %
- **Followers vs non-followers** split (creator analytics) — "X% followers / Y% non-followers" or impressions-by-audience

## Parsing instruction (for the lint-dispatch model)

Extract into this exact JSON. Use `null` for anything genuinely absent — never invent. Percentages as 0–100 numbers; the rollup converts ICP to 0–1 where needed.

```json
{
  "reach": {"impressions": null, "members_reached": null, "follower_pct": null, "non_follower_pct": null},
  "engagement": {
    "reactions": null,
    "reaction_breakdown": {"like": null, "celebrate": null, "support": null, "love": null, "insightful": null, "funny": null},
    "comments": null, "reposts": null
  },
  "demographics": {
    "top_titles": [], "top_industries": [], "top_seniority": [], "top_companies": [], "top_locations": []
  }
}
```

Rules:
- `total` and `engagement_rate` are computed by the skill, not parsed — don't ask the model for them.
- Demographic lists: keep the label, attach the % if shown (`"Architect — 22%"`). Cap each list at the top 5.
- If only follower% is shown, set `non_follower_pct = 100 − follower_pct`.
- If the paste is clearly partial (e.g. only impressions + reactions, no demographics), parse what's there and set the rest null — a partial capture is still useful. Note in the skill output which fields were missing.

## Confidence check

After parsing, if `impressions` is null OR all of `comments/reposts/reactions` are null, the paste was too sparse. Present the structured fallback template and ask the user to fill it:

```
Couldn't read enough from that. Paste these (leave blank if not shown):

Impressions: __
Members reached: __
Reactions (total): __   (Like __ / Celebrate __ / Support __ / Love __ / Insightful __ / Funny __)
Comments: __
Reposts: __
Follower % of viewers: __
Top job titles: __
Top industries: __
Seniority: __
Top locations: __
```

## Demographics → ICP match (Phase I3, auditor model)

Given the parsed demographics, estimate `icp_match_pct` (0–1): the share of the audience that matches Setu's ICP. Load `target-audience.md` for the real definition; the gist:
- **On-ICP:** architecture / interior design / construction / civil firms; owner / principal / founder / director seniority; India locations; small firms (3–50).
- **Off-ICP:** software engineers, marketers, other AI/automation builders, students, large enterprises, non-India unless decision-maker.

Weigh industries and seniority most. Example: top industries "Architecture & Planning, Construction, Design" + seniority "Owner, Director" + location "India" → ~0.7–0.85. Top industries "Software, Marketing" + seniority "Entry, Senior IC" → ~0.1–0.2. Return a single number plus one sentence of reasoning (reasoning goes to the report, not the JSON).
