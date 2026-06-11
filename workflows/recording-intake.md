# Workflow — Recording Intake (conversational trigger)

The entry point for the auto-edit pipeline. No always-on watcher. The user records
something, drops it in a sibling intake folder, and says a trigger phrase. The
orchestrator (Claude now; the executive agent later) turns that into a routed edit job.

## Trigger phrases

- "I dropped a recording in <folder>"
- "I recorded this, it's in <folder>"
- "edit my latest <loom|screen studio|youtube> recording"
- "I dropped a NEUTRAL screencast in ScreenStudioRecordings" (intent/type override inline)

## Intake folders (siblings under `/Users/sistaseetaram/Desktop/Claude/`)

Registry: `data/intake-folders.json` (auto-created; edit to rename / add folders).

| Key | Folder | Default intent | Default structure |
|---|---|---|---|
| `loom` | `LoomWalkthroughs/` | brand | talking-head |
| `screenstudio` | `ScreenStudioRecordings/` | brand | auto |
| `yt-long` | `YouTubeLongs/` | neutral | auto |
| `yt-short` | `YouTubeShorts/` | neutral | auto |

Defaults are a starting point. The user's drop message overrides intent (`brand`/`neutral`)
and structure (`talking-head`/`screencast`) per file. `auto` structure means the
video-studio frame-classifier decides.

## What the orchestrator does on trigger

1. Run the dispatcher to select + route the newest un-dispatched file:
   ```
   python tools/intake_dispatch.py dispatch <folder_key> [--intent ...] [--type ...]
   ```
   It probes the source, flags problems (sub-1080p, VFR/odd fps, low bitrate), resolves
   the edit profile (`<intent>-<structure>`), and writes a dispatch packet to
   `data/reports/<date>/intake-dispatch-*.json` + `data/intake-latest.json`.
2. **Honor the source flags before editing:**
   - `low_res` on a `brand` job → STOP. No edit fixes a 480p source for a premium/ICP video.
     Tell the user to re-record HD (Screen Studio @ 1080p) — do not silently ship it.
   - `needs_cfr` → the master pass must normalize to `MASTER.fps` CFR (fixes drift on cuts).
3. Hand the packet to `video-studio` (read `~/.claude/skills/video-studio/SKILL.md`):
   transcribe (mlx-whisper local) → classify structure → select profile → propose the
   plain-English cut+style plan → **Slack DM checkpoint** → on approve, render the master
   + derived formats unattended.
4. After a successful edit run, mark the source processed so it is not re-dispatched:
   ```
   python tools/intake_dispatch.py mark "<file path>" --dispatch-id <id>
   ```

## The record-once master

Everything is derived from one pristine master (`MASTER` in `tools/intake_dispatch.py`):
**1920×1080, 16:9, 30fps CFR, -16 LUFS, h264, high-bitrate.** Square (1:1), vertical
(9:16), short cuts, and clips are reframed/derived from this master on demand per
destination — never recorded separately.

## Edit profile = intent × structure

See the profile matrix in the plan and `video-use/profiles/`. Brand = restrained, on-brand,
no punch-in zooms, Setu overlays + end card. Neutral = reach-first, zooms allowed, punchy
captions, founder-tag outro, plus the visibility engine (competitor hook research).

## Useful commands

```
python tools/intake_dispatch.py folders          # show registry + which folders exist
python tools/intake_dispatch.py list [folder]     # list videos + NEW/done state
python tools/intake_dispatch.py dispatch loom --intent brand --type talking-head
python tools/intake_dispatch.py mark "<path>"     # commit processed state
```
