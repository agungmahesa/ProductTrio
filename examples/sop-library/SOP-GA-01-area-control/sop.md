# SOP-GA-01 Area Control

| Field | Value |
|---|---|
| Company | Acme Tea |
| SOP ID | SOP-GA-01 |
| Title | Area Control |
| Division / process owner | General Affairs (GA) / GA manager |
| Version | 1.0 |
| Status | Draft |
| Effective date | TBD |
| Next review | 2027-11 |
| Prepared by | GA staff |
| Approved by | TBD - GA manager |

## 1. Purpose
Keep every office and unit area of Acme Tea clean, safe and working, with every finding followed up within a clear time limit.

## 2. Scope
**Applies to:** daily inspection of office and unit areas (lobby, workspaces, toilets, pantry, warehouse, outdoor areas), from inspection until every finding is closed.
**Does not cover:** scheduled maintenance of machines and building (SOP-ENG-01), purchasing cleaning supplies (SOP-GA-03).

## 3. Definitions
| Term | Meaning |
|---|---|
| CS | Cleaning service staff (in-house or vendor) |
| WO | Work order: a written repair request to the engineering team |
| Finding | A condition that does not meet the standard on checklist F-01 |

## 4. References
- F-01 Area control checklist
- F-02 Work order
- Company cleanliness and workplace safety policy
- SOP-ENG-01 Scheduled maintenance

## 5. Roles and Responsibilities
| Role | Responsibility in this SOP |
|---|---|
| GA staff | Runs the control rounds, records findings, requests follow-up, verifies results |
| Cleaning service | Re-cleans areas according to findings |
| Engineering team | Repairs technical findings according to the work order |
| GA manager | Owns this SOP; signs off the daily checklist and handles escalations |

## 6. Procedure
Trigger: control round at 08:00 and 14:00 every working day. Output: every finding is closed and the checklist is filed.

| No | Activity | PIC | Input / tool | Output / record | Time / SLA | Notes and controls | BPMN |
|---|---|---|---|---|---|---|---|
| 1 | Start the control round on schedule, taking checklist F-01 and a phone for photos. | GA staff | F-01 | - | 08:00 and 14:00 | If unavailable, the GA manager assigns a replacement. | E-01 |
| 2 | Inspect each area in the order of F-01: floors, toilets, pantry, bins, air conditioning, lights and building condition. | GA staff | F-01 | - | 30 min | Use the "Standard" column on F-01, not personal judgement. | T-01 |
| 3 | Mark each item OK or Not OK and photograph every finding. | GA staff | Phone | F-01 | During inspection | **[Control]** Every "Not OK" needs a photo and a location. | T-02 |
| 4 | Decide the type of finding. Cleaning: go to 5. Technical (AC, lights, building): go to 8. Both: do 5 and 8. None: go to 11. | GA staff | F-01 | - | - | - | G-01 |
| 5 | Ask the CS supervisor to re-clean the area, giving the location and the finding. | GA staff | F-01 | F-01 follow-up column | Within 15 min | - | T-03 |
| 6 | Re-clean the area according to the finding, then report back to GA staff. | Cleaning service | Cleaning equipment | - | Within 60 min | - | T-04 |
| 7 | Re-inspect the area and mark it "Done" on F-01. | GA staff | F-01 | F-01 | After the CS report | If it still fails the standard, repeat step 5 once, then escalate to the GA manager. | T-05 |
| 8 | Raise work order F-02, sign it and hand it to the engineering team. | GA staff | F-02 | F-02 | Same day | **[Control]** One technical finding = one numbered work order. | T-06 |
| 9 | Repair the finding as described in the work order, then record the action and finish time on F-02. | Engineering team | F-02 | F-02 | Urgent 4 h; normal 3 working days | Urgent: leaks, electrical faults, safety risks. | T-07 |
| 10 | Check the repair, then close the work order with a signature. | GA staff | F-02 | F-02 closed | Same working day as the repair report | - | T-08 |
| 11 | Hand the completed F-01 to the GA manager and file it. | GA staff | F-01 | F-01 filed | Daily at 16:00 | **[Control]** The GA manager initials the daily checklist. | G-02, T-09, E-10 |

## 7. Flowchart
BPMN 2.0 diagram: [flow.html](flow.html) · [flow.bpmn](flow.bpmn).

## 8. Exceptions and Escalation
| Situation | Action | Who | Time limit | Escalate to |
|---|---|---|---|---|
| Area still fails the standard after re-cleaning | Escalate with photos | GA staff | Same day | GA manager |
| Work order past its SLA | Call the chief engineer | GA staff | When the SLA is missed | GA manager |
| Safety risk (exposed cable, slippery floor, leak) | Put up a warning sign, close the area, raise an urgent work order | GA staff | Immediately | GA manager and chief engineer |

## 9. Records and Forms
| Form / record | Filled by | Kept where | Retention |
|---|---|---|---|
| [F-01 Area control checklist](forms/F-01-area-control-checklist.md) | GA staff | Binder GA-01 | 1 year |
| [F-02 Work order](forms/F-02-work-order.md) | GA staff and engineering team | Binder GA-02 | 2 years |

## 10. Controls and KPIs
| Control / KPI | Target | Checked by | Frequency |
|---|---|---|---|
| Daily checklist complete and initialled | 100% | GA manager | Daily |
| Cleaning findings closed within 60 min | ≥ 95% | GA manager | Weekly |
| Work orders closed within SLA | ≥ 90% | GA manager | Monthly |

## 11. Training and Sign-off
| Name | Role | Trained by | Date | Signature |
|---|---|---|---|---|
| | | | | |

## 12. Revision History
| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-11-08 | Rewritten: measurable standards, time limits, technical path via work order, escalation | GA staff |

*Acme Tea and all data in this example are fictional.*
