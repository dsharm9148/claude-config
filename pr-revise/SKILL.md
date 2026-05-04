---
name: pr-revise
description: Use me when you have PR review comments to address. Give me a PR URL. I scan for unanswered comments, make minimal targeted fixes, ask when unclear, commit, push, reply to each thread, then post a summary review thanking the reviewer and marking it ready for re-review.
user_invocable: true
version: 1.1.0
---

# PR Revise

Address unanswered review comments on a GitHub PR end-to-end: scan for open threads, make minimal targeted edits, commit, push, reply to each comment, post a closing review summary.

---

## Inputs

Required:
- **PR URL** — e.g. `https://github.com/org/repo/pull/123`

Optional:
- Specific comments to focus on (default: all unanswered)
- Per-comment instructions (default: infer from comment text)

If the PR URL is missing, ask for it before doing anything.

---

## Workflow

### 1. Parse the PR

Extract `owner`, `repo`, `pr_number` from the URL.

```bash
gh pr view <pr_number> --repo <owner>/<repo> --json headRefName,files
```

### 2. Find unanswered comments

Fetch all inline review comments:
```bash
gh api repos/<owner>/<repo>/pulls/<pr_number>/comments \
  --jq '.[] | {id, path, body, line: .original_line, in_reply_to_id}'
```

A comment is **unanswered** if:
- It has no `in_reply_to_id` (it's a top-level thread starter), AND
- No other comment in the list has `in_reply_to_id` equal to its `id`

Filter to only unanswered top-level comments. Present the list to the user before proceeding:

```
Found N unanswered comments:
1. <path>:<line> — "<first 80 chars of comment body>"
2. ...
Proceeding with all unless you say otherwise.
```

### 3. Clarify ambiguous comments

Before touching any file, review each unanswered comment. If the required edit is **not obvious** from the comment text, ask the user:

```
Comment on <path>:<line>: "<comment body>"
What should I do here?
```

Wait for the answer before proceeding. Do not guess.

### 4. Check out the branch

If already in the repo:
```bash
gh pr checkout <pr_number> --repo <owner>/<repo>
```

If not in the repo, clone to `/tmp/<repo>`:
```bash
git clone https://github.com/<owner>/<repo>.git /tmp/<repo>
cd /tmp/<repo>
git fetch origin pull/<pr_number>/head:pr-<pr_number>
git checkout pr-<pr_number>
```

### 5. Make minimal edits

For each comment:
- Read the file first. Never edit blind.
- Make the **smallest possible change** that addresses the comment. Change only the lines the comment is about.
- Do not fix surrounding code, add comments, rename unrelated things, or clean up style.
- If a comment says "remove X", remove only X. If it says "rename Y", rename only Y.
- For comments where no edit is needed (disagree, punting, already correct), skip the edit but note it.

### 6. Commit

Single commit for all changes unless the user requests otherwise.

```
<type>(<scope>): address PR review comments

- <one line per change>
```

Show the diff summary and commit message. **Ask the user to confirm before committing.**

### 7. Push

```bash
git push origin <local-branch>:<headRefName>
```

Capture the short SHA:
```bash
git rev-parse --short HEAD
```

### 8. Reply to each comment

Reply inline to every unanswered comment using the `gh api` replies endpoint:

```bash
gh api repos/<owner>/<repo>/pulls/<pr_number>/comments/<comment_id>/replies \
  -X POST -f body="<reply>"
```

Keep replies short and direct. No pleasantries.

| Situation | Reply format |
|-----------|-------------|
| Edit made | `Fixed in <sha> — <one line on what changed>` |
| Agreed, no edit needed | `Agreed — <one line reason>` |
| Disagree | `Disagree — <one line reason>. <alternative if any>` |
| Punting | `Punting — will address in <follow-up>` |
| User clarified intent | `<what was done>, per discussion` |

### 9. Post closing review comment

After all inline replies are posted, submit a review comment on the PR (not inline — top-level) that:
- Thanks the reviewer by name
- Gives a 2–4 bullet summary of what was changed
- Says it's ready for re-review

```bash
gh pr review <pr_number> --repo <owner>/<repo> --comment --body "<body>"
```

Format:
```
Thanks <reviewer> — addressed your comments in <sha>.

Changes:
- <bullet 1>
- <bullet 2>
- <bullet 3>

Ready for re-review.
```

Keep it short. One line per bullet. No detail beyond what the inline replies already cover.

---

## Rules

**Only address unanswered comments.** Skip any thread that already has a reply.

**Minimal edits.** Change the fewest lines possible. Prefer a 1-line fix over a 5-line refactor.

**Read before editing.** Always Read the file before Edit.

**Ask when unsure.** If the right edit isn't clear from the comment, ask the user before touching the file.

**Confirm before pushing.** Show diff summary + commit message and wait for user approval.

**No pleasantries in inline replies.** "Fixed in abc1234" is complete.

**Always post the closing review.** Even if changes were minimal, post the summary so the reviewer knows it's ready.
