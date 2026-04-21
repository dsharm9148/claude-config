---
description: Generate a WHOOP-style Software Design Specification (.docx) for any ML algorithm or service. Sequential three-phase workflow: Gather → Generate → (optional) Validate & Improve. Calibration mode self-improves the skill against a gold standard document.
user-invocable: true
---

# Generate SDS

Produces a WHOOP-formatted Software Design Specification (`.docx`) from source code and Confluence documentation.

**Trigger:** `/generate-sds <args>` or "generate SDS for <algorithm>"

**Arguments:** space-separated, any combination of:
- GitHub repo names: `WhoopInc/some-service`
- Confluence page IDs: `1234567890`
- Output path (must end in `.docx`): `~/Downloads/DOC-001.docx`. Default: `~/Downloads/<SLUG>_SDS.docx`
- `--srs <path/to/srs.docx>` — Software Requirements Specification to extract requirement IDs from (repeat for multiple)
- `--refresh` — ignore cache, re-fetch all source material
- `--calibrate <path/to/gold_standard.docx>` — run calibration mode (all three phases)

**Modes:**

| Mode | Phases | When |
|------|--------|------|
| Production (default) | Phase 1 + Phase 2 | Normal document generation |
| Calibration | Phase 1 + Phase 2 + Phase 3 | `--calibrate <gold.docx>` provided |

---

## PART 0 — ARGUMENT PARSING

Extract from `$ARGUMENTS`:
- `SLUG` — short identifier (e.g. `anf`, `sleep`, `bloom`). Derive from repo name or feature name.
- `REPOS` — list of GitHub repo names (`WhoopInc/...`)
- `CONFLUENCE_PAGES` — list of numeric Confluence page IDs
- `OUTPUT_PATH` — output `.docx` path. Default: `~/Downloads/<SLUG>_SDS.docx`
- `REFRESH` — true if `--refresh` present
- `SRS_PATHS` — list of SRS docx paths from `--srs <path>` arguments
- `CALIBRATE_PATH` — path to gold standard docx if `--calibrate <path>` present

```bash
SKILL_DIR="$HOME/.claude/skills/generate-sds"
CACHE="$SKILL_DIR/resources/${SLUG}_context.json"
IMAGES_DIR="$SKILL_DIR/resources/images/${SLUG}"
```

---

## PHASE 1 — GATHER SOURCE MATERIAL

### Step 1a — Check Cache

```bash
python3 -c "
import pathlib, time
cache = pathlib.Path('$CACHE')
if cache.exists() and (time.time() - cache.stat().st_mtime) < 604800:
    print('HIT')
else:
    print('MISS')
"
```

- **HIT** (no `--refresh`): load cache, proceed to Step 1c.
- **MISS** or `--refresh`: proceed to Step 1b.

### Step 1b — Read Repos and Confluence

**For each repo** — read via `gh api`:
```bash
gh api repos/<ORG>/<REPO>/contents/          # root structure
gh api repos/<ORG>/<REPO>/contents/README.md # README
gh api repos/<ORG>/<REPO>/contents/docs/     # docs directory if present
```
Then read key source files: API endpoint definitions, Pydantic request/response models, algorithm pipeline files, configuration YAMLs, exception classes. Read only what is needed to fill the document.

**For each Confluence page** — call `confluence_get_page(page_id)`.

**Save raw context to cache:**
```python
import json, pathlib, datetime
cache = pathlib.Path(f'{SKILL_DIR}/resources/{SLUG}_context.json')
cache.parent.mkdir(parents=True, exist_ok=True)
cache.write_text(json.dumps({
    "repos": { "<repo>": { "readme": "...", "files": {...} } },
    "confluence": { "<page_id>": "<page_content>" },
    "fetched_at": datetime.datetime.now(datetime.UTC).isoformat()
}, indent=2))
```

### Step 1c — Extract SRS Requirements

For each path in `SRS_PATHS`:
```bash
python3 "$SKILL_DIR/resources/read_docx.py" "<srs_path>" > /tmp/${SLUG}_srs.txt
```
Read the extracted text. Identify and record:
- All formal requirement IDs and their text (e.g., `ANF-SRS-001`, `FR-001`, `REQ-001` — follow whatever numbering scheme the document uses)
- Any terms and definitions defined in the SRS
- Referenced standards or SOPs

