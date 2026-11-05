# B2B WhatsApp Order - Product Strategy
Status: Draft (example run) | Updated: 2026-11-05 | Links: 01-vision.md

## 1. Problem
B2B reorders arrive as free-text WhatsApp chats. Sales re-types them, creates an invoice by hand, forwards the order to a WhatsApp group for packing, and relays the tracking number back. Each hand-off is a place where an order can be dropped or delayed.

**Evidence:** orders have been dropped in the chat -> invoice -> WA group -> tracking relay (team report, 2026). Wati was evaluated and rejected because of subscription plus per-message markup.
**Beliefs to validate:** A-01 (buyers adopt the form), A-02 (loss comes from relays), A-03 (most messages are free).

## 2. Target segment (beachhead)
**Existing café partners who already reorder over WhatsApp.** Highest pain (repeat, time-sensitive restocks), easiest to reach (already in our chat list), and highest value (recurring revenue). New B2B leads come later via the same flow.

## 3. Jobs to be done
- When **my matcha stock is running low before a busy weekend**, I want to **place a reorder in a minute from my phone**, so I can **be sure it arrives in time without chasing anyone**.
- When **I've paid an invoice**, I want to **tell Acme Tea with one tap**, so I can **get it confirmed and shipped without sending a transfer screenshot and waiting**.
- (Sales admin) When **an order comes in**, I want **all its data already captured and priced**, so I can **invoice in minutes instead of re-typing**.

## 4. Value proposition
| Customer jobs | Pains | Gains | Pain relievers | Gain creators |
|---|---|---|---|---|
| Restock matcha; pay; receive on time | Long chat back-and-forth; unknown shipping cost; "was my order seen?"; asking for tracking | Fast, predictable, visible status | Structured form; live JNE/J&T rates; order ID + summary in chat | Automatic invoice, paid and tracking messages; one-tap "I have paid" |

**Positioning:** Reordering Matcha from Acme Tea is as fast as sending a chat, and you always know where your order is.

## 5. Competitive alternatives
| Alternative | What users like | Why they would switch |
|---|---|---|
| Free-text WhatsApp chat with sales (today) | Familiar, personal | Slow, error-prone, no status visibility |
| Ordering from a marketplace (Shopee/Tokopedia) | Prices and tracking visible | No B2B pricing/tax invoice, not personal |
| Competitor supplier with a sales rep | Personal service | Same manual issues; switching supplier is costly |
| Wati / other WA CRM (for Acme Tea) | Ready-made inbox | Monthly fee + per-message markup |

## 6. Strategic bets
| ID | We believe that... | ...will result in... | We'll know when... (signal) |
|---|---|---|---|
| B-01 | an in-chat WhatsApp Flow order form with live shipping cost | most B2B orders arriving structured, with fewer drop-offs than chat | >= 70% of forms sent are submitted (M-01) |
| B-02 | admin actions that push invoice, paid and tracking messages automatically | zero lost orders and a shorter order-to-ship cycle | 0 dropped orders/month; median order-to-ship <= 2 days (M-02) |
| B-03 | cheapest-channel messaging (24h window first, template fallback) on Meta Cloud API directly | WhatsApp cost per order staying near zero without Wati | messaging cost per order <= Rp 1,000 (G-01) |
| B-04 | a frictionless reorder experience | cafés reordering more often | 60-day repeat order rate up (M-05) |

## 7. Non-goals (for this horizon)
- Payment gateway inside WhatsApp (keep Jurnal.id / Mekari Pay).
- Automatic stock reservation.
- Self-serve B2B price lists per customer.
- A separate B2B app or customer login.

## 8. Roadmap
| Horizon | Theme / outcome | Bets | Confidence |
|---|---|---|---|
| Now (0-3 mo) | Every B2B order captured once and tracked to shipping | B-01, B-02, B-03 | High |
| Next (3-6 mo) | Faster payment confirmation (bank mutation matching, reminders) | B-02 | Medium |
| Later (6+ mo) | Reorder in one tap from last order; proactive restock nudges | B-04 | Low |

## 9. Key risks (Cagan's four)
| Risk | Question | Mitigation |
|---|---|---|
| Value | Will cafés use the form instead of chatting? | Sales sends the form button proactively; chat still works (Coexistence). |
| Usability | Can staff finish a 6-step form on a phone? | Lo-fi test with 3 cafés before Flow publish; pre-fill business data on reorder. |
| Feasibility | Meta Flow encryption, webhook signature, Vercel function limit | Shared `api/b2b.js` route; verify signature against real traffic before launch. |
| Viability | Does messaging cost stay low at scale? | Monitor G-01 weekly; ring-fence template sends. |
