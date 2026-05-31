# YouTube Edit Handoff → Video Studio

Downstream handoff from ContentGenerator (drafts) to the Video Editing Studio (renders + edits).

## Boundary

- **ContentGenerator owns:** script, hook, narrative structure, brand voice, thumbnail copy, title/description. See `workflows/platform-youtube.md` and the active content pillars.
- **Video Studio owns:** raw-footage-to-`final.mp4` — filler removal, cuts, color grade, captions, motion graphics, transitions. Lives at `/Users/sistaseetaram/Desktop/Claude/claude_projects/VideoEditorHyperframes`, driven by the global `video-studio` skill.

## Flow

1. ContentGenerator produces the YouTube script/brief (per `platform-youtube.md`).
2. Record footage (Loom, screen capture, talking head). Drop raw files into a footage folder.
3. Place a copy of the script/brief as `brief.md` in that footage folder so the studio reads narrative intent.
4. From the footage folder (or any session), say "edit this into a YouTube video" → `video-studio` skill fires.
5. Studio runs: transcribe → pre-scan → propose strategy → (confirm) → cut + grade + animate + caption → self-eval → `edit/final.mp4`.
6. Final video returns to ContentGenerator for publish (Blotato / platform upload) + metrics logging.

## Brand alignment

Studio must honor Setu brand direction. When grading/captioning, pull aesthetic from `setu-brand-context` skill if brand consistency is requested. Caption style + pacing should match the channel format defined in `platform-youtube.md`.

## Notes

- ElevenLabs key for transcription lives in the studio repo's `.env`, not here.
- All edit outputs stay in `<footage_dir>/edit/` — never written back into ContentGenerator or the studio repo.