These requirement IDs are the authoritative source for the RTM in Appendix A. Use them directly — do not invent requirement IDs.

### Step 1d — Download Confluence Images

1. For each Confluence page, call `confluence_get_attachments(content_id='<page_id>')`
2. Identify architecture diagrams, flowcharts, draw.io previews (PNG files)
3. For each image to embed, call `confluence_download_attachment(attachment_id='attXXXX')`
4. Extract and save images from the session transcript:
```bash
mkdir -p $IMAGES_DIR
python3 "$SKILL_DIR/resources/extract_images.py" "$SLUG"
```

### Step 1d — Extraction Checklist

Before proceeding to Phase 2, verify:
- [ ] `algo_version` found in code or config (mark [REQUIRES HUMAN INPUT] if not)
- [ ] All API endpoint paths identified
- [ ] All Pydantic request/response models read
- [ ] Configuration parameters catalogued
- [ ] For each DQ threshold and algorithm parameter: searched source code and inline comments for justification. Note rationale (e.g., "during model development, it was found that..."). If not found, mark [REQUIRES HUMAN INPUT: justify threshold value].
- [ ] DQ check count: read the full DQ assessment class and confirm every distinct condition that can label an epoch Insufficient Data — including any out-of-range value checks (beat-to-beat intervals and acceleration values outside expected bounds). These are separate named checks, not implicit behavior.
- [ ] Log storage: find the actual log storage system (Elasticsearch, CloudWatch, Datadog, etc.), the actual configured retention period in days, and the specific fields logged per event type. Do not repeat the SRS requirement floor — find the actual configured value in source code or infrastructure config.
- [ ] SOPs and related design documents identified by ID in code comments
- [ ] Confluence diagrams downloaded (or confirmed absent)
- [ ] Exception classes read and catalogued
- [ ] Initialization/startup sequence fully traced

---

## PHASE 2 — GENERATE DOCUMENT

### Quality Standards
- **Evidence-only.** Include only information observed in code, docs, or Confluence. Mark gaps: `[REQUIRES HUMAN INPUT: <what's needed>]`.
- **No hallucination.** If unclear, explicitly mark as an assumption.
- **Algorithm-first.** The document's primary purpose is to describe the algorithm precisely.
- **Execution order.** Algorithm sections must follow the actual pipeline execution order, not a logical/categorized structure.
- **Mathematical precision.** DQ checks and thresholds must be stated as exact criteria (e.g., "RR coverage ≥ 75%"), not prose summaries. Include threshold justification where found.
- **Schemas as tables.** Every request/response field gets a row: Field | Type | Required | Description.
- **Examples as code_blocks.** Full JSON request/response examples in `code_blocks`, not paragraphs.
- **Prefer real Confluence images** over auto-generated diagrams. Auto-generate only when no image exists.
- **Writing style (Algorithm Description).** Match the gold standard's prose-first pattern: describe each DQ check and classification rule in a complete prose paragraph ("An epoch is determined to have X if the following criteria are met: …"), then use a parameter table for values only. Embed decision rationale directly in the prose immediately after the criterion statement — do not defer it to a [REQUIRES HUMAN INPUT] block. Use consistent passive voice: "An epoch is determined to…", "The epoch is labeled…", "A window is assigned…".
- **Stay lean.** Only include sections from the "Always" or condition-met rows of the section list below. Do not add sections because they seem useful.

### Step 2a — Assemble Content JSON

Write to `/tmp/<slug>_sds_content.json`.

**Required top-level fields:**
- `doc_id` — e.g. `ANF1-001`. Derive: `<FEATURE_PREFIX>1-001`
- `title` — full document title: `WHOOP <Algorithm> Design Specification`
- `algo_version` — from code or config
- `date` — today's date `YYYY-MM-DD`
- `approvers` — list of `{"role": "...", "name": "..."}`. Use `[REQUIRES HUMAN INPUT]` if unknown.
- `sections` — list of section objects (see Section List below)
- `revision_history` — list of `{"version", "date", "description", "author"}`

