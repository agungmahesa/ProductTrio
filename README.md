# product-trio

A Claude Code plugin that gives Claude three product roles, chained into one traceable
discovery flow:

| Role | Skill | Output |
|---|---|---|
| Product Manager | `product-vision` | Vision statement, Moore elevator pitch, Pichler Vision Board |
| Product Manager | `product-strategy` | Problem, segment, JTBD, value proposition, bets, non-goals, Now/Next/Later roadmap |
| Product Manager | `product-metrics` | North Star, metric tree, HEART/AARRR, metric dictionary, guardrails, instrumentation |
| Business Analyst | `bpmn-flow` | **Real BPMN 2.0 `.bpmn`** (Camunda Modeler / bpmn.io / draw.io), HTML preview, process narrative |
| Product Manager | `use-case` | Cockburn fully-dressed use cases, actors, extensions, business rules |
| Product Manager | `user-story` | Epics, INVEST stories, Gherkin acceptance criteria, story map, MoSCoW, points |
| UX Designer | `lofi-wireframe` | Clickable grayscale HTML prototype: flows, states, annotations, mobile/desktop |

Plus the `/discovery <idea>` command that runs the whole chain and writes a traceability matrix.

```
Vision -> Strategy -> Metrics -> BPMN -> Use cases -> User stories -> Lo-fi wireframe
                         B-xx     M-xx     T-xx/G-xx     UC-xx         US-xx            S-xx
                         \________________ traceability.md links every ID ______________/
```

## Install

```bash
# from a local clone
claude plugin marketplace add /path/to/product-trio
claude plugin install product-trio@product-trio

# or from GitHub once pushed
claude plugin marketplace add <github-user>/product-trio
claude plugin install product-trio@product-trio
```

Inside Claude Code you can also use `/plugin marketplace add ...` and `/plugin install ...`.

Requirements: Python 3.8+ (BPMN build script, standard library only). Previews load
`bpmn-js` from unpkg, so the BPMN preview needs internet; the `.bpmn` file itself works offline.

## Use

```text
/discovery B2B reorder for cafe partners via WhatsApp
```

or call one skill directly, e.g. "Model the as-is refund process in BPMN" or "Write user
stories for UC-02". Outputs go to `docs/product/<feature-slug>/`:

```
01-vision.md  02-strategy.md  03-metrics.md
04-flow.json  04-flow.bpmn  04-flow.html  04-flow.md
05-use-cases.md  06-user-stories.md
07-wireframe.md  07-wireframe.html
traceability.md  README.md
```

### BPMN build script

The BA skill writes a JSON process spec; the script validates it and generates BPMN 2.0
XML with diagram layout (pools, lanes, events, gateways, message flows) plus a preview:

```bash
python3 plugins/product-trio/skills/bpmn-flow/scripts/bpmn_build.py examples/b2b-reorder/04-flow.json
```

Validation catches dead ends, unreachable nodes, unlabelled XOR/OR branches, implicit splits,
unpaired AND gateways, invalid event-based gateways, message flows inside a pool, and
system-named lanes. Spec format: `plugins/product-trio/skills/bpmn-flow/references/spec-format.md`.

### Wireframe template

`plugins/product-trio/skills/lofi-wireframe/templates/wireframe.html` - a self-contained
prototype engine: screens are `<section>`s, `data-go` links them, `FLOWS` defines journeys.
Keys: ← → step through a flow, H hotspots, N annotations.

## Examples

- `examples/b2b-wa-order/` - **full `/discovery` run** on a real feature (B2B order via WhatsApp
  Flow, Jurnal.id invoice, JNE/J&T shipping): vision, strategy, metrics, BPMN with the customer
  pool on top, 4 use cases, 15 user stories, an 18-screen clickable wireframe and the
  traceability matrix.
- `examples/purchase-approval/` - small BPMN with a rework loop.

Serve the repo and open the HTML files (bpmn-js needs http, not file://):

```bash
python3 -m http.server 8765
```

## Layout

```
.claude-plugin/marketplace.json
plugins/product-trio/
  .claude-plugin/plugin.json
  commands/discovery.md
  skills/<skill>/SKILL.md (+ scripts/, references/, templates/)
examples/
```
