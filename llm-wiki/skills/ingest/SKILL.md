---
name: ingest
description: Ingest a source (URL, local file, pasted text, or a raw note) into a topic wiki in the ZenNotes vault, updating summary, concept, entity and navigation pages. Creates the wiki if the topic is new (after the user confirms).
argument-hint: "[topic] <url | file path | raw note | pasted text>"
disable-model-invocation: true
---

# Ingest

Input: $ARGUMENTS

First read `../../reference/conventions.md` (relative to this skill's base directory). Everything below assumes those conventions. Ingest **one source per run**; if given several, do them one after another, each fully.

## 1. Resolve the topic

- If the input names a topic, find its wiki per "Finding the wiki for a topic".
- If not, read the source first (step 2), propose a topic (an existing wiki if one fits, else a new name), and wait for the user's OK.
- If creating a new wiki, do so per "Creating a wiki" only after the user confirms.
- Read the wiki's `<Topic> Schema` and `<Topic> Index`. The Schema's preferences override the conventions.

## 2. Capture the raw source

The goal is the **complete, unmodified** text in `raw/`.

| Input | How |
|---|---|
| A note already in `wiki/<slug>/raw/` | Use it as is. |
| URL | Fetch with WebFetch, prompting for the full article text verbatim as Markdown (no summarising). If the result says it was truncated, call again with the given `offset` until complete. |
| Local file | Read it (use the pdf skill for PDFs). |
| Pasted text | Use the text exactly as pasted. |

- If a URL is paywalled, blocked (401/403) or returns only a teaser, **stop**: tell the user it couldn't be read and ask them to paste the text. Do not use paywall-bypass mirrors or caches.
- Before creating, `search_by_title` for an existing `Raw - <short name>` from the same origin. If found, tell the user it was already ingested and ask whether to re-ingest.
- Create the raw note in `wiki/<slug>/raw/` using the raw note template.

## 3. Write the source page

Create `Source - <short name>` in `sources/` from the template: summary, key claims, notable quotes (verbatim, short). Link the raw note.

## 4. Update the wiki

For every concept and entity the source meaningfully touches (typically 5–15 pages):

- Existing page in this wiki: read it, then integrate the new information with citations. Prefer `replace_in_note` / `append_to_note` over rewriting whole pages. Flag contradictions; never silently overwrite.
- No page yet: check the title (per "Page titles"), then create it in `concepts/` or `entities/`.
- Keep `[[wikilinks]]` and `## Related` sections current in both directions.

Then:
- Add every new page to `<Topic> Index` under the right section, one line each: `- [[Title]]: <one-line description>`.
- If the big picture changed, update `<Topic> Overview` (current state and open questions).
- Append an `ingest` line to `<Topic> Log` listing every page touched.

## 5. Report

Tell the user, briefly:
- the wiki used (and whether it was created)
- pages created and pages updated
- any contradictions flagged
- open questions the source raised that the wiki can't answer yet