```bash
python3 -c "
import json, pathlib
content = { ... }  # assembled dict
pathlib.Path('/tmp/${SLUG}_sds_content.json').write_text(json.dumps(content, indent=2))
print('Wrote /tmp/${SLUG}_sds_content.json')
"
```

### Step 2b — Standard Section List

**Only include sections marked "Always" or whose condition is met.** Sections marked "Omit by default" must be explicitly requested by the user. Sections must be numbered sequentially in the final document.

| Standard # | Title | When to Include | Key Content |
|------------|-------|-----------------|-------------|
| 1 | Purpose and Background | Always | What the system does, why it exists, clinical/product context, regulatory context |
| 2 | References | Always | Always include: (a) GitHub repos, (b) Confluence pages, (c) applicable IEC standards, (d) internal SOPs referenced in code comments (e.g., SOP-003 Design and Development, SOP-027 SDLC), (e) related design documents by ID if referenced in code or docs (design plan, SRS, training plan, SBOM, anomaly reports), (f) model artifact location |
| 3 | Terms and Definitions | Always for SaMD documents | Glossary table of all acronyms and domain terms. Columns: Term \| Definition. Minimum: all acronyms present in the document. For SaMD: include SaMD classification, applicable standard names. |
| 4 | Initialization / Startup Sequence | When service has startup behavior | Server startup, external service init, model artifact load from disk, hash verification, SBOM reference |
| 5 | System Architecture | Always | Architecture diagram, component overview, data flow summary |
| 6 | Algorithm Description | When algorithm logic is central | **Must follow execution order** as named subsections: (1) Principles of operation overview, (2) Time periods that get labeled — with examples of which epochs/windows are labeled based on highwatermarks and data span, (3) Epoch-level DQ assessment — each named check as its own subsection with exact mathematical criteria and threshold justification; if justification not found mark [REQUIRES HUMAN INPUT], (4) Epoch-level classification, (5) Window-level classification, (6) High-water mark update logic with exact formula (e.g., "data HWM = N minutes prior to end of last classified epoch"), (7) Epoch classification history update logic (cap behavior, no-modification conditions), (8) Gap handling — state BOTH trigger conditions: (a) epoch history contains ≥N Insufficient Data events AND (b) ≥1h between classification HWM and first metric packet; state behavior (single INSUFFICIENT_DATA window spanning the gap) and cascading effect across successive requests |
| 7–N | API Endpoints | One subsection per endpoint | Request schema table, response schema table, JSON examples |
| N+1 | Observability, Logging, and Monitoring | When metrics/logging found in code | Metrics emitted (with names and tags), log strategy, log storage system and retention period, process lifecycle logging |
| N+2 | Error Handling and Failure Modes | Always | Exception types, HTTP codes, fallback behaviors, exception hierarchy |
| N+3 | Configuration | When configurable params found | All tunable parameters with defaults and units |
| N+4 | Edge Cases | Always | Table: Scenario \| Behavior \| Notes |
| N+5 | Appendix A — Requirements Traceability Matrix | Always for SaMD documents | Table mapping each requirement to the document sections that implement it. Columns: Requirement ID \| Requirement Summary \| Implementing Section(s). **If SRS provided:** use the actual requirement IDs from the SRS — do not invent IDs. If no SRS provided: derive requirements from design intent in code and docs. |
| — | Scope | **Omit by default** | What is and is not covered by this document |
| — | Goals and Non-Goals | **Omit by default** | Explicit goals; explicit non-goals |
| — | Requirements Summary | **Omit by default** | Table of key FRs + NFRs with IDs |
| — | System Components and Responsibilities | **Omit by default** | Each component: role, technology, owned interfaces |
| — | Dependencies and Integrations | **Omit by default** | Services, libraries, ML artifacts, infra |
| — | Security, Privacy, and Compliance | **Omit by default** | IEC 62304 software safety class, PHI handling, audit requirements |
| — | Reliability, Scalability, and Performance | **Omit by default** | Expected load, latency targets, degradation behavior |
| — | Deployment and Operational Considerations | **Omit by default** | Infra, deployment model, runtime dependencies, rollback |
| — | Risks and Mitigations | **Omit by default** | Table: Risk \| Likelihood \| Impact \| Mitigation \| Owner |
| — | Open Questions | **Omit by default** | Table: ID \| Question \| Blocking? |
| — | Assumptions | **Omit by default** | Numbered list |

