# llm-wiki

A Claude Code plugin implementing Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Claude builds and maintains an interlinked Markdown wiki per research topic from sources you curate, so knowledge compounds instead of being re-retrieved on every question.

> [!WARNING]
> **Early development (0.x).** The wiki layout, page conventions and `config.json` format may change between versions, and a wiki made by an older version may need a `/llm-wiki:lint` pass or manual fixes afterwards. Keep your wiki under version control or backed up.

## Install

```
/plugin marketplace add ayushnirwal/nirwal-plugins
/plugin install llm-wiki@nirwal-plugins
```

## Commands

| Command | Does |
|---|---|
| `/llm-wiki:ingest [topic] <url \| file \| raw page \| text>` | Saves the full source to `raw/`, writes a source page, updates concept/entity pages, index, overview and log. Creates the wiki (after confirming) if the topic is new. |
| `/llm-wiki:query [topic] <question>` | Answers from the wiki with citations; saves reusable answers to `answers/`. Claude may also run it on its own, read-only. |
| `/llm-wiki:lint <topic>` | Fixes mechanical issues (index, reciprocal links, moved-page links) and reports the rest as a checklist. |

## Backends

| Backend | Storage | Links |
|---|---|---|
| `zennotes` | A ZenNotes vault, through the `zennotes` MCP server | `[[wikilinks]]` |
| `obsidian` | An Obsidian vault on disk (Obsidian needn't be running) | `[[wikilinks]]`, or Markdown links if the vault prefers them |
| `folder` | Any directory of Markdown files, e.g. a git repo | Relative Markdown links |

## Setup

The first command you run detects the available backends, asks which to use, and writes `~/.config/llm-wiki/config.json`:

```json
{ "backend": "obsidian", "root": "~/Documents/Vault", "wikiDir": "wiki" }
```

`root` is required for `obsidian` and `folder`. `wikiDir` defaults to `wiki`; each topic lives in `<wikiDir>/<topic-slug>/`.

## Layout of a wiki

```
wiki/<topic-slug>/
  raw/        full, unmodified sources (never edited by Claude)
  sources/    one summary page per source
  concepts/   ideas, techniques, patterns
  entities/   people, organisations, tools
  answers/    saved query answers
  <Topic> Index · <Topic> Log · <Topic> Overview · <Topic> Schema
```

Shared rules live in `reference/conventions.md`, per-backend instructions in `reference/backends/`, and per-wiki preferences in each wiki's `<Topic> Schema` page.

## Credits

The wiki pattern this plugin implements comes from Andrej Karpathy's gist [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). This plugin is an independent implementation; any mistakes are its own.
