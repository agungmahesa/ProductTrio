# Example: B2B WhatsApp Order (Acme Tea)

A full `/discovery` run on a real feature: coffee shops ordering matcha through a WhatsApp Flow,
with invoicing in Jurnal.id and shipping via JNE/J&T.

| File | Contains | Status |
|---|---|---|
| [01-vision.md](01-vision.md) | Vision, elevator pitch, Vision Board, assumptions A-01..A-04 | Draft |
| [02-strategy.md](02-strategy.md) | Problem, JTBD, value proposition, bets B-01..B-04, roadmap | Draft |
| [03-metrics.md](03-metrics.md) | NSM, metric tree, AARRR, dictionary, guardrails, events | Draft |
| [04-flow.html](04-flow.html) / [.bpmn](04-flow.bpmn) / [.json](04-flow.json) / [.md](04-flow.md) | BPMN 2.0 to-be process, narrative, business rules BR-01..BR-05 | Draft |
| [05-use-cases.md](05-use-cases.md) | UC-01..UC-04 fully dressed | Draft |
| [06-user-stories.md](06-user-stories.md) | EP-01..EP-04, US-01..US-15 with Gherkin, story map | Draft |
| [07-wireframe.html](07-wireframe.html) / [.md](07-wireframe.md) | 18-screen clickable lo-fi prototype + flow map | Draft |
| [traceability.md](traceability.md) | BPMN -> UC -> US -> Screen -> Metric -> Bet | Draft |

**Open first:** `04-flow.html` and `07-wireframe.html` (serve the folder over http, e.g. `python3 -m http.server`).

**Validate next:** A-01 (buyers adopt the form) and A-02 (losses come from relays), and get baselines for M-NSM, M-02 and M-03.
