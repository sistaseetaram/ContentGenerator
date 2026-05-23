# Workflow — Platform: LinkedIn

## Role in system
Primary B2B platform. All pillars except Instagram-creative publish here. The anchor channel — every other platform either feeds into or repurposes from LinkedIn.

## Cadence
- Target: 3-5 posts/week
- Minimum: 3 posts/week (no excuses below this)
- Maximum: 1 post/day (more = algorithmic penalty + audience fatigue)
- Optimal time: 8-10am IST weekdays (adjust based on Week 2+ metrics)

## Format rules

### Post structure
```
[Hook — line 1, standalone sentence, makes reader stop]

[Body — 3-7 short paragraphs, each 1-3 sentences max]

[CTA — one clear ask: comment, DM, share, or none]

[Hashtags — max 3, end of post, relevant not decorative]
```

### Length
- Sweet spot: 150-300 words
- Short-form allowed: 50-100 words if the hook + insight is complete
- Long-form: up to 700 words for Build Receipts with deep how-to. No padding.

### Hook rules
- Line 1 = the hook. Must work standalone.
- Types: outcome-first ("I cut 8 hours to 2 minutes."), vulnerable ("I shipped the wrong thing for 3 weeks."), question (sparingly — no "Are you doing X?"), story-opener ("Last Tuesday, a client called.")
- Banned hook starters: "Excited to share", "Happy to announce", "Thrilled to", "I'm proud to"

### Formatting
- Short paragraphs. White space is not wasted.
- Line breaks every 2-3 sentences max.
- Bold sparingly — one key phrase per post if needed, never entire sentences.
- No bullet-point-heavy posts unless it's a how-to with genuinely parallel steps.

### Hashtags
- Max 3. End of post.
- Use: #n8n #AIautomation #IndiaStartups (adjust based on pillar)
- Never use: #entrepreneur #hustle #motivational or generic catch-all tags

## LinkedIn algorithm notes
- First 90 minutes after posting are critical. Engage with comments immediately.
- Posts with high early engagement (likes + comments in first hour) get pushed wider.
- Avoid external links in post body — kills reach. Put links in first comment.
- Native video and carousels get broader reach than text-only. Use when worth it.

## Publishing (Phase 1)
Via Blotato. Connect LinkedIn account. Schedule posts in Blotato calendar. After publishing, confirm post live in LinkedIn app, then log to `data/posts.json`.

## Publishing (Phase 3+)
Via `tools/linkedin_post.py` (direct LinkedIn API). Blotato runs parallel for 2 weeks during transition to validate parity.

## Voice check before every post
Run copy test: "Would a smart, busy architecture firm owner feel respected — or sold to?"
If sold to → rewrite.

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
