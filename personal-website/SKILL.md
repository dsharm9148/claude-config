---
description: Scaffold a personal portfolio website (Next.js 16 + React 19 + Tailwind 4, App Router) by interviewing the user for required assets (LinkedIn, résumé, bio, project images, headshot, favicon, etc.), pulling structured data from LinkedIn/résumé where possible, and writing copy in the user's voice. Use when the user asks to build a portfolio site, personal site, personal-website, "make me a website", "scaffold a portfolio", or runs /personal-website.
user-invocable: true
---

# personal-website

Scaffolds a minimalist, technical-editorial Next.js portfolio site for the user. Default vibe matches `~/Desktop/natalie-portfolio` (cream/olive/serif-display, blueprint grid, mono accents); the vibe is adjustable on request.

**Trigger:** `/personal-website` or "build me a portfolio".

**Token discipline:** This skill runs under caveman compression for all internal reasoning / status updates. Output to the user stays in write-chat style but should be terse. Skip narration. Do not dump file contents back at the user — just confirm what was written.

**Voice:** All prose written for the site (bio, hero blurb, project summaries, project bullets, about page) MUST be drafted through the `write-like-me` skill so it sounds like the user (Diya), unless the user explicitly says otherwise (e.g. site is for a different person — then ask them for samples or skip).

---

## Reference portfolios

Two on-disk references the agent should read before building. Do NOT copy whole — extract patterns.

| Path | Stack | Use as |
|---|---|---|
| `~/Desktop/natalie-portfolio` | Next 16 App Router, React 19, Tailwind 4, no framer-motion (CSS animations only), `next/font` Inter+Space Grotesk+JetBrains Mono | **Default template.** Minimalist, blueprint-grid hero, mono micro-labels, olive accent. Copy structure. |
| `~/Desktop/portfolio` | Next 15 Pages Router, Tailwind 4, `gray-matter` + `remark` for markdown blogs, `html2pdf.js` for résumé export | Alternate template if user wants a blog, travel pages, technique articles, or résumé-as-page. Pull selectively. |

Stack defaults (do not change without asking): Next.js 16 App Router, React 19, TypeScript, Tailwind 4 via `@tailwindcss/postcss`, ESLint 9, deploy target Vercel.

---

## How it works

### 1. Run the intake interview

Open `resources/intake.md` and ask the user the questions in the order listed. **One short message per question group, not a wall of text.** Use bullet lists. Skip groups that don't apply (e.g. if user is non-technical, skip "tools/skills tags").

Capture answers in memory as you go — do not lose them mid-conversation. If LinkedIn URL or résumé PDF path is given, offer to extract structured data (experience, education, skills) from them so the user only has to confirm rather than type. Images, headshot, favicon, project screenshots — these MUST come from the user; do not invent or stub with placeholders unless the user says "use placeholders for now."

### 2. Confirm vibe / theme

Default is `natalie-portfolio` (cream `#f4f3ee` bg, olive `#4a6d4a` accent, Space Grotesk display). Show the user 2–3 alternative palettes briefly (e.g. "warm cream / cool slate / dark mode") and ask. If they want something off-template, capture the descriptor (colors, mood, fonts) before scaffolding so the agent writes the right CSS variables on the first pass.

### 3. Scaffold the project

Decide the target directory with the user (default: `~/Desktop/<user-first-name>-portfolio` lowercased). Then:

```bash
# create dir, copy structure (not contents) from natalie-portfolio
cp -R ~/Desktop/natalie-portfolio/. <target>/
cd <target>
rm -rf node_modules .next .git
```

Then customize — do not leave Natalie's data anywhere:

| File | Action |
|---|---|
| `src/lib/site.ts` | Replace name, initials, role, school, location, links |
| `src/lib/experience.ts` | Replace with user's experience (from LinkedIn / résumé, confirm) |
| `src/lib/projects.ts` | Replace with user's projects |
| `src/components/Hero.tsx` | Rewrite hero blurb via `write-like-me` |
| `src/app/about/page.tsx` | Rewrite bio paragraphs via `write-like-me`; update facts list |
| `src/app/layout.tsx` | Update `metadata`, `SITE_URL`, title template |
| `src/app/globals.css` | Update CSS variables if theme changed |
| `src/components/QuickFacts.tsx` | Update the 4 at-a-glance facts |
| `public/headshot.jpg` | Replace with user-provided headshot |
| `public/resume.pdf` | Replace with user-provided résumé PDF |
| `src/app/icon.png` | Replace with user-provided favicon / tab icon |
| `public/*.svg` (`file`, `globe`, `window`, `next`, `vercel`) | Delete unless used |
| `README.md` | Rewrite minimal: project name, run commands, where to edit |
| `package.json` | Update `name` field |

If the user wants **blog / travel / résumé-page** features, pull from `~/Desktop/portfolio` (Pages Router patterns can be rewritten as App Router routes — `src/app/blog/page.tsx`, `src/app/blog/[slug]/page.tsx`, etc., using `gray-matter` + `remark` like the source).

### 4. Write copy in the user's voice

For every piece of prose the site needs — hero subtitle, about page paragraphs, project summaries, project bullets, experience bullets — invoke `write-like-me` with the raw facts and let it draft. Then show the user the draft and ask for edits before pasting into the file. Do not write prose directly; route through `write-like-me`.

Exception: short structural labels ("Selected work.", "Where I've worked.", "At a glance", "Get in touch") stay as-is — they're UI chrome, not voice.

### 5. Place user-provided assets

Required from the user (cannot be auto-generated):

- **Headshot** → `public/headshot.jpg` (5:6 aspect works best with hero/about layout)
- **Résumé PDF** → `public/resume.pdf`
- **Favicon / tab icon** → `src/app/icon.png` (512×512 recommended)
- **Project images** (if showing screenshots) → `public/projects/<slug>.jpg`
- **OG image** (optional) → `public/og.png` (1200×630). If provided, wire it into `metadata.openGraph.images` in `layout.tsx`.

If user has files on disk, ask for paths and `cp` them in. If they haven't gathered assets yet, leave a stub and note which assets are missing in the final summary.

### 6. Install + verify

```bash
cd <target>
npm install
npm run build  # catches type errors and missing assets
npm run dev    # open localhost:3000, eyeball it
```

Report the dev URL to the user. Do **not** run `git init`, `git push`, or deploy without asking.

---

## Output

A working Next.js portfolio at `<target>/` that:

1. Builds clean (`npm run build` exits 0)
2. Has zero Natalie / placeholder data
3. Uses the user's headshot, résumé, favicon, and project images
4. Has bio / project / experience prose drafted via `write-like-me`
5. Matches the requested vibe (default: minimalist editorial-technical)

Final message to user (terse, write-chat style):
- target dir path
- `npm run dev` command
- list of any still-missing assets the user owes
- next steps (deploy on Vercel? add domain?) — ask, don't auto-do

---

## Notes

- **Never** invent project descriptions, employer details, or résumé content. Pull from the user's résumé/LinkedIn or ask. Hallucinated portfolio content is worse than a placeholder.
- **Never** deploy or `git push` without explicit user approval (CLAUDE.md rule).
- If the user wants a non-Next stack (Astro, plain HTML, etc.), ask once whether to deviate from the default before scaffolding — but warn that the two reference portfolios are both Next.
- Keep `node_modules` out of any copies. Always `rm -rf node_modules` after `cp -R`.
- The `~/.claude/skills/` directory is a symlink to `~/claude-skills/`, so this skill is live in all sessions immediately after writing.
