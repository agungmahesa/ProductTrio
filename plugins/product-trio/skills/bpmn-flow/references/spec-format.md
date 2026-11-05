# 04-flow.json spec format

```json
{
  "id": "b2b-reorder",                       // XML id: letters, digits, - _ . ; no leading digit
  "name": "B2B Reorder via WhatsApp",
  "description": "To-be process for café partners reordering matcha.",
  "pool": {
    "id": "P-AcmeTea",                       // optional, default "Pool_main"
    "name": "Acme Tea",
    "lanes": [
      { "id": "L-Buyer", "name": "Café buyer" },
      { "id": "L-Sales", "name": "Sales admin" }
    ]
  },
  "externalPools": [                          // optional black-box pools for message flows
    { "id": "P-Customer", "name": "Customer", "position": "top" },   // customer above (convention)
    { "id": "P-Bank", "name": "Payment gateway" }                    // default: below
  ],
  "nodes": [
    { "id": "E-01", "type": "startEvent", "name": "Reorder needed", "lane": "L-Buyer" },
    { "id": "T-01", "type": "userTask", "name": "Submit order", "lane": "L-Buyer",
      "documentation": "Optional text stored in the BPMN file" },
    { "id": "G-01", "type": "exclusiveGateway", "name": "Stock available?", "lane": "L-Sales" },
    { "id": "E-02", "type": "intermediateCatchEvent", "event": "timer", "timer": "PT24H",
      "name": "24h passed", "lane": "L-Buyer" },
    { "id": "E-09", "type": "endEvent", "name": "Order fulfilled", "lane": "L-Sales", "column": 7 }
  ],
  "flows": [
    { "from": "E-01", "to": "T-01" },
    { "from": "G-01", "to": "T-02", "name": "Yes" },
    { "from": "G-01", "to": "T-05", "name": "No", "default": true }
  ],
  "messageFlows": [
    { "from": "T-03", "to": "P-Bank", "name": "Payment request" },
    { "from": "P-Bank", "to": "E-04", "name": "Payment confirmation" }
  ]
}
```

(Comments above are for explanation only; real JSON must not contain comments.)

## Fields
- `nodes[].type`: startEvent, endEvent, intermediateCatchEvent, intermediateThrowEvent,
  task, userTask, serviceTask, manualTask, sendTask, receiveTask, scriptTask,
  businessRuleTask, callActivity, subProcess, exclusiveGateway, parallelGateway,
  inclusiveGateway, eventBasedGateway.
- `nodes[].event` (events only): message, timer, error, signal, terminate, conditional, escalation.
- `nodes[].timer` (timer events): ISO 8601 duration, e.g. `PT24H`.
- `nodes[].column` (optional int): force horizontal rank; otherwise computed from flow order.
- `flows[].id` optional (auto `Flow_n`); `name` = condition label; `default: true` marks default flow.
- `externalPools[].position`: `top` or `bottom` (default). Put the customer on top, suppliers/systems below.
- `messageFlows[]`: one end must be an external pool id, the other a node id.

Order nodes in process order with the **happy path first**: when two nodes share a lane and a
column, the earlier one gets the top row, so list the main-path node before exception nodes
(e.g. 'Mark order paid' before the 'Follow up payment' merge). That keeps the happy path on a
straight line.
