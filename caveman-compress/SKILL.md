---
description: Compress markdown/text files into caveman-speak to reduce input tokens by ~46% per session. Preserves code, URLs, and commands. Trigger with /caveman:compress <filepath>.
user-invocable: true
---

# Caveman Compress

Compress natural language in markdown/text files to caveman-speak. Reduces input tokens ~46%. Code and technical content untouched.

**Argument:** `$ARGUMENTS` — file path to compress. Required.

---

## PROCESS

1. Read target file
2. Create backup: `<filename>.original.md`
3. Compress prose sections
4. Write compressed version to original path
5. Report: original size, compressed size, % reduction

---

## COMPRESSION RULES

Remove from prose:
- Articles: a, an, the
- Filler: just, really, basically, simply, quite, very, actually, essentially
- Hedging: I think, perhaps, maybe, it seems, might be
- Pleasantries and transitions
- Verbose constructions: "in order to" → "to", "due to the fact that" → "because"

Use fragments: "Run tests before commit" not "You should always run tests before committing."

---

## PRESERVATION RULES (NEVER COMPRESS)

- Code blocks (``` fenced and indented)
- Inline code (`backtick`)
- URLs and file paths
- Shell commands
- Technical terms and proper nouns
- Markdown structure: headings, lists, tables, links

---

## SCOPE

Only handles: `.md`, `.txt`, extensionless files

Skips: `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.yml` and all code files

---

## OUTPUT FORMAT

```
Compressed: <filepath>
Backup: <filepath>.original.md
Before: ~<N> tokens
After:  ~<N> tokens
Saved:  ~<N>% reduction
```
