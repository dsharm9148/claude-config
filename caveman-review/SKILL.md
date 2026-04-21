---
description: Generate ultra-compressed one-line PR/code review comments. Trigger with /caveman-review or "review this code in caveman style".
user-invocable: true
---

# Caveman Review

One-line code review findings. High signal, zero filler.

**Argument:** `$ARGUMENTS` — code to review, PR diff, or file path.

---

## FORMAT

```
L<line>: <problem>. <fix>.
```

**Severity prefixes (optional):**
- 🔴 bug — broken behavior, will cause incidents
- 🟡 risk — works but fragile (race conditions, null checks, error handling)
- 🔵 nit — style/naming (author can ignore)
- ❓ q — genuine question

---

## RULES

Cut:
- Hedging: "I noticed", "maybe", "perhaps", "you might want to"
- Praise: "Great job on...", "Nice implementation"
- Restating code logic
- Vague suggestions: "refactor this", "consider improving"

Keep:
- Exact line numbers
- Symbol names in backticks
- Concrete fixes
- "Why" when not obvious

---

## EXCEPTIONS

Full explanation for:
- Security vulnerabilities (CVE-class)
- Architectural disagreements
- Onboarding/junior dev contexts

---

## EXAMPLES

Good:
```
L42: 🔴 bug: `user` can be null. Add guard: `if (!user) return null`.
L67: 🟡 risk: no error handling on `fetchData()`. Wrap in try/catch.
L89: 🔵 nit: `getData` → `fetchUserProfile` (clearer intent).
```

Bad:
```
I noticed that on line 42, the user variable might potentially be null in some cases. You might want to consider adding a null check here to prevent potential errors.
```
