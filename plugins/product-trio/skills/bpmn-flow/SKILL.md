---
name: bpmn-flow
description: Model business processes as a Business Analyst using the BPMN 2.0 standard - pools, lanes, events (start/intermediate/end, timer, message, error), task types, gateways (XOR, AND, OR, event-based), sequence and message flows - and output a real .bpmn file (opens in Camunda Modeler, bpmn.io, draw.io), an HTML preview, and a process narrative table. Use when the user asks for a business process, BPMN, process flow, swimlane diagram, as-is / to-be process, workflow, or SOP flow.
---

# BPMN 2.0 Process Flow

You are acting as a senior Business Analyst. You model the process; a script turns
your model into standards-compliant BPMN 2.0 XML with diagram layout, so you never
hand-write coordinates.

## Workspace and conventions

- Read `01-vision.md`, `02-strategy.md`, `03-metrics.md` in `docs/product/<feature-slug>/` if present.
- Outputs (same folder):
  - `04-flow.json` - your process spec (source of truth, edit this to change the diagram)
  - `04-flow.bpmn` - BPMN 2.0 XML with DI (generated)
  - `04-flow.html` - interactive preview with zoom, .bpmn download and SVG export (generated)
  - `04-flow.md` - process narrative (you write it)
- Node IDs: tasks `T-01`, gateways `G-01`, events `E-01` (start/end/intermediate),
  lanes `L-<role>`, external pools `P-<name>`. Downstream skills reference these IDs.
- Write in English.

## Step 1 - Elicit the process

Ask (or infer and log as assumptions):
1. Process name, trigger (what starts it) and the outcome(s) that end it.
2. As-is or to-be? (If both are useful, model as-is first, then to-be with changes highlighted.)
3. Roles involved -> lanes. External parties (customer org, bank, courier) -> external pools.
4. Happy path steps in order, and who does each.
5. Decisions, waiting points (timers, waiting for a message), parallel work, and exceptions
   (rejections, timeouts, cancellations, errors).

## Step 2 - Model with correct BPMN semantics

Read `references/bpmn-cheatsheet.md` when choosing element types. Key rules:
- **Lanes are roles**, not systems or departments-of-one. Automated steps are `serviceTask`s
  in the lane of the role that owns them, or the system is an external pool.
- **Tasks** are named verb + object ("Verify payment"). Pick the type: `userTask` (person using
  software), `manualTask` (no software), `serviceTask` (automated), `sendTask`/`receiveTask`
  (messaging), `businessRuleTask` (decision table), `callActivity` (reusable sub-process).
- **Gateways**: exclusive (XOR, one path), parallel (AND, all paths), inclusive (OR, one or more),
  event-based (first event wins). Splitting XOR/OR gateways are named as a question and every
  outgoing flow is labelled with its condition (or marked `default`). Every AND-split has an AND-join.
- **Events**: one start per trigger; distinct end events per outcome ("Order fulfilled",
  "Order cancelled"). Use timer/message intermediate events for waits.
- **Sequence flow** stays inside the pool; **message flow** crosses pools only.
- Model the exceptions, not just the happy path.
- Keep one diagram readable: 5-30 nodes. Bigger? Split into a top-level process with
  `callActivity` nodes and separate specs per sub-process.

## Step 3 - Write the spec and build

Write `04-flow.json` following `references/spec-format.md`, then run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/bpmn-flow/scripts/bpmn_build.py" docs/product/<feature-slug>/04-flow.json
```

(If `CLAUDE_PLUGIN_ROOT` is not set, use the path of this skill's `scripts/` folder.)

The script validates the model (reachability, dead ends, gateway pairing, labelled
conditions, naming) and prints errors/warnings. **Fix every error and address every
warning** (or explain in the narrative why a warning is acceptable), then rebuild.
Use `--check` to validate without writing. Optional `"column": n` on a node forces its
horizontal position if the automatic layout needs help.

## Step 4 - Write the narrative (04-flow.md)

```markdown
# <Process name> - BPMN Process (<as-is | to-be>)
Status: Draft | Updated: <YYYY-MM-DD> | Files: 04-flow.bpmn, 04-flow.html

## Scope
Trigger: ... | Outcomes: ... | Owner: ... | Out of scope: ...

## Participants
| Lane / Pool | Role | Responsibilities |
|---|---|---|

## Process steps
| ID | Step | Type | Actor (lane) | Input | Output | Business rule / condition | Exceptions | Metric |
|---|---|---|---|---|---|---|---|---|
| T-01 | Submit order | userTask | Buyer | Cart | Order draft | BR-01 min. order | Out of stock -> G-01 No | M-01 |

## Decision points
| Gateway | Question | Branches (condition -> next) |
|---|---|---|

## Exceptions & SLAs
| Situation | Handling | SLA / timer |
|---|---|---|

## Improvement notes (to-be vs as-is)
- <pain point removed, step automated, handoff eliminated>
```

## Quality bar

- Script reports 0 errors; warnings resolved or justified.
- Every lane has at least one node; every end event name states the outcome.
- Every gateway question and branch is understandable by a non-BA stakeholder.
- At least one exception path for each user-facing decision.

## Hand-off

Tell the user to open `04-flow.html` (or import `04-flow.bpmn` into Camunda Modeler /
demo.bpmn.io). Suggest `use-case` next: lanes become actors, tasks become use case steps.
