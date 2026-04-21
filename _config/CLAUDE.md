# Global Claude Rules

## Skills Bootstrap

Skills live in `~/.claude/skills/`. Config is backed up at `https://github.com/dsharm9148/claude-config`.

**If any expected skill is missing** (write-chat, write-docs, write-pr, caveman, new-skill, career-ops, etc.), run this to restore:
```bash
git clone https://github.com/dsharm9148/claude-config /tmp/cc && bash /tmp/cc/setup.sh && rm -rf /tmp/cc
```

**To keep in sync on this machine:**
```bash
cd ~/.claude && git pull
```

## Writing Style Rules

For every output, apply exactly one of these three styles based on what is being written:

| Style | When to use |
|-------|-------------|
| **write-docs** | Writing to a file: `.md` docs, README, specs, reports, result files, runbooks, architecture docs |
| **write-pr** | PR titles/descriptions, PR review comments, responses to review feedback, anything posted to GitHub |
| **write-chat** | All conversational responses to the user in the chat interface |

Default to **write-chat** when the context is ambiguous. Never mix styles in a single output. If writing a file AND explaining it to the user, use write-docs for the file content and write-chat for the explanation.

---

## Permission Rules

**Always ask user before:**
- `git push` (any variant: force push, push --force, push origin, etc.)
- `rm` commands (any file/directory deletion)
- `git branch -D` or `git branch -d` (branch deletion)
- Dropping databases, tables, or collections
- Any destructive or irreversible operation

Even if the user previously approved a similar action, confirm each time.
