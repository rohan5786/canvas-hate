#!/usr/bin/env bash
# Runs the pipeline on each fixture and compares the final line.
# Expected values come from the independent Python oracle in make_fixtures.py.
cd "$(dirname "$0")/.."
fail=0
check() {  # file expected_final_line
    got="$(scripts/canvasgrade.sh "tests/fixtures/$1" | tail -n1)"
    if [[ "$got" == "$2" ]]; then echo "ok   $1"; else echo "FAIL $1: got '$got', want '$2'"; fail=1; fi
}
check unweighted.txt    "Final grade: 94.59%"
check weighted.txt      "Final grade: 94.39%"
check weighted_crlf.txt "Final grade: 94.39%"
exit $fail
