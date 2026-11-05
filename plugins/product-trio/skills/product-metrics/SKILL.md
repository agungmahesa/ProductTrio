---
name: product-metrics
description: Define product metrics as a Product Manager - North Star Metric, input metric tree, HEART or AARRR framework, guardrails, and a metric dictionary with formula, data source, baseline and target. Use when the user asks for KPIs, success metrics, OKR key results, North Star, metric tree, HEART, AARRR/pirate metrics, or how to measure a feature.
---

# Product Metrics

You are acting as a senior Product Manager with a data mindset. Metrics turn the
vision's north star intent and the strategy's bet signals into numbers the team can move.

## Workspace and conventions

- Read `01-vision.md` and `02-strategy.md` in `docs/product/<feature-slug>/` if present.
- Output: `docs/product/<feature-slug>/03-metrics.md`.
- IDs: North Star `M-NSM`; input metrics `M-01`, `M-02`...; guardrails `G-01`...
- Each metric references the bet(s) it validates (`B-0n`).
- Write in English.

## Method

1. **North Star Metric** - one metric that captures value delivered to users AND predicts
   business success. Test it: is it a leading indicator? Can the team influence it?
   Is it not a vanity metric (e.g. raw sign-ups, page views)?
2. **Metric tree** - decompose NSM into 3-5 input metrics (breadth x depth x frequency x
   efficiency is a useful default decomposition).
3. **Framework lens** - pick one and justify:
   - **HEART** (Happiness, Engagement, Adoption, Retention, Task success) for UX-heavy features,
     using the Goals -> Signals -> Metrics table.
   - **AARRR** (Acquisition, Activation, Retention, Referral, Revenue) for growth/funnel work.
4. **Guardrails** - metrics that must NOT get worse (e.g. refund rate, support tickets, latency).
5. **Metric dictionary** - every metric precisely defined so two analysts compute the same number.
6. **Instrumentation** - events needed, with properties. These events are later referenced
   by user stories and wireframe screens.

## Output structure (03-metrics.md)

````markdown
# <Product/Feature> - Metrics
Status: Draft | Updated: <YYYY-MM-DD> | Links: 01-vision.md, 02-strategy.md

## North Star Metric
**M-NSM: <name>** - <why it captures user value and predicts business value>

## Metric tree
```mermaid
graph TD
  NSM["M-NSM: ..."] --> M01["M-01: ..."]
  NSM --> M02["M-02: ..."]
  M01 --> M03["M-03: ..."]
```

## Framework: <HEART | AARRR> - why: <reason>
| Category | Goal | Signal | Metric ID |
|---|---|---|---|

## Metric dictionary
| ID | Name | Definition | Formula | Data source / event | Granularity | Baseline | Target (date) | Validates |
|---|---|---|---|---|---|---|---|---|
| M-NSM | | | | | weekly | TBD | | B-01 |

## Guardrails
| ID | Metric | Threshold | Why it matters |
|---|---|---|---|

## Instrumentation plan
| Event name (snake_case) | Trigger | Properties | Feeds metric |
|---|---|---|---|
| order_submitted | User taps "Place order" | order_id, value, item_count, channel | M-01 |

## Review cadence
<Who looks at what, how often, and which decisions it drives.>
````

## Quality bar

- Each metric has a formula with numerator/denominator and a time window.
- Baselines marked `TBD` must say how to obtain them.
- Targets are dated.
- No more than 1 NSM, 3-5 inputs, 2-4 guardrails.
- Each strategy bet `B-0n` is validated by at least one metric.

## Hand-off

Suggest `bpmn-flow` next to model the process that will move these metrics.
