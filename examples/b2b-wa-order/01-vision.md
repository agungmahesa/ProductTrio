# B2B WhatsApp Order - Product Vision
Status: Draft (example run) | Owner: Agung | Updated: 2026-11-05 | Horizon: 12 months

## Vision statement
Every coffee shop that serves Acme Tea can restock in the same chat where they already talk to us, and never has to wonder whether their order was seen.

## Elevator pitch (Geoffrey Moore)
For **coffee shops and cafés that buy matcha wholesale from Acme Tea**
who **reorder over WhatsApp and lose time (and sometimes orders) in back-and-forth chat, manual invoices and forwarded messages**,
the **Acme Tea B2B WhatsApp Order** is an **in-chat ordering and order-tracking flow**
that **turns "order" into a confirmed, priced, invoiced and tracked order without leaving WhatsApp**.
Unlike **free-text chat orders relayed by hand between sales, finance and the warehouse group**,
our product **captures every order once, prices shipping instantly, and pushes each status update to the buyer automatically, at near-zero messaging cost**.

## Vision Board (Roman Pichler)
| Target group | Needs | Product | Business goals |
|---|---|---|---|
| **Primary:** café owner / purchasing staff reordering 1-4x a month. **Secondary:** Acme Tea sales admin and order team. | Buyer: order in < 3 min from the phone, know the total incl. shipping up front, get invoice and tracking without asking. Team: no lost orders, no re-typing, one place to see status. | Order form inside WhatsApp (Flow) with live shipping cost; web Link Order fallback; admin actions (invoice, paid, shipped) that notify the buyer; cheapest-channel messaging. | Zero lost B2B orders; faster order-to-ship cycle; more repeat orders per café; WhatsApp cost per order near zero (no Wati subscription). |

## North star intent
More coffee shops getting their matcha delivered reliably and quickly, order after order.

## Principles
- **Stay where the buyer is**: WhatsApp first; the web link is a fallback, not the main path.
- **Capture once**: data entered by the buyer is never re-typed by the team.
- **Cheapest message that works**: free service messages inside the 24h window; paid templates only when needed.
- **Humans stay in the loop**: the team can still chat manually (Coexistence); automation never blocks a manual override.

## Out of scope
- Online payment collection inside WhatsApp (payment stays in Jurnal.id / Mekari Pay).
- Credit terms / tempo invoices and B2B price negotiation in the form.
- Retail (B2C) orders through this flow.
- Inventory management (stock is checked by the team, not the system, in R1).

## Assumptions & risks
| ID | Assumption | Risk if wrong | How to validate |
|---|---|---|---|
| A-01 | Most B2B buyers will use a WhatsApp Flow form instead of free-text chat. | Form ignored, team keeps manual flow. | Track form sent vs submitted (M-01) for the first 30 orders; interview 5 cafés. |
| A-02 | Lost orders come mainly from the relay between chat, invoice and WA group, not from stock issues. | Automating the relay does not remove losses. | Review last 3 months of dropped orders with sales. |
| A-03 | Most customer messages can be sent inside the free 24h window. | Template cost grows with volume. | Monitor `wa_message_sent` by type (G-01). |
| A-04 | Meta Coexistence is available for the Acme Tea number. | Team loses the WA Business app on that number. | Confirm during Meta setup. |
