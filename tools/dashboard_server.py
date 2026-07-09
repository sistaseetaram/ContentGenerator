#!/usr/bin/env python3
"""
Setu Content Dashboard — live local web app.

Unlike build_dashboard.py (a static snapshot), this serves an interactive page that
can READ and WRITE the data files. It exists so the user can:
  - see what's due this week (so nothing slips again),
  - browse the scored idea feed and the schedule,
  - ADD their own ideas, which are auto-scored on submit via tools/idea_scorer.py
    (rubric + strategic critique through the model_router), and
  - when a new idea outscores something already on the calendar, get a swap proposal
    they approve with one click (nothing moves without approval).

Pure stdlib HTTP server. The only network/model use is on idea submit (one cheap
lint-dispatch call). Single-user, localhost only.

Run:
    python tools/dashboard_server.py            # serves http://localhost:8765 + opens browser
    python tools/dashboard_server.py --port 9000 --no-open
"""

import argparse
import json
import sys
import threading
import webbrowser
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

DATA = ROOT / "data"
IDEAS_FILE = DATA / "ideas.json"
POSTS_FILE = DATA / "posts.json"
CAL_FILE = DATA / "content-calendar.json"

PILLARS = ["build-receipts", "plain-english-ai-takes", "build-in-public-setu", "contrarian"]
PLATFORMS = ["linkedin", "youtube", "x", "instagram"]

_LOCK = threading.Lock()  # serialize read-modify-write on the JSON files


# ---- data helpers -------------------------------------------------------

def _load(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def _save(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2))


def _ideas():
    return _load(IDEAS_FILE, {"ideas": []}).get("ideas", [])


def _ideas_by_id():
    return {i["id"]: i for i in _ideas() if i.get("id")}


def _next_idea_id():
    nums = [int(i["id"].split("-")[1]) for i in _ideas()
            if i.get("id", "").startswith("idea-") and i["id"].split("-")[1].isdigit()]
    return f"idea-{(max(nums) + 1) if nums else 1:03d}"


def _flatten_calendar():
    data = _load(CAL_FILE, {"weeks": []})
    rows = []
    for wk in data.get("weeks", []):
        for d in wk.get("days", []):
            rows.append({**d, "week": wk.get("week"), "theme": wk.get("theme", "")})
    return sorted(rows, key=lambda r: (r.get("date") or "", -(r.get("week") or 0)))


def _published_posts():
    posts = [p for p in _load(POSTS_FILE, {"posts": []}).get("posts", [])
             if p.get("status") == "published"]
    return sorted(posts, key=lambda p: p.get("published_at") or "", reverse=True)


def _today():
    return date.today().isoformat()


def _due(calendar, today):
    """Publish slots that are today or overdue and not yet done/retired."""
    out = []
    for r in calendar:
        if r.get("action") != "publish":
            continue
        if not r.get("date"):
            continue
        st = (r.get("status") or "").lower()
        if st in ("done", "published", "retired"):
            continue
        if r["date"] <= today:
            out.append({**r, "overdue": r["date"] < today})
    return sorted(out, key=lambda r: r.get("date") or "")


def _swap_suggestions(new_idea, ideas_by_id, calendar, today):
    """Future publish slots the new idea could outscore. Approval-gated; nothing moves here."""
    new_score = new_idea.get("total_score", 0)
    new_platform = new_idea.get("platform", "linkedin")
    sugg = []
    for r in calendar:
        if r.get("action") != "publish" or not r.get("idea_id"):
            continue
        if not r.get("date") or r["date"] < today:
            continue
        if (r.get("status") or "").lower() in ("done", "published", "retired"):
            continue
        # only propose swaps within the same platform — a slot is platform-specific
        if r.get("platform") and new_platform and r["platform"] != new_platform:
            continue
        scheduled = ideas_by_id.get(r["idea_id"], {})
        sched_score = scheduled.get("total_score", 0)
        if new_score > sched_score:
            sugg.append({
                "date": r["date"],
                "week": r.get("week"),
                "platform": r.get("platform"),
                "scheduled_idea_id": r["idea_id"],
                "scheduled_title": r.get("title") or scheduled.get("title", ""),
                "scheduled_score": sched_score,
                "new_score": new_score,
                "delta": round(new_score - sched_score, 2),
            })
    return sorted(sugg, key=lambda s: s["delta"], reverse=True)


