# SOP-WH-01 Receiving raw materials

| Field | Value |
|---|---|
| SOP ID | SOP-WH-01 |
| Title | Receiving raw materials |
| Division / process owner | Warehouse / Warehouse lead |
| Version | 0.1 |
| Status | Draft |
| Effective date | TBD |
| Next review | 2027-05 |
| Prepared by | Business Analyst (with Budi, warehouse staff) |
| Approved by | TBD - Operations manager |

## 1. Purpose
Make sure every delivery of tea leaves and packaging is checked against the order and for quality
before it enters stock, so we never pay for, store or use goods that are wrong, short or unsafe.

## 2. Scope
**Applies to:** all deliveries of raw materials (tea leaves, matcha powder, packaging) at the Acme
Tea warehouse, during opening hours 08:00-16:00.
**Does not cover:** purchase ordering (SOP-PU-01), stock opname (SOP-WH-02), deliveries of
finished goods to customers.

## 3. Definitions
| Term | Meaning |
|---|---|
| PO | Purchase order issued by purchasing |
| Delivery note | Supplier's document listing what was sent |
| FEFO | First expired, first out: goods with the earliest expiry date are used first |
| QC | Quality control check on a sample of the delivery |

## 4. References
| Type | Reference |
|---|---|
| Related SOP | SOP-PU-01 Purchase ordering; SOP-WH-02 Stock opname |
| Policy | Raw material specification sheet per item (moisture, aroma, packaging) |
| System | Inventory app (stock in), accounting app (supplier invoice) |
| Flowchart | [flow.html](flow.html) · [flow.bpmn](flow.bpmn) |

## 5. Roles and responsibilities
| Role | Responsibility in this SOP |
|---|---|
| Warehouse staff | Checks documents, weighs, labels, stores and records stock in |
| Quality control | Inspects samples and decides pass/fail against the specification |
| Purchasing admin | Handles refusals and returns with the supplier; matches invoice to receipt |
| Warehouse lead | Owns this SOP; checks the receiving log daily |

## 6. Procedure
Trigger: a supplier delivery arrives at the warehouse.   Output: goods are in stock and recorded, or returned with a rejection note.

| No | Activity | PIC | Input / tool | Output / record | Time / SLA | Notes and controls | BPMN |
|---|---|---|---|---|---|---|---|
| 1 | Receive the driver and collect the delivery note. | Warehouse staff | Delivery note | - | On arrival | Unload only after step 2. | E-01 |
| 2 | Compare the delivery note with the PO: item, quantity, supplier. | Warehouse staff | PO (inventory app) | F-01 columns 1-8 | 10 min | **[Control]** Do not accept goods without a PO. | T-01 |
| 3 | Decide: does the delivery match the PO? If yes, go to 5. If no, go to 4. | Warehouse staff | | | | Quantity tolerance ±2%. | G-01 |
| 4 | Refuse the delivery, write the reason on the delivery note, and message purchasing. End. | Warehouse staff | Delivery note | Signed refusal on delivery note | 15 min | Purchasing informs the supplier the same day. | T-02, E-09 |
| 5 | Take one sample per batch and inspect it against the specification sheet. | Quality control | F-02 QC checklist | F-02 completed | 20 min | **[Control]** Moisture ≤ 5%; packaging sealed; expiry ≥ 9 months away. | T-03 |
| 6 | Decide: does every check pass? If yes, go to 7. If no, go to 12. | Quality control | F-02 | Pass/fail on F-02 | | One failed check = fail. | G-02 |
| 7 | Weigh each sack and record the actual weight. | Warehouse staff | Calibrated scale | F-01 column 9 | 15 min | Scale calibration date must be within 6 months. | T-04 |
| 8 | Label each sack with item, batch, expiry date and received date. | Warehouse staff | Label printer | Labels on sacks | 10 min | Expiry in large print, top right. | T-05 |
| 9 | Store the sacks by FEFO: earliest expiry at the front of the rack. | Warehouse staff | Rack map | - | 15 min | Off the floor, away from the wall. | T-06 |
| 10 | Enter the received quantity and batch in the inventory app. | Warehouse staff | Inventory app | Stock-in record | Same day | **[Control]** Quantity = weighed quantity, not the delivery note. | T-07 |
| 11 | Match the supplier invoice with the PO and the receiving log, then approve it for payment. End. | Purchasing admin | Invoice, F-01 | Approved invoice | 2 working days | Difference > 2%: hold payment, contact supplier. | T-08, E-10 |
| 12 | Complete the rejection note with photos of the failed sample. | Quality control | F-03 | F-03 completed | 15 min | Keep the sample for 30 days. | T-09 |
| 13 | Arrange the return with the supplier and send them the rejection note. End. | Purchasing admin | F-03 | Return confirmation | 1 working day | Rejected goods stay in the red "Hold" area until collected. | T-10, E-11 |

## 7. Flowchart
See [flow.html](flow.html) (BPMN 2.0 swimlanes; open over http) and [flow.bpmn](flow.bpmn).

## 8. Exceptions and escalation
| Situation | Action | Who | Time limit | Escalate to |
|---|---|---|---|---|
| Delivery arrives without a PO | Refuse (step 4) | Warehouse staff | Immediately | Purchasing admin |
| Delivery after 16:00 | Accept only if the warehouse lead is present; otherwise refuse | Warehouse staff | Immediately | Warehouse lead |
| QC person absent | Hold goods in the "Hold" area; do not store | Warehouse staff | Until QC is done, max 24 h | Warehouse lead |
| Scale out of calibration | Use the backup scale; report | Warehouse staff | Same day | Warehouse lead |

## 9. Records and forms
| Form / record | Filled by | Kept where | Retention |
|---|---|---|---|
| [F-01 Receiving log](forms/F-01-receiving-log.md) | Warehouse staff | Binder WH-01 | 1 year |
| [F-02 QC checklist](forms/F-02-qc-checklist.md) | Quality control | Binder QC-01 | 2 years |
| [F-03 Rejection note](forms/F-03-rejection-note.md) | Quality control | Binder QC-01 + copy to supplier | 2 years |
| Stock-in record | Warehouse staff | Inventory app | As per system |

## 10. Controls and KPIs
| Control / KPI | Target | Checked by | Frequency |
|---|---|---|---|
| Deliveries received without PO | 0 | Warehouse lead | Weekly |
| Receiving log complete (all columns) | 100% | Warehouse lead | Daily |
| Stock-in entered same day | 100% | Warehouse lead | Daily |
| Invoice vs receipt differences resolved | within 5 working days | Purchasing admin | Monthly |

## 11. Training and sign-off
| Name | Role | Trained by | Date | Signature |
|---|---|---|---|---|
| | | | | |

## 12. Revision history
| Version | Date | Change | By |
|---|---|---|---|
| 0.1 | 2026-11-08 | First draft from interview with warehouse staff | Business Analyst |

*Acme Tea and all names, limits and numbers in this example are fictional.*
