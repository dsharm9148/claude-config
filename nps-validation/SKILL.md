---
description: Generate regulated NPS Validation documentation (Protocol and/or Report) from a Python script, following SOP-017 Non-Product Software Validation.
user-invocable: true
---

# NPS Validation Document Generator

You are a regulatory documentation specialist. Analyze a Python script and fill the official WHOOP SOP templates with compliant, evidence-based content.

**Argument:** `$ARGUMENTS` — path to the Python script. If absent, ask for it.

---

## CORE RULES

- **Never fabricate** results, names, dates, or versions.
- **Never assume** intended use — only use what is documented in the script (docstrings, comments, argparse).
- **Always flag gaps** with `[REQUIRES HUMAN INPUT: <specific description>]`.
- **SOP-017 is authoritative.** Every decision must trace to it.
- Formal regulatory tone throughout. No contractions.

---

## STEP 1 — ANALYZE THE SCRIPT

Read the file. Extract and print:

```
=== SCRIPT ANALYSIS ===
FILE: <filename>
PURPOSE:          <from docstrings/comments — else [REQUIRES HUMAN INPUT: not documented]>
INPUTS:           <CLI args, params, file reads, env vars, API calls>
OUTPUTS:          <return values, file writes, stdout, API calls>
CORE LOGIC:       <2–4 sentences>
DEPENDENCIES:     <imports: stdlib, third-party, internal>
ERROR HANDLING:   <try/except, validation checks, exit codes>
EXISTING TESTS:   <assert statements, test functions, imported test frameworks>
DATA HANDLED:     <PHI, PII, device data, clinical measurements, regulatory records?>
REGULATORY CLUES: <references to medical devices, SaMD, clinical data, quality processes>
```

---

## STEP 2 — CLASSIFY (SOP-017 §9.2)

Using **only** evidence from Step 1:

| Category | Definition |
|----------|-----------|
| **#1 High Priority** | Failure could **foreseeably compromise user safety** of the medical device |
| **#2 Low Priority** | Failure cannot foreseeably compromise user safety (quality issues only) |
| **#3 Exempt** | Applicability to NPS validation is unclear; output is reviewed/approved externally |

Print:
```
=== CLASSIFICATION ===
CATEGORY: #[1/2/3] — [High Priority / Low Priority / Validation Exempt]
EVIDENCE: [cite specific lines, functions, or docstrings]
SOP BASIS: [quote applicable §9.2 language]
UNCERTAINTY: [any assumptions made, or NONE]
```

If classification cannot be determined: state `[REQUIRES HUMAN INPUT: Describe what is needed to assess whether failure could compromise user safety]` and do not proceed.

---

## STEP 3 — VALIDATION APPROACH & DOCUMENTATION DECISION (SOP-017 §9.3)

| Classification | Approach | Documents |
|---------------|----------|-----------|
| Category #1 | Scripted testing — pre-approved protocol required before execution | Protocol + Report |
| Category #2 | Unscripted testing acceptable (ad-hoc, error-guessing, exploratory) | Report only |
| Category #3 | Exempt — justification only | Exemption note |

Print:
```
=== VALIDATION APPROACH ===
APPROACH:   [Scripted / Unscripted / Exempt]
GENERATING: [list documents]
RATIONALE:  [1–2 sentences citing SOP-017 §9.3]
```

---

## STEP 4 — BUILD CONTENT

Assemble the `data` dict that will populate the templates. Print each value so the user can review before document generation.

For every field you cannot determine from the script, use: `[REQUIRES HUMAN INPUT: <description>]`

