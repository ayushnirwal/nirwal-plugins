---
name: project-notes
description: Keep a project's task notes, plans and history in the ZenNotes vault (zennotes MCP). Use when creating, updating, tidying or closing out a task or subtask note, recording a decision, commit or agent token usage, or when the user says "update the notes", "clean up the notes" or "add this to the task note".
---

# Project notes in ZenNotes

Projects keep their notes, tasks and plans in the ZenNotes vault (zennotes MCP), not as files in the repo. The notes
are the project's history: someone reading them later should see what the task is, where it stands, what was
decided and why, without reading the chat.

Project-specific details (vault folder, hub note name, tags) come from the project's `CLAUDE.local.md` or
`CLAUDE.md`. If none are given, use a folder named after the repo and ask before creating a hub.

## Layout

- **One folder per project**, e.g. `next-pms/`. Always reuse the `path` the zennotes tools return; never build one.
- **Hub note** `<folder>/<project>.md`: links, a `## Tasks` list (each task, with subtasks nested under it, and
  its status), guides, other work.
- **One note per task and per subtask.** Title it as the user named it.
- **Plans** live in the vault as `<Task> plan.md`, linked from the task note. Never write plan files into the repo.

## Shape of a task note

```markdown
---
completed_pr: <PR URL, once merged>
completed_commit: <merge commit, or commit range without a PR>
planning_tokens: 0 MTok
executing_tokens: 0 MTok
post_executing_tokens: 0 MTok
---

# <Task>

#<project> #<topic>

Part of [[<parent>]] · Project: [[<project>]] · Status: **planning | in progress | done**

<one or two lines of context>

## Goal
## Pattern / Approach      (how the work is done; conventions learned along the way)
## Inventory / Plan        (the work items, often a table with status and commit per row)
## Decisions               (- YYYY-MM-DD — decision, and why in one clause)
## Open questions
## Next                    (checklist; tick with commit hashes)
## Commits
## History                 (- YYYY-MM-DD — one or two lines per working session)
## Token usage
```

No `## Related` section: when a note relates to another, link it with `[[…]]` where the content mentions it.
Leave out sections the task doesn't need. Keep the section order, and use the same headings across a project's notes.

## How to update

- **Update in place.** Fold new work into the sections that already exist: add a row to the inventory, a line to
  Decisions, items to Open questions, a tick to Next, a hash to Commits, a row to Token usage. Don't append a new
  "Update — <date>" section for each chunk of work. The only running log is the short `## History` list.
- **Write notes, not chat.** Use terse, impersonal note text. Not "I compared the Storybooks and found…" or "the
  user spotted…", but "Second review (React vs Vue Storybook) found DurationInput missing". No greetings, no
  "next I'll…", no questions to the reader except under Open questions.
- **Keep history without bloat.** Don't delete facts when tidying; merge them. Superseded items get ticked or
  struck through, not removed (open questions are the exception, below).
- **Only unanswered questions stay under Open questions.** When one is answered, delete it from that list and add
  the answer to Decisions (`- YYYY-MM-DD — answer, and why`). Don't strike it through or tick it in place, and drop
  the section once it's empty. The same question often appears in the parent task, its plan or sibling notes:
  search the project folder (`search_text`) and clear it everywhere, pointing to the note where it was decided.
  Also fix plan text that still offers the rejected option.
- **Tick with evidence.** `- [x] Port Filter — 971f2d9a`. Check that every hash exists (`git cat-file -t <hash>`).
- **Status everywhere.** When a task's status changes, update the task note, its parent's subtask list and the
  hub's `## Tasks` list together. Finished tasks become **done**; never delete them.
- **When to update.** At the end of each meaningful chunk of work: a commit, a decision, a plan change, or an agent
  finishing.

## Token usage

Every task records what it cost as three totals, whether or not subagents ran. Nothing else: no per-agent or
per-session rows, no turns or tool calls.

- **Phases:**
  - **Planning** — grilling, inventory / explore agents, writing and approving the plan, `/start-task`.
  - **Executing** — building the steps: code, checks, commits, build agents.
  - **Post-executing** — reviews and their fixes, UI parity runs, rebases, PRs and merges, closing notes.
- **Tokens** per phase = agents (from their completion notifications) + main thread (input + cache write + cache
  read + output). Main-thread spans come from `session-usage.py` in this skill's folder:
  `python3 -I <this skill's base directory>/session-usage.py <transcript.jsonl> [HH:MM:SS-from HH:MM:SS-to]`.
  Transcripts are `~/.claude/projects/<project-dir>/<session-id>.jsonl`; run it without a window first to list the
  prompts and pick the task's spans. Add new usage to the phase's existing value.
- **Section:**
  ```markdown
  ## Token usage
  | Phase | Tokens |
  |---|---|
  | Planning | 4.1 MTok |
  | Executing | 31 MTok |
  | Post-executing | 2.0 MTok |
  ```
  Add one line under the table only for a gap (e.g. an agent that never reported usage).
- **Frontmatter:** `planning_tokens`, `executing_tokens`, `post_executing_tokens`, the same values as the table.
  In millions as `<n> MTok`: whole numbers from 10M up, one decimal from 1M, two decimals below 1M (`143 MTok`,
  `1.9 MTok`, `0.07 MTok`).
- **A parent task's values** are the sum of its subtasks' plus any usage run directly for it. Update it too.

## Tidying a messy note

1. Read the whole note and every note it links to.
2. Check the commits it cites against the repo.
3. Rewrite it into the shape above with `write_note`, keeping the frontmatter. Merge appended update sections into
   the matching sections. Turn chat-voice paragraphs into note lines. Fold duplicated tables into one.
   Move answered open questions to Decisions and remove them from the list.
4. Report what moved where in a few lines, with the note's `zennotes://` link.
