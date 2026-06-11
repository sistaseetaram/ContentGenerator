"""
Recording intake dispatcher for the video-editing pipeline.

The conversational trigger is: the user records something, drops it in one of the
sibling intake folders under the Claude parent dir, and says "I dropped a recording
in X". This tool turns that into a deterministic routing decision: it finds the
newest un-dispatched video in the named folder, probes it, and emits a dispatch
packet that tells video-studio which edit profile to run (intent x structure),
what master to target, and whether the source needs a CFR / resolution fix.

It does NOT edit. It selects + routes. State (which files were already handled)
lives in data/processed-recordings.json and is only committed after an edit run.

Pure stdlib + ffprobe. Runnable headless (no model calls, no network).

Usage:
    python tools/intake_dispatch.py folders
    python tools/intake_dispatch.py list [<folder_key>]
    python tools/intake_dispatch.py dispatch <folder_key> [--intent brand|neutral]
                                    [--type talking-head|screencast|auto]
                                    [--file PATH] [--force]
    python tools/intake_dispatch.py mark <file_path> [--dispatch-id ID]
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
REGISTRY_FILE = ROOT / "data" / "intake-folders.json"
MANIFEST_FILE = ROOT / "data" / "processed-recordings.json"
LATEST_FILE = ROOT / "data" / "intake-latest.json"
REPORTS_DIR = ROOT / "data" / "reports"

IST = "+05:30"
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}

# The record-once master. Everything else (1:1, 9:16, clips) is derived from this.
MASTER = {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "fps_mode": "cfr",
    "loudness_lufs": -16,
    "container": "mp4",
    "vcodec": "h264",
}

# Frame rates we treat as "clean" for a talking-head/screencast master.
CLEAN_FPS = {24, 25, 30, 50, 60}


def _load(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + IST


def _default_registry() -> dict:
    """Sibling intake folders under the Claude parent dir. User can rename freely."""
    parent = ROOT.parent.parent  # .../Desktop/Claude
    return {
        "parent": str(parent),
        "folders": {
            "loom": {
                "path": "LoomWalkthroughs",
                "default_recording_type": "talking-head",
                "default_intent": "brand",
                "platform_hint": ["linkedin", "youtube"],
            },
            "screenstudio": {
                "path": "ScreenStudioRecordings",
                "default_recording_type": "auto",
                "default_intent": "brand",
                "platform_hint": ["youtube", "linkedin"],
            },
            "yt-long": {
                "path": "YouTubeLongs",
                "default_recording_type": "auto",
                "default_intent": "neutral",
                "platform_hint": ["youtube"],
            },
            "yt-short": {
                "path": "YouTubeShorts",
                "default_recording_type": "auto",
                "default_intent": "neutral",
                "platform_hint": ["youtube-short"],
            },
        },
    }


def load_registry() -> dict:
    reg = _load(REGISTRY_FILE, None)
    if reg is None:
        reg = _default_registry()
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        REGISTRY_FILE.write_text(json.dumps(reg, indent=2))
    return reg


def _folder_path(reg: dict, key: str) -> Path:
    folders = reg.get("folders", {})
    if key not in folders:
        raise KeyError(
            f"Unknown intake folder '{key}'. Known: {list(folders)}. "
            f"Edit {REGISTRY_FILE.relative_to(ROOT)} to add one."
        )
    parent = Path(reg.get("parent", str(ROOT.parent.parent)))
    return parent / folders[key]["path"]


def _file_key(p: Path) -> dict:
    st = p.stat()
    return {"path": str(p), "size": st.st_size, "mtime": int(st.st_mtime)}


def _is_processed(manifest: dict, p: Path) -> bool:
    key = _file_key(p)
    for e in manifest.get("processed", []):
        if e.get("path") == key["path"] and e.get("size") == key["size"] \
                and e.get("mtime") == key["mtime"]:
            return True
    return False


def _videos_in(folder: Path):
    if not folder.exists():
        return []
    vids = [p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in VIDEO_EXTS]
    vids.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return vids


def probe(path: Path) -> dict:
    """ffprobe the file. Returns {} (with 'error') if ffprobe is unavailable."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,avg_frame_rate,codec_name",
        "-show_entries", "format=duration,bit_rate,size",
        "-of", "json", str(path),
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"error": f"ffprobe unavailable: {exc}"}
    if out.returncode != 0:
        return {"error": out.stderr.strip()}
    data = json.loads(out.stdout or "{}")
    stream = (data.get("streams") or [{}])[0]
    fmt = data.get("format", {})

    def _fps(rate: str):
        try:
            num, den = rate.split("/")
            den = float(den)
            return round(float(num) / den, 3) if den else None
        except (ValueError, ZeroDivisionError, AttributeError):
            return None

    r_fps = _fps(stream.get("r_frame_rate", ""))
    avg_fps = _fps(stream.get("avg_frame_rate", ""))
    width = stream.get("width")
    height = stream.get("height")
    return {
        "codec": stream.get("codec_name"),
        "width": width,
        "height": height,
        "r_frame_rate": stream.get("r_frame_rate"),
        "avg_frame_rate": stream.get("avg_frame_rate"),
        "r_fps": r_fps,
        "avg_fps": avg_fps,
        "duration_s": round(float(fmt["duration"]), 2) if fmt.get("duration") else None,
        "bit_rate": int(fmt["bit_rate"]) if fmt.get("bit_rate") else None,
        "size": int(fmt["size"]) if fmt.get("size") else None,
    }


