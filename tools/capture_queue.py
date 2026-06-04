"""
Capture-reminder queue builder for linkedin-analyzer.

Reads published LinkedIn posts and computes which need their Day-3 / Day-7
analytics captured. Diffs against already-captured days in metrics.json.
Writes data/capture-queue.json — the file the daily /schedule routine reads
to build its Slack reminder DM.

Pure stdlib. Runnable headless (no model calls, no network).

Usage:
    python tools/capture_queue.py
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
POSTS_FILE = ROOT / "data" / "posts.json"
METRICS_FILE = ROOT / "data" / "metrics.json"
QUEUE_FILE = ROOT / "data" / "capture-queue.json"

CAPTURE_DAYS = (3, 7)
IST = "+05:30"


def _load(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def _parse_date(s: str):
    """Accept 'YYYY-MM-DD' or ISO datetime; return a date or None."""
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        return None


def _captured_days(metrics: dict, post_id: str) -> set:
    for m in metrics.get("metrics", []):
        if m.get("post_id") == post_id:
            return {c.get("day") for c in m.get("captures", [])}
    return set()


def build_queue(today=None):
    today = today or date.today()
    posts = _load(POSTS_FILE, {"posts": []})
    metrics = _load(METRICS_FILE, {"metrics": []})

    due, upcoming = [], []

    for post in posts.get("posts", []):
        if post.get("platform") != "linkedin":
            continue
        if post.get("status") != "published":
            continue
        pub = _parse_date(post.get("published_at"))
        if pub is None:
            continue

        already = _captured_days(metrics, post["id"])
        for day in CAPTURE_DAYS:
            if day in already:
                continue
            due_date = pub + timedelta(days=day)
            item = {
                "post_id": post["id"],
                "day": day,
                "due_date": due_date.isoformat(),
                "hook": post.get("hook", ""),
            }
            if due_date <= today:
                item["status"] = "overdue" if (today - due_date).days > 1 else "due"
                due.append(item)
            else:
                upcoming.append(item)

    due.sort(key=lambda x: x["due_date"])
    upcoming.sort(key=lambda x: x["due_date"])

    return {
        "refreshed_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + IST,
        "due": due,
        "upcoming": upcoming,
    }


def main():
    queue = build_queue()
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))
    print(f"Capture queue refreshed → {QUEUE_FILE.relative_to(ROOT)}")
    print(f"  Due now:  {len(queue['due'])}")
    for item in queue["due"]:
        print(f"    [{item['status']}] {item['post_id']} Day {item['day']} "
              f"(due {item['due_date']})")
    print(f"  Upcoming: {len(queue['upcoming'])}")
    for item in queue["upcoming"]:
        print(f"    {item['post_id']} Day {item['day']} (due {item['due_date']})")


if __name__ == "__main__":
    main()
