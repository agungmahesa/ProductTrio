# product-trio - Quick start

Free and open source (MIT). Seven skills that give your AI agent three product roles, chained
into one traceable discovery flow:

| Skill | Role | Output |
|---|---|---|
| product-vision | Product Manager | Vision statement, elevator pitch, Vision Board |
| product-strategy | Product Manager | Problem, JTBD, value proposition, bets, roadmap |
| product-metrics | Product Manager | North Star, metric tree, metric dictionary, events |
| bpmn-flow | Business Analyst | Real BPMN 2.0 `.bpmn` + validator + HTML preview |
| use-case | Product Manager | Fully-dressed use cases with extensions |
| user-story | Product Manager | INVEST stories with Gherkin acceptance criteria |
| lofi-wireframe | UX Designer | Clickable grayscale prototype with storyboard view |

Plus `/discovery <idea>` (Claude Code) to run the whole chain and write a traceability matrix.

## Install

**Claude Code (recommended: as a plugin, gets updates from GitHub)**
```bash
claude plugin marketplace add agungmahesa/ProductTrio
claude plugin install product-trio@product-trio
```

**Claude Code (from this zip)**
```bash
mkdir -p ~/.claude/skills ~/.claude/commands
cp -R skills/* ~/.claude/skills/ && cp commands/discovery.md ~/.claude/commands/
```

**Other agents that read SKILL.md folders** (Cursor, Codex CLI, Gemini CLI, Copilot and others):
copy `skills/*` into that agent's skills directory. `/discovery` is Claude Code only; elsewhere ask:
*"Run the product-trio discovery chain for <idea>"*.

Requirements: Python 3.8+ (BPMN script, standard library only). HTML previews load `bpmn-js`
from a CDN, so open them over http (`python3 -m http.server`).

## Try it
- *"Run discovery for: café partners reorder our coffee beans over WhatsApp"*
- *"Model our refund process in BPMN with the customer as a separate pool"*
- *"Write user stories for UC-02, then turn them into lo-fi wireframes"*

Outputs go to `docs/product/<feature-slug>/`. Full example and screenshots:
https://github.com/agungmahesa/ProductTrio

## Want more?
**product-trio Pro** adds a PRD generator, Jira/Linear/GitHub backlog export, personas, journey
maps, usability test scripts and BPMN as-is vs to-be gap analysis with time and cost saved.

License: MIT (`LICENSE.txt`) - Copyright (c) 2026 Agung Mahesa Yudhistira.
