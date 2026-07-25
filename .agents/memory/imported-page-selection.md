---
name: Imported page selection
description: How to disambiguate multiple uploaded static HTML snapshots in this project.
---

When multiple imported HTML snapshots have similar filenames, inspect each document's title and primary heading before choosing a route target. Treat the page's semantic content as authoritative over upload order or filename suffixes.

**Why:** Imported assets can arrive in several snapshots, and routing by the first or most recently uploaded file can expose the wrong user-facing page.

**How to apply:** For a requested page such as Technology, compare the candidate snapshots' `<title>` and `<h1>` content, route the matching snapshot explicitly, and document which file is intentionally selected.