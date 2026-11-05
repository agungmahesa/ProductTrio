# B2B WhatsApp Order - User Stories
Status: Draft (example run) | Updated: 2026-11-05 | Links: 05-use-cases.md

Personas: **Café buyer** (owner or purchasing staff at a partner coffee shop), **Sales admin**, **Order team**.

## Story map
| Activity -> | Ask to order | Fill the form | Get invoiced | Pay | Ship |
|---|---|---|---|---|---|
| **R1 (MVP)** | US-01 | US-02, US-03, US-04, US-05, US-06 | US-09, US-10, US-11 | US-12, US-13 | US-15 |
| **R2** | | US-07, US-08 | | US-14 | |

## EP-01: Place B2B order in WhatsApp (from UC-01)
**Goal:** buyers order in one structured form  **Success metric:** M-01

### US-01: Get the order form in chat
**As a** café buyer **I want** to type "order" and get an order button **so that** I can start ordering without waiting for sales.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 3 | R1 | UC-01 steps 1-2, 2a; BPMN E-01, T-01; M-01; Screen S-01 |
```gherkin
Scenario: Buyer asks to order
  Given the buyer chats with the Acme Tea number
  When the buyer sends "order"
  Then the buyer receives a message with an "Order Sekarang" button within 10 seconds
  And event "order_form_sent" is tracked with source "chat"

Scenario: Sales sends the form to a buyer outside the 24h window
  Given the buyer's last message was more than 24 hours ago
  When Sales taps "Kirim Form Order" for that buyer
  Then the form is sent with the paid template "b2b_form_order"
```

### US-02: Choose products and quantities
**As a** café buyer **I want** to pick matcha products and quantities with prices **so that** I know my subtotal before continuing.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 3 | R1 | UC-01 step 3; BPMN E-02; Screen S-02 |
```gherkin
Scenario: Select products
  Given the order form is open
  When the buyer sets quantity 2 for "Ceremonial 100g" and 1 for "Culinary 1kg"
  Then the subtotal updates
  And "Lanjut" is enabled only when at least one product has quantity > 0
```

### US-03: Enter business data
**As a** café buyer **I want** to enter my café name, PIC and whether I need a tax invoice **so that** the invoice is correct the first time.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 2 | R1 | UC-01 step 4; BR-04; Screen S-03 |
```gherkin
Scenario: Tax invoice requested
  Given the buyer is on the business data step
  When the buyer turns on "Butuh faktur pajak"
  Then an NPWP field appears and is required
```

### US-04: Address with postal code lookup
**As a** café buyer **I want** to enter my postal code and choose my subdistrict **so that** shipping cost is accurate.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 5 | R1 | UC-01 step 5, 5a; Screens S-04, S-04-error |
```gherkin
Scenario: Postal code found
  When the buyer enters postal code "40115"
  Then the subdistricts for that code are listed to choose from

Scenario: Postal code not found
  When the buyer enters a postal code with no match
  Then an inline error "Kode pos tidak ditemukan" is shown
  And the buyer can search the subdistrict by name instead
```

### US-05: Courier with live shipping cost
**As a** café buyer **I want** to see JNE and J&T options with their prices **so that** I can choose speed vs cost.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 5 | R1 | UC-01 step 6, 6a; BPMN T-02; BR-03; Screen S-05 |
```gherkin
Scenario: Rates available
  When the buyer reaches the courier step
  Then courier services are listed with price and estimated days

Scenario: Rates unavailable
  Given RajaOngkir does not respond within 5 seconds
  Then the step shows "Ongkir akan dihitung admin" and lets the buyer continue
```

### US-06: Review, submit and receive summary
**As a** café buyer **I want** to review everything and get an order number in chat **so that** I know my order was received.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 3 | R1 | UC-01 steps 7-8; BPMN T-02, T-03; M-01, M-NSM; Screens S-06, S-07 |
```gherkin
Scenario: Submit order
  Given the buyer is on the summary step
  When the buyer taps "Kirim Order"
  Then an order "ATB-..." is saved with channel "b2b_wa" and server-calculated total
  And the buyer sees the order summary in chat if it is free to send (BR-01)
  And events "order_form_submitted" and "order_created" are tracked
```

### US-07: Expired form
**As a** café buyer **I want** a clear message when my form link is too old **so that** I know how to start again.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Should | 2 | R2 | UC-01 7a; BPMN E-03, E-09; BR-02; Screen S-06-expired |
```gherkin
Scenario: Form older than 3 days
  Given the form was sent more than 3 days ago
  When the buyer opens or submits it
  Then the buyer sees "Form kedaluwarsa. Ketik *order* untuk form baru."
```