def _source_flags(p: dict) -> dict:
    """Decide what the master pass must fix on this source."""
    flags = {"needs_cfr": False, "low_res": False, "low_bitrate": False, "notes": []}
    if p.get("error"):
        flags["notes"].append(p["error"])
        return flags
    r, a = p.get("r_fps"), p.get("avg_fps")
    # VFR / absurd timebase (e.g. 90000/1) or r/avg mismatch -> force CFR.
    if r is None or r > 121 or (r not in CLEAN_FPS and round(r) not in CLEAN_FPS):
        flags["needs_cfr"] = True
        flags["notes"].append(f"non-standard frame rate r={r}; normalize to {MASTER['fps']}fps CFR")
    if r and a and abs(r - a) > 1.0:
        flags["needs_cfr"] = True
        flags["notes"].append(f"r_fps {r} != avg_fps {a} (VFR); normalize to CFR")
    h = p.get("height") or 0
    if h and h < 1080:
        flags["low_res"] = True
        flags["notes"].append(
            f"source is {p.get('width')}x{h} (<1080p) — no edit fixes this; re-record HD for brand/ICP"
        )
    br = p.get("bit_rate")
    if br and br < 1_000_000:
        flags["low_bitrate"] = True
        flags["notes"].append(f"low bitrate {br}bps — re-render quality will be capped by source")
    return flags


def build_packet(reg, folder_key, video: Path, intent=None, rec_type=None) -> dict:
    folders = reg.get("folders", {})
    cfg = folders.get(folder_key, {})
    intent = intent or cfg.get("default_intent", "brand")
    rec_type = rec_type or cfg.get("default_recording_type", "auto")

    p = probe(video)
    flags = _source_flags(p)

    # structure may be 'auto' -> video-studio classifier decides; profile resolves then.
    if rec_type == "auto":
        profile = f"{intent}-<structure>"  # placeholder until classifier runs
        profile_note = "structure=auto: video-studio frame-classifier picks talking-head|screencast"
    else:
        profile = f"{intent}-{rec_type}"
        profile_note = "structure declared at intake"

    return {
        "dispatch_id": f"intake-{int(time.time())}",
        "dispatched_at": _now(),
        "source": {
            "path": str(video),
            "folder_key": folder_key,
            "platform_hint": cfg.get("platform_hint", []),
        },
        "intent": intent,
        "recording_type": rec_type,
        "suggested_profile": profile,
        "profile_note": profile_note,
        "probe": p,
        "source_flags": flags,
        "master_target": MASTER,
        "next_step": (
            "video-studio: transcribe (mlx-whisper local) -> classify structure -> "
            "select profile -> propose plain-English plan -> Slack checkpoint -> render"
        ),
    }


def _write_packet(packet: dict) -> Path:
    day = date.today().isoformat()
    out_dir = REPORTS_DIR / day
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / f"intake-dispatch-{int(time.time())}.json"
    report.write_text(json.dumps(packet, indent=2))
    LATEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    LATEST_FILE.write_text(json.dumps(packet, indent=2))
    return report


