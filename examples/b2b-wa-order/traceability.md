# B2B WhatsApp Order - Traceability
| BPMN node | Use case (step) | User story | Screen(s) | Metric / event | Bet |
|---|---|---|---|---|---|
| E-01 Order request received | UC-01 (1) | US-01 | S-01 | M-01 / order_form_sent | B-01 |
| T-01 Send order form | UC-01 (2, 2a) | US-01, US-11 | S-01 | M-01, G-01 / order_form_sent | B-01, B-03 |
| E-02 Form submitted | UC-01 (3-7) | US-02..US-06, US-08 | S-02..S-06, S-04-error, S-09 | M-01 / order_form_submitted | B-01 |
| E-03 Form link expired -> E-09 | UC-01 (7a) | US-07 | S-06-expired | M-01 | B-01 |
| T-02 Recalculate price and shipping | UC-01 (6, 8, 6a) | US-05, US-06 | S-05, S-06 | - | B-01 |
| T-03 Save order and send summary | UC-01 (8) | US-06 | S-06, S-07 | M-NSM, M-02 / order_created | B-02 |
| T-04 Create invoice in Jurnal.id | UC-02 (2) | US-10 | S-11, S-12 | M-04 | B-02 |
| T-05 Send invoice | UC-02 (3-5, 3a, 4a) | US-10, US-11 | S-12, S-07 | M-03, M-04 / invoice_sent | B-02, B-03 |
| G-02/G-03 wait for payment | UC-03 (1) | US-12, US-14 | S-07, S-10 | M-03 | B-02 |
| E-04 Payment claimed | UC-03 (1-2) | US-12 | S-07, S-07-claimed | M-03 / payment_claimed | B-02 |
| E-05 2 days unpaid, T-07 Follow up | UC-03 (1a, 3a) | US-14 | S-10 | M-03 | B-02 |
| T-06 Check bank mutation, G-04 | UC-03 (3) | US-13 | S-13 | - | B-02 |
| T-08 Mark order paid | UC-03 (4-5) | US-13 | S-11, S-13, S-08 | M-03 / order_paid | B-02 |
| T-09 Pack order | UC-04 (1) | - (manual, off-product) | - | M-02 | B-02 |
| T-10 Book courier and enter tracking | UC-04 (2-3, 3a) | US-15 | S-11, S-14 | M-02 | B-02 |
| T-11 Send tracking number -> E-10 | UC-04 (4) | US-15 | S-14, S-08 | M-NSM / order_shipped | B-02 |
| (all sends) | BR-01 | US-11 | S-12, S-11 timeline | G-01 / wa_message_sent | B-03 |

## Coverage check
- BPMN user tasks without a use case: none.
- UC extensions without a story/scenario: none (2b -> US-08, 5a -> US-04, 6a -> US-05, 7a -> US-07, UC-02 3a/4a -> US-10, UC-03 1a/3a -> US-14, UC-04 3a -> US-15 note).
- R1 stories without a screen: none.
- Bets without a metric: none (B-04 -> M-05; no R1 story yet by design, it is a Later bet).
- Screens without a story: none.
- Gap: T-09 Pack order has no story because it is manual and off-product (by design).
- Gap: G-03 (2 days unpaid) has no R1 story; US-14 is R2, so in R1 Sales follows up from S-10 by hand.
