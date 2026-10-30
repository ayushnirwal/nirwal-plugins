# LLM Wiki conventions

Shared rules for the `ingest`, `query` and `lint` skills. Based on Karpathy's LLM Wiki pattern: an LLM maintains a persistent, interlinked Markdown wiki between the human and their sources, so knowledge compounds instead of being re-retrieved on every query.

These rules are storage-neutral. How to list, read, write and link pages is defined by the active **backend file** (see Setup).

## Setup

Do this before anything else in every skill.

### 1. Load the config

Read `$XDG_CONFIG_HOME/llm-wiki/config.json` (default `~/.config/llm-wiki/config.json`):

```json
{ "backend": "zennotes | obsidian | folder", "root": "<path>", "wikiDir": "wiki" }
```

- `backend`: required.
- `root`: required for `obsidian` and `folder` (absolute path or `~/...`); ignored for `zennotes`.
- `wikiDir`: optional, default `wiki`. Every wiki lives at `<wikiDir>/<slug>/` under the backend's root.

### 2. First run (no config file)

1. Detect what's available:
   - **zennotes:** `mcp__zennotes__*` tools exist (check deferred tools with ToolSearch).
   - **obsidian:** vaults listed in `~/.config/obsidian/obsidian.json` (Linux), `~/Library/Application Support/obsidian/obsidian.json` (macOS) or `%APPDATA%\obsidian\obsidian.json` (Windows), under `vaults.*.path`.
   - **folder:** always available.
2. Ask the user which backend to use (and for `obsidian`, which vault; for `folder`, which directory, suggesting `~/llm-wiki`). Do not pick for them.
3. Show the config you will write, write it after they agree, then continue.

### 3. Load the backend file

Read `backends/<backend>.md` (relative to this file) and follow it for every storage operation. If the config names an unknown backend, or the backend's own checks fail, stop and tell the user why. Never fall back to a different backend.

## Layout

Every research topic is its own wiki under `<wikiDir>/<slug>/` (slug: lowercase, hyphenated, e.g. `llm-knowledge-bases`). `<Topic>` below is the wiki's display name in Title Case (e.g. "LLM Knowledge Bases").

| Path | Owner | Purpose |
|---|---|---|
| `raw/` | Human | Full, unmodified source documents. **Never edit or delete anything here.** |
| `sources/` | Agent | One summary page per raw source, titled `Source - <short name>` |
| `concepts/` | Agent | Ideas, techniques, patterns |
| `entities/` | Agent | People, organisations, tools, products, projects |
| `answers/` | Agent | Saved answers to queries |
| `<Topic> Index` | Agent | Catalog of every page, one line each. Read first on every query. |
| `<Topic> Log` | Agent | Append-only change history |
| `<Topic> Overview` | Agent | Top-level synthesis of what the wiki knows, plus open questions |
| `<Topic> Schema` | Human + agent | This wiki's own preferences. Overrides these conventions where they conflict. |

The four navigation pages sit directly in `<wikiDir>/<slug>/`.

## Finding the wiki for a topic

1. List existing wikis (the direct subfolders of `<wikiDir>/`). For each, read its `<Topic> Overview` if you need more than the name.
2. **Exact match** (same slug or display name, ignoring case and spacing): use it.
3. **Close match** (synonym, broader/narrower topic, overlapping Overview): ask the user "Use the existing *X* wiki, or create a new one?" and wait.
4. **No match:** propose a display name and slug and wait for the user's OK. Only `ingest` may create a wiki; `query` and `lint` report that no such wiki exists.

### Creating a wiki
Create the five folders and the four navigation pages. Templates:

- **Schema:** `# <Topic> Schema`, one line on what the wiki covers, then `## Preferences` with `_None yet._` and `## Related` linking the Index.
- **Index:** `# <Topic> Index`, one line linking the Schema, then sections `## Navigation` (Overview, Schema, Log), `## Concepts`, `## Entities`, `## Sources`, `## Answers`, each `_None yet._` until filled.
- **Log:** `# <Topic> Log`, the line `Append-only. One entry per line.`, then a blank line and the first entry `- YYYY-MM-DD | create | wiki created`.
- **Overview:** `# <Topic> Overview`, `## Current state` (one line: just created), `## Open questions`, `## Related`.

## Links

Below, "link to *Page*" means a link in the backend's link syntax (see the backend file). `[[Page]]` in templates is shorthand for that.

- First mention of any concept or entity that has a page in this wiki becomes a link. If a mention matters and has no page, create a short stub rather than leave it unlinked.
- Every factual claim cites its source page inline: `([[Source - Foo]])`.

## Page titles

A page's title is its H1 and its file or note name. Titles must be unique across the whole backend root (not just the wiki), because some backends resolve links by title.

- Use plain Title Case noun phrases: `Docker`, `RAID 5`, `Andrej Karpathy`.
- Before creating a page, look for an existing page with that exact title. If it exists **in this wiki**, update it instead. If it exists **elsewhere**, title the new page `<Title> (<Topic>)` and display it as `<Title>` where the link syntax allows.
- Never share one page between two wikis.

## Page conventions

- First line after the H1: one sentence saying what the thing is.
- **Never silently overwrite** a claim that a new source contradicts. Keep both, and add:
  ```
  > [!warning] Contradiction
  > [[Source - A]] says X; [[Source - B]] says Y.
  ```
- End every non-trivial page with `## Related`.
- At most two tags per page; folders already classify.
- Use Mermaid for diagrams and LaTeX (`$...$`) for formulas. No ASCII art.

### Source pages
```
# Source - <short name>

**Origin:** <URL or file> · **Author:** <name> · **Date:** <published date> · **Raw:** [[<raw page title>]]

<one sentence: what this source is>

## Summary
## Key claims
## Notable quotes
## Related
```

### Raw pages
Title: `Raw - <short name>`. Body:
```
# Raw - <short name>

**Origin:** <URL, file path, or "pasted in chat"> · **Author:** <name or unknown> · **Published:** <date> · **Captured:** <today> · **Captured via:** <curl (verbatim) | WebFetch (may not be verbatim) | file | pasted>

---

<full source text, unmodified>
```

## Dates

Write a published date only if it comes from the source itself (its text, byline or the page's own metadata). Otherwise write `unknown`, or `<date> (unverified, from <where>)` if a secondary source gives one. Never present a guessed or summarised date as fact, on raw pages, source pages or anywhere else.

## Log entries

Append one line per operation to `<Topic> Log`:

```
- YYYY-MM-DD | ingest | [[Source - X]] | touched: [[Page A]], [[Page B]], ...
- YYYY-MM-DD | query  | [[Answer page]] or "not saved" | <question>
- YYYY-MM-DD | lint   | fixed <n> | open: <short list or "none">
- YYYY-MM-DD | schema | <what changed>
```

Never edit or reorder earlier lines.

## Showing pages to the user

When listing pages in chat, give each page's title plus whatever the backend file says to show (a clickable link, or a file path).
