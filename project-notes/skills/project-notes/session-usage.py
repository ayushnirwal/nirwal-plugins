#!/usr/bin/env python3
"""Main-thread token usage from Claude Code session transcripts.

Usage:
  session-usage.py <session.jsonl>                      per user prompt, to pick task boundaries
  session-usage.py <session.jsonl> <from> [<to>]        totals for a UTC time window, HH:MM:SS

Transcripts live in ~/.claude/projects/<project-dir>/<session-id>.jsonl. Each model response is counted once
(by message id). Total = input + cache write + cache read + output.
"""
import json
import sys

KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def prompt_text(message):
    content = message.get("content")
    if isinstance(content, str):
        return content
    return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")


def is_user_prompt(record):
    message = record.get("message")
    if record.get("type") != "user" or not isinstance(message, dict) or record.get("isMeta"):
        return False
    text = prompt_text(message)
    return bool(text) and not text.startswith(("<system-reminder>", "<task-notification", "<local-command"))


def blank(label, at):
    return {"label": label, "at": at, "turns": 0, "tools": 0, "first": None, "last": None, **{k: 0 for k in KEYS}}


def add(row, record, seen):
    message = record["message"]
    if isinstance(message.get("content"), list):
        row["tools"] += sum(1 for b in message["content"] if b.get("type") == "tool_use")
    if message.get("id") in seen:
        return
    seen.add(message.get("id"))
    row["turns"] += 1
    row["first"] = row["first"] or record["timestamp"][11:19]
    row["last"] = record["timestamp"][11:19]
    for k in KEYS:
        row[k] += message["usage"].get(k, 0)


def show(row):
    total = sum(row[k] for k in KEYS)
    print(
        f"{row['first']}-{row['last']} turns={row['turns']} tools={row['tools']} in={row['input_tokens']} "
        f"cw={row['cache_creation_input_tokens']} cr={row['cache_read_input_tokens']} out={row['output_tokens']} "
        f"total={total} | {row['label']}"
    )


def main():
    path, window = sys.argv[1], sys.argv[2:]
    start, end = (window + ["99:99:99"])[:2] if window else (None, None)
    rows, seen = ([blank("window", start)] if window else []), set()
    for line in open(path):
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if not window and is_user_prompt(record):
            rows.append(blank(prompt_text(record["message"])[:80].replace("\n", " "), record.get("timestamp")))
        message = record.get("message")
        if record.get("type") != "assistant" or not isinstance(message, dict) or not message.get("usage") or not rows:
            continue
        if window and not (start <= record.get("timestamp", "")[11:19] < end):
            continue
        add(rows[-1], record, seen)
    for row in rows:
        if row["turns"]:
            show(row)


main()