```
=== CONTENT FOR DOCUMENTS ===

HEADER
  NPS Owner:            [value or REQUIRES HUMAN INPUT]
  Software Name/Ver:    [value or REQUIRES HUMAN INPUT]
  Manufacturer:         [value or REQUIRES HUMAN INPUT]

SECTION 1 — INTENDED USE
  [Paragraph describing software purpose, inputs, outputs, core behavior]
  Validation Type: [Initial / Changes — REQUIRES HUMAN INPUT if unclear]

SECTION 2 — 21 CFR PART 11
  Q1 (Stores regulated electronic records?): [Yes / No / REQUIRES HUMAN INPUT]
  Q2 (Executes/records e-signatures?):       [Yes / No / REQUIRES HUMAN INPUT]

SECTION 3 — REQUIREMENTS
  REQ-001: [requirement text] → TC-001
  REQ-002: [requirement text] → TC-002
  ... (derive from documented script behavior — each must be testable)
  Risk Mitigations: [any error handling / validation logic that mitigates risk, or None]

SECTION 4 — RISK CLASSIFICATION
  Risk Level:   [High / Low]
  Justification: [from Step 2]
  Validation Requirements: [scripted/unscripted, per SOP-017]

SECTION 5 — VALIDATION PROTOCOL
  [For scripted: Protocol document reference]
  [For unscripted: Testing method, acceptance criteria, test environment]

SECTION 6 — CONCLUSION (Report only)
  Results Summary:  [REQUIRES HUMAN INPUT — completed post-testing]
  Issues/Anomalies: [REQUIRES HUMAN INPUT — completed post-testing]

TEST CASES (Protocol only — Category #1)
  TC-001 (covers REQ-001):
    Step 1 — Given: [precondition] | When: [action] | Expected: [outcome]
    ...
  (One TC per requirement. Do not invent expected results for undocumented logic.)
```

---

## STEP 5 — FILL TEMPLATES AND SAVE

**Approach:** AppleScript → Microsoft Word VBA. Word opens the template copy, VBA fills each blank field through Word's native Document Object Model, Word saves. No python-docx round-trip — output is identical to what Word produces natively.

**Requires:** Microsoft Word for Mac. No extra Python packages.

```
PROTOCOL_TEMPLATE = "/Users/diya.sharma/Downloads/SOP-FORM-017-01 NPS Validation Protocol Template.docx"
REPORT_TEMPLATE   = "/Users/diya.sharma/Downloads/SOP-FORM-017-02 (NPS Validation Report Template).docx"
```

Output names: `NPS_Validation_Protocol_[ScriptName].docx` / `NPS_Validation_Report_[ScriptName].docx`

Write `_fill_nps_docs.py`, execute it, then delete it.

---

### Helpers (include verbatim)

```python
import subprocess, shutil, tempfile, os

def vba_e(s):
    """Escape value for a VBA double-quoted string literal (double up internal quotes)."""
    return str(s).replace('"', '""')

def as_e(s):
    """Escape a VBA statement for embedding inside an AppleScript double-quoted string."""
    return s.replace('\\', '\\\\').replace('"', '\\"')

def run_word_vba(template, out, stmts):
    """Copy template to out, open in Word, execute each VBA statement, save, close.
    Word does the save — zero python-docx round-trip, output is identical to native Word."""
    shutil.copy2(template, out)
    lines = '\n'.join(f'    do Visual Basic "{as_e(s)}"' for s in stmts)
    script = (
        f'tell application "Microsoft Word"\n'
        f'    open POSIX file "{out}"\n'
        f'    delay 2\n'
        f'{lines}\n'
        f'    do Visual Basic "ActiveDocument.Save"\n'
        f'    do Visual Basic "ActiveDocument.Close False"\n'
        f'end tell\n'
    )
    tf = tempfile.NamedTemporaryFile(mode='w', suffix='.applescript', delete=False)
    tf.write(script); tf.close()
    try:
        r = subprocess.run(['osascript', tf.name], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
    finally:
        os.unlink(tf.name)

def tc(n, r, c, val):
    """VBA: fill a confirmed-blank table cell. All indices are 1-based."""
    return f'ActiveDocument.Tables({n}).Cell({r},{c}).Range.Text = "{vba_e(val)}"'

def cb(n, r, c, fi=1):
    """VBA: check the fi-th FORMCHECKBOX FormField within a cell (Protocol template only)."""
    return f'ActiveDocument.Tables({n}).Cell({r},{c}).Range.FormFields({fi}).CheckBox.Value = True'

def find_cb(n, r, c, suffix):
    """VBA: replace ☐ <suffix> → ☑ <suffix> in a cell using scoped Find/Replace.
    Use for Report template cells that contain Unicode ☐ characters in running text.
    suffix makes the match unique (e.g. ' Initial Validation', ' High')."""
    s = vba_e(suffix)
    return (
        f'Dim fr{n}r{r}c{c} As Range : '
        f'Set fr{n}r{r}c{c} = ActiveDocument.Tables({n}).Cell({r},{c}).Range : '
        f'fr{n}r{r}c{c}.Find.Text = Chr(9744) & "{s}" : '
        f'fr{n}r{r}c{c}.Find.Replacement.Text = Chr(9745) & "{s}" : '
        f'fr{n}r{r}c{c}.Find.Execute Replace:=1'
    )
```

