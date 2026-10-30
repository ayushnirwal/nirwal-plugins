# Backend: folder

Wikis live in a plain directory of Markdown files (`root` in the config) and are read and written with ordinary file tools (Read, Write, Edit, Glob, Grep). The output should read well in any Markdown viewer: GitHub, VS Code, a static site generator.

## Checks

- If `root` doesn't exist, ask the user whether to create it. Don't create it silently.
- Never touch anything outside `<root>/<wikiDir>/`.

## Files

- A page is `<Title>.md` in its folder; the H1 repeats the title.
- File names may not contain `* " \ / < > : | ? # ^ [ ]`. Replace them with `-` in the file name; keep the original in the H1.
- No frontmatter is required.

## Operations

| Operation | How |
|---|---|
| List wikis | Directories directly under `<root>/<wikiDir>/`. |
| List a wiki's pages | Glob `<root>/<wikiDir>/<slug>/**/*.md`. |
| Find a page by title | Glob `<root>/<wikiDir>/**/<Title>.md`. |
| Read | Read. |
| Create | Write the file (create parent directories as needed). |
| Create an empty folder | `mkdir -p`, plus a `.gitkeep` so git keeps it. |
| Append | Edit to add after the last line, or append with a shell heredoc. |
| Edit part of a page | Edit. |
| Rewrite a page | Read, then Write. |
| Search text | Grep within `<root>/<wikiDir>/<slug>/`. |
| Backlinks | Grep the wiki for `](<...>/<file name>.md)` with the page's file name URL-encoded (spaces as `%20`). |
| Move / rename | `mv`, then update every link to it found by Grep. |

## Links

Standard relative Markdown links, from the linking page's folder to the target file, with spaces encoded as `%20`:

- From `concepts/LLM Wiki Pattern.md` to `entities/Andrej Karpathy.md`: `[Andrej Karpathy](../entities/Andrej%20Karpathy.md)`
- From a navigation page to `concepts/Memex.md`: `[Memex](concepts/Memex.md)`

Wherever the conventions write `[[Page]]`, use this form. A link is **broken** if its target file doesn't exist; lint checks this by resolving the path.

Callouts (`> [!warning]`) render on GitHub and degrade to plain blockquotes elsewhere, so keep using them.

## Verifying a write

Compare `wc -c < <file>` with the expected byte length.

## Temporary files

Downloads go in a new, empty directory under the session scratchpad or the system temp dir, never inside `root`.

## Showing pages to the user

Give the title and the file path relative to `root`.
