# ContentGenerator — Shared Context Adapter

## What this is

A pointer to the cross-project shared context store in SharedInfra. ContentGenerator is the **write authority for published content** and a **reader of leads and brand voice**.

## Store location

```
/Users/sistaseetaram/Desktop/Claude/SharedInfra/shared_context/
  shared_context.py   ← accessor module (pure stdlib)
  store.json          ← live data (JSON, human-readable)
  schema.json         ← documented schema with field descriptions
```

## How to use from this project

```python
import sys
sys.path.insert(0, "/Users/sistaseetaram/Desktop/Claude/SharedInfra/shared_context")
from shared_context import (
    read_brand_voice,        # read: brand voice snapshot (forbidden words, values, etc.)
    read_icp,                # read: ICP definition (pains, products, outreach rule)
    read_leads,              # read: leads OutreachAutomation has written
    write_published_post,    # WRITE: log a newly published post so Outreach can reference it
    link_lead_to_content,    # write: record that a post was used as proof in outreach
)
```

## Authority table

| Data type        | ContentGenerator | OutreachAutomation |
|------------------|------------------|-------------------|
| brand_voice      | read             | read              |
| icp              | read             | read              |
| leads            | **READ ONLY**    | write             |
| published_content| **WRITE**        | read              |
| cross_references | write            | write             |

## When to call write_published_post

After a post is confirmed published (status = "published" in `data/posts.json`), sync it to the store:

```python
from shared_context import write_published_post

post = {
    "id": "post-010",
    "pillar": "build-receipts",
    "platform": "linkedin",
    "status": "published",
    "hook": "...",
    "topic": "...",
    "published_at": "2026-07-07",
    "url": "https://www.linkedin.com/posts/..."
}
write_published_post(post, written_by="ContentGenerator")
```

## Why this exists

Previously:
- Brand voice was duplicated in `OutreachAutomation/tools/setu_voice.py` (embedded) and in the Obsidian content-wiki.
- Published posts lived only in `data/posts.json` — OutreachAutomation had no way to reference which proof points had been publicly stated.
- Leads lived only in `OutreachAutomation/.tmp/leads.json` — ContentGenerator could not check whether a lead was active before naming them in public content.

Now: one store, two readers, clear write authorities.

## CLI quick-check

```bash
cd /Users/sistaseetaram/Desktop/Claude/SharedInfra/shared_context
python shared_context.py status        # counts + last-write metadata
python shared_context.py brand-voice   # print voice snapshot
python shared_context.py leads         # print all leads
python shared_context.py posts         # print all published posts
```

> **Warning (2026-07-07):** `refresh-voice` in the shared store is a stub — it stamps
> a new snapshot date without re-reading the wiki. Treat the brand-voice snapshot as
> manually maintained; verify content, not the date.