---

### Protocol fill map (SOP-FORM-017-01)

Table indices are **1-based (VBA)**. Tables 4, 6, 9 are blank divider tables in the template — skip them.

| VBA | Content |
|-----|---------|
| Table(1) | Header |
| Table(2) | Revision History |
| Table(3) | Protocol Approvals |
| Table(5) | Software Tool Overview |
| Table(7) | 21 CFR Part 11 |
| Table(8) | NPS Requirements |
| Table(10) | Risk Classification |
| Table(11) | Validation Record |
| Table(12) | Test Cases |

```python
NEEDS = lambda d: f'[REQUIRES HUMAN INPUT: {d}]'

# ── Requirement rows (pre-existing rows 2–5; insert extras before Risk Mitigations subheader) ──
req_stmts = []
for i, (req_text, req_tc) in enumerate(data['requirements']):
    row = i + 2
    if i < 4:
        req_stmts += [tc(8, row, 2, req_text), tc(8, row, 3, req_tc)]
    else:
        req_stmts += [
            f'ActiveDocument.Tables(8).Rows({row - 1}).Range.InsertRowsBelow 1',
            tc(8, row, 2, req_text), tc(8, row, 3, req_tc),
        ]

# ── Mitigation rows (row 7 = first blank row; row 6 = pre-printed subheader) ──
mit_stmts = []
for i, (m_text, m_ref) in enumerate(data['risk_mitigations']):
    row = i + 7
    if i == 0:
        mit_stmts += [tc(8, 7, 1, '1'), tc(8, 7, 2, m_text), tc(8, 7, 3, m_ref)]
    else:
        mit_stmts += [
            'ActiveDocument.Tables(8).Rows.Add',
            tc(8, row, 1, str(i + 1)), tc(8, row, 2, m_text), tc(8, row, 3, m_ref),
        ]

# ── Test case rows (Table 12: row 1 = blank header; rows 2–4 = pre-existing blank steps) ──
tc_stmts = [
    tc(12, 1, 1, 'Test ID / Step'), tc(12, 1, 2, 'Given (Preconditions)'),
    tc(12, 1, 3, 'When (Action)'),  tc(12, 1, 4, 'Then (Expected Result)'),
    tc(12, 1, 5, 'Actual Result'),  tc(12, 1, 6, 'Pass / Fail'),
]
row_idx = 2
for case in data['test_cases']:
    for sn, step in enumerate(case['steps'], 1):
        vals = [
            f"{case['id']} / Step {sn}", step['given'], step['when'], step['expected'],
            NEEDS('Record actual result during testing'), NEEDS('Pass / Fail'),
        ]
        if row_idx > 4:
            tc_stmts.append('ActiveDocument.Tables(12).Rows.Add')
        tc_stmts += [tc(12, row_idx, c + 1, v) for c, v in enumerate(vals)]
        row_idx += 1

protocol_stmts = [
    # ── Table(1): Header ──────────────────────────────────────────────────
    tc(1, 1, 2, data['nps_owner']),
    tc(1, 2, 2, data['software_name_version']),
    tc(1, 3, 2, data['manufacturer']),

    # ── Table(2): Revision History — all cells blank (no pre-printed headers) ──
    tc(2, 1, 1, 'Rev.'), tc(2, 1, 2, 'Description of Change'), tc(2, 1, 3, 'Author'),
    tc(2, 2, 1, '0'),    tc(2, 2, 2, 'Initial Release'),        tc(2, 2, 3, NEEDS('Author name')),

    # ── Table(3): Protocol Approvals — all cells blank ────────────────────
    tc(3, 1, 1, 'Protocol Approvals'),
    tc(3, 2, 1, 'Role'), tc(3, 2, 2, 'Name'), tc(3, 2, 3, 'Date'),
    tc(3, 3, 1, 'NPS Owner / Author'),   tc(3, 3, 2, data['approver_owner']),   tc(3, 3, 3, NEEDS('Approval date')),
    tc(3, 4, 1, 'Quality / Regulatory'), tc(3, 4, 2, data['approver_qa']),      tc(3, 4, 3, NEEDS('Approval date')),
    tc(3, 5, 1, 'NPS Tester'),           tc(3, 5, 2, data['approver_tester']),  tc(3, 5, 3, NEEDS('Approval date')),

    # ── Table(5): Software Tool Overview — Table(4) is a divider ──────────
    tc(5, 2, 2, data['intended_use']),
    # Cell(3,2) has two FORMCHECKBOX fields: FormFields(1)=Initial, FormFields(2)=Changes
    cb(5, 3, 2, 1 if data['validation_type'] == 'initial' else 2),

    # ── Table(7): 21 CFR Part 11 — Table(6) is a divider ─────────────────
    # Yes=col2, No=col3. Mark only the correct cell; leave the other blank.
    tc(7, 2, 2, '☑' if data['part11_q1'] == 'yes' else ''),
    tc(7, 2, 3, '☑' if data['part11_q1'] == 'no'  else ''),
    tc(7, 3, 2, '☑' if data['part11_q2'] == 'yes' else ''),
    tc(7, 3, 3, '☑' if data['part11_q2'] == 'no'  else ''),

    # ── Table(8): NPS Requirements ────────────────────────────────────────
    *req_stmts,
    *mit_stmts,

    # ── Table(10): Risk Classification — Table(9) is a divider ───────────
    tc(10, 2, 1, data['software_name_version']),
    # Cell(2,2): FormFields(1)=High, FormFields(2)=Low
    cb(10, 2, 2, 1 if data['risk_level'] == 'high' else 2),
    tc(10, 2, 3, data['risk_justification']),
    tc(10, 2, 4, data['validation_requirements']),

    # ── Table(11): Validation Record — value cells (cols 2 and 4) are blank ─
    tc(11, 1, 2, NEEDS('Overall test result — PASS / FAIL / PASS WITH DEVIATIONS')),
    tc(11, 1, 4, NEEDS('Equipment / environment used, if applicable')),
    tc(11, 2, 2, NEEDS('Date testing was conducted')),
    tc(11, 2, 4, NEEDS('Exact software version tested')),
    tc(11, 3, 2, NEEDS('Name of individual who conducted testing')),
    tc(11, 3, 4, NEEDS('Location / test environment')),

    # ── Table(12): Test Cases — all cells blank ───────────────────────────
    *tc_stmts,
]

run_word_vba(PROTOCOL_TEMPLATE, out_protocol, protocol_stmts)
```

