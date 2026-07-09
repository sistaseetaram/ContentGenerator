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
    "plain-english-ai-takes": "#2F6F6A",
    "plain-english-ai": "#2F6F6A",
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


def load_calendar(path: Path) -> list:
    """Flatten content-calendar.json weeks[].days[] for the Schedule tab.

    Newest week first; within a week, chronological by date.
    """
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    rows = []
    for wk in data.get("weeks", []):
        for d in wk.get("days", []):
            rows.append({**d, "week": wk.get("week"), "theme": wk.get("theme", "")})
    return sorted(rows, key=lambda r: (-(r.get("week") or 0), r.get("date") or ""))


def load_skills(path: Path) -> dict:
    """Skills build-status board for the Skills tab."""
    if not path.exists():
        return {"groups": [], "summary": {}}
    return json.loads(path.read_text())


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


def render(ideas: list, posts: list, calendar: list, skills: dict) -> str:
    # Sort by total_score desc by default; JS handles re-sort/filter client-side.
    ideas = sorted(ideas, key=lambda i: i.get("total_score", 0), reverse=True)
    return (
        _TEMPLATE
        .replace("__ROWS__", _embed(ideas))
        .replace("__POSTS__", _embed(posts))
        .replace("__CALENDAR__", _embed(calendar))
        .replace("__SKILLS__", _embed(skills))
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
  .grp { margin:18px 28px 0; font-size:13px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); font-weight:700; }
  .note { color:var(--muted); font-size:12px; margin-top:2px; }
  .sumbar { display:flex; gap:8px; flex-wrap:wrap; padding:8px 28px 0; }
  .sumpill { padding:4px 12px; border-radius:999px; font-size:12px; font-weight:700; color:#fff; }
  .prep td { background:#FBF6EE; }
  .legend2 { padding:12px 28px 0; color:var(--muted); font-size:12.5px; line-height:1.5; max-width:900px; }
  .legend2 b { color:var(--terra); }
  .scard { background:#fff; border:1px solid var(--line); border-radius:12px; margin:14px 28px; padding:16px 18px; max-width:760px; }
  .scard-h { display:flex; justify-content:space-between; align-items:flex-start; gap:14px; flex-wrap:wrap; margin-bottom:12px; }
  .scard-score { font-size:32px; font-weight:800; font-variant-numeric:tabular-nums; line-height:1; white-space:nowrap; }
  .scard-score small { font-size:13px; color:var(--muted); font-weight:600; }
  .scard-badges { margin-top:6px; display:flex; gap:6px; flex-wrap:wrap; }
  .dimrow { display:grid; grid-template-columns:150px 1fr 26px; gap:10px; align-items:center; margin:6px 0; font-size:12px; }
  .dimlbl { color:var(--ink); } .dimlbl span { color:var(--muted); }
  .track { background:var(--line); border-radius:6px; height:12px; overflow:hidden; }
  .fill { height:100%; border-radius:6px; }
  .dimval { text-align:right; font-variant-numeric:tabular-nums; color:var(--muted); font-weight:700; }
  .swatch { display:inline-block; width:10px; height:10px; border-radius:2px; vertical-align:middle; }
</style></head>
<body>
<header>
  <h1>Setu — Content Dashboard</h1>
  <div class="sub">__COUNT__ ideas · __PCOUNT__ published · Ideas · Schedule · Skills · Published</div>
</header>
<div class="tabs">
  <div class="tab active" data-pane="ideas">Ideas</div>
  <div class="tab" data-pane="scoring">Scoring</div>
  <div class="tab" data-pane="schedule">Schedule</div>
  <div class="tab" data-pane="skills">Skills</div>
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

<div class="pane" id="pane-scoring">
  <div class="controls">
    <select id="cf-pillar"><option value="">all pillars</option></select>
    <select id="cf-verdict"><option value="">all verdicts</option><option value="post_now">post now</option><option value="post_later">post later</option><option value="drop">drop</option></select>
  </div>
  <div id="cmount"></div>
</div>

<div class="pane" id="pane-schedule">
  <div class="controls">
    <select id="sf-week"><option value="">all weeks</option></select>
    <select id="sf-pillar"><option value="">all pillars</option></select>
    <select id="sf-action"><option value="">all actions</option></select>
  </div>
  <div id="smount"></div>
</div>

<div class="pane" id="pane-skills">
  <div class="controls">
    <select id="kf-status"><option value="">all statuses</option></select>
    <select id="kf-kind"><option value="">all kinds</option></select>
    <input id="kf-search" placeholder="search skill / note…" size="28">
  </div>
  <div id="kmount"></div>
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
const CALENDAR = __CALENDAR__;
const SKILLS = __SKILLS__;
const PILLAR_COLORS = __PILLAR_COLORS__;
const SOURCE_BADGE = __SOURCE_BADGE__;
const VERDICT_COLORS = __VERDICT_COLORS__;
const STATUS_COLORS = {built:"#2A7A4A", partial:"#B5852A", pending:"#8A7F75", dropped:"#9E3030"};
const ACTION_COLORS = {publish:"#2F6F6A", prep:"#B5852A", checkpoint:"#7A5C9E"};
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

// ---- Scoring tab ----
const DIMS=[["pillar_fit","Pillar fit",1.0],["value_fit","Brand-value fit",1.0],["new_info","New information",1.5],["lived_exp","Lived experience",1.5],["proof_level","Proof level",1.5],["timeliness","Timeliness",1.0],["effort","Effort",0.75]];
const SCORE_MAX=41.25, HI="#C25A3C", LO="#9BB0AE";
function pct100(t){ return Math.round((t/SCORE_MAX)*100); }
cfillSel("cf-pillar","pillar");
function cfillSel(id,key){ const s=document.getElementById(id); if(!s) return; [...new Set(IDEAS.filter(i=>i.scores).map(i=>i[key]).filter(Boolean))].sort().forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=v;s.appendChild(o);}); }

function crender(){
  const fp=f("cf-pillar"),fv=f("cf-verdict");
  let rows=IDEAS.filter(i=>i.scores).filter(i=>(!fp||i.pillar===fp)&&(!fv||getVerdict(i)===fv))
    .sort((a,b)=>(b.total_score||0)-(a.total_score||0));
  const mount=document.getElementById("cmount");
  let h=`<div class="legend2">Every idea is graded on <b>7 checks</b>, each scored 1–5. Bars in <span class="swatch" style="background:${HI}"></span> <b>terracotta</b> are the heaviest checks (×1.5) — <b>new information, lived experience, proof</b> — the things that make Setu content un-fakeable. <span class="swatch" style="background:${LO}"></span> grey-green are the lighter checks. The big number is the weighted total shown out of 100 (raw max 41.25).</div>`;
  if(!rows.length){ mount.innerHTML=h+'<div class="empty">No scored ideas match.</div>'; return; }
  rows.forEach(i=>{
    const pc=PILLAR_COLORS[i.pillar]||"#888";
    const op=i.strategic_opinion||{}, vc=VERDICT_COLORS[op.verdict]||"#888";
    h+=`<div class="scard"><div class="scard-h">
      <div><div class="title">${esc(i.title)}</div>
        <div class="scard-badges">
          <span class="badge" style="background:${pc}">${esc(i.pillar||"")}</span>
          ${op.verdict?`<span class="badge" style="background:${vc}">${esc((op.verdict||"").replace(/_/g," "))}</span>`:""}
          <span class="nolink">${esc(i.id||"")}</span>
        </div>
      </div>
      <div style="text-align:right"><div class="scard-score">${pct100(i.total_score||0)}<small>/100</small></div>
        <div class="nolink">${(i.total_score||0).toFixed(2)} / 41.25</div></div>
    </div>`;
    DIMS.forEach(([k,lbl,w])=>{
      const v=i.scores[k]||0, col=(w===1.5)?HI:LO;
      h+=`<div class="dimrow"><div class="dimlbl">${lbl} <span>×${w}</span></div>
        <div class="track"><div class="fill" style="width:${v/5*100}%;background:${col}"></div></div>
        <div class="dimval">${v}</div></div>`;
    });
    if(i.proof_plan) h+=`<div class="proof" style="margin-top:8px">▸ ${esc(i.proof_plan)}</div>`;
    h+=`</div>`;
  });
  mount.innerHTML=h;
}
["cf-pillar","cf-verdict"].forEach(id=>document.getElementById(id).oninput=crender);

// ---- Schedule tab ----
function suniq(key){ return [...new Set(CALENDAR.map(r=>r[key]).filter(v=>v!==null&&v!==undefined&&v!==""))].sort(); }
function sfill(id,key){ const s=document.getElementById(id); if(!s) return; suniq(key).forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=(id==="sf-week"?"week "+v:v);s.appendChild(o);}); }
sfill("sf-week","week"); sfill("sf-pillar","pillar"); sfill("sf-action","action");