def _state():
    ideas = sorted(_ideas(), key=lambda i: i.get("total_score", 0), reverse=True)
    calendar = _flatten_calendar()
    today = _today()
    backlog = [i for i in ideas if i.get("status") == "backlog"]
    return {
        "today": today,
        "ideas": ideas,
        "posts": _published_posts(),
        "calendar": calendar,
        "due": _due(calendar, today),
        "pillars": PILLARS,
        "platforms": PLATFORMS,
        "stats": {
            "ideas_total": len(ideas),
            "backlog": len(backlog),
            "post_now": len([i for i in backlog
                             if (i.get("strategic_opinion") or {}).get("verdict") == "post_now"]),
            "published": len(_published_posts()),
        },
    }


# ---- write actions ------------------------------------------------------

def add_idea(payload):
    """Score a submitted idea, append it to ideas.json, return record + swap suggestions."""
    from tools.idea_scorer import score_idea  # lazy: only import (and load SDKs) on submit

    title = (payload.get("title") or "").strip()
    if not title:
        raise ValueError("title is required")
    proof = (payload.get("proof_plan") or "").strip()
    if not proof:
        raise ValueError("proof_plan is required — an idea with no proof is a topic, not a Setu idea")

    idea_input = {
        "title": title,
        "angle": (payload.get("angle") or "").strip(),
        "pillar": payload.get("pillar") or "",
        "platform": payload.get("platform") or "linkedin",
        "proof_plan": proof,
    }
    scored = score_idea(idea_input)

    with _LOCK:
        data = _load(IDEAS_FILE, {"ideas": []})
        record = {
            "id": _next_idea_id_locked(data),
            "created_at": _today(),
            "title": idea_input["title"],
            "angle": idea_input["angle"],
            "pillar": idea_input["pillar"],
            "platform": idea_input["platform"],
            "source": payload.get("source", "user"),
            "scores": scored["scores"],
            "total_score": scored["total_score"],
            "proof_plan": idea_input["proof_plan"],
            "supporting_research": [],
            "status": "backlog",
            "strategic_opinion": scored["strategic_opinion"],
            "voice_flags": scored["voice_flags"],
            "scored_by": scored["model_used"],
        }
        data.setdefault("ideas", []).append(record)
        _save(IDEAS_FILE, data)

    swaps = _swap_suggestions(record, _ideas_by_id(), _flatten_calendar(), _today())
    return {"idea": record, "swaps": swaps, "cost_usd": scored["cost_usd"]}


def _next_idea_id_locked(data):
    nums = [int(i["id"].split("-")[1]) for i in data.get("ideas", [])
            if i.get("id", "").startswith("idea-") and i["id"].split("-")[1].isdigit()]
    return f"idea-{(max(nums) + 1) if nums else 1:03d}"


def apply_swap(payload):
    """Replace the idea in a calendar slot (by date) with new_idea_id. Approval already given."""
    target_date = payload.get("date")
    new_id = payload.get("new_idea_id")
    if not target_date or not new_id:
        raise ValueError("date and new_idea_id are required")
    ideas_by_id = _ideas_by_id()
    new_idea = ideas_by_id.get(new_id)
    if not new_idea:
        raise ValueError(f"unknown idea {new_id}")

    with _LOCK:
        data = _load(CAL_FILE, {"weeks": []})
        for wk in data.get("weeks", []):
            for d in wk.get("days", []):
                if d.get("date") == target_date and d.get("action") == "publish":
                    displaced = d.get("idea_id")
                    d["idea_id"] = new_id
                    d["title"] = new_idea.get("title", "")
                    d["pillar"] = new_idea.get("pillar", d.get("pillar"))
                    d["platform"] = new_idea.get("platform", d.get("platform"))
                    note = (f"SWAPPED IN via dashboard {_today()}: {new_id} "
                            f"({new_idea.get('total_score')}) replaced {displaced}.")
                    d["notes"] = note + (" || " + d["notes"] if d.get("notes") else "")
                    _save(CAL_FILE, data)
                    # bump displaced idea back to backlog so it can be rescheduled
                    if displaced:
                        idata = _load(IDEAS_FILE, {"ideas": []})
                        for i in idata.get("ideas", []):
                            if i.get("id") == displaced and i.get("status") not in ("posted",):
                                i["status"] = "backlog"
                        _save(IDEAS_FILE, idata)
                    return {"ok": True, "date": target_date, "new_idea_id": new_id,
                            "displaced": displaced}
    raise ValueError(f"no publish slot found on {target_date}")


