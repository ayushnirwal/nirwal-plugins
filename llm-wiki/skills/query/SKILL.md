---
name: query
description: Answer a question from the user's LLM-maintained topic wikis, with citations to wiki pages. Use when the user asks what they know, have read or have researched about a topic that may be covered by one of their wikis, or runs /llm-wiki:query.
argument-hint: "[topic] <question>"
---

# Query

Input: $ARGUMENTS

First read `../../reference/conventions.md` (relative to this skill's base directory) and do its Setup (config, then backend file). Every storage operation below is done the way the backend file says. If there is no config yet and you were invoked on your own (not typed by the user), don't run first-run setup: just answer normally without the wiki.

## Write permission

- **Typed by the user** (the input arrived via `/llm-wiki:query`): you may save the answer back into the wiki (step 4).
- **Invoked on your own** because the conversation fit: **read only**. Do not create, edit or log anything.

## 1. Pick the wiki

- If a topic is given, find its wiki per "Finding the wiki for a topic". Never create one; if none exists, say so and suggest `/llm-wiki:ingest`.
- If not, list the wikis, read each `<Topic> Overview`, and use the best match. If several are relevant, search them all. If it's unclear, ask.

## 2. Gather

1. Read the wiki's `<Topic> Schema` and `<Topic> Index`.
2. Read the pages the Index points to. Follow links as far as the question needs.
3. Only if the Index isn't enough, search the wiki's text.
4. Go to `raw/` only to check an exact quote or detail a source page lacks.

## 3. Answer

- Answer from the wiki, citing wiki pages inline (shown per the backend's "Showing pages to the user").
- Say clearly where the wiki is silent or its sources disagree. You may add outside knowledge only if you label it as not from the wiki.

## 4. Save back (typed invocation only)

If the answer is a reusable synthesis (comparison, explanation, decision, connection between pages), not a one-line fact lookup:

1. Create a page in `answers/` titled after the question's subject (per "Page titles"), with the question, the answer, and citations.
2. Link it from the most relevant concept/entity pages' `## Related`.
3. Add it to `<Topic> Index` under `## Answers`.
4. Append a `query` line to `<Topic> Log`.
5. Tell the user it was saved.

Otherwise, append a `query` line with `not saved`.
