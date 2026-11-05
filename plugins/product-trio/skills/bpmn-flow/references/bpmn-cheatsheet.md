# BPMN 2.0 cheat sheet (for choosing spec types)

## Events
| Spec type | event | Meaning | Use when |
|---|---|---|---|
| startEvent | (none) | Process starts | Manual/unspecified trigger |
| startEvent | message | Starts on receiving a message | Order received, form submitted by external party |
| startEvent | timer | Starts on schedule | "Every Monday 08:00", monthly closing |
| startEvent | conditional / signal | Starts on condition / broadcast | Stock below threshold |
| intermediateCatchEvent | timer | Wait | "Wait 24h for payment" |
| intermediateCatchEvent | message | Wait for message | Wait for supplier confirmation |
| intermediateThrowEvent | message / signal / escalation | Send/broadcast mid-process | Notify customer |
| endEvent | (none) | Path ends | Normal outcome |
| endEvent | message | Ends by sending a message | Send invoice and finish |
| endEvent | error | Ends with business error | Payment failed |
| endEvent | terminate | Kills all parallel paths | Order cancelled while other branches active |

Timer values (optional `"timer"` field) use ISO 8601 durations: `PT24H`, `P3D`, `PT30M`.

## Activities
| Spec type | Use for |
|---|---|
| userTask | A person does it in software (approve, fill form, review) |
| manualTask | A person does it without software (pack goods, hand over) |
| serviceTask | Fully automated (charge card, send WhatsApp via API, update stock) |
| sendTask / receiveTask | Explicit message send/receive with an external pool |
| businessRuleTask | Decision table / pricing / eligibility rules |
| scriptTask | Script executed by engine (rare in business models) |
| callActivity | Reusable sub-process modelled in another diagram |
| subProcess | Collapsed embedded sub-process |
| task | Undefined type (avoid in final models) |

## Gateways
| Spec type | Symbol | Split semantics | Join semantics |
|---|---|---|---|
| exclusiveGateway | ◇ X | Exactly one outgoing path (conditions mutually exclusive) | Passes first arriving token (merge) |
| parallelGateway | ◇ + | All outgoing paths at once | Waits for all incoming |
| inclusiveGateway | ◇ O | One or more paths whose conditions are true | Waits for all activated paths |
| eventBasedGateway | ◇ ⬠ | First event to occur wins (targets must be catch events / receive tasks) | n/a |

## Flows
- **Sequence flow** (`flows`): order inside one pool. Label conditions after XOR/OR splits.
- **Message flow** (`messageFlows`): communication between pools only; name it after the message.

## Common modelling mistakes the script catches
- Dead ends / unreachable nodes, start with incoming flow, end with outgoing flow.
- Unlabelled XOR/OR branches, multiple defaults.
- Task with several outgoing flows (implicit split) - use a gateway.
- AND-split without AND-join.
- Message flow inside one pool.
- Lanes named after systems.

## Common mistakes the script cannot catch (check yourself)
- Using XOR where branches can both be true (should be OR).
- Merging XOR paths with an AND-join (deadlock) or AND paths with an XOR-join (duplicate tokens).
- Mixing levels of detail (one task "Handle order", the next "Click save").
- Missing exception paths (timeouts, rejection, cancellation).
