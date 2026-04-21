# ANF SDS Calibration Report — Entry 2

**Date:** 2026-04-17
**Gold standard:** ANF1-010 — WHOOP ANF Classification Algorithm Design Specification
**Generated doc:** ~/Downloads/anf_SDS.docx (777 KB, 438 lines)
**Inputs used:** WhoopInc/data-sci-anf-service + ANF1-003 SRS

---

## Score Table (9 Dimensions)

| # | Dimension | Score | Gold Behavior | Generated Behavior | Gap |
|---|-----------|-------|---------------|--------------------|-----|
| 1 | Completeness | 3/5 | All 5 DQ checks including out-of-range values; 2-condition gap trigger; response schema with 13 fields; SBOM ref; 30-day log retention | Missing: 5th DQ check (out-of-range); gap criterion #1 (epoch history); response schema missing git_commit_id / build_number / ff_spec / epoch_classifications / prelim label; log retention = 14 days (should be 30) | Multiple fields and criteria absent |
| 2 | Technical Depth | 4/5 | Clinical rationale in prose per DQ section; feature list delegated to ANF1-011; startup as prose not table | DQ threshold tables strong; HWM formulas with source constants; config table complete; feature table present | Feature table is an addition; minor depth gap in DQ prose |
| 3 | Structure | 4/5 | Flat heading style, no numbering, section names as prose headings | Numbered sections, ToC, hierarchical subsections — more navigable | Generated structure is better; no deficit |
| 4 | Clarity | 4/5 | Precise passive constructions ("An epoch is determined to have X if…"); rationale embedded inline after criterion | Direct and clear; some descriptions abbreviated; terms defined in glossary but not inline | Minor abbreviation |
| 5 | Correctness | 3/5 | 30-day log retention (AWS Elasticsearch); gap = epoch history with ≥30 ID events AND ≥1h time gap; 5 DQ checks | Log retention = 14 days (WRONG); gap condition #1 absent; 5th DQ check absent | Three factual errors verified against gold |
| 6 | Traceability | 4/5 | RTM with section refs only (no summaries); includes CLOUD-003-001, CLOUD-004-003, CLOUD-005-015, CLOUD-005-017 | RTM has summaries + section refs (richer); missing CLOUD-003-001, CLOUD-004-003, CLOUD-005-015, CLOUD-005-017 | 4 requirement IDs absent |
| 7 | Formatting | 4/5 | Tables for schemas; inline flowchart figures; no code examples | Numbered tables, code blocks, captions, consistent style | Minor: example request rendered in table, not code_block |
| 8 | Decision Quality | 2/5 | Quantitative rationale for ALL thresholds: MeanDiffLag1 ">99.5% of AFib-positive training epochs exceeded 80ms"; Window 25/30 "suppresses false positive rate by factor >2,000 vs. 1-in-million/year baseline"; two-stage architecture rationale | Most DQ thresholds marked [REQUIRES HUMAN INPUT]; window 25/30 rule in table with no rationale; MeanDiffLag1 called "HRV proxy" with no quantitative basis | CRITICAL: quantitative decision rationale entirely absent for multiple thresholds |
| 9 | Writing Style | 3/5 | Prose-first: each DQ check is a full paragraph with criteria stated in prose and rationale embedded inline; passive voice throughout | Table-first: each DQ check is a parameter table; rationale deferred to [REQUIRES HUMAN INPUT]; less clinical narrative | Style inverted: gold embeds rationale in prose; generated uses tables and defers rationale |

**Total: 31/45**

---

## Section-by-Section Comparison

### Sections in Gold Standard

| Gold Section | In Generated | Depth | Key Differences |
|---|---|---|---|
| Purpose | Yes §1 | Comparable | Generated adds audience statement — acceptable addition |
| References | Yes §2 | Gap | Gold: ANF1-001, ANF1-003, ANF1-038, DCR-003, ANF1-040, IEC 62304, SOP-003, SOP-027. Generated: adds ANF1-002, ANF1-011, ANF1-031; missing ANF1-038, DCR-003, ANF1-040 |
| Terms and Definitions | Yes §3 | Over-expanded | Gold: 4 terms. Generated: 20 terms. Gold is minimal |
| Initialization | Yes §4 | Different format | Gold: prose with SBOM ref (ANF1-019). Generated: 7-row table. Gold mentions "model artifact included in source code of the device" |
| Principles of Operation | Yes §6.1 | Gold richer | Gold explains clinical rationale: why 1-min epochs (Paroxysmal AFib), why 30-min windows (exponential FP suppression). Generated omits |
| Time Periods Labeled | Yes §6.2 | Gold richer | Gold has 3 worked examples with specific times. Generated has 1 |
| Input Schema | Yes §7.1 | Different | Gold: afib_classification_history as nested object; fw_version/hw_version/dsp_version in request; Diagnostic Tool field. Generated matches code API |
| DQ: Low Motion | Yes §6.3.1–2 | Split into 2 | Gold treats as 1 check; generated splits accel diff + accel mag. Functionally correct |
| DQ: Signal Quality | Yes §6.3.3 | Partial | Gold describes sig_error bit extraction (bit 13 = LowQualityLowSignal, bit 7 = HighFreqHighNoise). Generated omits bit detail |
| DQ: RR Floor | Yes §6.3.5 | Comparable | Both include threshold rationale from code comments |
| DQ: RR Coverage | Yes §6.3.4 | Comparable | Both state 75% / 135 s criterion |
| DQ: Out-of-range values | **ABSENT** | — | Gold 5th check: epoch fails if any metric data has beat-to-beat interval or acceleration outside expected range. Entirely absent from §6.3 |
| Epoch Classification | Yes §6.4 | Different emphasis | Gold: brief prose, delegates feature list to ANF1-011. Generated: full feature table. Gold post-processing has quantitative MeanDiffLag1 rationale (>99.5%); generated says "HRV proxy" |
| Window Classification | Yes §6.5 | Missing rationale | Gold: full statistical rationale for 25/30 (1-in-million/year FP rate, 2000x suppression). Generated: rules table only |
| High-Water Marks | Yes §6.6 | Comparable | Formulas mathematically equivalent (window_end − 29 min = window_start + 1 min) |
| Epoch History Update | Yes §6.7 | Comparable | Both correct |
| Gap Handling | Yes §6.8 | Incomplete | Generated states only the ≥1h time gap condition. Missing condition #1: epoch history must contain ≥30 Insufficient Data events |
| Output Schema | Yes §7.2 | Simplified | Generated missing: git_commit_id, build_number, ff_spec, epoch_classifications (count array), window_classification_label_prelim, processed_time |
| Logging | Yes §8 | Missing details | Gold: AWS Elasticsearch, 30-day retention, specific fields per event. Generated: 14-day (WRONG), generic descriptions |
| Exceptions | Yes §9 | More structured | Generated adds HTTP status codes and class names — richer than gold |
| RTM | Yes §A | Format better | Generated adds requirement summaries. Missing CLOUD-003-001, CLOUD-004-003, CLOUD-005-015, CLOUD-005-017 |

