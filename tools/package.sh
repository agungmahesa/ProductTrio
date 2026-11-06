#!/usr/bin/env bash
# Build distribution zips of the free product-trio skills into dist/ (for skill marketplaces
# such as Agensi, which install by zip). Bump "version" in plugin.json before each release.
#   dist/product-trio-<ver>-skills.zip         7 skills + /discovery + quick start (any SKILL.md agent)
#   dist/product-trio-<ver>-claude-plugin.zip  the Claude Code plugin folder
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
P="$ROOT/plugins/product-trio"
VER="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$P/.claude-plugin/plugin.json")"
rm -rf dist && mkdir -p dist
STAGE="$(mktemp -d)"; trap 'rm -rf "$STAGE"' EXIT

B="$STAGE/product-trio-$VER"
mkdir -p "$B"
cp -R "$P/skills" "$B/skills"
cp -R "$P/commands" "$B/commands"
cp "$ROOT/LICENSE" "$B/LICENSE.txt"
cp "$ROOT/docs/QUICKSTART.md" "$B/README.md"
(cd "$STAGE" && zip -qr "$ROOT/dist/product-trio-$VER-skills.zip" "product-trio-$VER" -x '*.DS_Store' '*__pycache__*')
(cd "$ROOT/plugins" && zip -qr "$ROOT/dist/product-trio-$VER-claude-plugin.zip" product-trio -x '*.DS_Store' '*__pycache__*')

ls -la dist | sed 's/^/  /'
