# Backend: obsidian

Wikis live in an Obsidian vault on disk (`root` in the config) and are read and written with ordinary file tools (Read, Write, Edit, Glob, Grep). Obsidian does not need to be running; it picks up changes on disk.

## Checks

- `root` must exist and contain a `.obsidian/` directory. If not, stop: "`<root>` isn't an Obsidian vault (no .obsidian/ folder)."
- Never touch `.obsidian/`, `.trash/` or anything outside `<root>/<wikiDir>/`, except reading `.obsidian/app.json` (below) and checking titles vault-wide.
- Read `.obsidian/app.json` if present:
  - `attachmentFolderPath`: where images and other attachments go. If unset or `/`, use `<root>/<wikiDir>/<slug>/raw/assets/`.
  - `useMarkdownLinks: true` means the user prefers `[Title](path.md)` links; follow the folder backend's link rules instead of wikilinks.

## Files

- A page is `<Title>.md` in its folder; the H1 repeats the title.
- File names may not contain `* " \ / < > : | ? # ^ [ ]`. Replace them with `-` in the file name; keep the original in the H1.
- Pages may start with YAML frontmatter. Add it to wiki pages so Dataview can query them:
  ```yaml
  ---
  wiki: <slug>
  type: source | concept | entity | answer | raw | index | log | overview | schema
  ---
  ```
  Never add or change frontmatter in `raw/` pages after creating them.

## Operations

| Operation | How |
|---|---|
| List wikis | Directories directly under `<root>/<wikiDir>/`. |
| List a wiki's pages | Glob `<root>/<wikiDir>/<slug>/**/*.md`. |
| Find a page by title | Glob `<root>/**/<Title>.md` (whole vault, since links resolve vault-wide). |
| Read | Read. |
| Create | Write the file (create parent directories as needed). |
| Create an empty folder | `mkdir -p`. |
| Append | Edit to add after the last line, or append with a shell heredoc. |
| Edit part of a page | Edit. |
| Rewrite a page | Read, then Write. |
| Search text | Grep within `<root>/<wikiDir>/<slug>/`. |
| Backlinks | Grep the vault for `[[<Title>]]`, `[[<Title>|` and `[[<Title>#`. |
| Move / rename | `mv`, then update every backlink found by Grep. |

## Links

`[[Title]]`, resolved by title across the vault. Use `[[Title (Topic)|Title]]` for disambiguated titles. Callouts (`> [!warning]`) render natively.

## Verifying a write

Compare `wc -c < <file>` with the expected byte length.

## Temporary files

Downloads go in a new, empty directory under the session scratchpad or the system temp dir, never inside the vault.

## Showing pages to the user

Give the title and the file path relative to `root`. Optionally add an `obsidian://open?vault=<vault name>&file=<url-encoded path without .md>` link.
