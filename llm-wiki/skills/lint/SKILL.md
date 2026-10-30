---
name: lint
description: Health-check a topic wiki in the ZenNotes vault. Fixes mechanical problems and reports the rest as a checklist.
argument-hint: "<topic>"
disable-model-invocation: true
---

# Lint

Input: $ARGUMENTS

First read `../../reference/conventions.md` (relative to this skill's base directory).

A topic is required. Find its wiki per "Finding the wiki for a topic"; never create one. If no topic is given, list the existing wikis and ask which one.

## 1. Survey

- Read `<Topic> Schema`, `<Topic> Index` and `<Topic> Overview`.
- List every page in `wiki/<slug>/` per "Listing a wiki's pages" and collect titles, subfolders, wikilinks and timestamps.
- Use `backlinks` to find what links to each page.

## 2. Fix automatically (mechanical only)

- Pages that exist but are missing from the Index: add them.
- Index entries pointing at pages that no longer exist: remove them.
- A `[[link]]` that clearly points at a renamed page (one obvious target): repoint it.
- Pages missing a `## Related` section, or related pages that link one way only: add the reciprocal link.
- Raw notes with no source page: list them (do not ingest them here).

Never touch `raw/`. Never change a factual claim.

## 3. Report (needs judgment, do not fix)

- Contradictions between pages, including unresolved `[!warning] Contradiction` callouts.
- Claims that look stale (old sources, superseded by newer ones).
- Orphan pages (no backlinks other than the Index).
- Dangling links with no obvious target.
- Concepts mentioned often but with no page; open questions in the Overview that a new source could answer.
- Places where the Overview no longer matches the pages.

## 4. Log and reply

- Append a `lint` line to `<Topic> Log`: `fixed <n> | open: <short list or "none">`.
- Reply with what was fixed, then the open issues as a `- [ ]` checklist with links.
