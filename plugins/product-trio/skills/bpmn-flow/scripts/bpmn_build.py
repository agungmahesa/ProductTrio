#!/usr/bin/env python3
"""Build a BPMN 2.0 file (with diagram layout) and an HTML preview from a JSON process spec.

Usage:
    python3 bpmn_build.py <spec.json> [--out-dir DIR] [--name BASENAME] [--strict]

Writes <BASENAME>.bpmn and <BASENAME>.html (default BASENAME = spec file name without
extension) and prints a validation report. Exit code 1 on validation errors (or on
warnings too with --strict). Standard library only; Python 3.8+.

Spec format: see ../references/spec-format.md
"""
import argparse
import html
import json
import os
import re
import sys
from collections import defaultdict, deque
from xml.sax.saxutils import escape, quoteattr

BPMN_JS_VERSION = "18.30.1"

EVENT_TYPES = {"startEvent", "endEvent", "intermediateCatchEvent", "intermediateThrowEvent"}
TASK_TYPES = {"task", "userTask", "serviceTask", "manualTask", "sendTask", "receiveTask",
              "scriptTask", "businessRuleTask", "callActivity", "subProcess"}
GATEWAY_TYPES = {"exclusiveGateway", "parallelGateway", "inclusiveGateway", "eventBasedGateway"}
EVENT_DEFS = {"message", "timer", "error", "signal", "terminate", "conditional", "escalation"}
ALL_TYPES = EVENT_TYPES | TASK_TYPES | GATEWAY_TYPES

SIZE = {"event": (36, 36), "gateway": (50, 50), "task": (100, 80)}
COL_W = 160          # horizontal distance between ranks
ROW_H = 110          # height of one row inside a lane
LANE_LABEL = 30      # lane name strip
POOL_LABEL = 30      # pool name strip
LEFT_PAD = 60        # space between lane label and first node
BLACKBOX_H = 70      # external (black-box) pool height
GAP = 40             # gap between pools

NCNAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.\-]*$")


def kind(t):
    if t in EVENT_TYPES:
        return "event"
    if t in GATEWAY_TYPES:
        return "gateway"
    return "task"


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


