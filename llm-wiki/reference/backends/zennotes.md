# Backend: zennotes

Wikis live in a ZenNotes vault and are read and written **only** through the `zennotes` MCP tools (`mcp__zennotes__*`). Never write vault files directly on disk, even if the vault is local.

## Checks

- If no `mcp__zennotes__*` tools are available (not even as deferred tools), stop: "The zennotes MCP server isn't connected, so llm-wiki can't reach the vault."
- Load deferred zennotes tools with ToolSearch before calling them.
- Call `vault_info` once per session. It reports `primaryNotesLocation`:
  - `root`: notes in the conceptual inbox live at the vault root, so wiki paths look like `<wikiDir>/<slug>/...`.
  - `inbox`: they live under `inbox/`, so paths look like `inbox/<wikiDir>/<slug>/...`.
- Either way, when creating notes or folders pass `folder: "inbox"` and `subpath: "<wikiDir>/<slug>/<subfolder>"`; the server maps it.
- Always pass back the `path` a tool returned, verbatim. Never build paths yourself.

## Operations

| Operation | How |
|---|---|
| List wikis | `list_folders`; the wikis are the direct children of `<wikiDir>` under `inbox`. |
| List a wiki's pages | See "Listing pages" below. |
| Find a page by title | `search_by_title` with the exact title; check `title` equality and that `path` is in this wiki. |
| Read | `read_note`. |
| Create | `create_note` with `folder: "inbox"`, `subpath`, `title`, `body`. Missing parent folders are created. |
| Create an empty folder | `create_folder` with `folder: "inbox"`, `subpath`. |
| Append | `append_to_note`. |
| Edit part of a page | `replace_in_note` (literal find/replace). |
| Rewrite a page | `read_note` first, then `write_note`. |
| Search text | `search_text`, then keep results whose `path` is in this wiki. |
| Backlinks | `backlinks` with the page's `path`. |
| Move / rename | `move_note` / `rename_note`; check `backlinks` first. |

### Listing pages

`list_notes` with `subpath` returns nothing on some ZenNotes servers (upstream bug). Until that is fixed:

1. Call `list_notes` with `folder: "inbox"`, no `subpath`, and `limit: 5000`.
2. If the number of results equals the limit, call again with a higher limit; never work from a capped list.
3. Keep only notes whose `path` is inside `<wikiDir>/<slug>/` (allowing for the `inbox/` prefix in inbox mode). The subfolder is the next path segment.

Each result includes `title`, `wikilinks` and timestamps, so one call is enough for a whole-wiki survey.

## Links

`[[Title]]`, resolved by title across the vault. Use `[[Title (Topic)|Title]]` for disambiguated titles.

## Verifying a write

`create_note` and `write_note` return `size` (bytes). Compare it with the expected byte length of the body.

## Temporary files

Downloads (e.g. `curl` during ingest) go in a new, empty directory under the session scratchpad or the system temp dir, never inside the vault.

## Showing pages to the user

Note results may carry a `link` field (`zennotes://...`). If present, render the title as `[Title](<link>)`; otherwise give the `path`.