### Step 2c — Generate Document

```bash
python3 "$SKILL_DIR/resources/generate_sds.py" \
    /tmp/${SLUG}_sds_content.json \
    "$OUTPUT_PATH"
```

### Step 2d — Verify and Report

Report:
- Output file path and size (bytes)
- Section count and table count
- Images embedded vs. missing (placeholder count)
- `[REQUIRES HUMAN INPUT]` markers — list each one
- Cache: HIT or MISS

---

## PHASE 3 — VALIDATE AND IMPROVE

**Calibration mode only (`--calibrate` flag).** Skip entirely in production mode.

### Step 3a — Extract Document Text

```bash
python3 "$SKILL_DIR/resources/read_docx.py" "$CALIBRATE_PATH" > /tmp/${SLUG}_gold.txt
python3 "$SKILL_DIR/resources/read_docx.py" "$OUTPUT_PATH"     > /tmp/${SLUG}_generated.txt
```

Read both output files. Use the `##` / `###` / `####` heading markers and `[TABLE]` / `[/TABLE]` blocks to compare section-by-section.

### Step 3b — Score on 9 Dimensions

| # | Dimension | Score 1 | Score 3 | Score 5 |
|---|-----------|---------|---------|---------|
| 1 | Completeness | Major sections missing | Minor gaps | All sections present with substantive content |
| 2 | Technical Depth | High-level only, no implementation detail | Some depth, key areas thin | Full implementation detail — schemas, algorithms, config values |
| 3 | Structure | Inconsistent headings, poor flow | Logical but some weak transitions | Clear hierarchy, ToC-navigable, each section builds on prior |
| 4 | Clarity | Ambiguous language, undefined terms | Mostly clear, some jargon | Precise, defined terms, consistent language throughout |
| 5 | Correctness | Wrong facts, missing field types | Mostly correct, minor errors | All technical claims verified against source code |
| 6 | Traceability | No connection between requirements and design | Some cross-references | Explicit requirement → design decision mapping |
| 7 | Formatting | Tables malformed, inconsistent style | Tables present, minor issues | Consistent tables, captions, code blocks, WHOOP style |
| 8 | Decision Quality | Decisions stated without rationale | Some rationale present | All key decisions include quantitative rationale (percentages, statistical derivations, clinical benchmarks) |
| 9 | Writing Style | Terse tables only, no prose, no embedded rationale | Mix of prose and tables; some rationale deferred | Prose-first for each algorithm check; rationale embedded inline; consistent passive voice; matches gold standard register |

### Step 3c — Write Comparison Report

Write to `/tmp/<slug>_calibration_report.md` and copy to `$SKILL_DIR/resources/calibration_report.md`.

The report must include:
1. **Score table** — dimension × score × gold behavior × generated behavior × gap description
2. **Section-by-section comparison** — for each section in the gold standard: presence in generated doc, depth comparison, key differences. For each section in the generated doc NOT in the gold standard: flag it.
3. **Prioritized improvements** — ordered list of concrete SKILL.md changes, most impactful first. For each: which section to change, the current text, and the proposed replacement.

### Step 3d — Update SKILL.md

Apply at most **5 targeted changes** per calibration run. Priority order:
1. Dimensions scoring ≤ 3/5
2. Sections in gold standard but missing from generated doc → add to Part 2b section list
3. Sections in generated doc but absent from gold standard → change to "Omit by default" in Part 2b

Do not modify sections scoring 4/5 or higher unless required to fix a ≤3/5 issue.

**Dimension → SKILL.md section mapping:**

| Low-scoring dimension | Target section |
|----------------------|----------------|
| Completeness | Part 2b — add missing section or strengthen "Key Content" |
| Technical Depth | Phase 2 Quality Standards — add depth criterion |
| Structure | Part 2b Algorithm Description row — clarify subsection expectations |
| Clarity | Phase 2 Quality Standards — add clarity rule |
| Correctness | Phase 1 Extraction Checklist — add verification step |
| Traceability | Part 2b RTM row or Algorithm Description row |
| Formatting | Content Guidelines — add formatting rule |
| Decision Quality | Phase 1 Extraction Checklist or Part 2b Algorithm row |