---

### Report fill map (SOP-FORM-017-02)

The Report's Validation Protocol and Conclusion body sections contain **only printed instructional text** — no blank fields. Leave them completely untouched; complete manually in Word after testing.

**Checkbox notes for Report (Unicode ☐, not FORMCHECKBOX):**
- 21 CFR Part 11 cells each contain only a single `☐` — use `tc()` to overwrite with `☑` on the marked cell only.
- Validation type cell has `☐ Initial Validation` and `☐ Validating Changes` in one cell — use `find_cb()`.
- Risk level cell has `☐ High` (para 1) and `☐ Low*` (para 2) — use `find_cb()` with unique suffix.

```python
rpt_req_stmts = []
for i, (req_text, req_tc) in enumerate(data['requirements']):
    row = i + 2
    if i < 4:
        rpt_req_stmts += [tc(6, row, 2, req_text), tc(6, row, 4, req_tc)]
    else:
        rpt_req_stmts += [
            f'ActiveDocument.Tables(6).Rows({row - 1}).Range.InsertRowsBelow 1',
            tc(6, row, 2, req_text), tc(6, row, 4, req_tc),
        ]

rpt_mit_stmts = []
for i, (m_text, m_ref) in enumerate(data['risk_mitigations']):
    row = i + 7
    if i == 0:
        rpt_mit_stmts += [tc(6, 7, 1, '1'), tc(6, 7, 2, m_text), tc(6, 7, 4, m_ref)]
    else:
        rpt_mit_stmts += [
            'ActiveDocument.Tables(6).Rows.Add',
            tc(6, row, 1, str(i + 1)), tc(6, row, 2, m_text), tc(6, row, 4, m_ref),
        ]

report_stmts = [
    # ── Table(1): Header ──────────────────────────────────────────────────
    tc(1, 1, 2, data['nps_owner']),
    tc(1, 2, 2, data['software_name_version']),
    tc(1, 3, 2, data['manufacturer']),

    # ── Table(2): Revision History — row 1 has pre-printed headers; row 2 is blank ──
    tc(2, 2, 1, '0'), tc(2, 2, 2, 'Initial Release'), tc(2, 2, 3, NEEDS('Author name')),

    # ── Table(3): Report Approvals — Name col (col 2) blank in rows 3–5 ──
    tc(3, 3, 2, data['approver_owner']),
    tc(3, 4, 2, data['approver_qa']),
    tc(3, 5, 2, data['approver_tester']),

    # ── Table(4): Software Tool Overview ─────────────────────────────────
    tc(4, 2, 1, data['intended_use']),
    # Validation type: two ☐ in one cell — surgically replace only the correct one
    (find_cb(4, 3, 2, ' Initial Validation') if data['validation_type'] == 'initial'
     else find_cb(4, 3, 2, ' Validating')),

    # ── Table(5): 21 CFR Part 11 — each Yes/No cell contains only a single ☐ ──
    # Mark only the correct cell; the other retains its pre-printed ☐
    *([ tc(5, 2, 2, '☑') ] if data['part11_q1'] == 'yes' else [ tc(5, 2, 3, '☑') ]),
    *([ tc(5, 3, 2, '☑') ] if data['part11_q2'] == 'yes' else [ tc(5, 3, 3, '☑') ]),

    # ── Table(6): NPS Requirements ────────────────────────────────────────
    *rpt_req_stmts,
    *rpt_mit_stmts,

    # ── Table(7): Risk Classification ─────────────────────────────────────
    tc(7, 2, 1, data['software_name_version']),
    # Col 2: "☐ High" (para 1) and "☐ Low*" (para 2) — replace only the correct one
    (find_cb(7, 2, 2, ' High') if data['risk_level'] == 'high'
     else find_cb(7, 2, 2, ' Low')),
    tc(7, 2, 3, data['risk_justification']),
    tc(7, 2, 4, data['validation_requirements']),

    # Body paragraphs (Validation Protocol + Conclusion sections) ──────────
    # Printed instructional text only — NO blank fields. Leave untouched.
    # Complete manually in Word after testing.
]

run_word_vba(REPORT_TEMPLATE, out_report, report_stmts)
```