function srender(){
  const fw=f("sf-week"),fp=f("sf-pillar"),fa=f("sf-action");
  let rows=CALENDAR.filter(r=>(!fw||String(r.week)===fw)&&(!fp||r.pillar===fp)&&(!fa||r.action===fa));
  const mount=document.getElementById("smount");
  if(!rows.length){ mount.innerHTML='<div class="empty">No scheduled days. Run the ideator Schedule mode.</div>'; return; }
  let h='<table><thead><tr><th>Wk</th><th>Date</th><th>Action</th><th>Where</th><th>Pillar</th><th>What is scheduled</th><th>Status</th></tr></thead><tbody>';
  rows.forEach(r=>{
    const pc=PILLAR_COLORS[r.pillar]||"#888", ac=ACTION_COLORS[r.action]||"#888";
    const title=r.title||"";
    const plat=r.platform?`<span class="badge" style="background:#2F6F6A">${esc(r.platform)}</span>`:'<span class="nolink">—</span>';
    const pillar=r.pillar?`<span class="badge" style="background:${pc}">${esc(r.pillar)}</span>`:'<span class="nolink">—</span>';
    const idea=r.idea_id?`<span class="proof">▸ ${esc(r.idea_id)}</span>`:"";
    h+=`<tr class="${r.action==='prep'?'prep':''}">
      <td style="white-space:nowrap">${esc(String(r.week||""))}</td>
      <td style="white-space:nowrap">${esc(r.date||"")}</td>
      <td><span class="badge" style="background:${ac}">${esc(r.action||"")}</span></td>
      <td>${plat}</td>
      <td>${pillar}</td>
      <td><div class="title">${esc(title)}</div>${idea}${r.notes?`<div class="note">${esc(r.notes)}</div>`:""}</td>
      <td>${esc(r.status||"")}</td>
    </tr>`;
  });
  mount.innerHTML=h+'</tbody></table>';
}
["sf-week","sf-pillar","sf-action"].forEach(id=>document.getElementById(id).oninput=srender);

