# B2B order via WhatsApp - BPMN Process (to-be)
Status: Draft (example run) | Updated: 2026-11-05 | Files: 04-flow.bpmn, 04-flow.html, 04-flow.json

## Scope
Trigger: a coffee shop asks to order (types "order") or Sales sends the form. | Outcomes: Order shipped, Order abandoned. | Owner: Sales admin. | Out of scope: payment collection (Jurnal.id), stock reservation, B2C orders.

## Participants
| Lane / Pool | Role | Responsibilities |
|---|---|---|
| P-Buyer (external, top) | Coffee shop buyer | Requests form, fills it, pays invoice, taps "Saya sudah bayar" |
| L-Sales | Sales admin (+ automated server steps they own) | Sends form, invoices, confirms payment, follows up |
| L-Order | Order team | Packs, books courier, enters tracking |
| P-RajaOngkir (external) | Shipping rate API | Returns JNE/J&T rates |
| P-Courier (external) | JNE / J&T | Picks up parcel |

## Process steps
| ID | Step | Type | Actor (lane) | Input | Output | Business rule / condition | Exceptions | Metric |
|---|---|---|---|---|---|---|---|---|
| E-01 | Order request received | message start | Sales | "order" chat or admin button | Request | - | - | - |
| T-01 | Send order form | serviceTask | Sales | Buyer phone | Flow button with signed flow_token | BR-01 cheapest channel; BR-02 token valid 3 days | Outside 24h -> paid template | M-01 |
| G-01 | (event-based) | gateway | Sales | - | - | First event wins | - | - |
| E-02 | Form submitted | message catch | Sales | Products, business data, address, courier | Form payload | - | - | M-01 |
| E-03 | Form link expired | timer P3D | Sales | - | - | BR-02 | -> E-09 Order abandoned | M-01 |
| T-02 | Recalculate price and shipping | serviceTask | Sales | Form payload | Server-side total | BR-03 server recalculates, form price is an estimate | RajaOngkir down -> keep form estimate, flag for admin | - |
| T-03 | Save order and send summary | serviceTask | Sales | Total | Order `ATB-...`, chat summary, admin notification | BR-01 (summary only if free) | - | M-NSM, M-02 |
| T-04 | Create invoice in Jurnal.id | userTask | Sales | Order | Invoice number + link | BR-04 tax invoice if requested | - | M-04 |
| T-05 | Send invoice | sendTask | Sales | Invoice | WA invoice with "Saya sudah bayar" button | BR-01 | - | M-03, M-04 |
| G-02 | (merge) | XOR join | Sales | - | - | - | - | - |
| G-03 | (event-based) | gateway | Sales | - | - | First event wins | - | - |
| E-04 | Payment claimed | message catch | Sales | Buyer tap | Admin "check mutation" alert | Opens new 24h window | - | M-03 |
| E-05 | 2 days unpaid | timer P2D | Sales | - | Reminder task | - | - | M-03 |
| T-06 | Check bank mutation | userTask | Sales | Mutation | Match result | - | - | - |
| G-04 | Payment matches invoice? | XOR split | Sales | - | Yes -> T-08, No -> G-05 | BR-05 amount must equal invoice total | - | - |
| T-07 | Follow up payment | userTask | Sales | - | Reminder to buyer | BR-01 | - | M-03 |
| T-08 | Mark order paid | userTask | Sales | Match | Buyer confirmation; Order team notified | BR-01 | - | M-03 |
| T-09 | Pack order | manualTask | Order team | Paid order | Parcel | - | - | M-02 |
| T-10 | Book courier and enter tracking | userTask | Order team | Parcel | Tracking number | - | - | M-02 |
| T-11 | Send tracking number | serviceTask | Order team | Tracking | WA tracking message | BR-01 | - | M-NSM |
| E-10 | Order shipped | end | Order team | - | - | - | - | M-NSM |

## Decision points
| Gateway | Question | Branches (condition -> next) |
|---|---|---|
| G-01 | Which happens first? | Form submitted -> T-02; 3 days pass -> E-09 Order abandoned |
| G-03 | Which happens first? | Buyer taps "Saya sudah bayar" -> T-06; 2 days pass -> T-07 |
| G-04 | Payment matches invoice? | Yes -> T-08; No -> T-07 follow up |

## Exceptions & SLAs
| Situation | Handling | SLA / timer |
|---|---|---|
| Form not submitted | Link expires; buyer must type "order" again | 3 days (BR-02) |
| Unpaid invoice | Reminder by Sales, loop back to waiting | every 2 days |
| Wrong amount paid | Follow up with buyer | same day |
| Postal code not found in form | Inline error, buyer picks subdistrict manually | - |
| Buyer cannot use Flow (old app) | Web Link Order `acmetea.example/b2b` (fallback, same order table) | - |

## Business rules
| ID | Rule |
|---|---|
| BR-01 | Send as a free service message if the buyer messaged within 24h; otherwise use the paid utility template. Order summary is sent only when free. |
| BR-02 | flow_token is signed with the buyer's phone and valid for 3 days. |
| BR-03 | Price and shipping are always recalculated on the server; form values are estimates. |
| BR-04 | Tax invoice (faktur pajak) only when the buyer requests it in the form. |
| BR-05 | An order is paid only when the transfer amount matches the invoice total. |

## Improvement notes (to-be vs as-is)
- Removed: re-typing chat orders, forwarding to the WA group, relaying tracking by hand.
- Automated: form, shipping quote, summary, invoice/paid/tracking messages, team notification.
- Added: explicit timeouts (3-day form, 2-day payment reminder) so no order waits silently.
