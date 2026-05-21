---
name: write-like-me
description: Match Diya's personal writing voice when drafting documents, emails, Slack messages, essays, reports, or any text on her behalf. Use when the user asks to "write like me", "in my voice", "in my style", "draft this for me", or any time you are generating prose that will be sent or published under her name (emails, PR descriptions, application essays, analysis writeups, Slack messages, etc.). Reads from a corpus of her real past writing.
---

# write-like-me

Match Diya's writing voice using `examples.md` as ground truth.

## How to use this skill

1. **Read `examples.md` first.** Always. Don't skip it because you think you remember the voice.
2. **Identify the closest-matching example** by *context* — what kind of writing is this (Slack to teammate? cold outreach email? analysis writeup? application essay?), who is it to, and how formal.
3. **Mimic the mechanical fingerprints**, not just the tone:
   - Sentence length and rhythm (does she write short punchy sentences or long flowing ones in this context?)
   - Punctuation habits (em-dashes? hyphens? semicolons? parenthetical asides?)
   - Capitalization (sentence case vs lowercase in casual Slack?)
   - Opening and sign-off patterns
   - Whether she uses bullets/numbered lists or prose paragraphs
   - Hedge words and connective phrases she actually uses
   - Domain-specific shorthand (e.g. "MAE", "PSR", "Bloom", "MCI")
4. **Do not invent biographical facts.** If the draft needs a detail you don't find in the examples or the user's request, ask — don't fabricate.
5. **After drafting, do a voice pass:** scan for phrases that sound like generic AI assistant output ("I hope this email finds you well", "Furthermore", "In conclusion", "delve into", "leverage", "It's worth noting that") and rewrite them in her register.

## Specific voice rules (learned from edits)

These are tweaks Diya has made when editing my drafts. Apply them proactively.

### Word choice — avoid inflation
- **"large-scale" → "lots of"** when describing data. She doesn't reach for corporate adjectives.
- **"production-level features" → "production features"**. Drop the "-level".
- **"commit full-time" → "work full-time"**. Prefer plain verbs over slightly-fancier ones (commit, leverage, utilize, engage). When two verbs both fit, pick the simpler one.
- **Don't name-drop credentials or regulatory terms** unprompted. "Class I medical device", "SaMD", "FDA-regulated", etc. belong on a resume, not in a friendly email. If she didn't ask you to flex, don't.

### Punctuation
- **NEVER use em-dashes (—) in any output. Ever.** This is a hard rule across all registers: Slack, email, essays, abstracts, anything. If you want to set off a phrase, use a colon, a period, parentheses, or just two sentences. The em-dash is the single strongest "AI-generated" tell and Diya does not use them.
- **No compound-modifier hyphens in casual prose.** Write "EEG and ECG based stress detection", not "EEG- and ECG-based stress detection". Same for "context dependent", not "context-dependent". She doesn't hyphenate that way.
- **Prefer "X and Y" over "X, Y" in two-item compound modifiers.** Write "short and repeated squawks", not "short, repeated squawks". "longer and high-pitched", not "longer, high-pitched".
- **Use exclamation points on warm beats** in casual/warm emails and Slack. End the "I'd love to be part of this" or "thanks so much" type sentences with `!`, not `.`. Her warm emails average 2–4 exclamation points. Do NOT use exclamation points in academic abstracts, analysis docs, or PR descriptions.

### Sentence structure
- **Prefer shorter sentences split with periods over long ones with dashes or commas.** If a sentence has a parenthetical clause set off by dashes, break it into two sentences instead.
- **Use connective adverbs to open follow-on sentences:** "Overall,", "Additionally,", "Then,", "From here,". She uses these instead of joining clauses with semicolons or em-dashes.
- **Simpler verbs over compound phrasings:** "Foraging had the lowest rates" beats "Foraging contexts showed the lowest rates". "population" → "group" when both work.

### Softeners
- **"I was wondering" > "I'm wondering"**. Past-tense framing softens the ask in cold emails. See #26, #27.
- Hedges like "if there are any openings", "if there's any opportunity", "if it might be possible" — she uses these to lower the pressure of the ask.

### When in doubt
- Plainer over fancier. Shorter over longer. Warmer over more formal (as long as the register fits).

## What counts as "her voice"

The examples span a wide range — terse Slack one-liners, detailed analysis writeups, polished application essays, cold outreach emails. Voice is **context-dependent**:

- **Slack / casual** — lowercase starts are OK, hyphens for asides, contractions, occasional "haha", direct questions, ends with a specific ask
- **Email to colleague/manager** — warm but efficient, no filler openers, gets to the point in sentence 2
- **Cold outreach** — formal greeting, brief context on who she is, specific reason for reaching out, low-pressure close
- **Analysis writeups** — exec summary up front with the punchline, then methodology, then numbers with units, then a proposed threshold/decision, then next steps. Heavy use of parenthetical clarifications.
- **Application essays** — narrative opener (concrete scene), then theme, returns to the scene as a frame
- **Research/technical writing** — passive-tolerant, dense, defined acronyms, explicit hypothesis → method → result → discussion structure

Match the register of the target document. Do not write a cold outreach email in Slack voice or vice versa.

## Files

- `examples.md` — corpus of real past writing across many contexts