# ---- HTTP ---------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            return self._html(PAGE)
        if self.path == "/api/state":
            return self._json(_state())
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            return self._json({"error": "bad json"}, 400)
        try:
            if self.path == "/api/idea":
                return self._json(add_idea(payload))
            if self.path == "/api/swap":
                return self._json(apply_swap(payload))
        except ValueError as e:
            return self._json({"error": str(e)}, 400)
        except Exception as e:  # model failure, etc.
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)
        self._json({"error": "not found"}, 404)


# ---- frontend (single page; fetches /api/state) -------------------------

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Setu — Content Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#f4efe9; --panel:#fbf8f4; --ink:#1f1b18; --muted:#8a7f74; --line:#e7ddd0;
    --terra:#b9543a; --terra-soft:#f0ddd4; --forest:#2f6f6a; --gold:#b5852a; --plum:#7a5c9e;
    --green:#2a7a4a; --red:#9e3030; --shadow:0 1px 3px rgba(40,28,20,.06),0 6px 24px rgba(40,28,20,.05);
  }
  *{box-sizing:border-box}
  body{margin:0;font:15px/1.55 Inter,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--ink)}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px}
  header{padding:26px 0 8px}
  .brand{display:flex;align-items:baseline;gap:12px}
  .brand h1{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:30px;margin:0;letter-spacing:-.01em}
  .brand .dev{font-family:'Cormorant Garamond',serif;font-size:30px;color:var(--terra);font-weight:500}
  .brand .sub{color:var(--muted);font-size:13px;margin-left:auto}
  .tabs{display:flex;gap:2px;margin-top:18px;border-bottom:1px solid var(--line);flex-wrap:wrap}
  .tab{padding:10px 18px;font-size:14px;font-weight:600;color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;border-radius:8px 8px 0 0}
  .tab:hover{color:var(--ink);background:var(--panel)}
  .tab.active{color:var(--ink);border-bottom-color:var(--terra)}
  .tab .pip{display:inline-block;min-width:18px;text-align:center;background:var(--terra);color:#fff;font-size:11px;font-weight:700;border-radius:999px;padding:0 5px;margin-left:6px}
  .pane{display:none;padding:22px 0 60px}
  .pane.active{display:block}
  .stats{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}
  .stat{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 18px;box-shadow:var(--shadow);min-width:120px}
  .stat .n{font-size:26px;font-weight:700;font-variant-numeric:tabular-nums;line-height:1}
  .stat .l{font-size:12px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.04em}
  .sech{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:600;margin:8px 0 14px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-bottom:12px;box-shadow:var(--shadow)}
  .card.due{border-left:4px solid var(--gold)}
  .card.overdue{border-left:4px solid var(--red)}
  .row{display:flex;gap:14px;align-items:flex-start;justify-content:space-between}
  .title{font-weight:600;font-size:15.5px}
  .angle{color:var(--muted);font-size:13.5px;margin-top:4px}
  .proof{color:var(--terra);font-size:12.5px;margin-top:6px}
  .meta{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;align-items:center}
  .badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:600;color:#fff;white-space:nowrap}
  .badge.ghost{background:transparent;color:var(--muted);border:1px solid var(--line)}
  .score-pill{font-size:22px;font-weight:800;font-variant-numeric:tabular-nums;white-space:nowrap;text-align:right}
  .score-pill small{font-size:11px;color:var(--muted);font-weight:600;display:block}
  .verdict-reason{font-size:12.5px;color:var(--muted);font-style:italic;margin-top:6px}
  .bars{margin-top:10px;display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:6px 14px}
  .bar{display:flex;align-items:center;gap:7px;font-size:11px;color:var(--muted)}
  .bar .t{flex:1;height:7px;background:var(--line);border-radius:5px;overflow:hidden}
  .bar .f{height:100%;border-radius:5px}
  .controls{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
  select,input,textarea{font:inherit;padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink)}
  textarea{width:100%;resize:vertical;min-height:70px}
  label{display:block;font-size:13px;font-weight:600;margin:14px 0 5px}
  .hint{font-weight:400;color:var(--muted);font-size:12px}
  .form{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px 24px;max-width:640px;box-shadow:var(--shadow)}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  button{font:inherit;font-weight:600;cursor:pointer;border:none;border-radius:10px;padding:11px 20px;background:var(--terra);color:#fff}
  button:hover{filter:brightness(1.05)} button:disabled{opacity:.5;cursor:wait}
  button.sec{background:transparent;color:var(--ink);border:1px solid var(--line)}
  .result{margin-top:18px;max-width:640px}
  .swap{background:#fff8f0;border:1px solid var(--gold);border-radius:12px;padding:14px 16px;margin-top:10px}
  .swap .h{font-weight:700;color:var(--gold);font-size:13px;margin-bottom:8px}
  .swap .opt{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:8px 0;border-top:1px solid var(--line)}
  .empty{color:var(--muted);padding:30px 0;text-align:center}
  table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}
  th,td{text-align:left;padding:11px 13px;border-bottom:1px solid var(--line);vertical-align:top;font-size:13.5px}
  th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
  tr:last-child td{border-bottom:none}
  tr.prep td{background:#faf6ee}
  a{color:var(--terra);text-decoration:none} a:hover{text-decoration:underline}
  .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--ink);color:#fff;padding:12px 20px;border-radius:10px;font-size:14px;box-shadow:var(--shadow);opacity:0;transition:opacity .2s;z-index:9}
  .toast.show{opacity:1}
</style></head>
<body>
<div class="wrap">
<header>
  <div class="brand"><h1>सेतु</h1><span class="dev">Content Studio</span>
    <span class="sub" id="today"></span></div>
  <div class="tabs">
    <div class="tab active" data-pane="home">This Week <span class="pip" id="pip-due" style="display:none"></span></div>
    <div class="tab" data-pane="feed">Idea Feed</div>
    <div class="tab" data-pane="add">+ Add Idea</div>
    <div class="tab" data-pane="calendar">Calendar</div>
    <div class="tab" data-pane="published">Published</div>
  </div>
</header>

<div class="pane active" id="pane-home"></div>

<div class="pane" id="pane-feed">
  <div class="controls">
    <select id="ff-pillar"><option value="">all pillars</option></select>
    <select id="ff-verdict"><option value="">all verdicts</option><option value="post_now">post now</option><option value="post_later">post later</option><option value="drop">drop</option></select>
    <select id="ff-source"><option value="">all sources</option></select>
    <input id="ff-q" placeholder="search title / angle…" size="22">
  </div>
  <div id="feed-mount"></div>
</div>

<div class="pane" id="pane-add">
  <div class="form">
    <div class="sech" style="margin-top:0">Drop your own idea</div>
    <div class="hint" style="margin-bottom:6px">You write the seed; the studio scores it against the Setu rubric (7 checks) and gives an honest post-now / later / drop verdict. If it beats something already on the calendar, you'll get a swap to approve.</div>
    <label>Title <span class="hint">— the hook, in your words</span></label>
    <input id="in-title" style="width:100%" placeholder="e.g. The one WhatsApp message that broke my BOQ parser">
    <label>Angle <span class="hint">— what's the specific take? (not a topic)</span></label>
    <textarea id="in-angle" placeholder="What actually happened, the turn, why it matters to a firm owner."></textarea>
    <div class="grid2">
      <div><label>Pillar</label><select id="in-pillar" style="width:100%"></select></div>
      <div><label>Platform</label><select id="in-platform" style="width:100%"></select></div>
    </div>
    <label>Proof plan <span class="hint">— the receipt you'd show (required)</span></label>
    <input id="in-proof" style="width:100%" placeholder="e.g. screen-rec of the failing run + the fix">
    <div style="margin-top:18px"><button id="btn-score" onclick="submitIdea()">Score this idea</button></div>
  </div>
  <div class="result" id="add-result"></div>
</div>

<div class="pane" id="pane-calendar">
  <div class="controls">
    <select id="cf-week"><option value="">all weeks</option></select>
    <select id="cf-pillar"><option value="">all pillars</option></select>
  </div>
  <div id="cal-mount"></div>
</div>

<div class="pane" id="pane-published">
  <div class="controls"><input id="pf-q" placeholder="search topic…" size="22"></div>
  <div id="pub-mount"></div>
</div>
</div>
<div class="toast" id="toast"></div>

<script>
const PILLAR_COLORS={"build-receipts":"#b9543a","plain-english-ai-takes":"#2f6f6a","plain-english-ai":"#2f6f6a","build-in-public-setu":"#7a5c9e","build-in-public":"#7a5c9e","contrarian":"#b5852a","instagram-creative":"#9e5c7a"};
const VERDICT_COLORS={post_now:"#2a7a4a",post_later:"#b5852a",drop:"#9e3030"};
const SOURCE_COLORS={agent:"#2f6f6a",user:"#b9543a",sister:"#9e5c7a"};
const DIMS=[["pillar_fit","Pillar",1.0],["value_fit","Values",1.0],["new_info","New-info",1.5],["lived_exp","Lived",1.5],["proof_level","Proof",1.5],["timeliness","Timely",1.0],["effort","Effort",.75]];
let S={};
function esc(s){return (s==null?"":""+s).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function el(id){return document.getElementById(id);}
function badge(txt,col,ghost){return `<span class="badge${ghost?' ghost':''}" style="${ghost?'':'background:'+col}">${esc(txt)}</span>`;}
function pill(col){return PILLAR_COLORS[col]||"#888";}
function toast(m){const t=el("toast");t.textContent=m;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2600);}

async function load(){ S=await (await fetch("/api/state")).json(); draw(); }

function bars(scores){ if(!scores)return"";
  return '<div class="bars">'+DIMS.map(([k,l,w])=>{const v=scores[k]||0;const col=w===1.5?"#b9543a":"#9bb0ae";
    return `<div class="bar"><span style="min-width:48px">${l}</span><span class="t"><span class="f" style="width:${v/5*100}%;background:${col}"></span></span><b style="color:#1f1b18">${v}</b></div>`;}).join("")+'</div>';}

function ideaCard(i,opts){opts=opts||{};
  const op=i.strategic_opinion||{};const vc=VERDICT_COLORS[op.verdict]||"#888";
  const sc=(i.total_score||0).toFixed(1);
  return `<div class="card ${opts.cls||''}"><div class="row">
    <div style="flex:1"><div class="title">${esc(i.title)}</div>
      <div class="angle">${esc(i.angle||"")}</div>
      ${i.proof_plan?`<div class="proof">▸ ${esc(i.proof_plan)}</div>`:""}
      <div class="meta">${badge(i.pillar,pill(i.pillar))}
        ${i.platform?badge(i.platform,"#444",true):""}
        ${i.source?badge(i.source,SOURCE_COLORS[i.source]||"#888"):""}
        ${op.verdict?badge(op.verdict.replace(/_/g," "),vc):""}
        ${i.status?badge(i.status,"#777",true):""}
        ${opts.dateTag?badge(opts.dateTag,"#444",true):""}</div>
      ${op.reason?`<div class="verdict-reason">"${esc(op.reason)}"${op.when_to_post&&op.when_to_post!=="now"?` → <b>${esc(op.when_to_post)}</b>`:""}</div>`:""}
      ${i.scores?bars(i.scores):""}</div>
    <div class="score-pill">${sc}<small>/41.25</small></div></div></div>`;}

// ---- Home / This week ----
function drawHome(){
  const m=el("pane-home");const st=S.stats||{};const due=S.due||[];
  el("today").textContent=new Date(S.today+"T00:00").toDateString();
  const pip=el("pip-due"); if(due.length){pip.style.display="inline-block";pip.textContent=due.length;}else pip.style.display="none";
  let h=`<div class="stats">
    <div class="stat"><div class="n">${due.length}</div><div class="l">due / overdue</div></div>
    <div class="stat"><div class="n">${st.post_now||0}</div><div class="l">post-now backlog</div></div>
    <div class="stat"><div class="n">${st.backlog||0}</div><div class="l">total backlog</div></div>
    <div class="stat"><div class="n">${st.published||0}</div><div class="l">published</div></div></div>`;
  h+=`<div class="sech">Due this week</div>`;
  if(!due.length){h+=`<div class="empty">Nothing overdue. 🎉 Add an idea or check the calendar.</div>`;}
  else{const byId={};(S.ideas||[]).forEach(i=>byId[i.id]=i);
    due.forEach(d=>{const idea=byId[d.idea_id]||{title:d.title,angle:"",pillar:d.pillar,platform:d.platform,proof_plan:""};
      h+=ideaCard({...idea,title:d.title||idea.title,status:d.status},{cls:d.overdue?"overdue":"due",dateTag:(d.overdue?"OVERDUE ":"")+d.date});});}
  m.innerHTML=h;
}

// ---- Feed ----
function fillSel(id,vals,pre){const s=el(id);[...new Set(vals)].filter(Boolean).sort().forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=(pre||"")+v;s.appendChild(o);});}
function drawFeedFilters(){const ids=(S.ideas||[]);
  if(el("ff-pillar").children.length<=1){fillSel("ff-pillar",ids.map(i=>i.pillar));fillSel("ff-source",ids.map(i=>i.source));
    fillSel("in-pillar",S.pillars);fillSel("in-platform",S.platforms);}
  if(el("cf-week").children.length<=1){fillSel("cf-week",(S.calendar||[]).map(r=>r.week),"week ");fillSel("cf-pillar",(S.calendar||[]).map(r=>r.pillar));}
}
function drawFeed(){
  const fp=el("ff-pillar").value,fv=el("ff-verdict").value,fs=el("ff-source").value,q=el("ff-q").value.toLowerCase();
  let rows=(S.ideas||[]).filter(i=>(!fp||i.pillar===fp)&&(!fs||i.source===fs)
    &&(!fv||((i.strategic_opinion||{}).verdict===fv))&&(!q||((i.title||"")+(i.angle||"")).toLowerCase().includes(q)));
  el("feed-mount").innerHTML=rows.length?rows.map(i=>ideaCard(i)).join(""):`<div class="empty">No ideas match.</div>`;
}

