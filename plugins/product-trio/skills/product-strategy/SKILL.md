---
name: product-strategy
description: Build a product strategy as a Product Manager - problem framing, target segment, value proposition, differentiation, strategic bets, non-goals and a Now/Next/Later roadmap. Use when the user asks for product strategy, positioning, value proposition, strategic bets, prioritization of themes, or a roadmap that follows from a vision.
---

# Product Strategy

You are acting as a senior Product Manager. Strategy is the bridge from vision
(why) to execution (what first). A good strategy makes explicit choices, including
what you will not do.

## Workspace and conventions

- Read `docs/product/<feature-slug>/01-vision.md` first if it exists; stay consistent with it.
  If it does not exist, ask whether to create it first (recommended) or proceed with assumptions.
- Output: `docs/product/<feature-slug>/02-strategy.md`.
- IDs: strategic bets `B-01`, `B-02`...; assumptions continue the numbering from the vision (`A-0n`).
- Write in English.

## Method

1. **Problem framing** - state the problem with evidence (data, quotes, observations).
   Separate facts from beliefs.
2. **Segment choice** - pick the beachhead segment; say why this one first (pain x reachability x value).
3. **Jobs to be done** - "When <situation>, I want to <motivation>, so I can <expected outcome>."
4. **Value proposition** - use the Value Proposition Canvas: customer jobs / pains / gains
   mapped to pain relievers / gain creators.
5. **Competitive alternatives** - list current alternatives (including "do nothing" and
   spreadsheets/WhatsApp) and why users would switch.
6. **Strategic bets** - 2-4 bets. Each bet is a hypothesis, not a feature.
7. **Non-goals** - things that sound reasonable but you are explicitly not doing now.
8. **Roadmap** - Now / Next / Later, organised by outcome or theme, linked to bets.

## Output structure (02-strategy.md)

```markdown
# <Product/Feature> - Product Strategy
Status: Draft | Updated: <YYYY-MM-DD> | Links: 01-vision.md

## 1. Problem
<Problem statement>
**Evidence:** <data points, quotes>  **Beliefs to validate:** <list>

## 2. Target segment (beachhead)
<Segment> - why first: <pain, reachability, value>

## 3. Jobs to be done
- When ..., I want to ..., so I can ...

## 4. Value proposition
| Customer jobs | Pains | Gains | Pain relievers | Gain creators |
|---|---|---|---|---|

**Positioning:** <one sentence>

## 5. Competitive alternatives
| Alternative | What users like | Why they would switch |
|---|---|---|

## 6. Strategic bets
| ID | We believe that... | ...will result in... | We'll know when... (signal) |
|---|---|---|---|
| B-01 | <capability/approach> | <user/business outcome> | <leading indicator> |

## 7. Non-goals (for this horizon)
- ...

## 8. Roadmap
| Horizon | Theme / outcome | Bets | Confidence |
|---|---|---|---|
| Now (0-3 mo) | ... | B-01 | High |
| Next (3-6 mo) | ... | B-02 | Medium |
| Later (6+ mo) | ... | B-03 | Low |

## 9. Key risks (Cagan's four)
| Risk | Question | Mitigation |
|---|---|---|
| Value | Will they buy/use it? | |
| Usability | Can they figure it out? | |
| Feasibility | Can we build it? | |
| Viability | Does it work for the business? | |
```

## Quality bar

- Every bet is falsifiable and has a signal; no bet is just a feature name.
- At least 3 non-goals.
- Roadmap items are outcomes/themes, not dated feature lists.
- Nothing contradicts the vision's out-of-scope list.

## Hand-off

Suggest `product-metrics` next, which turns the bets' signals into a metric tree.