// ---- Skills tab ----
const SKILL_ROWS=[]; (SKILLS.groups||[]).forEach(g=>(g.items||[]).forEach(it=>SKILL_ROWS.push({...it,group:g.group})));
function kuniq(key){ return [...new Set(SKILL_ROWS.map(r=>r[key]).filter(Boolean))].sort(); }
function kfill(id,key){ const s=document.getElementById(id); kuniq(key).forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=v;s.appendChild(o);}); }
kfill("kf-status","status"); kfill("kf-kind","kind");

function krender(){
  const fst=f("kf-status"),fk=f("kf-kind"),q=f("kf-search").toLowerCase();
  const mount=document.getElementById("kmount");
  const sum=SKILLS.summary||{};
  let head='<div class="sumbar">';
  ["built","partial","pending","dropped"].forEach(s=>{ if(sum[s]!==undefined) head+=`<span class="sumpill" style="background:${STATUS_COLORS[s]}">${sum[s]} ${s}</span>`; });
  head+='</div>'+(sum.note?`<div class="note" style="margin:6px 28px 0">${esc(sum.note)}</div>`:"");
  let rows=SKILL_ROWS.filter(r=>(!fst||r.status===fst)&&(!fk||r.kind===fk)&&(!q||((r.name||"")+(r.note||"")).toLowerCase().includes(q)));
  if(!rows.length){ mount.innerHTML=head+'<div class="empty">No skills match.</div>'; return; }
  let h=head, lastGroup=null;
  rows.forEach(r=>{
    if(r.group!==lastGroup){ if(lastGroup!==null) h+='</tbody></table>'; lastGroup=r.group;
      h+=`<div class="grp">${esc(r.group)}</div><table><thead><tr><th>Name</th><th>Kind</th><th>Status</th><th>Note</th></tr></thead><tbody>`; }
    const sc=STATUS_COLORS[r.status]||"#888";
    const ver=r.version?` <span class="nolink">${esc(r.version)}</span>`:"";
    h+=`<tr>
      <td><span class="title">${esc(r.name)}</span>${ver}</td>
      <td><span class="nolink">${esc(r.kind||"")}</span></td>
      <td><span class="badge" style="background:${sc}">${esc(r.status||"")}</span></td>
      <td><div class="note" style="margin-top:0">${esc(r.note||"")}</div></td>
    </tr>`;
  });
  h+='</tbody></table>';
  mount.innerHTML=h;
}
["kf-status","kf-kind","kf-search"].forEach(id=>document.getElementById(id).oninput=krender);

// ---- Tab switching ----
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".pane").forEach(x=>x.classList.remove("active"));
  t.classList.add("active");
  document.getElementById("pane-"+t.dataset.pane).classList.add("active");
});

render();
crender();
prender();
srender();
krender();
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ideas", default=str(ROOT / "data" / "ideas.json"))
    ap.add_argument("--posts", default=str(ROOT / "data" / "posts.json"))
    ap.add_argument("--calendar", default=str(ROOT / "data" / "content-calendar.json"))
    ap.add_argument("--skills", default=str(ROOT / "data" / "skills-status.json"))
    ap.add_argument("--out", default=str(ROOT / "data" / "ideas-dashboard.html"))
    args = ap.parse_args()

    ideas = load_ideas(Path(args.ideas))
    posts = load_posts(Path(args.posts))
    calendar = load_calendar(Path(args.calendar))
    skills = load_skills(Path(args.skills))
    Path(args.out).write_text(render(ideas, posts, calendar, skills))
    print(f"Dashboard written: {args.out} "
          f"({len(ideas)} ideas, {len(posts)} published, "
          f"{len(calendar)} schedule rows, {len(skills.get('groups', []))} skill groups)")


if __name__ == "__main__":
    main()