### US-08: Web Link Order fallback
**As a** café buyer whose WhatsApp cannot open forms **I want** a web order page **so that** I can still order.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Should | 5 | R2 | UC-01 2b; Screen S-09 |
```gherkin
Scenario: Order through the web link
  Given the buyer opens acmetea.example/b2b
  When the buyer completes and submits the form
  Then the order is saved in the same orders table with channel "b2b_wa"
```

## EP-02: Invoice an order (from UC-02)
**Goal:** invoice within 2 working hours  **Success metric:** M-04

### US-09: See B2B orders by status
**As a** Sales admin **I want** a list of B2B orders grouped by status **so that** nothing waits unnoticed.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 3 | R1 | UC-02 step 1; G-02; Screens S-10, S-10-empty |
```gherkin
Scenario: New orders on top
  Given there are B2B orders with statuses new, invoiced, paid
  When Sales opens "Order B2B"
  Then tabs show counts per status and "Baru" is selected
  And orders older than 24h without invoice are highlighted
```

### US-10: Send invoice to the buyer
**As a** Sales admin **I want** to paste the Jurnal.id invoice number, link and total and send it in one action **so that** the buyer can pay right away.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 5 | R1 | UC-02 steps 3-5, 3a, 4a; BPMN T-04, T-05; M-04; Screens S-11, S-12 |
```gherkin
Scenario: Send invoice
  Given an order with status "new"
  When Sales fills invoice number, link and total and taps "Kirim Invoice"
  Then the buyer receives the invoice with a "Saya sudah bayar" button
  And the order status becomes "invoiced"
  And event "invoice_sent" is tracked

Scenario: Sending fails
  Given the WhatsApp API returns an error
  When Sales taps "Kirim Invoice"
  Then an error is shown with "Coba lagi" and the status stays "new"
```

### US-11: Cheapest-channel sending (enabler)
**As a** Sales admin **I want** every automatic message to use the free 24h window when possible **so that** WhatsApp cost per order stays near zero.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 5 | R1 | BR-01; all send steps (T-01, T-03, T-05, T-07, T-08, T-11); G-01 |
```gherkin
Scenario: Inside the 24h window
  Given the buyer messaged 3 hours ago
  When any automatic message is sent
  Then it is sent as a service message and logged with message_type "service"

Scenario: Outside the 24h window
  Given the buyer last messaged 30 hours ago
  When the invoice is sent
  Then template "b2b_invoice" is used and logged with message_type "template"
```

## EP-03: Confirm payment (from UC-03)
**Goal:** paid within 7 days  **Success metric:** M-03

### US-12: Tell Acme Tea I have paid
**As a** café buyer **I want** to tap "Saya sudah bayar" **so that** I don't have to send a screenshot and wait.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 3 | R1 | UC-03 steps 1-2; BPMN E-04; Screen S-07 |
```gherkin
Scenario: Payment claimed
  When the buyer taps "Saya sudah bayar"
  Then the buyer gets "Terima kasih, kami cek dulu ya"
  And the order shows "Klaim bayar" for Sales with an alert
  And event "payment_claimed" is tracked
```

### US-13: Mark order paid
**As a** Sales admin **I want** to mark an order paid after checking the mutation **so that** the buyer is confirmed and the order team starts packing.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 2 | R1 | UC-03 steps 3-5; BPMN T-06, G-04, T-08; BR-05; Screens S-11, S-13 |
```gherkin
Scenario: Mark paid
  Given an invoiced order
  When Sales taps "Tandai Lunas" and confirms the amount matches
  Then the buyer receives the payment confirmation
  And the order team is notified and the status becomes "paid"
```

### US-14: Follow up unpaid invoices
**As a** Sales admin **I want** unpaid invoices older than 2 days listed with a reminder button **so that** I can follow up quickly.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Should | 3 | R2 | UC-03 1a, 3a; BPMN E-05, G-05, T-07; Screen S-10 |
```gherkin
Scenario: Reminder
  Given an invoice sent more than 2 days ago without payment
  When Sales opens the "Perlu follow up" tab and taps "Ingatkan"
  Then a payment reminder is sent to the buyer using BR-01
```

## EP-04: Ship order (from UC-04)
**Goal:** ship within 48h of order  **Success metric:** M-NSM, M-02

### US-15: Mark shipped and send tracking
**As an** Order team member **I want** to enter courier and tracking number once **so that** the buyer gets it automatically.
| Priority | Points | Release | Traces |
|---|---|---|---|
| Must | 3 | R1 | UC-04 steps 3-4, 3a; BPMN T-10, T-11, E-10; M-NSM; Screens S-14, S-08 |
```gherkin
Scenario: Ship order
  Given a paid order
  When the order team taps "Tandai Dikirim" and enters "JNE" and a tracking number
  Then the buyer receives the tracking number in chat
  And the status becomes "shipped" and event "order_shipped" is tracked
```