After applying changes, append a new entry to the CALIBRATION LOG at the bottom of this file.

---

## CONTENT SCHEMA

Full schema for the content JSON written to `/tmp/<slug>_sds_content.json`:

```json
{
  "doc_id": "XYZ1-001",
  "title": "WHOOP <Algorithm> Design Specification",
  "algo_version": "1.0",
  "date": "YYYY-MM-DD",
  "approvers": [
    {"role": "Algorithm Owner", "name": "[REQUIRES HUMAN INPUT]"},
    {"role": "SaMD Reviewer",   "name": "[REQUIRES HUMAN INPUT]"}
  ],
  "sections": [
    {
      "number": "1",
      "title": "Section Title",
      "paragraphs": ["Body text paragraph 1.", "Body text paragraph 2."],
      "figures": [],
      "tables": [],
      "code_blocks": [],
      "subsections": [
        {
          "number": "1",
          "title": "Subsection Title",
          "paragraphs": [],
          "figures": [],
          "tables": [],
          "code_blocks": [],
          "subsections": []
        }
      ]
    }
  ],
  "revision_history": [
    {"version": "1.0", "date": "YYYY-MM-DD", "description": "Initial release", "author": "..."}
  ]
}
```

**Table object:**
```json
{
  "caption": "Table N-M. Description",
  "headers": ["Field", "Type", "Required", "Description"],
  "rows": [["field_name", "string", "Yes", "Description of field"]],
  "col_widths": [1.5, 1.0, 0.8, 3.2]
}
```
`col_widths` in inches; should sum to ≤ 6.5.

**Terms and Definitions table:**
```json
{
  "caption": "Table 3-1. Terms and Definitions",
  "headers": ["Term", "Definition"],
  "rows": [["AFib", "Atrial fibrillation — ..."]],
  "col_widths": [1.5, 5.0]
}
```

**RTM table (Appendix A):**
```json
{
  "caption": "Table A-1. Requirements Traceability Matrix",
  "headers": ["Requirement ID", "Requirement Summary", "Implementing Section(s)"],
  "rows": [["FR-001", "...", "Section 6.3"]],
  "col_widths": [1.2, 3.3, 2.0]
}
```

**Code block object:**
```json
{"label": "Example Request", "code": "{\n  \"field\": \"value\"\n}"}
```

**Figure — Confluence image (preferred):**
```json
{
  "type": "image",
  "path": "~/.claude/skills/generate-sds/resources/images/<slug>/filename.png",
  "caption": "Figure N-M. Description",
  "width": 5.5
}
```

**Figure — auto-generated architecture:**
```json
{
  "type": "architecture",
  "title": "System Architecture",
  "caption": "Figure N-M. Description",
  "components": [
    {"label": "Service A", "sub": "Python", "x": 2.0, "y": 2.5, "color": "#2E75B6"},
    {"label": "Service B", "sub": "Go",     "x": 5.5, "y": 2.5, "color": "#1F3763"}
  ],
  "flows": [
    {"from": 0, "to": 1, "label": "REST"},
    {"from": 1, "to": 0, "label": "response"}
  ]
}
```

**Figure — auto-generated state machine:**
```json
{
  "type": "state_machine",
  "title": "State Transitions",
  "caption": "Figure N-M. Description",
  "states": ["STATE_A", "STATE_B", "STATE_C"],
  "transitions": [
    {"from": "STATE_A", "to": "STATE_B", "label": "trigger"},
    {"from": "STATE_B", "to": "STATE_C", "label": "trigger"}
  ]
}
```

---

## CONTENT GUIDELINES

