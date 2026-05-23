# Workflow — Instagram Creative Feed

## ISOLATION RULES — READ FIRST

This feed is **completely separate** from the B2B content system.

- Audience: friends, family, personal circle — NOT Setu clients or LinkedIn network
- NO Setu mention in any post
- NO informative content — no AI tips, no automation, no industry takes
- NO cross-posting from LinkedIn, X, or YouTube
- NO Setu branding, logo, or agency positioning

Agents handling this feed must never inject Setu brand context. Load **zero** brand wiki files.

## Objective
Funny, sarcastic, and relatable posts for personal Instagram. Pure entertainment. Roasting tech culture, everyday observations, and whatever is actually funny right now. 2-3/week.

## Required inputs
- The bit: what's funny, what you're roasting, the observation
- Format: single image caption / reel concept / carousel / story
- Tone: sarcastic / dry / absurdist / roast — pick one per post

## Voice rules (THIS FEED ONLY — different from all other pillars)
- No banned words list here — this is a different voice entirely
- Be actually funny. If it's not funny, don't post it.
- Sarcasm must land, not confuse. Read it out loud. Does it work?
- Short captions win. One punchline. Don't over-explain the joke.
- Emojis OK if they add to the joke. Not for decoration.

## Sequence

1. Do NOT load any brand wiki files. Do NOT inject Setu context.
2. User provides the bit + tone + format.
3. Dispatch `content-ideator` sub-agent with: feed=instagram-creative, tone, format, bit. Explicitly instruct: no Setu mention, no brand voice.
4. Sub-agent returns 2-3 caption or concept variants.
5. User picks. No formal voice-checker — user's gut is the quality check here.
6. Post manually to Instagram (no API integration in Phase 1; Blotato handles scheduling).
7. Append minimal entry to `data/posts.json`:
   ```json
   {"id": "...", "pillar": "instagram-creative", "platform": "instagram",
    "hook": "...", "published_at": "...", "format": "caption|reel|carousel"}
   ```

## Edge cases
- Bit involves a real person → roast the archetype, not the individual. No names.
- Reel concept requires a screen recording → `.tmp/` intermediates, then upload. No credentials in frame.
- Accidentally funny LinkedIn post → do not cross-post. Rewrite as pure entertainment, no informative angle.

## Expected outputs
- 2-3 Instagram posts/week (no formal report required — metrics tracked manually or via Blotato)
- `data/posts.json` minimal entry per post

## Learnings log
*Append as discovered:*
- (none yet — Day 1)
