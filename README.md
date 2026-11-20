# canvas-grades

Compute a course grade from a pasted Canvas grades page (plain `.txt`).

    grades.txt --> scripts/parse_canvas.awk --> TSV --> build/gradecalc --> report

- **awk** does the messy part: finds each `Click to test a different score` line,
  walks upward to find the assignment's group, reads the weights footer.
- **C** does the math: per-group totals, weighted or unweighted final.

## Use

    make            # build
    make test       # run fixtures
    scripts/canvasgrade.sh path/to/grades.txt

## Rules
- `- / N` (ungraded) is skipped, never counted as zero.
- Weighted page: final = sum(w * earned/possible) / sum(w) over groups that have graded work.
- "not weighted" page: total earned / total possible.

## Known limits (good first improvements)
- Group is found by scanning upward past indented lines and status words
  (`late`, `missing`, ...). A new Canvas status word would need adding in `is_filler`.
- Canvas "drop lowest N" rules are not modeled.
- Fixtures are synthetic, modeled on real pastes; add a real redacted page.