- **Evidence-only.** Include only information observed in code, docs, or Confluence. Mark gaps: `[REQUIRES HUMAN INPUT: describe what's needed]`.
- **Algorithm section follows execution order.** Do not reorganize by category — follow the actual pipeline execution order.
- **Mathematical precision for DQ checks.** State exact thresholds as inequalities, not prose.
- **JSON schemas as tables.** Every request/response field gets a row. Include nested objects as sub-tables.
- **JSON examples as code_blocks.** Full example in `code_blocks`, not in paragraphs.
- **Edge cases as tables.** Columns: Scenario | Behavior | Notes.
- **Prefer real Confluence images** over auto-generated diagrams. Auto-generate only when no Confluence diagram exists.
- **Architecture diagram.** Include when system has 3+ components.
- **State machines.** Include for any field with an enum that transitions over time.
- **Decision rationale (mandatory for all thresholds).** For every algorithmic threshold and classification rule, search code comments, docstrings, AND related design documents (anomaly reports, training plans) for QUANTITATIVE justification — specific percentages, statistical derivations, clinical benchmarks. Quote the exact language found (e.g., "more than 99.5% of AFib-positive training epochs exceeded this threshold"; "suppresses the false positive rate by a factor of more than 2,000"). If no quantitative rationale is found after re-reading the source class and referenced docs, mark [REQUIRES HUMAN INPUT: provide quantitative justification for <threshold>]. Never replace rationale with a generic description of what the threshold does.
- **No extra sections.** Only include sections from the approved rows in Part 2b.

---

## FORMATTING REFERENCE

All formatting is inherited from `whoop_sds_template.docx`. These values are baked in:

| Element | Value |
|---------|-------|
| Body font | Arial 10pt |
| H1/H2 heading color | `#2F5496` (blue) |
| H3 heading color | `#1F3763` (navy) |
| Table header fill | `#F2F2F2` (light gray) |
| Table alt row fill | `#EFEFEF` |
| Table border color | `#000000` (black, single) |
| Code block background | `#F6F8FA` |
| Code font | Courier New 8.5pt |

---

## RESOURCES

```
resources/
├── generate_sds.py          # docx engine: content.json → .docx  (DO NOT MODIFY)
├── extract_images.py        # saves Confluence images from session transcript
├── read_docx.py             # extracts structured text from .docx for validation
├── whoop_sds_template.docx  # stripped ANF template (preserves all styles)
└── images/
    └── <slug>/              # downloaded Confluence diagram PNGs (gitignored)
```

Dependencies: `python-docx`, `matplotlib`
```bash
pip3 install python-docx matplotlib
```

---

## CALIBRATION LOG

*(Append new entries below after each calibration run. Do not delete prior entries.)*

### Entry 1 — 2026-04-17
**Gold standard:** ANF1-010 WHOOP Arrhythmia Notification Feature (ANF) — Classification Algorithm Design Specification
**Scores:** Completeness 3/5, Technical Depth 4/5, Structure 3/5, Clarity 4/5, Correctness 5/5, Traceability 4/5, Formatting 4/5, Decision Quality 3/5 — **Total: 30/40**
**Changes applied:**
1. Added "Terms and Definitions" as required section (Always for SaMD)
2. Added "Appendix A — Requirements Traceability Matrix" as required section (Always for SaMD)
3. Algorithm Description row rewritten to require named subsections in execution order, including HWM update, EH update, and threshold justifications from code comments
4. Extraction checklist: added threshold justification search step and SOP/design-doc ID identification
5. References row: strengthened to require internal SOPs and design document IDs
6. All 11 sections not in gold standard changed to "Omit by default"
7. References moved to section 2 (matches gold standard placement)
8. Removed multi-agent framing; skill is now a single sequential three-phase workflow

### Entry 2 — 2026-04-17
**Gold standard:** ANF1-010 (same — second calibration run with SRS input and improved generation)
**Inputs:** WhoopInc/data-sci-anf-service + ANF1-003 SRS
**Scores (9 dimensions):** Completeness 3/5, Technical Depth 4/5, Structure 4/5, Clarity 4/5, Correctness 3/5, Traceability 4/5, Formatting 4/5, Decision Quality 2/5, Writing Style 3/5 — **Total: 31/45**
**Changes applied:**
1. Decision Quality: replaced rationale bullet in Content Guidelines with mandatory quantitative-rationale requirement (quote exact language, percentages, statistical derivations)
2. Writing Style: added prose-first guideline to Phase 2 Quality Standards (passive voice, rationale embedded inline, not deferred)
3. Correctness (DQ): added checklist item to count all DQ checks including out-of-range value checks
4. Correctness (gap): strengthened gap handling subsection to require BOTH trigger conditions (epoch history criterion AND time gap criterion)
5. Correctness (logging): added checklist item to find actual log retention period from config, not SRS minimum; added Writing Style as 9th scoring dimension in Phase 3
