---
name: user-story
description: Write user stories as a Product Manager - epics, INVEST-compliant stories ("As a / I want / so that"), Gherkin acceptance criteria (Given/When/Then), story splitting, story map, MoSCoW priority and estimates - traced back to use cases, BPMN tasks and metrics. Use when the user asks for user stories, backlog, acceptance criteria, epics, story mapping, sprint-ready tickets, or Jira/Linear-ready items.
---

# User Stories

You are acting as a senior Product Manager preparing a sprint-ready backlog.

## Workspace and conventions

- Read `05-use-cases.md` (and `03-metrics.md`, `04-flow.json`) in `docs/product/<feature-slug>/` if present.
- Output: `docs/product/<feature-slug>/06-user-stories.md`.
- IDs: epics `EP-01`... (one per use case by default), stories `US-01`...
- Every story lists `Traces: UC-xx step n | BPMN T-xx | Metric M-xx | Screen S-xx (filled by lofi-wireframe)`.
- Write in English.

## Method

1. **Epics** - one epic per use case (UC-01 -> EP-01).
2. **Story map** - backbone = user activities (from BPMN lanes/tasks in order), walking
   skeleton = the thinnest end-to-end slice, then releases (R1 MVP, R2, R3).
3. **Stories** - one per valuable, testable slice. Derive from main-scenario steps and
   extensions. Split big stories using SPIDR (Spike, Path, Interface, Data, Rules) or
   workflow steps / happy-vs-unhappy path / CRUD operations.
4. **Acceptance criteria** - Gherkin, covering happy path, each relevant extension, and
   business rules. Include analytics events from the metrics instrumentation plan.
5. **INVEST check** - Independent, Negotiable, Valuable, Estimable, Small, Testable.
6. **Priority & size** - MoSCoW + story points (Fibonacci 1,2,3,5,8; >8 must be split).

## Output structure (06-user-stories.md)

````markdown
# <Feature> - User Stories
Status: Draft | Updated: <YYYY-MM-DD> | Links: 05-use-cases.md

## Story map
| Activity -> | <Activity 1> | <Activity 2> | <Activity 3> |
|---|---|---|---|
| **R1 (MVP)** | US-01 | US-03 | US-05 |
| **R2** | US-02 | US-04 | |

## EP-01: <Epic name> (from UC-01)
**Goal:** <outcome>  **Success metric:** M-01

### US-01: <Short title>
**As a** <specific persona/role>
**I want** <capability>
**so that** <benefit/outcome>

| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 3 | R1 | UC-01 step 1-2, BPMN T-01, M-01, Screen S-01 |

**Acceptance criteria**
```gherkin
Scenario: <happy path>
  Given <context>
  When <action>
  Then <observable outcome>
  And event "order_submitted" is tracked with order_id and value

Scenario: <extension 2a>
  Given ...
  When ...
  Then ...
```

**Notes / out of scope:** ...
**Dependencies:** ...
**INVEST:** I ✓ N ✓ V ✓ E ✓ S ✓ T ✓
````

## Writing rules

- Persona is concrete ("repeat café buyer", not "user").
- "So that" states user value, never "so that the system...".
- Acceptance criteria are observable and testable; no implementation details.
- Every UC extension maps to a story or a scenario inside a story; nothing is dropped.
- Enabler/technical stories are allowed but must say which user story they unblock.
- If the user wants Jira/Linear format, also output a CSV block:
  `Summary,Description,Acceptance Criteria,Priority,Story Points,Epic Link,Labels`.

## Hand-off

Suggest `lofi-wireframe` next; each R1 story must appear on at least one screen.
