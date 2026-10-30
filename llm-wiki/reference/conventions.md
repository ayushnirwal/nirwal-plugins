# LLM Wiki conventions

Shared rules for the `ingest`, `query` and `lint` skills. Based on Karpathy's LLM Wiki pattern: an LLM maintains a persistent, interlinked Markdown wiki between the human and their sources, so knowledge compounds instead of being re-retrieved on every query.

## Backend

All wikis live in the user's ZenNotes vault and are read and written **only** through the `zennotes` MCP tools (`mcp__zennotes__*`).

- If no `mcp__zennotes__*` tools are available (not even as deferred tools to load), stop and tell the user: "The zennotes MCP server isn't connected, so llm-wiki can't reach the vault." Never fall back to writing files on disk.
- Load deferred zennotes tools with ToolSearch before calling them.
- Always use the `path` returned by zennotes tools verbatim. The vault runs in root mode, so wiki paths look like `wiki/<slug>/...` with no `inbox/` prefix. In `create_note` / `create_folder`, pass `folder: "inbox"` and `subpath: "wiki/<slug>/..."`.
- When showing notes to the user, render titles as `[Title](<link>)` using the note's `link` field if the tool returned one; otherwise give the vault path.

## Layout

Every research topic is its own wiki under `wiki/<slug>/` (slug: lowercase, hyphenated, e.g. `llm-knowledge-bases`). `<Topic>` below is the wiki's display name in Title Case (e.g. "LLM Knowledge Bases").

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

The four navigation notes sit directly in `wiki/<slug>/`.

## Finding the wiki for a topic

1. List existing wikis: `list_folders` and take the direct children of `wiki/`. For each, read its `<Topic> Overview` if you need more than the name.
2. **Exact match** (same slug or display name, ignoring case and spacing): use it.
3. **Close match** (synonym, broader/narrower topic, overlapping Overview): ask the user "Use the existing *X* wiki, or create a new one?" and wait.
4. **No match:** propose a display name and slug and wait for the user's OK. Only `ingest` may create a wiki; `query` and `lint` report that no such wiki exists.

### Creating a wiki
Create the five folders and the four navigation notes. Templates:

- **Schema:** `# <Topic> Schema`, one line on what the wiki covers, then `## Preferences` with `_None yet._` and `## Related` linking the Index.
- **Index:** `# <Topic> Index`, one line pointing at the Schema, then sections `## Navigation` (Overview, Schema, Log), `## Concepts`, `## Entities`, `## Sources`, `## Answers`, each `_None yet._` until filled.
- **Log:** `# <Topic> Log`, the line `Append-only. One entry per line.`, then a blank line and the first entry `- YYYY-MM-DD | create | wiki created`.
- **Overview:** `# <Topic> Overview`, `## Current state` (one line: just created), `## Open questions`, `## Related`.

## Page titles

ZenNotes resolves `[[wikilinks]]` by title across the whole vault, so titles must be vault-unique.

- Use plain Title Case noun phrases: `Docker`, `RAID 5`, `Andrej Karpathy`.
- Before creating a page, `search_by_title` for the exact title. If a note with that title exists **in this wiki**, update it instead. If it exists **elsewhere** in the vault, title the new page `<Title> (<Topic>)` and link to it with `[[<Title> (<Topic>)|<Title>]]`.
- Never share one page between two wikis.

## Page conventions

- First line after the H1: one sentence saying what the thing is.
- First mention of any concept or entity that has a page in this wiki becomes a `[[wikilink]]`. If a mention matters and has no page, create a short stub rather than leave it unlinked.
- Every factual claim cites its source page inline: `([[Source - Foo]])`.
- **Never silently overwrite** a claim that a new source contradicts. Keep both, and add:
  ```
  > [!warning] Contradiction
  > [[Source - A]] says X; [[Source - B]] says Y.
  ```
- End every non-trivial page with `## Related`.
- At most two tags per page; folders already classify.
- Use ZenNotes' native renderers (Mermaid, KaTeX, etc.) for any diagram or formula. No ASCII art.

### Source pages
```
# Source - <short name>

**Origin:** <URL or raw note link> · **Author:** <name> · **Date:** <published date> · **Raw:** [[<raw note title>]]

<one sentence: what this source is>

## Summary
## Key claims
## Notable quotes
## Related
```

### Raw notes
Title: `Raw - <short name>`. Body:
```
# Raw - <short name>

**Origin:** <URL, file path, or "pasted in chat"> · **Author:** <name or unknown> · **Published:** <date or unknown> · **Captured:** <today>

---

<full source text, unmodified>
```

## Log entries

Append one line per operation with `append_to_note` on `<Topic> Log`:

```
- YYYY-MM-DD | ingest | [[Source - X]] | touched: [[Page A]], [[Page B]], ...
- YYYY-MM-DD | query  | [[Answer page]] or "not saved" | <question>
- YYYY-MM-DD | lint   | fixed <n> | open: <short list or "none">
- YYYY-MM-DD | schema | <what changed>
```

Never edit or reorder earlier lines.
