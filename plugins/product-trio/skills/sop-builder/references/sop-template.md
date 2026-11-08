# SOP document template

Copy this structure into `sop.md`. Replace everything in angle brackets.

```markdown
# <SOP-ID> <Title>

| Field | Value |
|---|---|
| SOP ID | <SOP-WH-01> |
| Title | <Receiving raw materials> |
| Division / process owner | <Warehouse / Warehouse lead> |
| Version | <0.1> |
| Status | Draft / In review / Approved |
| Effective date | <YYYY-MM-DD> |
| Next review | <YYYY-MM-DD, at most 12 months later> |
| Prepared by | <name, role> |
| Approved by | <name, role> |

## 1. Purpose
<One or two sentences: why this procedure exists and what risk it controls.>

## 2. Scope
**Applies to:** <locations, roles, products, situations>
**Does not cover:** <what is handled by another SOP; name it>

## 3. Definitions
| Term | Meaning |
|---|---|
| <FEFO> | <First expired, first out: items with the earliest expiry date are used first> |

## 4. References
| Type | Reference |
|---|---|
| Related SOP | <SOP-PU-02 Purchase ordering> |
| Policy / regulation | <food safety rule, internal policy> |
| System | <inventory app, accounting app> |

## 5. Roles and responsibilities
| Role | Responsibility in this SOP |
|---|---|
| <Warehouse staff> | <Receives, weighs, labels and stores goods> |

## 6. Procedure
Trigger: <what starts the procedure>   Output: <what is true when it ends>

| No | Activity | PIC | Input / tool | Output / record | Time / SLA | Notes and controls | BPMN |
|---|---|---|---|---|---|---|---|
| 1 | <Verb + object> | <Role> | <Document, tool> | <Record, form ID> | <5 min> | <Limits; **[Control]** if critical> | <T-01> |
| 2 | Decide: <question?> If yes, go to 3. If no, go to 8. | <Role> | | | | | <G-01> |

## 7. Flowchart
See `flow.html` (BPMN 2.0 swimlanes; open over http) and `flow.bpmn` (opens in Camunda Modeler,
bpmn.io or draw.io).

## 8. Exceptions and escalation
| Situation | Action | Who | Time limit | Escalate to |
|---|---|---|---|---|

## 9. Records and forms
| Form / record | Filled by | Kept where | Retention |
|---|---|---|---|
| <F-01 Receiving log> | <Warehouse staff> | <Binder WH-01 / inventory app> | <1 year> |

## 10. Controls and KPIs
| Control / KPI | Target | Checked by | Frequency |
|---|---|---|---|

## 11. Training and sign-off
| Name | Role | Trained by | Date | Signature |
|---|---|---|---|---|

## 12. Revision history
| Version | Date | Change | By |
|---|---|---|---|
| 0.1 | <YYYY-MM-DD> | First draft | <name> |
```

## Form template (forms/F-xx-<slug>.md)

```markdown
# <F-01> <Receiving log>   (SOP <SOP-WH-01>, step <3-6>)
| Date | Time | Supplier | PO no. | Item | Batch | Expiry | Qty ordered | Qty received (kg) | QC result (pass/fail) | Received by | Signature |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |
```
Checklists use one row per check with the limit in its own column:
`| No | Check | Limit | Result | OK / Not OK |`.

## Typical SOPs by division (starting list for Mode A)

| Division | Common SOPs |
|---|---|
| Purchasing | Supplier selection, purchase ordering, price and contract review |
| Warehouse | Receiving goods, storage and FEFO/FIFO, stock opname, issuing goods, returns to supplier |
| Production / kitchen | Recipe and batch production, quality check, hygiene and cleaning, waste handling |
| Sales & customer service | Order intake, quotation, complaint handling, refunds and returns |
| Fulfilment | Packing, shipping and tracking, delivery issues |
| Finance | Invoicing, payment confirmation, petty cash, daily cash closing, expense claims |
| HR | Recruitment, onboarding, attendance, leave, offboarding and handover |
| Front office (hospitality) | Check-in, check-out, room move, lost and found, guest complaint |
| Housekeeping | Room cleaning standard, linen handling, room inspection |
| IT & data | Account access, backups, personal data requests, incident handling |
| General & safety | Opening and closing, emergency response, equipment maintenance |
