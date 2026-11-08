#!/usr/bin/env python3
"""Render an SOP folder (sop.md + flow.bpmn + forms/*.md) into one printable HTML page.

Usage:
    python3 sop_render.py <sop-folder> [--out sop.html]

The page shows the SOP as a controlled document, embeds the BPMN swimlane flowchart
(bpmn-js from a CDN, interactive on screen) in section 7, and appends every form as a
printable appendix, each on its own page when printed. Standard library only.
"""
import argparse
import glob
import html
import os
import re
import sys

BPMN_JS_VERSION = "18.30.1"


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: '<a href="%s">%s</a>' % (html.escape(m.group(2)), m.group(1)), s)
    s = s.replace("[Control]", '<span class="ctl">Control</span>')
    return s


def md_to_html(md):
    """Small Markdown subset: headings, tables, lists, paragraphs, bold/italic/code/links."""
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            text = m.group(2).strip()
            sid = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append('<h%d id="%s">%s</h%d>' % (lvl, sid, inline(text), lvl))
            i += 1
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            body = [r for r in rows if not all(re.match(r"^:?-{2,}:?$", c) for c in r if c)]
            t = ['<table>']
            for k, r in enumerate(body):
                tag = "th" if k == 0 and len(rows) > 1 and re.match(r"^:?-{2,}", rows[1][0] or "--") else "td"
                t.append("<tr>" + "".join("<%s>%s</%s>" % (tag, inline(c) if c else "&nbsp;", tag) for c in r) + "</tr>")
            t.append("</table>")
            out.append("\n".join(t))
            continue
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\s*[-*]\s+", "", lines[i])))
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\s*\||\s*[-*]\s)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="https://unpkg.com/bpmn-js@__VER__/dist/assets/bpmn-js.css">
<style>
  :root { --ink:#1d1f24; --muted:#5d6470; --line:#d9dce1; --paper:#ffffff; --bg:#eef0f3; --head:#f4f5f7; --accent:#2f5fa7; --ctl:#b4441c; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:14px/1.5 -apple-system, "Segoe UI", Roboto, Arial, sans-serif; }
  .bar { position:sticky; top:0; z-index:5; display:flex; gap:10px; align-items:center; padding:10px 16px; background:#fff; border-bottom:1px solid var(--line); }
  .bar b { flex:1; }
  .bar button { font:inherit; padding:6px 12px; border:1px solid var(--line); border-radius:6px; background:#fff; cursor:pointer; }
  .page { max-width:1060px; margin:24px auto; background:var(--paper); padding:44px 52px; box-shadow:0 2px 14px rgba(0,0,0,.08); border-radius:4px; }
  h1 { font-size:26px; margin:0 0 16px; padding-bottom:12px; border-bottom:3px solid var(--ink); }
  h2 { font-size:17px; margin:30px 0 10px; padding:6px 10px; background:var(--head); border-left:4px solid var(--accent); }
  h3 { font-size:15px; margin:18px 0 8px; }
  table { border-collapse:collapse; width:100%; margin:8px 0 14px; font-size:13px; }
  th, td { border:1px solid var(--line); padding:6px 8px; text-align:left; vertical-align:top; }
  th { background:var(--head); font-weight:600; }
  .doc-control td:first-child { width:28%; background:var(--head); font-weight:600; }
  .ctl { display:inline-block; font-size:11px; font-weight:700; color:#fff; background:var(--ctl); border-radius:3px; padding:0 5px; text-transform:uppercase; letter-spacing:.03em; }
  code { background:var(--head); padding:0 4px; border-radius:3px; }
  a { color:var(--accent); }
  #flow { height:460px; border:1px solid var(--line); border-radius:4px; margin:8px 0; }
  .flow-note { color:var(--muted); font-size:12px; }
  .appendix { page-break-before:always; }
  .form h1 { font-size:20px; border-bottom-width:2px; }
  .form td { height:30px; }
  .meta { color:var(--muted); font-size:12px; margin-top:28px; border-top:1px solid var(--line); padding-top:8px; }
  @media print {
    body { background:#fff; }
    .bar { display:none; }
    .page { box-shadow:none; margin:0; max-width:none; padding:0 6mm; }
    #flow { height:auto; border:none; }
    .page + .page { page-break-before:always; }
    h2 { break-after:avoid; }
    tr { break-inside:avoid; }
  }
  @media (max-width:700px) { .page { padding:24px 16px; margin:0; } table { font-size:12px; } }
</style>
</head>
<body>
<div class="bar"><b>__TITLE__</b><button onclick="window.print()">Print / save as PDF</button></div>
<div class="page">
__DOC__
<p class="meta">Rendered from sop.md by product-trio sop-builder. The Markdown file is the source of truth.</p>
</div>
__FORMS__
<script type="text/xml" id="bpmn-xml">__XML__</script>
<script src="https://unpkg.com/bpmn-js@__VER__/dist/bpmn-navigated-viewer.production.min.js"></script>
<script>
(async function () {
  const el = document.getElementById('flow');
  const xml = document.getElementById('bpmn-xml').textContent.trim();
  if (!el) return;
  if (!xml) { el.outerHTML = '<p class="flow-note">No flow.bpmn found next to sop.md.</p>'; return; }
  if (!window.BpmnJS) { el.outerHTML = '<p class="flow-note">Flowchart viewer could not load (offline). Open flow.bpmn in bpmn.io or Camunda Modeler.</p>'; return; }
  const v = new BpmnJS({ container: el });
  try { await v.importXML(xml); } catch (e) { el.outerHTML = '<p class="flow-note">Flowchart error: ' + e.message + '</p>'; return; }
  const c = v.get('canvas');
  const fit = () => { try { c.resized(); c.zoom('fit-viewport', 'auto'); } catch (e) {} };
  requestAnimationFrame(fit); window.addEventListener('resize', fit); window.addEventListener('beforeprint', fit);
})();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--out")
    a = ap.parse_args()
    src = os.path.join(a.folder, "sop.md")
    if not os.path.exists(src):
        sys.exit("sop.md not found in %s" % a.folder)
    md = open(src, encoding="utf-8").read()
    doc = md_to_html(md)
    doc = doc.replace("<table>", '<table class="doc-control">', 1)
    # section 7: embed the flowchart right after its heading
    doc = re.sub(r'(<h2 id="7-[^"]*">.*?</h2>)', r'\1\n<div id="flow"></div>', doc, count=1)
    title = re.search(r"^#\s+(.*)$", md, re.M)
    title = title.group(1).strip() if title else os.path.basename(os.path.abspath(a.folder))
    forms = []
    for f in sorted(glob.glob(os.path.join(a.folder, "forms", "*.md"))):
        forms.append('<div class="page form appendix">%s</div>' % md_to_html(open(f, encoding="utf-8").read()))
    bpmn = os.path.join(a.folder, "flow.bpmn")
    xml = open(bpmn, encoding="utf-8").read() if os.path.exists(bpmn) else ""
    page = (PAGE.replace("__TITLE__", html.escape(title)).replace("__VER__", BPMN_JS_VERSION)
            .replace("__DOC__", doc).replace("__FORMS__", "\n".join(forms))
            .replace("__XML__", xml.replace("</script", "<\\/script")))
    out = a.out or os.path.join(a.folder, "sop.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("Wrote %s (%d form%s)" % (out, len(forms), "" if len(forms) == 1 else "s"))


if __name__ == "__main__":
    main()
