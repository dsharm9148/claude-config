# WHOOP Presentation Design Guide

Brand reference for reveal.js HTML slide decks. Source of truth: *WHOOP Brand Guidelines 2026*.

---

## Stack

- **Framework**: reveal.js 5.1.0 (CDN — no local install)
- **Format**: Single self-contained HTML file, 1280×720, `margin: 0`
- **Transition**: `fade` / `fast`

---

## Brand Voice & Design Principles

| Principle | What it means in presentations |
|---|---|
| **Always On** | Precision matters — every element should be intentional |
| **Powerfully Simple** | Less is more; distill to what matters most |
| **Human Centered** | Celebrate the individual; avoid generic corporate tone |
| **Driven by Design** | Design-forward executions; never default to generic templates |

---

## Typography

Source: *WHOOP Brand Guidelines 2026*, Slides 16–18.

### Type System

| Style | Font | Weight | Case | Tracking | Use |
|---|---|---|---|---|---|
| **Eyebrow** | Proxima Nova | Bold | UPPERCASE | 10% / 100 | Section labels, tags, metadata |
| **Headline** | Proxima Nova | Bold / Regular / Light | Sentence case | 0 | Slide titles |
| **Sub-head** | Proxima Nova | Bold / Light / Regular | Sentence case | 0 | Subtitles, column headers |
| **Body copy** | Proxima Nova | Bold / Light / Regular | Sentence case | 0 | Bullet points, descriptions |
| **CTA** | Proxima Nova | Bold | UPPERCASE | −3% / −20pt | Buttons, calls-to-action |
| **Numbers** | DINPro | Bold | — | auto | Stats, metrics |

Fallback stack: `'Proxima Nova', 'Helvetica Neue', Helvetica, Arial, sans-serif`

> Do NOT use Inter or Google Fonts — they are off-brand.

### Alignment
- **Default**: left-aligned (easiest to read)
- Headlines may be center-aligned when appropriate
- Right-aligned only when absolutely necessary; never combine alignments

---

## Color Palette

Source: *WHOOP Brand Guidelines 2026*, Slides 19–22.

### Primary (brand communications)

| Name | Hex | Use |
|---|---|---|
| Black | `#000000` | Primary — predominant in brand applications |
| White | `#FFFFFF` | Text, logos on dark backgrounds |

### Secondary (app data system)

| Name | Hex | Feature |
|---|---|---|
| Recovery Blue | `#67AEE6` | Recovery (no valuation) |
| High Recovery | `#19EC06` | Recovery 100–67% |
| Medium Recovery | `#FFDE00` | Recovery 66–34% |
| Low Recovery | `#FF0026` | Recovery 33–0% |
| Strain | `#0093E7` | Strain / activities |
| Strain Zone 1 | `#ADC2CD` | Lowest effort |
| Strain Zone 2 | `#479AC2` | Light effort |
| Strain Zone 3 | `#59B996` | Moderate effort |
| Strain Zone 4 | `#FCAC5D` | Hard effort |
| Strain Zone 5 | `#FF6422` | Max effort |
| Sleep | `#7BA1BB` | Sleep data |
| Deep Sleep | `#FA95FA` | Deep sleep stage |
| REM Sleep | `#AC5AED` | REM stage |
| Light Sleep | `#A4A3F1` | Light sleep stage |
| Awake | `#C8C8C8` | Awake time |
| Positive Trend | `#00F19F` | Teal — positive trends, CTAs, highlights |
| Negative Trend | `#FFA722` | Warning / negative trend |
| Focus | `#FFEB62` | Focus feature |
| Onboarding | `#CB4ED8` | Onboarding flows |
| Background–Std | `#101518` | Standard dark background |
| Background–Alt | `#1A2227` | Alternate dark background |

> Every color has meaning — use intentionally and in context.

### Gradients

| Name | Colors | Direction |
|---|---|---|
| Slide background | `#283339` → `#14191D` → `#101518` | Linear 90° |
| Accent | `#50D5FF` → `#8B62FF` | Linear 45° |


---

## Logo

Assets in `resources/brand/logos/`. Source: *WHOOP Brand Guidelines 2026*, Slides 12–15.

| File | Description | Use |
|---|---|---|
| `wordmark_white.png` | WHOOP wordmark, white on transparent | On dark backgrounds |
| `wordmark_black.png` | WHOOP wordmark, black on transparent | On light backgrounds |
| `puck_white.png` | W-circle puck, white on transparent | App icons, small-scale |
| `puck_black.png` | W-circle puck, black on transparent | On light backgrounds |

**Placement rules** (every deck):
- Slide header on every slide
- Large on title slide
- On section dividers

**On dark backgrounds**: use `wordmark_white.png` or apply `filter: invert(1); mix-blend-mode: screen` to black versions.

**Logo DONTs**: recolor, rotate, distort/warp, overlay on illegible background, place near visualized data.

Minimum sizes: wordmark ≥ 100px wide, puck ≥ 30px wide. Exclusion zone: 2× logo height on all sides.

