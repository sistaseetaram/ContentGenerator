"""
Analyzer rollup for linkedin-analyzer.

Joins per-post captures (metrics.json) with content attributes (posts.json)
and computes the derived steering signals that content-ideator consumes via
data/analyzer-latest.json.

Pure stdlib math — no model calls, no network. ICP-match is read from the
capture (set at ingest by the auditor model), never computed here. Outlier
hypotheses are added by the skill's analyze mode, not here.

Usage:
    python tools/analyzer_rollup.py
"""

import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
POSTS_FILE = ROOT / "data" / "posts.json"
METRICS_FILE = ROOT / "data" / "metrics.json"
OUT_FILE = ROOT / "data" / "analyzer-latest.json"

IST = "+05:30"
WINDOW = "last_30_days"

PILLAR_CANON = {"build-in-public-setu": "build-in-public"}


def _load(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def _latest_capture(captures: list) -> dict | None:
    """Prefer Day 7, else the highest day available."""
    if not captures:
        return None
    return sorted(captures, key=lambda c: c.get("day", 0))[-1]


def _canon_pillar(p: str) -> str:
    return PILLAR_CANON.get(p, p or "unknown")


def _format_of(post: dict) -> str:
    asset = post.get("asset") or {}
    t = (asset.get("type") or "").lower()
    if not t:
        return "text"
    if t in ("native_video", "video", "loom"):
        return "video"
    if t in ("infographic", "image", "quote_card"):
        return "image"
    if t == "carousel":
        return "carousel"
    return "text"


def _hook_type(hook: str) -> str:
    h = (hook or "").strip().lower()
    first = h.split("\n", 1)[0]
    if "?" in first:
        return "question"
    if any(t in first for t in ("stop ", "nobody ", "don't ", "everyone ", "unpopular")):
        return "contrarian"
    if any(ch.isdigit() for ch in first) or "$" in first or "%" in first:
        return "numeric-outcome"
    return "story-open"


def _dow(published_at: str) -> str | None:
    try:
        return date.fromisoformat(published_at[:10]).strftime("%A")
    except (ValueError, TypeError):
        return None


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else 0.0


def build_rollup() -> dict:
    posts = {p["id"]: p for p in _load(POSTS_FILE, {"posts": []}).get("posts", [])}
    metrics = _load(METRICS_FILE, {"metrics": []}).get("metrics", [])

    rows = []
    for m in metrics:
        post = posts.get(m.get("post_id"))
        if not post:
            continue
        cap = _latest_capture(m.get("captures", []))
        if not cap:
            continue

        eng = cap.get("engagement", {})
        reach = cap.get("reach", {})
        impressions = reach.get("impressions") or 0
        reactions = eng.get("reactions") or 0
        comments = eng.get("comments") or 0
        reposts = eng.get("reposts") or 0
        total = eng.get("total")
        if total is None:
            total = reactions + comments + reposts

        er = (total / impressions) if impressions else 0.0
        icp = cap.get("icp_match_pct")
        icp_w_er = er * (0.5 + icp) if icp is not None else er
        weighted_engage = reactions * 1 + comments * 3 + reposts * 5

        rows.append({
            "post_id": m["post_id"],
            "pillar": _canon_pillar(post.get("pillar")),
            "format": _format_of(post),
            "hook_type": _hook_type(post.get("hook", "")),
            "dow": _dow(post.get("published_at")),
            "er": round(er, 4),
            "icp_w_er": round(icp_w_er, 4),
            "weighted_engage": weighted_engage,
            "icp_known": icp is not None,
        })

    n_posts = len(rows)
    confidence = "low" if n_posts < 8 else ("med" if n_posts <= 15 else "high")

    # pillar_weights — mean icp_w_er per pillar, normalized so mean = 1.0
    pillar_weights = {}
    if rows:
        by_pillar = {}
        for r in rows:
            by_pillar.setdefault(r["pillar"], []).append(r["icp_w_er"])
        raw = {p: _mean(v) for p, v in by_pillar.items()}
        overall = _mean(list(raw.values()))
        if overall > 0:
            pillar_weights = {p: round(v / overall, 2) for p, v in raw.items()}
        else:
            pillar_weights = {p: 1.0 for p in raw}

    # hook_signals
    hook_signals = []
    by_hook = {}
    for r in rows:
        by_hook.setdefault(r["hook_type"], []).append(r)
    for htype, hrows in by_hook.items():
        hook_signals.append({
            "pattern": htype,
            "n": len(hrows),
            "avg_er": round(_mean([r["er"] for r in hrows]), 4),
            "avg_icp_weighted_er": round(_mean([r["icp_w_er"] for r in hrows]), 4),
        })
    hook_signals.sort(key=lambda x: x["avg_icp_weighted_er"], reverse=True)

    # format_signals
    format_signals = []
    by_fmt = {}
    for r in rows:
        by_fmt.setdefault(r["format"], []).append(r)
    for fmt, frows in by_fmt.items():
        format_signals.append({
            "format": fmt,
            "n": len(frows),
            "avg_er": round(_mean([r["er"] for r in frows]), 4),
        })
    format_signals.sort(key=lambda x: x["avg_er"], reverse=True)

    # leaders / underperformers by icp_weighted_er
    ranked = sorted(rows, key=lambda r: r["icp_w_er"], reverse=True)
    icp_reach_leaders = [r["post_id"] for r in ranked[:3]]
    underperformers = (
        [r["post_id"] for r in ranked[-2:]] if n_posts >= 4 else []
    )

    # best day-of-week by mean ER
    best_dow_time = None
    by_dow = {}
    for r in rows:
        if r["dow"]:
            by_dow.setdefault(r["dow"], []).append(r["er"])
    if by_dow:
        best_day = max(by_dow.items(), key=lambda kv: _mean(kv[1]))[0]
        best_dow_time = best_day  # time-of-day omitted: published_at is date-only

    notes = f"n={n_posts} posts captured."
    if confidence == "low":
        notes += " Directional only; weights not yet trustworthy."

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + IST,
        "window": WINDOW,
        "n_posts": n_posts,
        "confidence": confidence,
        "pillar_weights": pillar_weights,
        "hook_signals": hook_signals,
        "format_signals": format_signals,
        "best_dow_time": best_dow_time,
        "icp_reach_leaders": icp_reach_leaders,
        "underperformers": underperformers,
        "notes": notes,
    }


def main():
    rollup = build_rollup()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(rollup, indent=2))
    print(f"Analyzer rollup written → {OUT_FILE.relative_to(ROOT)}")
    print(f"  n_posts={rollup['n_posts']} confidence={rollup['confidence']}")
    print(f"  pillar_weights={rollup['pillar_weights']}")
    print(f"  leaders={rollup['icp_reach_leaders']}")
    print(f"  notes: {rollup['notes']}")


if __name__ == "__main__":
    main()
