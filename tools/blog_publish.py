#!/usr/bin/env python3
"""
Blog pipeline — ContentGenerator -> setuagency.com (Astro 5 static site).

Deterministic. Python stdlib only. No model calls, no network, no tokens at runtime.
Drafting the prose is a separate job (a content sub-agent, per CLAUDE.md Hard Rule #4).
This tool owns the mechanical half: frontmatter, slug, validation, placement, deploy command.

WHY THIS EXISTS
    The site lives in a different repo (MyPersonalBrand) from the content system
    (ContentGenerator). Rather than have an agent reach across projects, this writes a
    self-contained, Astro-ready post into data/blog/ here, and hands over one copy command.

ASTRO 5 CONTRACT (verified against docs.astro.build 2026-09-19, not from memory)
    - collection config lives at   src/content.config.ts      (NOT src/content/config.ts)
    - loader:  glob({ pattern: "**/*.md", base: "./src/content/blog" })
    - imports: defineCollection from 'astro:content', glob from 'astro/loaders', z from 'astro/zod'
    - dynamic route file MUST be   src/pages/blog/[...id].astro
      because getStaticPaths maps params: { id: post.id }   (Astro 4 used .slug — it changed)
    - render:  import { render } from 'astro:content';  const { Content } = await render(post);
               (Astro 4's  post.render()  is gone)

USAGE
    # scaffold a new post
    python3 tools/blog_publish.py new "Why AI renders don't match your floor plan" \
        --description "What breaks, why it breaks, and the check that catches it." \
        --tags ai-rendering,architecture,verification

    # validate before it goes near the site
    python3 tools/blog_publish.py validate data/blog/why-ai-renders-dont-match-your-floor-plan.md

    # print the collection config the site needs (paste into the site repo once)
    python3 tools/blog_publish.py scaffold-config

    # stage into the site repo once a blog page exists there
    python3 tools/blog_publish.py deploy data/blog/<file>.md --site /path/to/site
"""

import argparse
import datetime as _dt
import os
import re
import shutil
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BLOG_DIR = os.path.join(REPO, "data", "blog")

# CLAUDE.md Hard Rule #1. A post needing one of these to sound interesting is a weak post.
BANNED = [
    "revolutionary", "game-changing", "game changing", "disrupt", "synergy",
    "cutting-edge", "cutting edge", "empowering businesses to unlock potential",
]

# Frontmatter keys the Astro collection schema accepts. Keep in lockstep with scaffold-config.
REQUIRED_KEYS = ["title", "description", "pubDate"]
OPTIONAL_KEYS = ["updatedDate", "tags", "draft"]


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text) or "untitled"


def today():
    return _dt.date.today().isoformat()


def parse_frontmatter(path):
    """Minimal YAML-ish frontmatter reader. Returns (dict, body). No yaml dependency."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw
    meta = {}
    for line in parts[1].strip().splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, parts[2].lstrip("\n")


def cmd_new(args):
    slug = args.slug or slugify(args.title)
    os.makedirs(BLOG_DIR, exist_ok=True)
    path = os.path.join(BLOG_DIR, f"{slug}.md")
    if os.path.exists(path) and not args.force:
        sys.exit(f"refusing to overwrite {path} (pass --force)")

    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    tags_line = f"tags: [{', '.join(tags)}]\n" if tags else ""

    body = f"""---
title: "{args.title}"
description: "{args.description}"
pubDate: {args.date or today()}
{tags_line}draft: true
---

<!--
  DRAFT. Written by a content sub-agent, not by hand and not by the orchestrator
  (CLAUDE.md Hard Rule #4). Before publishing:
    - every technical claim traces to the design-automation wiki
    - no time/cost/ROI figure that isn't measured
    - five-value gate: work not tech / quiet over loud / respect owners /
      ship don't slide / map before build
    - flip draft: false
-->

## The problem

## What actually happened

## The method

## What it means for a studio
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"created {os.path.relpath(path, REPO)}")
    print(f"slug    {slug}")
    print(f"url     https://setuagency.com/blog/{slug}/   (once the blog page exists)")