**Inline SVG fallback** (when PNG not available):
```html
<svg height="14" viewBox="0 0 80 14" fill="none" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="12" font-family="'Proxima Nova','Helvetica Neue',sans-serif"
        font-weight="700" font-size="13" letter-spacing="0.15em" fill="white">WHOOP</text>
</svg>
```

---

## Photography

Source: *WHOOP Brand Guidelines 2026*, Slides 24–28.

Three content types — choose based on slide purpose:

| Type | Files | Style | Use for |
|---|---|---|---|
| **Band / Product** | `band_01–07.jpg` | Device-forward, natural moments | Title slides, product features |
| **Casual / Lifestyle** | `casual_01–07.jpg` | Docu-style, authentic, never staged | Section dividers, culture slides |
| **Active / Athlete** | `active_01–16.jpg` | Subject centric, intensity/emotion | Performance, data, metric slides |

All images are 1280×720. Use as full-bleed backgrounds with a dark scrim overlay:
```css
.cover-scrim {
  background: linear-gradient(90deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.35) 100%);
}
```

---

## Icons

24 WHOOP-style icons available in `resources/brand/icons/icon_01.png` through `icon_24.png`.

All icons are line-style, RGBA transparent background. On dark slides use `filter: invert(1)`.

---

## WHOOP Terminology

Source: *WHOOP Brand Guidelines 2026*, Slides 5–11, 30–35. Use these exact terms in slide copy.

### Hardware & Accessories

| Use this | Not this |
|---|---|
| **WHOOP** (band + clasp + sensor complete) | WHOOPs, WHOOP's |
| **Band** | strap, watch |
| **WHOOP Sensor** | device |
| **Fast Link™ Slider** | slider (without TM) |
| **Wireless PowerPack** | charger (for on-wrist version) |
| **WHOOP 5.0** | WHOOP 5, 5.0 alone |
| **WHOOP MG** | MG device, MG sensor |

### Memberships

| Term | Definition |
|---|---|
| **WHOOP One** | Entry-tier — core fitness features |
| **WHOOP Peak** | Mid-tier — advanced health features |
| **WHOOP Life** | Top-tier — medical-grade insights |
| **Member** | A person with a membership (not "user" or "customer") |
| **Family Plan** | Shared billing plan (not "family membership") |

### Metrics & Features (always capitalize as shown)

| Correct | Avoid |
|---|---|
| Sleep, Strain, Recovery, Stress | lowercase versions when used as WHOOP metrics |
| WHOOP Coach | "AI coach" or "coach" alone |
| Heart Screener | "heart monitor" |
| Healthspan, WHOOP Age, Pace of Aging | alternate names |
| Impact Tags | "behavior tags" |
| Sleep Planner | "sleep coach" |
| Strength Trainer | "lifting tracker" |

### Words to Avoid

| Avoid | Reason |
|---|---|
| Track | Oversimplifies WHOOP functionality |
| Tier | Use membership names instead |
| Holistic | Generic/overused |

---

## CSS Component Classes

| Class | Purpose |
|---|---|
| `.slide` | Slide shell (flex column, 1280×720) |
| `.slide-header` | Top bar with logo + metadata |
| `.slide-body` | Content area (flex, fills remaining space) |
| `.slide-title` | Cover slide |
| `.slide-divider` | Section break slide |
| `.section-label` | Eyebrow-style teal label above slide title |
| `h2.content-title` | Headline (uppercase, bold) |
| `.content-subtitle` | Muted subtitle below headline |
| `ul.b` | Bullet list (teal dash markers) |
| `ul.b li.sub` | Sub-bullet (muted, indented) |
| `.two-col` / `.three-col` | Grid layouts |
| `.challenge-col` | Column for challenge slides |
| `.col-label-pain` / `.col-label-ask` | Challenge column headers |
| `.box-blue` / `.box-teal` / `.box-gray` | Highlighted content boxes |
| `.callout` / `.callout-teal` | Left-border callout boxes |
| `.flow` / `.flow-step` / `.flow-num` | Numbered flow diagrams |
| `table.t` | Data table |
| `.tag-on` / `.tag-off` / `.tag-manual` | Status tags |
| `.code-block` | Code block (monospace, dark bg) |
| `.stat-num` / `.stat-label` | Large metric numbers |

---

## Cover Slide Sizes

Source: *WHOOP Deck Template Cover Slides*, Slide 2.

| Element | Size | Weight |
|---|---|---|
| Title (top line) | 60pt | Semibold |
| Subtitle (second line) | 48pt | Normal |

---

## Content Principles

- Slides are conversation companions — bullets and short phrases, no dense paragraphs
- Use **Eyebrow** style (`.section-label`) for all category/section labels — uppercase, teal, 10% tracking
- Use correct WHOOP terminology (see Terminology section) — never say "track", "tier", or "user"
- Challenge slides: two columns — "Current State" (`.col-label-pain`) | "What We're Looking For" (`.col-label-ask`)
- Wins: embed as `.callout` boxes within relevant slides, not standalone slides
- Hyperlinks: always preserve, styled with `var(--blue)`
- Photography: match image category to slide mood (band → product, active → performance, casual → culture)