### Sections in Generated NOT in Gold Standard

| Section | Decision |
|---|---|
| §5 System Architecture | Auto-diagram is acceptable filler; gold has inline prose diagrams |
| §10 Configuration | Absent from gold; useful but omit by default per calibration rules |
| §11 Edge Cases | Absent from gold; omit by default |

---

## Prioritized Improvements (ordered by impact)

### Change 1 — Decision Quality: require quantitative threshold rationale
**Dimension:** Decision Quality (2/5)
**SKILL.md location:** Phase 2 Quality Standards
**Current text:** "For algorithm thresholds and architectural decisions, include the justification found in code comments. If none found, mark [REQUIRES HUMAN INPUT: justify this value]."
**Problem:** Generated marks all DQ thresholds [REQUIRES HUMAN INPUT] except the RR floor. Gold has full quantitative rationale for every threshold (99.5% training data stat, 1-in-million/year FP, 2000x suppression). The skill must require more thorough search and mandate quoting the actual wording.
**Replacement:**
> "**Decision rationale (mandatory for all thresholds).** For every algorithmic threshold and classification rule, search code comments, docstrings, AND related design documents (anomaly reports, training plans) for QUANTITATIVE justification — specific percentages, statistical derivations, clinical benchmarks. Quote the exact language found (e.g., 'more than 99.5% of AFib-positive training epochs exceeded this threshold'; 'suppresses the false positive rate by a factor of more than 2,000'). If no quantitative rationale is found after re-reading the source class and any referenced docs, mark [REQUIRES HUMAN INPUT: provide quantitative justification for <threshold>]. Never replace rationale with a generic description of what the threshold does."

### Change 2 — Writing Style: add prose-first pattern for Algorithm Description
**Dimension:** Writing Style (3/5)
**SKILL.md location:** Phase 2 Quality Standards (new bullet)
**Current text:** (no writing style guidance)
**Proposed addition:**
> "**Writing style (Algorithm Description).** Match gold standard's prose-first pattern: describe each DQ check and classification rule in a complete prose paragraph ('An epoch is determined to have X if the following criteria are met: …'), then use a parameter table for values only. Embed decision rationale directly in the prose immediately after the criterion statement, do not defer it to a separate [REQUIRES HUMAN INPUT] block. Use consistent passive voice: 'An epoch is determined to…', 'The epoch is labeled…', 'A window is assigned…'."

### Change 3 — Correctness: add 5th DQ check (out-of-range values) to extraction checklist
**Dimension:** Correctness (3/5)
**SKILL.md location:** Phase 1 Extraction Checklist
**Current text:** "For each DQ threshold and algorithm parameter: searched source code and inline comments for justification."
**Addition:**
> "- DQ check count: read the full DQ assessment class and confirm every distinct condition that can label an epoch Insufficient Data — including any out-of-range value checks (beat-to-beat intervals outside expected bounds, acceleration values outside expected bounds). These are separate named checks."

### Change 4 — Correctness: gap handling requires two conditions
**Dimension:** Correctness (3/5)
**SKILL.md location:** Part 2b, Algorithm Description row, item (9) Gap handling
**Current text:** "Gap handling"
**Replacement:**
> "(9) Gap handling — state BOTH trigger conditions: (a) epoch history contains ≥30 Insufficient Data events AND (b) ≥1h between classification HWM and first metric packet; behavior (single INSUFFICIENT_DATA window spanning the gap); cascading effect across successive requests."

### Change 5 — Correctness: log retention from actual config, not SRS minimum
**Dimension:** Correctness (3/5)
**SKILL.md location:** Phase 1 Extraction Checklist
**Current text:** (no log retention step)
**Addition:**
> "- Log storage: find the actual log storage system (Elasticsearch, CloudWatch, Datadog, etc.), the actual configured retention period in days, and the specific fields logged per event type. Do not repeat the SRS requirement floor — find the actual configured value in source code or infrastructure config."
