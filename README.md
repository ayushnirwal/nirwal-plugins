# nirwal-plugins

A Claude Code plugin marketplace.

> [!WARNING]
> **Early development.** These plugins are experimental and change often. Commands, file layouts and config formats may change between versions without a migration path. Expect rough edges, and please open an issue if something breaks.

## Plugins

| Plugin | Version | Description |
|---|---|---|
| [llm-wiki](llm-wiki/) | 0.3.0 | Karpathy-style LLM wikis per research topic, with ingest, query and lint commands. Works with ZenNotes, Obsidian or a plain folder. |
| [project-notes](project-notes/) | 0.1.0 | Keep a project's task notes, plans, decisions, commits and token usage in a ZenNotes vault, one note per task and subtask under a project hub. |

## Install

```
/plugin marketplace add ayushnirwal/nirwal-plugins
/plugin install llm-wiki@nirwal-plugins
/plugin install project-notes@nirwal-plugins
```

To pick up new versions, run `/plugin marketplace update nirwal-plugins`.

## Credits

- **llm-wiki** implements Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.

## License

[MIT](LICENSE)
