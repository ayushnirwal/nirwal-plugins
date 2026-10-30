---
name: ingest
description: Ingest a source (URL, local file, pasted text, or a raw note) into a topic wiki in the ZenNotes vault, updating summary, concept, entity and navigation pages. Creates the wiki if the topic is new (after the user confirms).
argument-hint: "[topic] <url | file path | raw note | pasted text>"
disable-model-invocation: true
---

# Ingest

Input: $ARGUMENTS

If the input is empty, ask the user what to ingest (URL, file path, pasted text or raw note, optionally preceded by a topic) and stop.

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
| URL | See "Fetching URLs" below. |
| Local file | Read it (use the pdf skill for PDFs). |
| Pasted text | Use the text exactly as pasted. |

### Fetching URLs

WebFetch passes pages through a model, so its output can be paraphrased. Prefer an exact copy:

1. **Plain-text version first.** If the content is available as plain text or Markdown, download it with `curl -sSL` into a new, empty temporary directory (the session scratchpad if there is one) and read the file. Examples:
   - GitHub gist `gist.github.com/<user>/<id>` → `https://gist.githubusercontent.com/<user>/<id>/raw`
   - GitHub file `github.com/<o>/<r>/blob/<ref>/<path>` → `https://raw.githubusercontent.com/<o>/<r>/<ref>/<path>`
   - URLs that already point at `.md`, `.txt` or other plain text
   Record `**Captured via:** curl (verbatim)`.
2. **Otherwise WebFetch**, prompting for the full article text verbatim as Markdown (no summarising). If the result says it was truncated, call again with the given `offset` until complete. Record `**Captured via:** WebFetch (may not be verbatim)`.

If a URL is paywalled, blocked (401/403) or returns only a teaser, **stop**: tell the user it couldn't be read and ask them to paste the text. Do not use paywall-bypass mirrors or caches.

### Duplicate check

Before creating anything, `search_by_title` for both `Raw - <short name>` and `Source - <short name>` in this wiki (and check `Origin:` lines for the same URL or file):

- **Raw note exists:** tell the user it was already ingested and ask whether to re-ingest. On re-ingest, reuse the raw note.
- **Source page exists but no raw note** (e.g. ingested before capture worked): capture the raw note now, then rebuild the existing source page in place in step 3. Never create a second source page.

### Create and verify the raw note

1. Create the raw note in `wiki/<slug>/raw/` using the raw note template.
2. Verify it is complete: the `size` returned by `create_note` should equal the captured text's byte size plus the header (title, metadata line, `---` and blank lines). For a downloaded file, compare with `wc -c`. If the difference is more than the header accounts for, `read_note` it, find what was dropped or altered, and fix it with `replace_in_note` / `write_note` before continuing.

## 3. Write the source page

Create `Source - <short name>` in `sources/` from the template: summary, key claims, notable quotes (verbatim, short). Link the raw note. If the duplicate check found an existing source page, read it and rewrite it in place instead, keeping its title so existing links still work.

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