def cmd_validate(args):
    path = args.path
    if not os.path.exists(path):
        sys.exit(f"not found: {path}")
    meta, body = parse_frontmatter(path)
    problems, warnings = [], []

    for key in REQUIRED_KEYS:
        if not meta.get(key):
            problems.append(f"missing required frontmatter: {key}")

    unknown = [k for k in meta if k not in REQUIRED_KEYS + OPTIONAL_KEYS]
    if unknown:
        problems.append(
            f"frontmatter keys not in the collection schema: {', '.join(unknown)} "
            "(Astro will fail the build — add them to content.config.ts or remove them)"
        )

    if meta.get("pubDate"):
        try:
            _dt.date.fromisoformat(meta["pubDate"])
        except ValueError:
            problems.append(f"pubDate not ISO yyyy-mm-dd: {meta['pubDate']}")

    lower = body.lower()
    for word in BANNED:
        if word in lower:
            problems.append(f"banned voice word present: {word!r}")

    if meta.get("draft", "").lower() == "true":
        warnings.append("draft: true — will not publish until flipped to false")
    words = len(body.split())
    if words < 300:
        warnings.append(f"body is short ({words} words) for a canonical long-form piece")

    rel = os.path.relpath(path, REPO)
    for w in warnings:
        print(f"  warn  {rel}: {w}")
    if problems:
        for p in problems:
            print(f"  FAIL  {rel}: {p}")
        sys.exit(1)
    print(f"  ok    {rel} ({words} words)")


def cmd_scaffold_config(args):
    print("""# Paste into the SITE repo (MyPersonalBrand), not this one.
# File: src/content.config.ts    <-- Astro 5 path. NOT src/content/config.ts

import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };

# --- and the route file: src/pages/blog/[...id].astro ---
# NOTE the filename is [...id].astro  (Astro 5 maps params:{ id: post.id }).
# [...slug].astro + post.slug is the Astro 4 pattern and will not build.
#
# ---
# import { getCollection, render } from 'astro:content';
# import Base from '../../layouts/Base.astro';
# export async function getStaticPaths() {
#   const posts = await getCollection('blog', ({ data }) => !data.draft);
#   return posts.map(post => ({ params: { id: post.id }, props: { post } }));
# }
# const { post } = Astro.props;
# const { Content } = await render(post);
# ---
# <Base title={post.data.title}>
#   <h1>{post.data.title}</h1>
#   <Content />
# </Base>
""")


def cmd_deploy(args):
    src = args.path
    if not os.path.exists(src):
        sys.exit(f"not found: {src}")

    meta, _ = parse_frontmatter(src)
    if meta.get("draft", "").lower() == "true":
        sys.exit("refusing to deploy: frontmatter says draft: true")

    dest_dir = os.path.join(args.site, "src", "content", "blog")
    if not os.path.isdir(os.path.join(args.site, "src")):
        sys.exit(
            f"{args.site} does not look like the Astro site (no src/).\n"
            "Expected the site root, e.g. .../setu-brand/03-collateral/website/site"
        )
    if not os.path.isdir(dest_dir):
        sys.exit(
            f"no blog collection at {dest_dir}.\n"
            "The site has no blog page yet. Run `scaffold-config` and add it in the site repo first."
        )

    dest = os.path.join(dest_dir, os.path.basename(src))
    if args.dry_run:
        print(f"[dry-run] would copy\n  {src}\n-> {dest}")
        return
    shutil.copy2(src, dest)
    print(f"staged {dest}")
    print("\nNot deployed. From the site repo, review then run:")
    print("  npm run build && git add -A && git commit && git push origin HEAD")


def main():
    ap = argparse.ArgumentParser(description="Blog pipeline for setuagency.com")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="scaffold an Astro-ready post")
    p.add_argument("title")
    p.add_argument("--description", required=True)
    p.add_argument("--tags", help="comma separated")
    p.add_argument("--slug")
    p.add_argument("--date", help="ISO yyyy-mm-dd, defaults to today")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("validate", help="frontmatter + voice check")
    p.add_argument("path")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("scaffold-config", help="print the config the site repo needs")
    p.set_defaults(func=cmd_scaffold_config)

    p = sub.add_parser("deploy", help="stage a post into the site repo")
    p.add_argument("path")
    p.add_argument("--site", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_deploy)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
