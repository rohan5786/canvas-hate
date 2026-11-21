Paste your Canvas 'Grades' page into a `.txt` and run the following script from your terminal:
    make                                        # first build
    scripts/canvasgrade.sh path/to/grades.txt   # output in your terminal/CLI

## Note the following:
- `- / N` (ungraded) is skipped and rather than counted as zero.
- If an assignment does not note a point total (e.g., formatted `<points_earned> (<grade_earned>)`) then it will be skipped.
- "weighted page" computes sum(weights * `<total_points_earned> / <total_points_possible>` ) / sum(weights).
- "not weighted" page computes `<total_points_earned> / <total_points_possible>`.
- 'awk' script to read lines efficiently, math done in C.