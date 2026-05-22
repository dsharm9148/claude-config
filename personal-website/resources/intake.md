# Intake Questionnaire

Ask the user these in order. Group questions into short messages — 3–5 questions per turn, not all at once. Skip groups that don't apply.

If LinkedIn URL or résumé PDF is given, offer to read the résumé and pre-fill experience/education/skills so the user only confirms.

---

## Group 1 — Identity

- Full name (as it should appear on the site)
- Initials (2 chars, for the nav logo square)
- Role / title in one line (e.g. "Mechanical Engineer", "ML Engineer", "Design Researcher")
- Current city / location
- School + expected grad year (if student) OR current company (if working)
- Pronouns (optional, only if they want them shown)

## Group 2 — Links

- LinkedIn URL
- GitHub URL (if relevant)
- Email (will it be public on the site?)
- Personal domain (if they have one — for `metadata.url`)
- Any other links to surface (Twitter/X, Are.na, Read.cv, Substack, etc.)

## Group 3 — Résumé + LinkedIn data

- Path to résumé PDF on disk (we'll `cp` it to `public/resume.pdf`)
- Can I parse the résumé to pre-fill experience and education? (yes/no)
- LinkedIn URL — should I scrape (if possible) or will you paste the experience block?

## Group 4 — Bio

- 2–3 sentences max, raw facts, no styling. Examples of what to include:
  - What you study / do
  - What you're working on right now
  - One thing outside of work / school you care about
- We'll route this through `write-like-me` to draft the actual prose.

## Group 5 — Projects

For each project (aim for 3–6):

- Title
- Course / context (e.g. "ME 2110", "Personal", "Internship side project")
- Year
- One-line summary
- 2–4 bullet points: what you built, methods/tools used, outcome
- Tools/tech tags (e.g. SolidWorks, MATLAB, FEA, Python, React)
- Image path (optional — drops into `public/projects/<slug>.jpg`)

## Group 6 — Experience

For each role (résumé will pre-fill if provided):

- Organization
- Role
- Location + on-site / remote
- Dates (e.g. "May 2025 — Aug 2025")
- 1–3 bullet points of impact
- Skills/tools tags

## Group 7 — Visual assets (REQUIRED from user, cannot generate)

- **Headshot** — path to jpg/png on disk. Best aspect ratio is 5:6 (vertical). Goes to `public/headshot.jpg`.
- **Tab icon / favicon** — path to png on disk, ideally 512×512 square. Goes to `src/app/icon.png`.
- **OG / share image** (optional) — 1200×630 png. Goes to `public/og.png`.
- **Project screenshots** (optional) — paths. Go to `public/projects/<slug>.jpg`.

## Group 8 — Vibe

Default vibe is `natalie-portfolio`: cream `#f4f3ee` background, olive `#4a6d4a` accent, Space Grotesk display font, JetBrains Mono micro-labels, blueprint grid in hero. Editorial-technical minimalism.

Offer 2–3 alternatives briefly:
- "warm cream + olive (default)"
- "off-white + cool slate / navy accent"
- "dark mode — black bg + warm cream text"
- custom — let user describe colors/mood/font feel

If user picks non-default, capture: bg color, fg color, accent color, font pairing (display / body / mono).

## Group 9 — Pages

Default pages: `/`, `/about`, `/projects`. Ask if they want any extras:

- `/blog` — markdown blog (pulls patterns from `~/Desktop/portfolio`)
- `/travel` — country/photo pages
- `/resume` — résumé rendered as a styled page (not just PDF link)
- Anything custom

## Group 10 — Target directory + name

- Where to scaffold? Default: `~/Desktop/<firstname>-portfolio` lowercased
- `package.json` name field — default: `<firstname>-portfolio`
- Site URL for metadata (e.g. `https://diya.dev` or the Vercel preview URL — placeholder OK)
