---
description: Generate terse commit messages in Conventional Commits format (≤50 chars). Trigger with /caveman-commit, /commit, or "write a commit message".
user-invocable: true
---

# Caveman Commit

Generate ultra-compressed commit messages. Conventional Commits format. No fluff.

**Argument:** `$ARGUMENTS` — optional diff/context. If absent, analyze staged changes or ask.

---

## FORMAT

```
<type>(<scope>): <summary>

[optional body — only if "why" isn't obvious]
```

**Subject:** ≤50 chars (hard cap 72). Imperative mood. No period.

**Types:** feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert

---

## RULES

Include body only for:
- Non-obvious reasoning
- Breaking changes (`BREAKING CHANGE:` prefix)
- Data migrations or security fixes
- Issue refs (`Closes #42`)

Never include:
- "This commit does X"
- First-person pronouns
- AI attribution ("Claude generated")
- Emoji (unless project uses them)
- Restate scope in summary

---

## EXAMPLES

Good:
```
feat(auth): add JWT refresh token rotation
```

```
fix(api): handle null user in session middleware

Closes #234
```

Bad:
```
updated some files and fixed stuff
```

```
I added the new feature that was requested by the user to improve the authentication flow
```

---

## OUTPUT

Produce formatted commit message block ready to paste. Do NOT execute git commands unless explicitly asked.
