---
description: Writing style for formal documentation — result.md, specs, reports, READMEs, technical docs. Professional, condensed, evidence-based. No fluff, no unsupported claims.
user-invocable: true
---

# Write Docs Style

Apply this style when writing any formal documentation: result.md, README, specs, reports, architecture docs, runbooks, design docs.

---

## PRINCIPLES

**Condense without omitting.** Every sentence must earn its place. If a sentence doesn't add information, cut it.

**Evidence-only.** Only state what is supported by code, data, tests, or direct observation. No speculation presented as fact. If uncertain, say "unclear" or omit.

**Professional tone.** No casual language, no hedging phrases, no filler. Present tense for current state, past tense for completed actions.

---

## WHAT TO CUT

- Introductory throat-clearing: "This document describes...", "The purpose of this doc is..."
- Obvious restatements: don't explain what a section header already says
- Unsupported assertions: "This is best practice", "This is the most efficient approach" — only if you can cite why
- Padding: "as mentioned above", "it is important to note", "please note that"
- Hedging: "might", "could potentially", "in some cases" — be precise or omit

---

## STRUCTURE

Lead with the most important information. Use headers to chunk content. Use bullet points for lists of 3+. Use tables for comparisons. Use code blocks for all commands, paths, and code.

If explaining a decision, state: what was decided → why (evidence) → tradeoffs if relevant.

---

## EXAMPLE

Bad:
> This document provides an overview of the authentication system. It is important to note that the current implementation uses JWT tokens, which is a widely-used approach in modern web applications. The system was designed to be scalable and secure.

Good:
> ## Authentication
> JWT-based. Tokens expire in 24h, refreshed via `/auth/refresh`. Secrets stored in env vars, never in code.