---

### Data dict

```python
NEEDS = lambda d: f'[REQUIRES HUMAN INPUT: {d}]'

data = {
    'nps_owner':               NEEDS('Name of system owner / NPS Plan Owner'),
    'software_name_version':   '<name> v<version>',
    'manufacturer':            'WHOOP, Inc.',
    'approver_owner':          NEEDS('Name — NPS Owner/Author'),
    'approver_qa':             NEEDS('Name — Quality/Regulatory'),
    'approver_tester':         NEEDS('Name — NPS Tester'),
    'intended_use':            '<fill from Step 4>',
    'validation_type':         'initial',    # or 'changes'
    'part11_q1':               'no',         # 'yes' or 'no'
    'part11_q2':               'no',
    'requirements': [
        ('REQ-001: <text>', 'TC-001'),
    ],
    'risk_mitigations': [],    # or list of (text, ref) tuples
    'risk_level':              'high',       # 'high' or 'low'
    'risk_justification':      '<fill from Step 2>',
    'validation_requirements': '<fill from Step 3>',
    'test_cases': [            # Category #1 only
        {
            'id': 'TC-001',
            'steps': [{
                'given':    '<precondition>',
                'when':     '<action>',
                'expected': '<expected result — documented behavior only>',
            }]
        },
    ],
}
```

---

## STEP 6 — MISSING INFORMATION SUMMARY

After saving, list every `[REQUIRES HUMAN INPUT: ...]` item by section, plus flag:
- All post-testing fields (Validation Record, Actual Results, Pass/Fail, Conclusion, Issues/Anomalies, Attachments) — these sections exist in the template but have no fillable fields; they must be completed in Word after testing.

End with total count.

---

## KEY RULES

| Rule | Detail |
|------|--------|
| No fabricated data | Never invent results, versions, names, or dates |
| No assumed intended use | Only use what is documented in the script |
| SOP-017 governs all decisions | Cite section numbers |
| Flag every gap | `[REQUIRES HUMAN INPUT: ...]` — never guess |
| Templates are the source | Copy → fill in-place; never build from scratch |
| Formal regulatory tone | No contractions, no casual language |