def mark_processed(file_path: str, dispatch_id: str = "") -> None:
    p = Path(file_path)
    manifest = _load(MANIFEST_FILE, {"processed": []})
    entry = _file_key(p)
    entry["dispatched_at"] = _now()
    entry["dispatch_id"] = dispatch_id
    manifest.setdefault("processed", []).append(entry)
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))


# ---- CLI ----------------------------------------------------------------

def cmd_folders(_args):
    reg = load_registry()
    print(f"Intake parent: {reg['parent']}")
    for key, cfg in reg.get("folders", {}).items():
        path = Path(reg["parent"]) / cfg["path"]
        exists = "ok" if path.exists() else "MISSING"
        print(f"  [{key:12}] {cfg['path']:24} {cfg['default_intent']}/"
              f"{cfg['default_recording_type']} ({exists})")


def cmd_list(args):
    reg = load_registry()
    manifest = _load(MANIFEST_FILE, {"processed": []})
    keys = [args.folder_key] if args.folder_key else list(reg.get("folders", {}))
    for key in keys:
        folder = _folder_path(reg, key)
        vids = _videos_in(folder)
        print(f"\n[{key}] {folder}")
        if not vids:
            print("  (no videos)")
            continue
        for v in vids:
            tag = "done" if _is_processed(manifest, v) else "NEW "
            print(f"  {tag}  {v.name}")


def cmd_dispatch(args):
    reg = load_registry()
    manifest = _load(MANIFEST_FILE, {"processed": []})

    if args.file:
        video = Path(args.file)
        if not video.exists():
            print(f"File not found: {video}", file=sys.stderr)
            sys.exit(1)
    else:
        folder = _folder_path(reg, args.folder_key)
        vids = _videos_in(folder)
        if not args.force:
            vids = [v for v in vids if not _is_processed(manifest, v)]
        if not vids:
            print(f"No new videos in [{args.folder_key}] {folder}. "
                  f"Use --force to re-dispatch the newest.", file=sys.stderr)
            sys.exit(2)
        video = vids[0]

    packet = build_packet(reg, args.folder_key, video,
                          intent=args.intent, rec_type=args.type)
    report = _write_packet(packet)

    print(f"Dispatched: {video.name}")
    print(f"  intent={packet['intent']}  type={packet['recording_type']}  "
          f"profile={packet['suggested_profile']}")
    pr = packet["probe"]
    if not pr.get("error"):
        print(f"  source: {pr.get('width')}x{pr.get('height')} "
              f"@ {pr.get('r_fps')}fps  {pr.get('duration_s')}s")
    for note in packet["source_flags"]["notes"]:
        print(f"  ! {note}")
    print(f"  packet -> {report.relative_to(ROOT)}")
    print(f"  latest -> {LATEST_FILE.relative_to(ROOT)}")
    print("  (not marked processed yet — call `mark` after the edit run completes)")


def cmd_mark(args):
    mark_processed(args.file_path, dispatch_id=args.dispatch_id or "")
    print(f"Marked processed: {args.file_path}")


def main():
    ap = argparse.ArgumentParser(description="Recording intake dispatcher")
    sub = ap.add_subparsers(dest="command", required=True)

    sub.add_parser("folders", help="show intake folder registry").set_defaults(func=cmd_folders)

    p_list = sub.add_parser("list", help="list videos + processed state")
    p_list.add_argument("folder_key", nargs="?", default=None)
    p_list.set_defaults(func=cmd_list)

    p_disp = sub.add_parser("dispatch", help="route the newest un-dispatched video")
    p_disp.add_argument("folder_key")
    p_disp.add_argument("--intent", choices=["brand", "neutral"], default=None)
    p_disp.add_argument("--type", choices=["talking-head", "screencast", "auto"], default=None)
    p_disp.add_argument("--file", default=None, help="dispatch a specific file instead of newest")
    p_disp.add_argument("--force", action="store_true", help="ignore processed manifest")
    p_disp.set_defaults(func=cmd_dispatch)

    p_mark = sub.add_parser("mark", help="mark a file processed (after edit completes)")
    p_mark.add_argument("file_path")
    p_mark.add_argument("--dispatch-id", default="")
    p_mark.set_defaults(func=cmd_mark)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
