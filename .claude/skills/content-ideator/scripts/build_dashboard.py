#!/usr/bin/env python3
"""
Render data/ideas.json into a standalone, sortable/filterable HTML dashboard.
No server, no build step — open the file in a browser.

Usage:
    python .claude/skills/content-ideator/scripts/build_dashboard.py
    python .../build_dashboard.py --ideas data/ideas.json --out data/ideas-dashboard.html

Deterministic: no model calls. Reads ideas.json, writes ideas-dashboard.html.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # project root (…/ContentGenerator)

PILLAR_COLORS = {
    "build-receipts": "#C25A3C",      # terracotta
    "plain-english-takes": "#2F6F6A",
    "build-in-public": "#7A5C9E",
    "build-in-public-setu": "#7A5C9E",
    "contrarian": "#B5852A",
    "instagram-creative": "#9E5C7A",
}
SOURCE_BADGE = {"agent": "#2F6F6A", "user": "#C25A3C", "sister": "#9E5C7A"}
VERDICT_COLORS = {"post_now": "#2A7A4A", "post_later": "#B5852A", "drop": "#9E3030"}


def load_ideas(path: Path) -> list:
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return data.get("ideas", [])


def load_posts(path: Path) -> list:
    """Published posts for the Published tab. Newest first."""
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    posts = [p for p in data.get("posts", []) if p.get("status") == "published"]
    return sorted(posts, key=lambda p: p.get("published_at") or "", reverse=True)


def _embed(obj) -> str:
    """JSON for safe embedding inside a <script> tag.

    A string like '</script>' in the data would otherwise terminate the
    script block and let the browser parse the rest as HTML (breakout/XSS).
    Unicode-escaping <, >, & keeps the JSON valid while making breakout
    impossible. JS-side esc() still guards innerHTML at render time.
    """
    return (
        json.dumps(obj)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def render(ideas: list, posts: list) -> str:
    # Sort by total_score desc by default; JS handles re-sort/filter client-side.
    ideas = sorted(ideas, key=lambda i: i.get("total_score", 0), reverse=True)
    return (
        _TEMPLATE
        .replace("__ROWS__", _embed(ideas))
        .replace("__POSTS__", _embed(posts))
        .replace("__PILLAR_COLORS__", _embed(PILLAR_COLORS))
        .replace("__SOURCE_BADGE__", _embed(SOURCE_BADGE))
        .replace("__VERDICT_COLORS__", _embed(VERDICT_COLORS))
        .replace("__COUNT__", str(len(ideas)))
        .replace("__PCOUNT__", str(len(posts)))
    )


_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Setu — Idea Feed</title>
<style>
  :root { --bg:#FBF7F2; --ink:#2B2622; --muted:#8A7F75; --line:#E6DCD0; --terra:#C25A3C; }
  * { box-sizing:border-box; }
  body { margin:0; font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif; background:var(--bg); color:var(--ink); }
  header { padding:24px 28px 12px; }
  h1 { margin:0; font-size:20px; letter-spacing:-.01em; }
  .sub { color:var(--muted); font-size:13px; margin-top:2px; }
  .controls { display:flex; gap:8px; flex-wrap:wrap; padding:8px 28px 16px; }
  .controls select, .controls input { padding:6px 10px; border:1px solid var(--line); border-radius:8px; background:#fff; font-size:13px; }
  table { width:calc(100% - 56px); margin:0 28px 40px; border-collapse:collapse; background:#fff; border:1px solid var(--line); border-radius:12px; overflow:hidden; }
  th, td { text-align:left; padding:10px 12px; border-bottom:1px solid var(--line); vertical-align:top; }
  th { font-size:12px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); cursor:pointer; user-select:none; white-space:nowrap; }
  th:hover { color:var(--ink); }
  tr:last-child td { border-bottom:none; }
  .score { font-weight:700; font-variant-numeric:tabular-nums; }
  .title { font-weight:600; }
  .angle { color:var(--muted); font-size:13px; margin-top:2px; }
  .proof { font-size:12px; color:var(--terra); margin-top:4px; }
  .verdict-reason { font-size:12px; color:var(--muted); margin-top:3px; font-style:italic; }
  .verdict-when { font-size:11px; color:var(--ink); margin-top:2px; }
  .badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px; color:#fff; white-space:nowrap; }
  .dims { font-size:11px; color:var(--muted); font-variant-numeric:tabular-nums; white-space:nowrap; }
  .empty { padding:40px 28px; color:var(--muted); }
  .tabs { display:flex; gap:4px; padding:0 28px; border-bottom:1px solid var(--line); }
  .tab { padding:10px 16px; font-size:14px; font-weight:600; color:var(--muted); cursor:pointer; border-bottom:2px solid transparent; margin-bottom:-1px; }
  .tab.active { color:var(--ink); border-bottom-color:var(--terra); }
  .pane { display:none; }
  .pane.active { display:block; }
  a.postlink { color:var(--terra); text-decoration:none; }
  a.postlink:hover { text-decoration:underline; }
  .nolink { color:var(--muted); font-size:12px; }
</style></head>
<body>
<header>
  <h1>Setu — Content Dashboard</h1>
  <div class="sub">__COUNT__ ideas · __PCOUNT__ published · source: data/ideas.json + data/posts.json</div>
</header>
<div class="tabs">
  <div class="tab active" data-pane="ideas">Ideas</div>
  <div class="tab" data-pane="published">Published</div>
</div>

<div class="pane active" id="pane-ideas">
  <div class="controls">
    <select id="f-pillar"><option value="">all pillars</option></select>
    <select id="f-source"><option value="">all sources</option></select>
    <select id="f-status"><option value="">all statuses</option></select>
    <select id="f-verdict"><option value="">all verdicts</option><option value="post_now">post now</option><option value="post_later">post later</option><option value="drop">drop</option></select>
    <input id="f-search" placeholder="search title / angle…" size="28">
  </div>
  <div id="mount"></div>
</div>

<div class="pane" id="pane-published">
  <div class="controls">
    <select id="pf-platform"><option value="">all platforms</option></select>
    <select id="pf-pillar"><option value="">all pillars</option></select>
    <input id="pf-search" placeholder="search topic…" size="28">
  </div>
  <div id="pmount"></div>
</div>
<script>
const IDEAS = __ROWS__;
const POSTS = __POSTS__;
const PILLAR_COLORS = __PILLAR_COLORS__;
const SOURCE_BADGE = __SOURCE_BADGE__;
const VERDICT_COLORS = __VERDICT_COLORS__;
let sortKey = "total_score", sortDir = -1;

function uniq(key){ return [...new Set(IDEAS.map(i=>i[key]).filter(Boolean))].sort(); }
function fill(id,key){ const s=document.getElementById(id); uniq(key).forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=v;s.appendChild(o);}); }
fill("f-pillar","pillar"); fill("f-source","source"); fill("f-status","status");

function dims(s){ if(!s) return ""; const k=["pillar_fit","value_fit","new_info","lived_exp","proof_level","timeliness","effort"]; const lbl=["P","V","N","L","Pf","T","E"]; return k.map((x,i)=>lbl[i]+s[x]).join(" "); }

function verdictCell(op){
  if(!op) return "";
  const vc=VERDICT_COLORS[op.verdict]||"#888";
  const label=(op.verdict||"").replace(/_/g," ");
  return `<span class="badge" style="background:${vc}">${esc(label)}</span>`
    +(op.reason?`<div class="verdict-reason">${esc(op.reason)}</div>`:"")
    +(op.when_to_post&&op.when_to_post!=="now"?`<div class="verdict-when">→ ${esc(op.when_to_post)}</div>`:"");
}

function getVerdict(i){ return i.strategic_opinion&&i.strategic_opinion.verdict||""; }

function render(){
  const fp=f("f-pillar"),fs=f("f-source"),fst=f("f-status"),fv=f("f-verdict"),q=f("f-search").toLowerCase();
  let rows=IDEAS.filter(i=>(!fp||i.pillar===fp)&&(!fs||i.source===fs)&&(!fst||i.status===fst)&&(!fv||getVerdict(i)===fv)&&(!q||((i.title||"")+(i.angle||"")).toLowerCase().includes(q)));
  rows.sort((a,b)=>{const x=a[sortKey]??"",y=b[sortKey]??""; return (x>y?1:x<y?-1:0)*sortDir;});
  const mount=document.getElementById("mount");
  if(!rows.length){ mount.innerHTML='<div class="empty">No ideas match. Run the ideator to populate the feed.</div>'; return; }
  const head=[["title","Idea"],["pillar","Pillar"],["source","Source"],["total_score","Score"],["status","Status"]];
  let h='<table><thead><tr>'+head.map(([k,l])=>`<th data-k="${k}">${l}${sortKey===k?(sortDir<0?" ▾":" ▴"):""}</th>`).join("")+'<th>Strategic Opinion</th><th>Dimensions</th></tr></thead><tbody>';
  rows.forEach(i=>{
    const pc=PILLAR_COLORS[i.pillar]||"#888", sc=SOURCE_BADGE[i.source]||"#888";
    h+=`<tr>
      <td><div class="title">${esc(i.title)}</div><div class="angle">${esc(i.angle||"")}</div>${i.proof_plan?`<div class="proof">▸ ${esc(i.proof_plan)}</div>`:""}</td>
      <td><span class="badge" style="background:${pc}">${esc(i.pillar||"")}</span></td>
      <td><span class="badge" style="background:${sc}">${esc(i.source||"")}</span></td>
      <td class="score">${(i.total_score??0).toFixed(2)}</td>
      <td>${esc(i.status||"")}</td>
      <td>${verdictCell(i.strategic_opinion)}</td>
      <td class="dims">${dims(i.scores)}</td>
    </tr>`;
  });
  mount.innerHTML=h+'</tbody></table>';
  mount.querySelectorAll("th[data-k]").forEach(th=>th.onclick=()=>{const k=th.dataset.k; if(sortKey===k)sortDir*=-1; else{sortKey=k;sortDir=(k==="total_score")?-1:1;} render();});
}
function f(id){return document.getElementById(id).value;}
function esc(s){return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
["f-pillar","f-source","f-status","f-verdict","f-search"].forEach(id=>document.getElementById(id).oninput=render);

// ---- Published tab ----
function puniq(key){ return [...new Set(POSTS.map(p=>p[key]).filter(Boolean))].sort(); }
function pfill(id,key){ const s=document.getElementById(id); puniq(key).forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=v;s.appendChild(o);}); }
pfill("pf-platform","platform"); pfill("pf-pillar","pillar");

function prender(){
  const fp=f("pf-platform"),fpi=f("pf-pillar"),q=f("pf-search").toLowerCase();
  let rows=POSTS.filter(p=>(!fp||p.platform===fp)&&(!fpi||p.pillar===fpi)&&(!q||((p.topic||"")+(p.hook||"")).toLowerCase().includes(q)));
  const mount=document.getElementById("pmount");
  if(!rows.length){ mount.innerHTML='<div class="empty">No published posts yet.</div>'; return; }
  let h='<table><thead><tr><th>Date</th><th>Where</th><th>Pillar</th><th>Post</th><th>Link</th></tr></thead><tbody>';
  rows.forEach(p=>{
    const pc=PILLAR_COLORS[p.pillar]||"#888";
    const title=p.topic||p.hook||p.id;
    const link=p.url?`<a class="postlink" href="${esc(p.url)}" target="_blank" rel="noopener">open ↗</a>`:'<span class="nolink">no link</span>';
    h+=`<tr>
      <td style="white-space:nowrap">${esc(p.published_at||p.created_at||"")}</td>
      <td><span class="badge" style="background:#2F6F6A">${esc(p.platform||"")}</span></td>
      <td><span class="badge" style="background:${pc}">${esc(p.pillar||"")}</span></td>
      <td><div class="title">${esc(title)}</div></td>
      <td>${link}</td>
    </tr>`;
  });
  mount.innerHTML=h+'</tbody></table>';
}
["pf-platform","pf-pillar","pf-search"].forEach(id=>document.getElementById(id).oninput=prender);

// ---- Tab switching ----
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".pane").forEach(x=>x.classList.remove("active"));
  t.classList.add("active");
  document.getElementById("pane-"+t.dataset.pane).classList.add("active");
});

render();
prender();
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ideas", default=str(ROOT / "data" / "ideas.json"))
    ap.add_argument("--posts", default=str(ROOT / "data" / "posts.json"))
    ap.add_argument("--out", default=str(ROOT / "data" / "ideas-dashboard.html"))
    args = ap.parse_args()

    ideas = load_ideas(Path(args.ideas))
    posts = load_posts(Path(args.posts))
    Path(args.out).write_text(render(ideas, posts))
    print(f"Dashboard written: {args.out} ({len(ideas)} ideas, {len(posts)} published)")


if __name__ == "__main__":
    main()
