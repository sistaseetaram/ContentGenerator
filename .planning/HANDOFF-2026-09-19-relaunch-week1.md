# HANDOFF — 2026-09-19 · relaunch Week 1 scheduled, publishing unblocked

**Written to survive a context compact.** Stands alone. Read this first, then only what it points to.

**Immediate next task: build the $0 tracking scripts.** Everything else below is context.

---

## 1. The next task, specced

Four deterministic Python scripts (stdlib + free APIs, no MCP, no paid tool — tier 1 of the
efficiency hierarchy). Full spec lives in two places:

- Original research: `research_tracking-systems.txt` in this session's scratchpad
  (`/private/tmp/claude-501/-Users-sistaseetaram-.../scratchpad/`)
- Distilled bet: `content-wiki/wiki/syntheses/zero-cost-tracking-beats-paid-tools-now.md`

| Script | Job | Cadence |
|---|---|---|
| `tools/yt_tracker_channels.py` | Resolve watchlist handles → channel IDs + uploads playlist. Cache forever. | weekly / ad hoc |
| `tools/yt_tracker_snapshot.py` | Daily stats pull, compute outlier ratio vs channel trailing median | daily 08:00 IST |
| `tools/yt_tracker_rss_watch.py` | Per-channel RSS poll — zero quota, zero auth, catches uploads in minutes | every 4h |
| `tools/trend_watch.py` | Autocomplete + Google Trends RSS + HN + Reddit + arXiv | daily (arXiv weekly) |

Key verified facts: `channels.list`/`playlistItems.list`/`videos.list` cost **1 unit each**; budget is
10,000/day; a 20–40 channel watchlist costs ~45–300 units/day. Outlier = views-per-day ÷ channel
trailing median (same format bucket), flag at ≥2.0, exclude videos <3 days old. Reddit RSS **requires
a custom User-Agent** or it silently returns a block page. Data model goes under `data/tracking/`.

**Structurally impossible, do not promise it:** impressions, CTR, retention, demographics for channels
you don't own — no API at any price. Paid tools selling "competitor CTR" sell panel estimates.
**No historical backfill** — tracking only sees forward from the day polling starts.

---

## 2. Standing rules added this session (both already written into the files)

- **Explanations are never caveman.** Any "explain / what is this / why do we need it" request gets
  clean full English. (`~/.claude/CLAUDE.md`)
- **NEVER edit `~/.claude/CLAUDE.md` without asking first** — every time, even in auto mode, even for
  a one-line change. Ask once, then edit. (Not yet recorded anywhere; Seetaram must approve where it
  goes before it is written down.)
- **Fable routing is a SUGGESTION, not a recorded rule.** On any major UI/UX **or backend** build,
  point out that this may be a Fable job and *ask* whether to switch — do not stop unilaterally and do
  not encode it as a hard rule. A STRICT version was briefly written into `~/.claude/CLAUDE.md` on
  2026-09-19 and **has been removed**: it asserted what Fable is good at without any verification,
  which is precisely what the VERIFY-BEFORE-SUGGESTING rule forbids.
  **Open task: establish what Fable is actually strong at, from a real source, before suggesting it
  by name.** Until that exists, say "this might warrant a different model" rather than claiming Fable
  specifically is better at it.

---

## 3. What shipped this session

**Publishing unblocked.** Supergrow verified live (workspace + LinkedIn account authenticated, IDs in
`.env`). YouTube OAuth re-authed successfully — token fresh, channel confirmed (5 subs, 2 videos).
Fixed a real bug in `youtube_upload.py`: a dead refresh token crashed instead of falling back to
re-auth.

