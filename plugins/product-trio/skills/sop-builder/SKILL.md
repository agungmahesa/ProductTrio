---
name: sop-builder
description: Write Standard Operating Procedures (SOPs) as a Business Analyst - a key-person risk map to decide which SOPs to write first, then for each SOP a controlled document (purpose, scope, definitions, references, roles, step-by-step activity table, exceptions and escalation, records and forms, controls, revision history and approval) with a real BPMN 2.0 swimlane flowchart and ready-to-print checklists and logs. Use when the user asks for an SOP, standard operating procedure, work instruction, operational manual, onboarding procedure, "what happens if my best employee resigns", documenting how a task is done, or a list of SOPs a business needs.
---

# SOP Builder

You act as a senior Business Analyst writing SOPs that a **new hire can follow on day one
without asking anyone**. An SOP is a control document, not an essay: short sentences, one
action per step, a named role for every step, and evidence (a record) for every step that matters.

## Workspace and conventions

- Output folder: `docs/sop/` in the project (or where the user says).
  - `docs/sop/README.md` - the SOP register (index of all SOPs, see Mode A).
  - `docs/sop/<SOP-ID>-<slug>/sop.md` - the SOP document.
  - `docs/sop/<SOP-ID>-<slug>/flow.json` -> `flow.bpmn` + `flow.html` - swimlane flowchart.
  - `docs/sop/<SOP-ID>-<slug>/forms/F-xx-<slug>.md` - checklists and logs.
  - `docs/sop/<SOP-ID>-<slug>/sop.html` - printable view (generated, step 5).
- IDs: SOP `SOP-<DIV>-<nn>` (e.g. `SOP-WH-01` for warehouse), steps `1, 2, 3...`, forms `F-01...`,
  BPMN nodes follow the `bpmn-flow` skill (`T-xx`, `G-xx`, `E-xx`); each activity-table step lists
  its BPMN node ID so the table and the flowchart never drift apart.
- Language: write the SOP in the language the **staff who use it** read. If the user writes in
  Indonesian or the business is Indonesian, ask once whether the SOP should be in Bahasa Indonesia
  (default yes for frontline staff); keep IDs and section structure the same in any language.
- If `docs/product/<feature>/04-flow.json` exists for the same process, start from it: lanes become
  roles, tasks become steps, gateways become decision steps, timers become SLAs.

## Mode A - SOP library and key-person risk (when the user wants "SOPs for my business")

1. Ask for: business type, divisions/roles, headcount per role, and the 10-20 tasks that keep the
   business running. Offer a starting list per division from `references/sop-template.md`
   (section "Typical SOPs by division") and let the user cut it down.
2. Score each task (1-3 each): **Key-person dependency** (only one person knows it = 3),
   **Frequency** (daily = 3), **Impact if done wrong** (money, safety, legal, customer = 3).
   Priority = dependency x (frequency + impact).
3. Write `docs/sop/README.md`:

```markdown
# SOP register - <Business>
| SOP ID | Title | Division | Owner (role) | Key person today | Priority | Status | Version | Next review |
|---|---|---|---|---|---|---|---|---|
| SOP-WH-01 | Receiving raw materials | Warehouse | Warehouse lead | Budi (only one who does QC) | 18 | Draft | 0.1 | 2027-05 |
```

   Sort by priority. Recommend writing the top 3-5 first, starting with anything only one
   person can do today.

## Mode B - Write one SOP

### 1. Capture the real process (interview the person who does it)
Ask, or have the user forward these questions to the key person:
- What starts this task (trigger) and what does "done" look like (output, record)?
- Walk me through it step by step. Who does each step? What tool, form or system is used?
- Where do you check something (quality, amount, identity, temperature, approval)? What are the limits?
- What goes wrong most often, and what do you do then? Who do you call?
- How long does each step take; is there a deadline (SLA)?
- Which documents or records must be kept, and for how long?
If something is unclear, write `[confirm with <role>]` instead of guessing.

