# project-notes

A Claude Code plugin that keeps a project's task notes, plans and history in a ZenNotes vault through the `zennotes` MCP server, instead of as files in the repo. Each project gets a folder with a hub note, one note per task and subtask, and plan notes linked from them.

> [!WARNING]
> **Early development (0.x).** The note shape and conventions may change between versions.

## Install

```
/plugin marketplace add ayushnirwal/nirwal-plugins
/plugin install project-notes@nirwal-plugins
```

Requires the `zennotes` MCP server.

## Skill

| Skill | Does |
|---|---|
| `project-notes` | Creates, updates, tidies and closes out task and subtask notes: goal, approach, plan, decisions, open questions, commits, history and token usage per phase. Claude runs it on its own when you say "update the notes", "clean up the notes" or "add this to the task note". |

Project-specific details (vault folder, hub note name, tags) go in the project's `CLAUDE.local.md` or `CLAUDE.md`.

## Token usage

`skills/project-notes/session-usage.py` sums main-thread token usage from a Claude Code transcript, per prompt or for a time window:

```
python3 -I session-usage.py ~/.claude/projects/<project-dir>/<session-id>.jsonl [HH:MM:SS-from HH:MM:SS-to]
```
