# llm-wiki

Private Claude Code plugin implementing Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) on top of a ZenNotes vault. Each research topic gets its own wiki under `wiki/<topic>/`, which the LLM writes and maintains from sources you curate.

## Commands

| Command | Does |
|---|---|
| `/llm-wiki:ingest [topic] <url \| file \| raw note \| text>` | Saves the full source to `raw/`, writes a source page, updates concept/entity pages, index, overview and log. Creates the wiki (after confirming) if the topic is new. |
| `/llm-wiki:query [topic] <question>` | Answers from the wiki with citations; saves reusable answers to `answers/`. Claude may also run it on its own, read-only. |
| `/llm-wiki:lint <topic>` | Fixes mechanical issues (index, reciprocal links, renamed-page links) and reports the rest as a checklist. |

## Setup

Requires the `zennotes` MCP server to be connected. Shared rules live in `reference/conventions.md`; per-wiki preferences go in each wiki's `<Topic> Schema` note.