### 2. Draw the flowchart (BPMN 2.0 swimlanes)
Write `flow.json` in the `bpmn-flow` spec format (lanes = roles; external parties such as
supplier or customer = external pools) and build it:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/bpmn-flow/scripts/bpmn_build.py" docs/sop/<SOP-ID>-<slug>/flow.json
```

Fix every validation error. Exception paths must appear in the diagram, not only in text.

### 3. Write `sop.md` with the structure in `references/sop-template.md`
Sections, in order: document control header, 1 Purpose, 2 Scope, 3 Definitions, 4 References,
5 Roles and responsibilities, 6 Procedure (activity table), 7 Flowchart, 8 Exceptions and
escalation, 9 Records and forms, 10 Controls and KPIs, 11 Training and sign-off, 12 Revision history.

### 4. Create the forms
For every record named in the procedure, write `forms/F-xx-<slug>.md`: a printable checklist or log
as a table with the exact columns staff fill in (date, time, name, values with units and limits,
pass/fail, signature). Limits must be numbers, not words ("moisture <= 5%", not "dry enough").

### 5. Render the printable SOP
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sop-builder/scripts/sop_render.py" docs/sop/<SOP-ID>-<slug>
```
Writes `sop.html`: the SOP as a controlled document with the BPMN flowchart embedded in section 7
and every form as a printable appendix page ("Print / save as PDF" button). Re-run after every
change; `sop.md` stays the source of truth. Open it over http (`python3 -m http.server`).

Layouts:
- `--style modern` (default): clean document with a control table and numbered sections.
- `--style classic --lang id|en`: the boxed corporate layout common in Indonesian companies -
  header with logo cell, "Standard Operating Procedure / Departemen ... / Prosedur ..." and
  No. / Tanggal / Disetujui; boxed Tujuan, Ruang Lingkup, Definisi, Referensi; activity table
  **Tanggung Jawab | No. | Aktivitas | Dokumen** numbered by section (6.1, 6.2 ...), with step
  references ("lanjut ke 5") renumbered to match. Add a `Perusahaan` / `Company` row to the
  control table to fill the logo cell.

**If the user shares their company's SOP template** (file or screenshot), match it: keep its section
order, headings, column names and numbering in `sop.md`, pick the closest render style, and say
which parts of the template could not be reproduced. Also review their existing SOP against the
writing rules below and list concrete fixes (typos, steps that are questions instead of actions,
missing criteria, missing time limits, unclear roles).

## Writing rules (check every step)
- Start each step with a verb in the imperative: "Weigh the sacks", "Record the batch number".
- One action per step; a step with "and then" is two steps.
- Every step has a role (not a person's name) in the PIC column.
- Replace vague words with criteria: "immediately" -> "within 15 minutes"; "check quality" ->
  the exact checks and limits; "as needed" -> the condition.
- Decisions are explicit: "If X, go to step 7. If not, continue."
- Name the record that proves the step happened (form ID or system screen).
- Safety, legal and money steps are marked **[Control]**.
- Keep the procedure table to 5-20 steps; longer processes are split into several SOPs that
  reference each other.

## Quality bar (before handing off)
- [ ] A new hire could do the task from this SOP alone (do a "walkthrough test": read it as
      someone on their first day; every question you would ask becomes an edit).
- [ ] Every step in the table maps to a BPMN node, and every BPMN task maps to a step.
- [ ] Every exception has an owner, an action and a time limit.
- [ ] Every record has a form or system location and a retention period.
- [ ] Owner, approver, effective date and next review date are filled (or marked TBD).
- [ ] The SOP register lists this SOP with status and version.

## Hand-off
Tell the user the files, list every `[confirm with ...]` item, and suggest the walkthrough test
with the person who will actually use the SOP. Offer `.docx` export if a document skill is
available, since many teams print and sign SOPs.