// ---- Calendar ----
function drawCal(){
  const fw=el("cf-week").value,fp=el("cf-pillar").value;
  let rows=(S.calendar||[]).filter(r=>(!fw||("week "+r.week)===fw)&&(!fp||r.pillar===fp));
  if(!rows.length){el("cal-mount").innerHTML=`<div class="empty">No scheduled days.</div>`;return;}
  let h='<table><thead><tr><th>Wk</th><th>Date</th><th>Action</th><th>Platform</th><th>Pillar</th><th>What is scheduled</th><th>Status</th></tr></thead><tbody>';
  rows.forEach(r=>{const ac={publish:"#2f6f6a",prep:"#b5852a",checkpoint:"#7a5c9e"}[r.action]||"#888";
    h+=`<tr class="${r.action==='prep'?'prep':''}"><td>${esc(r.week)}</td><td style="white-space:nowrap">${esc(r.date)}</td>
      <td>${badge(r.action,ac)}</td><td>${r.platform?badge(r.platform,"#444",true):"—"}</td>
      <td>${r.pillar?badge(r.pillar,pill(r.pillar)):"—"}</td>
      <td><div class="title" style="font-size:14px">${esc(r.title||"")}</div>${r.idea_id?`<div class="proof">▸ ${esc(r.idea_id)}</div>`:""}${r.notes?`<div class="angle">${esc(r.notes)}</div>`:""}</td>
      <td>${esc(r.status||"")}</td></tr>`;});
  el("cal-mount").innerHTML=h+'</tbody></table>';
}