# --------------------------------------------------------------------------- validation
def validate(spec, rep):
    pool = spec.get("pool") or {}
    lanes = pool.get("lanes") or []
    nodes = spec.get("nodes") or []
    flows = spec.get("flows") or []
    externals = spec.get("externalPools") or []
    mflows = spec.get("messageFlows") or []

    if not spec.get("id") or not NCNAME.match(str(spec.get("id"))):
        rep.err("spec.id is required and must be a valid XML id (letters, digits, -, _, .; no leading digit)")
    if not lanes:
        rep.err("pool.lanes must contain at least one lane (one lane per role/actor)")

    ids = set()
    def reg(i, what):
        if not i or not NCNAME.match(str(i)):
            rep.err("%s id %r is not a valid XML id" % (what, i))
        elif i in ids:
            rep.err("duplicate id %r" % i)
        ids.add(i)

    reg(spec.get("id"), "process")
    reg(pool.get("id", "Pool_main"), "pool")
    lane_ids = set()
    for ln in lanes:
        reg(ln.get("id"), "lane")
        lane_ids.add(ln.get("id"))
        if re.search(r"\b(system|database|api|server)\b", ln.get("name", ""), re.I):
            rep.warn("lane %r looks like a system; lanes should be roles. Use serviceTask in the "
                     "owning lane or an external pool instead" % ln.get("name"))
    ext_ids = set()
    for ep in externals:
        reg(ep.get("id"), "external pool")
        ext_ids.add(ep.get("id"))

    by_id = {}
    for n in nodes:
        reg(n.get("id"), "node")
        by_id[n.get("id")] = n
        t = n.get("type")
        if t not in ALL_TYPES:
            rep.err("node %s has unknown type %r (allowed: %s)" % (n.get("id"), t, ", ".join(sorted(ALL_TYPES))))
        if n.get("lane") not in lane_ids:
            rep.err("node %s references unknown lane %r" % (n.get("id"), n.get("lane")))
        ev = n.get("event")
        if ev and ev not in EVENT_DEFS:
            rep.err("node %s has unknown event definition %r (allowed: %s)" % (n.get("id"), ev, ", ".join(sorted(EVENT_DEFS))))
        if ev and t not in EVENT_TYPES:
            rep.err("node %s: 'event' is only valid on event types" % n.get("id"))
        if t in TASK_TYPES:
            name = (n.get("name") or "").strip()
            if len(name.split()) < 2:
                rep.warn("task %s name %r should be verb + object (e.g. 'Approve order')" % (n.get("id"), name))
        if t == "intermediateCatchEvent" and not ev:
            rep.warn("intermediate catch event %s has no event definition (timer/message/...)" % n.get("id"))

    out_e, in_e = defaultdict(list), defaultdict(list)
    for i, f in enumerate(flows):
        f.setdefault("id", "Flow_%d" % (i + 1))
        reg(f["id"], "sequence flow")
        a, b = f.get("from"), f.get("to")
        if a not in by_id or b not in by_id:
            rep.err("sequence flow %s connects unknown node(s) %r -> %r" % (f["id"], a, b))
            continue
        out_e[a].append(f)
        in_e[b].append(f)

    starts = [n for n in nodes if n.get("type") == "startEvent"]
    ends = [n for n in nodes if n.get("type") == "endEvent"]
    if not starts:
        rep.err("process needs at least one startEvent")
    if not ends:
        rep.err("process needs at least one endEvent")

    for n in nodes:
        nid, t = n.get("id"), n.get("type")
        ins, outs = len(in_e[nid]), len(out_e[nid])
        if t == "startEvent" and ins:
            rep.err("startEvent %s must not have incoming sequence flows" % nid)
        if t == "endEvent" and outs:
            rep.err("endEvent %s must not have outgoing sequence flows" % nid)
        if t != "startEvent" and ins == 0:
            rep.err("%s %s has no incoming sequence flow" % (t, nid))
        if t != "endEvent" and outs == 0:
            rep.err("%s %s has no outgoing sequence flow (dead end)" % (t, nid))
        if t in TASK_TYPES and outs > 1:
            rep.warn("task %s has %d outgoing flows; use a gateway to make the split explicit" % (nid, outs))
        if t in TASK_TYPES and ins > 1:
            rep.warn("task %s has %d incoming flows (implicit merge); add an exclusive merge gateway before it"
                     % (nid, ins))
        if t in GATEWAY_TYPES:
            if ins > 1 and outs > 1:
                rep.warn("gateway %s both joins and splits; use two gateways for clarity" % nid)
            if ins <= 1 and outs <= 1:
                rep.warn("gateway %s neither splits nor joins; remove it" % nid)
            if outs > 1 and t in ("exclusiveGateway", "inclusiveGateway"):
                for f in out_e[nid]:
                    if not f.get("name") and not f.get("default"):
                        rep.err("flow %s leaving %s %s needs a condition label (name) or default:true"
                                % (f["id"], t, nid))
                if not (n.get("name") or "").strip().endswith("?"):
                    rep.warn("splitting gateway %s should be named as a question (e.g. 'Stock available?')" % nid)
                if sum(1 for f in out_e[nid] if f.get("default")) > 1:
                    rep.err("gateway %s has more than one default flow" % nid)
            if t == "eventBasedGateway":
                for f in out_e[nid]:
                    tgt = by_id.get(f.get("to"), {})
                    if tgt.get("type") not in ("intermediateCatchEvent", "receiveTask"):
                        rep.err("eventBasedGateway %s must lead to intermediate catch events or receive tasks "
                                "(found %s)" % (nid, tgt.get("type")))

    par_split = sum(1 for n in nodes if n.get("type") == "parallelGateway" and len(out_e[n["id"]]) > 1)
    par_join = sum(1 for n in nodes if n.get("type") == "parallelGateway" and len(in_e[n["id"]]) > 1)
    if par_split != par_join:
        rep.warn("parallel gateways: %d split(s) vs %d join(s); every AND-split should be joined by an AND-join"
                 % (par_split, par_join))

    # reachability
    seen = set(s["id"] for s in starts)
    q = deque(seen)
    while q:
        cur = q.popleft()
        for f in out_e[cur]:
            if f["to"] not in seen:
                seen.add(f["to"]); q.append(f["to"])
    for n in nodes:
        if n["id"] not in seen and n.get("type") != "startEvent":
            rep.err("node %s is not reachable from any start event" % n["id"])
    back = set(e["id"] for e in ends)
    q = deque(back)
    while q:
        cur = q.popleft()
        for f in in_e[cur]:
            if f["from"] not in back:
                back.add(f["from"]); q.append(f["from"])
    for n in nodes:
        if n["id"] not in back and n.get("type") != "endEvent":
            rep.err("node %s can never reach an end event (infinite loop or dead end)" % n["id"])

    for i, m in enumerate(mflows):
        m.setdefault("id", "MsgFlow_%d" % (i + 1))
        reg(m["id"], "message flow")
        a, b = m.get("from"), m.get("to")
        for end in (a, b):
            if end not in by_id and end not in ext_ids:
                rep.err("message flow %s references unknown node/pool %r" % (m["id"], end))
        if a in by_id and b in by_id:
            rep.err("message flow %s connects two nodes in the same pool; use a sequence flow" % m["id"])
        if a in ext_ids and b in ext_ids:
            rep.err("message flow %s connects two external pools; out of scope for this diagram" % m["id"])
        if not m.get("name"):
            rep.warn("message flow %s should be named after the message (e.g. 'Invoice')" % m["id"])

    return by_id, out_e, in_e


