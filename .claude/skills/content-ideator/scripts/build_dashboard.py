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


def load_ideas(path: Path) -> list:
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return data.get("ideas", [])


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


def render(ideas: list) -> str:
    # Sort by total_score desc by default; JS handles re-sort/filter client-side.
    ideas = sorted(ideas, key=lambda i: i.get("total_score", 0), reverse=True)
    return _TEMPLATE.replace("__ROWS__", _embed(ideas)).replace(
        "__PILLAR_COLORS__", _embed(PILLAR_COLORS)
    ).replace("__SOURCE_BADGE__", _embed(SOURCE_BADGE)).replace(
        "__COUNT__", str(len(ideas))
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
  .badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px; color:#fff; white-space:nowrap; }
  .dims { font-size:11px; color:var(--muted); font-variant-numeric:tabular-nums; white-space:nowrap; }
  .empty { padding:40px 28px; color:var(--muted); }
</style></head>
<body>
<header>
  <h1>Setu — Idea Feed</h1>
  <div class="sub">__COUNT__ ideas · source of truth: data/ideas.json · sort by clicking a column</div>
</header>
<div class="controls">
  <select id="f-pillar"><option value="">all pillars</option></select>
  <select id="f-source"><option value="">all sources</option></select>
  <select id="f-status"><option value="">all statuses</option></select>
  <input id="f-search" placeholder="search title / angle…" size="28">
</div>
<div id="mount"></div>
<script>
const IDEAS = __ROWS__;
const PILLAR_COLORS = __PILLAR_COLORS__;
const SOURCE_BADGE = __SOURCE_BADGE__;
let sortKey = "total_score", sortDir = -1;

function uniq(key){ return [...new Set(IDEAS.map(i=>i[key]).filter(Boolean))].sort(); }
function fill(id,key){ const s=document.getElementById(id); uniq(key).forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=v;s.appendChild(o);}); }
fill("f-pillar","pillar"); fill("f-source","source"); fill("f-status","status");

function dims(s){ if(!s) return ""; const k=["pillar_fit","value_fit","new_info","lived_exp","proof_level","timeliness","effort"]; const lbl=["P","V","N","L","Pf","T","E"]; return k.map((x,i)=>lbl[i]+s[x]).join(" "); }

function render(){
  const fp=f("f-pillar"),fs=f("f-source"),fst=f("f-status"),q=f("f-search").toLowerCase();
  let rows=IDEAS.filter(i=>(!fp||i.pillar===fp)&&(!fs||i.source===fs)&&(!fst||i.status===fst)&&(!q||((i.title||"")+(i.angle||"")).toLowerCase().includes(q)));
  rows.sort((a,b)=>{const x=a[sortKey]??"",y=b[sortKey]??""; return (x>y?1:x<y?-1:0)*sortDir;});
  const mount=document.getElementById("mount");
  if(!rows.length){ mount.innerHTML='<div class="empty">No ideas match. Run the ideator to populate the feed.</div>'; return; }
  const head=[["title","Idea"],["pillar","Pillar"],["source","Source"],["total_score","Score"],["status","Status"]];
  let h='<table><thead><tr>'+head.map(([k,l])=>`<th data-k="${k}">${l}${sortKey===k?(sortDir<0?" ▾":" ▴"):""}</th>`).join("")+'<th>Dimensions</th></tr></thead><tbody>';
  rows.forEach(i=>{
    const pc=PILLAR_COLORS[i.pillar]||"#888", sc=SOURCE_BADGE[i.source]||"#888";
    h+=`<tr>
      <td><div class="title">${esc(i.title)}</div><div class="angle">${esc(i.angle||"")}</div>${i.proof_plan?`<div class="proof">▸ ${esc(i.proof_plan)}</div>`:""}</td>
      <td><span class="badge" style="background:${pc}">${esc(i.pillar||"")}</span></td>
      <td><span class="badge" style="background:${sc}">${esc(i.source||"")}</span></td>
      <td class="score">${(i.total_score??0).toFixed(2)}</td>
      <td>${esc(i.status||"")}</td>
      <td class="dims">${dims(i.scores)}</td>
    </tr>`;
  });
  mount.innerHTML=h+'</tbody></table>';
  mount.querySelectorAll("th[data-k]").forEach(th=>th.onclick=()=>{const k=th.dataset.k; if(sortKey===k)sortDir*=-1; else{sortKey=k;sortDir=(k==="total_score")?-1:1;} render();});
}
function f(id){return document.getElementById(id).value;}
function esc(s){return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
["f-pillar","f-source","f-status","f-search"].forEach(id=>document.getElementById(id).oninput=render);
render();
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ideas", default=str(ROOT / "data" / "ideas.json"))
    ap.add_argument("--out", default=str(ROOT / "data" / "ideas-dashboard.html"))
    args = ap.parse_args()

    ideas = load_ideas(Path(args.ideas))
    Path(args.out).write_text(render(ideas))
    print(f"Dashboard written: {args.out} ({len(ideas)} ideas)")


if __name__ == "__main__":
    main()
