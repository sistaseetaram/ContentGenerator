# Publishing SOP — YouTube + LinkedIn (learned 2026-06-11, post-009)

Proven once end-to-end. Platforms locked to **YouTube + LinkedIn** (user decision; X/IG off for now).
Rule still holds: **auto-draft → human review → publish.** Never auto-publish without explicit go.

## Credentials (read silently, never echo)

- **YouTube:** OAuth client + token live in `~/Documents/credentials/`:
  - client secrets: `~/Documents/credentials/YoutubeManagerCreds/client_secret_*.apps.googleusercontent.com.json`
  - token: `~/Documents/credentials/.youtube_token.json` (has refresh_token → no browser needed)
  - Point the uploader at them via env, don't move them:
    `YOUTUBE_CLIENT_SECRETS_PATH=…`, `YOUTUBE_TOKEN_PATH=…`
  - Auth channel verified = **"Sista Seetaram"** (UCi2XEq9BuhQQVr2Dp4YNpRQ).
- **LinkedIn:** no raw API creds. Publish via **Supergrow MCP** instead (account `kYTV-mUl7U`,
  workspace `e7632ac0-e9c6-43c3-8fef-974b4265e55b`).

## YouTube

- Upload: `tools/youtube_upload.py --file <16x9.mp4> --title … --description … --tags … --privacy unlisted`.
  Run via `uv run --with google-api-python-client --with google-auth-oauthlib --with google-auth-httplib2`.
  Mac has no `timeout` cmd — don't wrap with it.
- **Default privacy = `unlisted` first** (reviewable; equivalent to a draft). Flip to `public` after review.
  Unlisted videos are **invisible on the public channel page / Videos grid / search** — they only show in
  **Studio → Content**. (User confusion point: "I can't see it" = it's unlisted, not wrong channel.)
- Edit description / privacy after upload via `youtube.videos().update(part="snippet"|"status", …)` —
  fetch the current snippet/status first and preserve title/categoryId/tags.
- **Clickable description links require channel "Advanced Features" / identity verification**
  (Studio → Settings → Channel → Feature eligibility; ~4–6 hr after verifying). Until then ALL
  description links render as plain text — not fixable by us, it's channel-level. Links must be `https://`.
- Use the 16:9 master for YouTube.

## LinkedIn (via Supergrow MCP)

Flow: `list_workspaces` → `create_media`(video/mp4) → **multipart POST** the file to the presigned
`upload.url` with every `upload.fields` key + `file=@…` (S3 presigned-POST, NOT a PUT; returns 204) →
`confirm_media` → `create_post`(text, `media_ids`, `video_title`) → returns a **draft** + `app_url`.
- Use the **1:1 square** for LinkedIn (more feed height).
- **`update_post` with only `text` keeps media**, but pass `media_ids` + `video_title` anyway to be safe.
- **Native video > text.** Don't post text-only when a video exists.
- **Link strategy:** external link in the post body suppresses reach AND fights the video for a
  link-preview card. Put the CTA link in an **auto first-comment** (`create_auto_plug_comments`,
  delay 1 min) and keep the body link-free ("link in the comments"). Best reach + link one tap away.
- A stale link-preview may linger in the editor after removing the URL — harmless; LinkedIn renders
  the video on publish.

## Link shortening

- **Use `da.gd`** (`https://da.gd/s?url=<encoded>`) — clean direct redirect.
- **Avoid TinyURL** — it wraps the target in a **viglink affiliate redirect** (extra hop, off-brand).
- `is.gd`/`v.gd` rejected the Gemini URL ("database insert failed").
- Verify any short link's redirect target before using: `curl -s -o /dev/null -w "%{redirect_url}" <short>`.

## Copy drafting

- Drafts via a **content sub-agent** (orchestrator never drafts directly) using `tools/model_router.py`
  `route(task_type, prompt, system)` — `long_form` for post/description, `short_post` for title/tags.
  Output to `data/drafts/<date>-<slug>/`. Ground in `clean_script.txt` + wiki voice/values. Five-value gate.
- **YouTube title:** use the `youtube-packaging` skill (research-backed, no clickbait). Lead with the
  video's truest specific hook (a real number) over generic phrasing.

## Logging (hard rule)

Log every post to `data/posts.json` (next id, platform, status, url, asset masters, tags, five-values,
drafts_dir, gem_link). For a video on both platforms, one entry with a `linkedin` sub-object is fine.

## Known gaps (fix later)

- `model_router`: Gemini primary fails with `ModuleNotFoundError` (google-generativeai SDK not installed)
  and the router **re-raises instead of failing over**. Either install the SDK or treat ModuleNotFound as
  a failover trigger. For now it falls through to GPT-4o only after Gemini is dropped from the chain.
- No branded short domain (e.g. `setu.agency/gem`) — using da.gd. Set up a redirect when a domain exists.
