---
description: Run the full product-trio discovery chain (vision -> strategy -> metrics -> BPMN -> use cases -> user stories -> lo-fi wireframe) for a feature, with a traceability matrix
argument-hint: <feature or product idea> [--from <step>] [--only <step,step>]
---

# Product discovery: $ARGUMENTS

Run the product-trio chain for the feature described above. Work as a trio: Product
Manager, Business Analyst and UX Designer.

## 0. Setup
- Derive a kebab-case `<feature-slug>` and create `docs/product/<feature-slug>/`.
- Look for existing artifacts there; never overwrite a file without saying so. If some exist,
  resume from the first missing step (or from `--from <step>` if given; `--only` runs just those).
- Ask the user up to 5 discovery questions in ONE message (target user, problem + evidence,
  business goal, scope/constraints, as-is process). If they say "assume", proceed and log
  every assumption as `A-xx`.

## 1-7. Chain (use each skill's full instructions)
| # | Skill | Output |
|---|---|---|
| 1 | `product-vision` | 01-vision.md |
| 2 | `product-strategy` | 02-strategy.md |
| 3 | `product-metrics` | 03-metrics.md |
| 4 | `bpmn-flow` | 04-flow.json / .bpmn / .html / .md |
| 5 | `use-case` | 05-use-cases.md |
| 6 | `user-story` | 06-user-stories.md |
| 7 | `lofi-wireframe` | 07-wireframe.md / .html |

After steps 3, 4 and 6, pause briefly and show the user a 3-5 line summary (NSM + bets;
process diagram link; story map) and ask whether to continue or adjust. Skip the pauses if the
user asked for an uninterrupted run.

## 8. Traceability matrix
Write `docs/product/<feature-slug>/traceability.md`:

```markdown
# <Feature> - Traceability
| BPMN node | Use case (step) | User story | Screen(s) | Metric / event | Bet |
|---|---|---|---|---|---|
| T-01 Submit order | UC-01 (1-2) | US-01 | S-02, S-02-error | M-01 / order_submitted | B-01 |

## Coverage check
- BPMN user tasks without a use case: ...
- UC extensions without a story/scenario: ...
- R1 stories without a screen: ...
- Bets without a metric: ...
- Screens without a story: ...
```

Every gap must be either fixed or listed with a reason.

## 9. Wrap up
Write `docs/product/<feature-slug>/README.md` as an index: one line per artifact with what it
contains, status, open questions and assumptions to validate. Then tell the user which files
to open first (`04-flow.html`, `07-wireframe.html`).