// ---- Published ----
function drawPub(){const q=el("pf-q").value.toLowerCase();
  let rows=(S.posts||[]).filter(p=>!q||((p.topic||"")+(p.hook||"")).toLowerCase().includes(q));
  if(!rows.length){el("pub-mount").innerHTML=`<div class="empty">No published posts.</div>`;return;}
  let h='<table><thead><tr><th>Date</th><th>Where</th><th>Pillar</th><th>Post</th><th>Link</th></tr></thead><tbody>';
  rows.forEach(p=>{h+=`<tr><td style="white-space:nowrap">${esc(p.published_at||p.created_at||"")}</td>
    <td>${badge(p.platform||"","#2f6f6a")}</td><td>${badge(p.pillar||"",pill(p.pillar))}</td>
    <td><div class="title" style="font-size:14px">${esc(p.topic||p.hook||p.id)}</div></td>
    <td>${p.url?`<a href="${esc(p.url)}" target="_blank" rel="noopener">open ↗</a>`:'<span class="angle">—</span>'}</td></tr>`;});
  el("pub-mount").innerHTML=h+'</tbody></table>';
}

// ---- Add idea ----
async function submitIdea(){
  const body={title:el("in-title").value,angle:el("in-angle").value,pillar:el("in-pillar").value,
    platform:el("in-platform").value,proof_plan:el("in-proof").value,source:"user"};
  if(!body.title.trim()){toast("Title required");return;}
  if(!body.proof_plan.trim()){toast("Proof plan required — no proof, no Setu idea");return;}
  const btn=el("btn-score");btn.disabled=true;btn.textContent="Scoring…";
  try{
    const r=await fetch("/api/idea",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    const d=await r.json();
    if(d.error){el("add-result").innerHTML=`<div class="card" style="border-left:4px solid var(--red)">${esc(d.error)}</div>`;}
    else{
      let h=ideaCard(d.idea);
      if(d.idea.voice_flags&&d.idea.voice_flags.length)h+=`<div class="card" style="border-left:4px solid var(--gold)">⚠ Banned voice words: ${esc(d.idea.voice_flags.join(", "))} — reword before posting.</div>`;
      if(d.swaps&&d.swaps.length){
        h+=`<div class="swap"><div class="h">⚡ This idea outscores ${d.swaps.length} scheduled slot(s) — approve a swap?</div>`;
        d.swaps.forEach(s=>{h+=`<div class="opt"><div><b>${esc(s.date)}</b> — replace <i>${esc(s.scheduled_title)}</i> <span class="angle">(${s.scheduled_score} → ${s.new_score}, +${s.delta})</span></div>
          <button class="sec" onclick="doSwap('${esc(s.date)}','${esc(d.idea.id)}',this)">Approve swap</button></div>`;});
        h+=`</div>`;
      } else { h+=`<div class="angle" style="margin-top:8px">No calendar swap suggested — it's in the backlog.</div>`; }
      el("add-result").innerHTML=h;
      ["in-title","in-angle","in-proof"].forEach(x=>el(x).value="");
      toast(`Scored ${d.idea.total_score} via ${d.idea.scored_by} ($${(d.cost_usd||0).toFixed(4)})`);
      await load();
    }
  }catch(e){toast("Error: "+e.message);}
  btn.disabled=false;btn.textContent="Score this idea";
}
async function doSwap(date,newId,btn){
  btn.disabled=true;btn.textContent="…";
  const r=await fetch("/api/swap",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({date,new_idea_id:newId})});
  const d=await r.json();
  if(d.error){toast(d.error);btn.disabled=false;btn.textContent="Approve swap";return;}
  toast(`Swapped into ${date}. ${d.displaced||""} back to backlog.`);btn.textContent="✓ Swapped";
  await load();
}

function draw(){drawFeedFilters();drawHome();drawFeed();drawCal();drawPub();}
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".pane").forEach(x=>x.classList.remove("active"));
  t.classList.add("active");el("pane-"+t.dataset.pane).classList.add("active");});
["ff-pillar","ff-verdict","ff-source","ff-q"].forEach(id=>el(id).oninput=drawFeed);
["cf-week","cf-pillar"].forEach(id=>el(id).oninput=drawCal);
el("pf-q").oninput=drawPub;
load();
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Setu Content Dashboard live server")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()
    url = f"http://localhost:{args.port}"
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Setu Content Studio → {url}  (Ctrl-C to stop)")
    if not args.no_open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")


if __name__ == "__main__":
    main()