**Week 1 scheduled** → `data/content-calendar.json` (Mon 2026-09-21 → Fri 09-25, ISO W39, + YouTube
Tue 23). Month concept → `.planning/CONTENT-MONTH-2026-09.md` (Week 2 is a *swappable block* because
the timed build isn't shot yet).

**Three LinkedIn drafts written** by sub-agent → `data/drafts/2026-09-2{1,2,3}-*/linkedin-post.md`.
**Not yet reviewed by Seetaram. Do not publish until he has read them.**

**Blog pipeline built + tested** → `tools/blog_publish.py` (`new` / `validate` / `scaffold-config` /
`deploy`). Site is Astro 5 at `MyPersonalBrand/setu-brand/03-collateral/website/site`, domain
`setuagency.com`, deploy = `astro build && git push`. **The site has no blog page yet** — Seetaram is
having the personal-brand project build it. Hand that project the output of
`python3 tools/blog_publish.py scaffold-config`; it prints the exact `src/content.config.ts` and
`[...id].astro` that match what this pipeline emits.

Astro 5 traps verified against live docs: config is `src/content.config.ts` (NOT `src/content/config.ts`);
route is **`[...id].astro`** with `params:{id: post.id}` (NOT `[...slug]`); `render()` is imported from
`astro:content`, not `post.render()`.

**Router + registry:** `video-studio` wired to the 14 student-kit skills; registered as ONE registry row
(rationale in the registry note). Cherry-pick task CLOSED — both halves were already covered by our own
skills.

**Wiki:** 4 syntheses written (3 content, 1 design-automation), both indexes rebuilt, committed.

---

## 4. Corrections made — these had all propagated into content

Six factual defects caught, several *after* they'd reached drafts. Pattern worth remembering: every one
came from trusting an upstream doc instead of the primary source.

1. **"Bengaluru" → Nine Bricks is in Vijayawada and Hyderabad.** Was in the plan, propagated to the
   sub-agent brief, landed in Tuesday's *opening line* under the client's name. Fixed in drafts, plan,
   and `workflows/pillar-build-in-public.md`. The plan cited `company-profile.md` as its source — **that
   file does not exist.**
2. **The "good enough to show their own clients and vendors" quote is WITHDRAWN.** Seetaram confirmed the
   studio has not shown it to clients or vendors. It was in the video script's spoken opener, the beat
   sheet, and the description. Removed from all. The plan had called it "the single strongest credibility
   fact in this entire project" — losing it genuinely weakens Wednesday. What survives and IS documented:
   *accepted after eight rounds of changes, cleared to be shown publicly.*
3. **Pipeline was out of date** — direct whitebox→photoreal in one hop replaced the line-art chain; line
   art is now only a designer deliverable. The old version would have had Tuesday describing a step
   Monday blames for the failures.
4. **"two couches" → two consoles** (my error, filled in from a truncated index line).
5. **Eight refine passes were two parallel options** (A: v1–v3, B: drafts B–B4), not one chain. Do not
   narrate a straight-line progression.
6. **Higharc funding ≈$169M → $78M** per their own About page. Do not quote the higher figure.

---

## 5. Open / blocked

- **Commit is parked.** Nothing committed this session in ContentGenerator. Seetaram wants to read the
  three drafts first — reasonable, given two factual errors surfaced in them.
- **Phase 0.3 (linkedin-analyzer ingest) paused** at his request — he'll paste analytics when he has time.
  Until it runs, `metrics.json` stays empty and every week is planned blind.
- **Video #1 records this weekend (Sep 19–20).** Package at
  `data/drafts/2026-09-16-video-01-control-office/youtube.md` — naming now cleared, real failure image
  located (`FAILED-refine-texture-swallow.png`), title rank 3 promoted to A/B partner.
- **The accepted B4 image is not clearly named on disk.** Locate it before building any payoff slide.
- **No baseline data exists.** `analyzer-latest.json` is `n_posts=0`. Do not promise engagement lifts;
  realistic early expectation is ~5 engagements/post at ~2.17% at this follower tier.

## 6. Permissions on record (2026-09-19)

Nine Bricks Studio may be **named**. Project may be called a **government office**. The **floor plan may
be shown**. The render is cleared for public showing. Any *other* client stays anonymous by default.
Do NOT name the office's occupant or describe its emblem/portrait layout — not covered.
