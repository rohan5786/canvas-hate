#!/usr/bin/env bash
# canvasgrade.sh -- glue: parse a pasted Canvas grades page, then compute.
# Usage: scripts/canvasgrade.sh grades.txt
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bin="$here/../build/gradecalc"

if [[ $# -ne 1 || ! -r "$1" ]]; then
    echo "usage: $0 <grades.txt>" >&2
    exit 2
fi
if [[ ! -x "$bin" ]]; then
    echo "gradecalc not built yet; run 'make' in the repo root" >&2
    exit 2
fi

awk -f "$here/parse_canvas.awk" "$1" | "$bin"
