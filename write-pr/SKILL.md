---
description: Writing style for PRs, PR descriptions, PR reviews, and review responses on GitHub. Always use the WHOOP PR template. Minimum words, link to commits or code locations. No pleasantries.
user-invocable: true
---

# Write PR Style

Apply this style for: PR titles, PR descriptions, PR review comments, responses to review feedback, commit messages.

---

## PR TITLES

Format: `[TICKET-ID] Verb phrase describing the change`

Rules:
- If a Jira/Linear ticket exists, prefix with `[TICKET-ID]` — e.g. `[RAA-9] Add generate-coding-standards skill`
- If no ticket, omit the brackets entirely — e.g. `Add writing-style plugin`
- Sentence case: capitalize first word and proper nouns only
- Start with an imperative verb: Add, Update, Fix, Remove, Refactor
- No conventional commit prefixes (`feat:`, `fix:`, `chore:`) — those belong in commit messages, not PR titles
- No trailing punctuation
- Keep it under 72 characters

Examples:
- `[RAA-9] Add generate-coding-standards skill` ✓
- `Add writing-style plugin` ✓
- `feat(writing-style): add writing-style plugin with write-docs, write-pr, write-chat skills` ✗
- `Writing style plugin` ✗ (no verb)
- `Added the new writing style plugin` ✗ (past tense, "the")

---

## PR DESCRIPTIONS

Always use this template. Fill every section. Use `N/A` if a section genuinely doesn't apply — do not omit sections.

```markdown
## Background
<Why this change was needed. What problem exists, what was missing, what prompted this.
One paragraph max. No restatement of what the diff already shows.>

## Definition of Done
<What success looks like. Specific, observable criteria. Not "the feature works" —
state what behavior, output, or capability constitutes done.>

## In this PR
<Bullet list of what was added or changed. Reference files or commit SHAs where useful.>
- Added `path/to/file` — <one line on what it does>
- Updated `path/to/other` — <one line on what changed>

## Algorithm Version
<Version string if a model, algorithm, or pipeline version changed. Otherwise: N/A>

## Feature Flags
<List any flags gating this change. Otherwise: N/A>

## Testing
<How this was verified. Specific: what was run, on what data/repos/inputs, what the output was.
Not "manually tested" — describe what was done.>
```

---

## PR REVIEW COMMENTS

State the issue and the fix. One comment per finding.

```
<file>:<line> — <problem>. <fix or question>.
```

No "Nice catch", "Good work", "Looks good to me" padding. If it looks good, approve silently or with a single "LGTM". For blockers, state why. For nits, prefix with `nit:`.

---

## RESPONDING TO REVIEW FEEDBACK

Address each comment directly. No "Thanks for the feedback!" opener.

```
Done — <commit sha or "see <file>:<line>">
```
```
Disagree — <one line reason>. <alternative if applicable>.
```
```
Q: <clarifying question if genuinely unclear>
```

---

## COMMIT MESSAGES

Conventional Commits. Subject ≤50 chars. Body only if "why" isn't obvious from the diff.

```
<type>(<scope>): <imperative summary>
```

Types: feat, fix, docs, refactor, test, chore, perf, ci

---

## WHAT TO CUT

- All pleasantries: "Thanks!", "Great catch!", "Nice job on this"
- Summaries of what the reviewer can already read in the diff
- "As discussed", "Per our conversation"
- Restating the PR title in the description body
- Vague Testing sections: "Tested locally", "Manually verified" without specifics
