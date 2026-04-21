---
description: Create a new Claude Code skill in ~/claude-skills/ (shared by terminal Claude and Cursor). Use when the user wants to add a skill, build a skill, create a new /command, or automate a recurring workflow.
user-invocable: true
---

# New Skill

Creates a skill in `~/claude-skills/<name>/SKILL.md`, making it immediately live for both terminal Claude and Cursor Claude Code.

**Trigger:** `/new-skill [name or description]` or "create a skill for X"

**Architecture reminder:** `~/.claude/skills/` is a symlink → `~/claude-skills/`. Any skill placed there is available globally in all sessions and projects. To make a skill available in one project only, place it in `.claude/skills/<name>/` inside that repo instead.

---

## Step 1 — Extract requirements

From `$ARGUMENTS` or prior conversation, determine:

| Question | Why it matters |
|---|---|
| What does the skill do? | Drives the body content |
| How is it triggered? | Sets the description trigger terms and whether `user-invocable: true` is needed |
| Global or project-only? | Determines file location |
| Does it need scripts, templates, or reference files? | Determines whether to create a `resources/` subdirectory |

If any are unclear, ask before writing.

---

## Step 2 — Choose a name

- Lowercase letters, hyphens only, max 64 chars
- Match the slash command or the natural phrase that invokes it
- Examples: `standup-summary`, `db-migrate`, `pr-checklist`

---

## Step 3 — Write the description

The description is loaded into the system prompt and drives automatic skill detection. Make it specific:

- Third person: "Generates…" not "I will…"
- Include WHAT (capabilities) and WHEN (trigger phrases / scenarios)
- Max 1024 chars

**Good:**
```
Generates a weekly standup summary from Jira tickets and git log. Use when the user asks for a standup, status update, or weekly summary.
```

**Bad:**
```
Helps with standups.
```

---

## Step 4 — Create the files

**Global skill (available everywhere):**
```bash
mkdir -p ~/claude-skills/<name>
# then write ~/claude-skills/<name>/SKILL.md
```

**Project-only skill:**
```bash
mkdir -p .claude/skills/<name>
# then write .claude/skills/<name>/SKILL.md
```

---

## SKILL.md template

```markdown
---
description: <third-person description — WHAT it does and WHEN to use it>
user-invocable: true
---

# <Skill Name>

<One sentence: what this skill produces or does.>

**Trigger:** `/<name> [args]` or "phrase that invokes it"

---

## How it works

<Numbered steps in execution order. Follow actual pipeline order, not logical categories.>

1. Step one
2. Step two
3. Step three

---

## Output

<What the skill produces — file path, format, content summary.>
```

Include `user-invocable: true` only when the skill should respond to an explicit `/name` command. Omit it for skills that trigger automatically from context.

---

## Quality checklist

Before writing the file, verify:

- [ ] Description includes specific WHEN trigger terms (not just WHAT)
- [ ] Body follows execution order, not a logical/category structure
- [ ] Supporting files go in `resources/` — not inlined in SKILL.md
- [ ] SKILL.md stays under 500 lines (use `resources/reference.md` for overflow)
- [ ] No time-sensitive statements ("as of April 2026…")
- [ ] One term per concept — pick it and use it throughout

---

## Step 5 — Verify

```bash
ls ~/claude-skills/<name>/
head -6 ~/claude-skills/<name>/SKILL.md
```

The skill is live in the next Claude session. No restart needed. Test by starting a fresh session and invoking it, or by describing the task it handles.

---

## Adding the skill to a specific project via symlink

If the skill is global but you want it explicitly visible in a project's `.claude/skills/`:

```bash
ln -s ~/claude-skills/<name> <project-root>/.claude/skills/<name>
```

This follows the same pattern used for `frontend-slides` in the current repo.
