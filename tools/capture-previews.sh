#!/usr/bin/env bash
# Regenerate the README images in docs/images/ with headless Chrome.
# Usage: tools/capture-previews.sh   (macOS; set CHROME=/path/to/chrome elsewhere)
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
OUT="$ROOT/docs/images"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT
mkdir -p "$OUT"

shot() { # url out width height [scale]
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$PROFILE" \
    --force-device-scale-factor="${5:-2}" --window-size="$3,$4" --virtual-time-budget=8000 \
    --screenshot="$OUT/$2" "$1" >/dev/null 2>&1
  echo "wrote docs/images/$2"
}

svg() { # bpmn-preview-html out.svg
  "$CHROME" --headless=new --disable-gpu --user-data-dir="$PROFILE" --virtual-time-budget=10000 \
    --dump-dom "file://$1?export=svg" 2>/dev/null |
    python3 -c 'import sys,re,html; m=re.search(r"<pre id=\"svg-out\">(.*?)</pre>", sys.stdin.read(), re.S); sys.exit("no svg (offline?)") if not m else sys.stdout.write(html.unescape(m.group(1)))' > "$OUT/$2"
  echo "wrote docs/images/$2"
}

EX="$ROOT/examples/b2b-wa-order"
svg "$EX/04-flow.html" bpmn-b2b-wa-order.svg
svg "$ROOT/examples/purchase-approval/04-flow.html" bpmn-purchase-approval.svg
svg "$ROOT/examples/sop-library/SOP-WH-01-receiving-raw-materials/flow.html" bpmn-sop-receiving.svg
shot "file://$EX/07-wireframe.html?overview=1&flow=0&notes=0&clean=1" wireframe-buyer-flow.png 2560 640
shot "file://$EX/07-wireframe.html?overview=1&flow=1&vp=desktop&notes=0&clean=1" wireframe-admin-flow.png 1700 880
shot "file://$EX/07-wireframe.html?vp=mobile#S-05" wireframe-prototype.png 1440 900
if [ -f docs/social-preview.html ]; then shot "file://$ROOT/docs/social-preview.html" social-preview.png 1280 640; fi