# --------------------------------------------------------------------------- layout
def layout(spec, by_id, out_e, in_e):
    nodes = spec["nodes"]
    lanes = spec["pool"]["lanes"]
    order = {n["id"]: i for i, n in enumerate(nodes)}

    # find back edges with DFS from starts (so loops do not break ranking)
    back_edges, state = set(), {}
    def dfs(u):
        state[u] = 1
        for f in sorted(out_e[u], key=lambda f: order.get(f["to"], 0)):
            v = f["to"]
            if state.get(v) == 1:
                back_edges.add(f["id"])
            elif v not in state:
                dfs(v)
        state[u] = 2
    sys.setrecursionlimit(10000)
    for n in nodes:
        if n["type"] == "startEvent" and n["id"] not in state:
            dfs(n["id"])
    for n in nodes:
        if n["id"] not in state:
            dfs(n["id"])

    # longest-path rank over forward edges (Kahn)
    indeg = defaultdict(int)
    for n in nodes:
        for f in out_e[n["id"]]:
            if f["id"] not in back_edges:
                indeg[f["to"]] += 1
    rank = {n["id"]: 0 for n in nodes}
    q = deque(sorted([n["id"] for n in nodes if indeg[n["id"]] == 0], key=order.get))
    while q:
        u = q.popleft()
        for f in out_e[u]:
            if f["id"] in back_edges:
                continue
            v = f["to"]
            rank[v] = max(rank[v], rank[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    for n in nodes:
        if n.get("column") is not None:
            rank[n["id"]] = int(n["column"])

    # rows inside each lane: nodes sharing lane+rank stack vertically
    slot = defaultdict(list)
    for n in sorted(nodes, key=lambda n: order[n["id"]]):
        slot[(n["lane"], rank[n["id"]])].append(n["id"])
    row = {}
    lane_rows = defaultdict(lambda: 1)
    for (lane, _r), ids in slot.items():
        for i, nid in enumerate(ids):
            row[nid] = i
        lane_rows[lane] = max(lane_rows[lane], len(ids))

    max_rank = max(rank.values()) if rank else 0
    x0 = POOL_LABEL + LANE_LABEL + LEFT_PAD
    width = x0 + (max_rank + 1) * COL_W
    pool_y = 40
    lane_box, y = {}, pool_y
    for ln in lanes:
        h = lane_rows[ln["id"]] * ROW_H + 20
        lane_box[ln["id"]] = (POOL_LABEL, y, width - POOL_LABEL, h)
        y += h
    pool_box = (0, pool_y, width, y - pool_y)

    shapes = {}
    for n in nodes:
        w, h = SIZE[kind(n["type"])]
        lx, ly, _, _ = lane_box[n["lane"]]
        cx = x0 + rank[n["id"]] * COL_W + 50
        cy = ly + 10 + row[n["id"]] * ROW_H + ROW_H / 2
        shapes[n["id"]] = (cx - w / 2, cy - h / 2, w, h)

    ext_box, ey = {}, y + GAP
    tops = [ep for ep in spec.get("externalPools") or [] if ep.get("position") == "top"]
    ty = pool_y - GAP - BLACKBOX_H
    for ep in reversed(tops):
        ext_box[ep["id"]] = (0, ty, width, BLACKBOX_H)
        ty -= BLACKBOX_H + GAP
    for ep in spec.get("externalPools") or []:
        if ep.get("position") == "top":
            continue
        ext_box[ep["id"]] = (0, ey, width, BLACKBOX_H)
        ey += BLACKBOX_H + GAP

    def right(b): return (b[0] + b[2], b[1] + b[3] / 2)
    def left(b): return (b[0], b[1] + b[3] / 2)
    def top(b): return (b[0] + b[2] / 2, b[1])
    def bottom(b): return (b[0] + b[2] / 2, b[1] + b[3])

    edges = {}
    for f in spec["flows"]:
        s, t = shapes[f["from"]], shapes[f["to"]]
        if f["id"] in back_edges or t[0] + t[2] / 2 <= s[0] + s[2] / 2:
            # loop back: exit right into the column gap, run along the bottom of the lower
            # lane (clear of nodes), then up into the target's bottom
            sr, tb = right(s), bottom(t)
            gx = s[0] + s[2] / 2 + 70          # gap between this column and the next
            ls, lt = lane_box[by_id[f["from"]]["lane"]], lane_box[by_id[f["to"]]["lane"]]
            yy = max(ls[1] + ls[3], lt[1] + lt[3]) - 7
            pts = [sr, (gx, sr[1]), (gx, yy), (tb[0], yy), tb]
        else:
            a, b = right(s), left(t)
            blockers = [sh for nid, sh in shapes.items()
                        if nid not in (f["from"], f["to"]) and sh[0] > a[0] and sh[0] + sh[2] < b[0]
                        and sh[1] <= a[1] <= sh[1] + sh[3]] if abs(a[1] - b[1]) < 1 else []
            if blockers:
                # straight line would cross other nodes: detour under them
                lb = lane_box[by_id[f["from"]]["lane"]]
                yy = min(max(sh[1] + sh[3] for sh in blockers) + 14, lb[1] + lb[3] - 4)
                sb, tb = bottom(s), bottom(t)
                pts = [sb, (sb[0], yy), (tb[0], yy), tb]
            elif abs(a[1] - b[1]) < 1:
                pts = [a, b]
            elif by_id[f["from"]]["type"] in GATEWAY_TYPES:
                # leave gateway from top/bottom, then horizontally into target
                a = top(s) if b[1] < a[1] else bottom(s)
                pts = [a, (a[0], b[1]), b]
            else:
                mx = a[0] + (b[0] - a[0]) / 2
                pts = [a, (mx, a[1]), (mx, b[1]), b]
        edges[f["id"]] = pts

    medges = {}
    used = defaultdict(int)   # spread several message flows on one node side
    for m in spec.get("messageFlows") or []:
        a, b = m["from"], m["to"]
        pool_id, node_id = (b, a) if b in ext_box else (a, b)
        if node_id not in shapes or pool_id not in ext_box:
            medges[m["id"]] = []
            continue
        sh, pb = shapes[node_id], ext_box[pool_id]
        above = pb[1] < sh[1]
        k = used[(node_id, above)]; used[(node_id, above)] += 1
        x = sh[0] + sh[2] / 2 + (k * 16 - 8 if sh[2] >= 50 else 0) * (1 if k else 0)
        node_y = sh[1] if above else sh[1] + sh[3]
        pool_y_edge = pb[1] + pb[3] if above else pb[1]
        lo, hi = min(node_y, pool_y_edge), max(node_y, pool_y_edge)

        def blocked(xx):
            return any(o != node_id and o_sh[0] - 4 <= xx <= o_sh[0] + o_sh[2] + 4
                       and o_sh[1] < hi and o_sh[1] + o_sh[3] > lo
                       for o, o_sh in shapes.items())
        if blocked(x):
            half = sh[2] / 2 - 6
            for dx in (half, -half, half * .6, -half * .6):
                if not blocked(sh[0] + sh[2] / 2 + dx):
                    x = sh[0] + sh[2] / 2 + dx
                    break
        if node_id == a:
            medges[m["id"]] = [(x, node_y), (x, pool_y_edge)]
        else:
            medges[m["id"]] = [(x, pool_y_edge), (x, node_y)]
    return dict(shapes=shapes, lane_box=lane_box, pool_box=pool_box, ext_box=ext_box,
                edges=edges, medges=medges)


# --------------------------------------------------------------------------- xml
def fmt(v):
    return ("%d" % v) if float(v).is_integer() else ("%.1f" % v)


def bounds(b):
    return '<dc:Bounds x="%s" y="%s" width="%s" height="%s" />' % tuple(fmt(v) for v in b)


def to_xml(spec, by_id, out_e, in_e, lay):
    pid = spec["id"]
    pool = spec["pool"]
    pool_id = pool.get("id", "Pool_main")
    collab_id = "Collab_" + pid
    L = []
    w = L.append
    w('<?xml version="1.0" encoding="UTF-8"?>')
    w('<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
      'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
      'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
      'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
      'id="Defs_%s" targetNamespace="http://bpmn.io/schema/bpmn" exporter="product-trio bpmn_build" exporterVersion="0.1.0">' % pid)
    w('  <bpmn:collaboration id=%s>' % quoteattr(collab_id))
    w('    <bpmn:participant id=%s name=%s processRef=%s />' % (quoteattr(pool_id), quoteattr(pool.get("name", spec.get("name", pid))), quoteattr(pid)))
    for ep in spec.get("externalPools") or []:
        w('    <bpmn:participant id=%s name=%s />' % (quoteattr(ep["id"]), quoteattr(ep.get("name", ep["id"]))))
    for m in spec.get("messageFlows") or []:
        w('    <bpmn:messageFlow id=%s name=%s sourceRef=%s targetRef=%s />' % (
            quoteattr(m["id"]), quoteattr(m.get("name", "")), quoteattr(m["from"]), quoteattr(m["to"])))
    w('  </bpmn:collaboration>')

    w('  <bpmn:process id=%s name=%s isExecutable="false">' % (quoteattr(pid), quoteattr(spec.get("name", pid))))
    if spec.get("description"):
        w('    <bpmn:documentation>%s</bpmn:documentation>' % escape(spec["description"]))
    w('    <bpmn:laneSet id="LaneSet_%s">' % pid)
    for ln in pool["lanes"]:
        w('      <bpmn:lane id=%s name=%s>' % (quoteattr(ln["id"]), quoteattr(ln.get("name", ln["id"]))))
        for n in spec["nodes"]:
            if n["lane"] == ln["id"]:
                w('        <bpmn:flowNodeRef>%s</bpmn:flowNodeRef>' % escape(n["id"]))
        w('      </bpmn:lane>')
    w('    </bpmn:laneSet>')

    defaults = {}
    for f in spec["flows"]:
        if f.get("default"):
            defaults[f["from"]] = f["id"]
    for n in spec["nodes"]:
        t = n["type"]
        attrs = 'id=%s name=%s' % (quoteattr(n["id"]), quoteattr(n.get("name", "")))
        if n["id"] in defaults and t in ("exclusiveGateway", "inclusiveGateway"):
            attrs += ' default=%s' % quoteattr(defaults[n["id"]])
        w('    <bpmn:%s %s>' % (t, attrs))
        if n.get("documentation"):
            w('      <bpmn:documentation>%s</bpmn:documentation>' % escape(n["documentation"]))
        for f in in_e[n["id"]]:
            w('      <bpmn:incoming>%s</bpmn:incoming>' % escape(f["id"]))
        for f in out_e[n["id"]]:
            w('      <bpmn:outgoing>%s</bpmn:outgoing>' % escape(f["id"]))
        ev = n.get("event")
        if ev:
            edid = "%s_def" % n["id"]
            if ev == "timer":
                w('      <bpmn:timerEventDefinition id="%s">' % edid)
                if n.get("timer"):
                    w('        <bpmn:timeDuration xsi:type="bpmn:tFormalExpression" '
                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">%s</bpmn:timeDuration>' % escape(n["timer"]))
                w('      </bpmn:timerEventDefinition>')
            elif ev == "conditional":
                w('      <bpmn:conditionalEventDefinition id="%s"><bpmn:condition xsi:type="bpmn:tFormalExpression" '
                  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" /></bpmn:conditionalEventDefinition>' % edid)
            else:
                w('      <bpmn:%sEventDefinition id="%s" />' % (ev, edid))
        w('    </bpmn:%s>' % t)
    for f in spec["flows"]:
        w('    <bpmn:sequenceFlow id=%s name=%s sourceRef=%s targetRef=%s />' % (
            quoteattr(f["id"]), quoteattr(f.get("name", "")), quoteattr(f["from"]), quoteattr(f["to"])))
    w('  </bpmn:process>')

    # diagram interchange
    w('  <bpmndi:BPMNDiagram id="Diagram_%s">' % pid)
    w('    <bpmndi:BPMNPlane id="Plane_%s" bpmnElement=%s>' % (pid, quoteattr(collab_id)))
    w('      <bpmndi:BPMNShape id="%s_di" bpmnElement=%s isHorizontal="true">%s</bpmndi:BPMNShape>' % (
        pool_id, quoteattr(pool_id), bounds(lay["pool_box"])))
    for ln in pool["lanes"]:
        w('      <bpmndi:BPMNShape id="%s_di" bpmnElement=%s isHorizontal="true">%s</bpmndi:BPMNShape>' % (
            ln["id"], quoteattr(ln["id"]), bounds(lay["lane_box"][ln["id"]])))
    for n in spec["nodes"]:
        b = lay["shapes"][n["id"]]
        extra = ' isMarkerVisible="true"' if n["type"] == "exclusiveGateway" else ""
        label = ""
        if kind(n["type"]) in ("event", "gateway") and n.get("name"):
            lw = 100
            label = '<bpmndi:BPMNLabel>%s</bpmndi:BPMNLabel>' % bounds(
                (b[0] + b[2] / 2 - lw / 2, b[1] + b[3] + 4, lw, 27))
        w('      <bpmndi:BPMNShape id="%s_di" bpmnElement=%s%s>%s%s</bpmndi:BPMNShape>' % (
            n["id"], quoteattr(n["id"]), extra, bounds(b), label))
    for ep in spec.get("externalPools") or []:
        w('      <bpmndi:BPMNShape id="%s_di" bpmnElement=%s isHorizontal="true">%s</bpmndi:BPMNShape>' % (
            ep["id"], quoteattr(ep["id"]), bounds(lay["ext_box"][ep["id"]])))
    for f in spec["flows"]:
        pts = "".join('<di:waypoint x="%s" y="%s" />' % (fmt(x), fmt(y)) for x, y in lay["edges"][f["id"]])
        label = ""
        if f.get("name"):
            pts_ = lay["edges"][f["id"]]
            x, y = pts_[0]
            x2, y2 = pts_[1]
            if len(pts_) == 4 and abs(x - x2) < 1 and abs(pts_[1][1] - pts_[2][1]) < 1:
                # detour / loop: label on the horizontal leg, clear of the source label
                lx, ly = x + 55 if pts_[2][0] > x else x - 125, y2 - 16
            elif abs(y - y2) < 1:
                lx, ly = (x + x2) / 2 + 4, y - 18
            else:
                lx, ly = x + 6, (y + y2) / 2 - 7
            label = '<bpmndi:BPMNLabel>%s</bpmndi:BPMNLabel>' % bounds((lx, ly, 70, 14))
        w('      <bpmndi:BPMNEdge id="%s_di" bpmnElement=%s>%s%s</bpmndi:BPMNEdge>' % (
            f["id"], quoteattr(f["id"]), pts, label))
    for m in spec.get("messageFlows") or []:
        if lay["medges"].get(m["id"]):
            pts = "".join('<di:waypoint x="%s" y="%s" />' % (fmt(x), fmt(y)) for x, y in lay["medges"][m["id"]])
            w('      <bpmndi:BPMNEdge id="%s_di" bpmnElement=%s>%s</bpmndi:BPMNEdge>' % (
                m["id"], quoteattr(m["id"]), pts))
    w('    </bpmndi:BPMNPlane>')
    w('  </bpmndi:BPMNDiagram>')
    w('</bpmn:definitions>')
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- html preview
PREVIEW = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ - BPMN</title>
<link rel="stylesheet" href="https://unpkg.com/bpmn-js@__VER__/dist/assets/bpmn-js.css">
<style>
  :root { --bg:#fafafa; --fg:#1d1d1f; --muted:#6b6b70; --line:#e2e2e6; --card:#fff; }
  * { box-sizing:border-box; }
  body { margin:0; font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif; background:var(--bg); color:var(--fg); }
  header { display:flex; gap:12px; align-items:center; flex-wrap:wrap; padding:12px 16px; border-bottom:1px solid var(--line); background:var(--card); }
  h1 { font-size:16px; margin:0; flex:1; min-width:200px; }
  .meta { color:var(--muted); font-size:12px; }
  button, a.btn { font:inherit; font-size:13px; padding:6px 12px; border:1px solid var(--line); border-radius:6px; background:var(--card); color:var(--fg); cursor:pointer; text-decoration:none; }
  button:hover, a.btn:hover { border-color:#999; }
  #canvas { height:calc(100vh - 58px); background:#fff; }
  #err { display:none; padding:16px; color:#b00020; white-space:pre-wrap; }
  .bjs-powered-by { opacity:.5; }
</style>
</head>
<body>
<header>
  <h1>__TITLE__ <span class="meta">BPMN 2.0 · __COUNTS__</span></h1>
  <button id="fit">Fit</button>
  <button id="zin">+</button>
  <button id="zout">−</button>
  <a class="btn" id="dl" download="__FILE__">Download .bpmn</a>
  <button id="svg">Export SVG</button>
</header>
<div id="err"></div>
<div id="canvas"></div>
<script type="text/xml" id="bpmn-xml">__XML__</script>
<script src="https://unpkg.com/bpmn-js@__VER__/dist/bpmn-navigated-viewer.production.min.js"></script>
<script>
(async function () {
  const xml = document.getElementById('bpmn-xml').textContent.trim();
  document.getElementById('dl').href = URL.createObjectURL(new Blob([xml], {type: 'application/xml'}));
  const err = document.getElementById('err');
  if (!window.BpmnJS) { err.style.display = 'block'; err.textContent = 'Could not load bpmn-js from unpkg (offline?). Open the .bpmn file in https://demo.bpmn.io or Camunda Modeler.'; return; }
  const viewer = new BpmnJS({ container: '#canvas' });
  try {
    const res = await viewer.importXML(xml);
    if (res.warnings && res.warnings.length) console.warn(res.warnings);
  } catch (e) { err.style.display = 'block'; err.textContent = 'Import error: ' + e.message; return; }
  const canvas = viewer.get('canvas');
  const fit = () => { try { canvas.resized(); canvas.zoom('fit-viewport', 'auto'); } catch (e) { /* container not sized yet */ } };
  requestAnimationFrame(fit);
  window.addEventListener('resize', fit);
  document.getElementById('fit').onclick = fit;
  document.getElementById('zin').onclick = () => canvas.zoom(canvas.zoom() * 1.2);
  document.getElementById('zout').onclick = () => canvas.zoom(canvas.zoom() / 1.2);
  document.getElementById('svg').onclick = async () => {
    const { svg } = await viewer.saveSVG();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([svg], {type: 'image/svg+xml'}));
    a.download = '__FILE__'.replace(/\\.bpmn$/, '.svg'); a.click();
  };
})();
</script>
</body>
</html>
"""


def to_html(spec, xml, filename):
    counts = "%d lanes · %d nodes · %d flows" % (len(spec["pool"]["lanes"]), len(spec["nodes"]), len(spec["flows"]))
    title = html.escape(spec.get("name", spec["id"]))
    return (PREVIEW.replace("__TITLE__", title).replace("__VER__", BPMN_JS_VERSION)
            .replace("__COUNTS__", counts).replace("__FILE__", html.escape(filename))
            .replace("__XML__", xml.replace("</script", "<\\/script")))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out-dir")
    ap.add_argument("--name")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    a = ap.parse_args()

    with open(a.spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    spec.setdefault("pool", {})
    spec.setdefault("nodes", [])
    spec.setdefault("flows", [])
    rep = Report()
    by_id, out_e, in_e = validate(spec, rep)

    for m in rep.errors:
        print("ERROR   " + m)
    for m in rep.warnings:
        print("WARNING " + m)
    if rep.errors or (a.strict and rep.warnings):
        print("\nValidation failed: %d error(s), %d warning(s). Nothing written." % (len(rep.errors), len(rep.warnings)))
        sys.exit(1)
    if a.check:
        print("Validation passed: %d warning(s)." % len(rep.warnings))
        return

    lay = layout(spec, by_id, out_e, in_e)
    xml = to_xml(spec, by_id, out_e, in_e, lay)
    out_dir = a.out_dir or os.path.dirname(os.path.abspath(a.spec))
    base = a.name or os.path.splitext(os.path.basename(a.spec))[0]
    os.makedirs(out_dir, exist_ok=True)
    bpmn_path = os.path.join(out_dir, base + ".bpmn")
    html_path = os.path.join(out_dir, base + ".html")
    with open(bpmn_path, "w", encoding="utf-8") as fh:
        fh.write(xml)
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(to_html(spec, xml, os.path.basename(bpmn_path)))
    print("\nValidation passed: %d warning(s)." % len(rep.warnings))
    print("Wrote %s" % bpmn_path)
    print("Wrote %s" % html_path)


if __name__ == "__main__":
    main()
