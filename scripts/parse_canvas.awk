# parse_canvas.awk -- turn a pasted Canvas grades page into clean TSV.
#
# Output records (tab-separated), weights first, then assignments:
#   W <group> <weight_percent>
#   A <group> <earned> <possible>
#
# Plain POSIX awk (Ubuntu's default awk is mawk, not gawk), so no gawk-isms.
# Usage: awk -f parse_canvas.awk grades.txt

BEGIN {
    OFS  = "\t"
    MARK = "Click to test a different score"
    nlines = 0; nw = 0; na = 0
    inweights = 0; saw_weight_hdr = 0
}

# Pass 1: slurp everything. We must look BACKWARD from each score line to
# find its group, so we keep the whole file in memory (a grades page is tiny).
{
    sub(/\r$/, "")          # tolerate Windows line endings
    line[++nlines] = $0
}

# Can this line sit between a group name and its score line?
# (indented junk, blank lines, status flags, bare Details numbers)
function is_filler(s) {
    if (s ~ /^[ \t]/ || s ~ /^[ \t]*$/) return 1
    if (s ~ /^(late|missing|excused|extended|resubmitted)[ \t]*$/) return 1
    if (s ~ /^[0-9]+[ \t]*$/) return 1
    return 0
}

function trim(s) {
    gsub(/^[ \t]+|[ \t]+$/, "", s)
    return s
}

END {
    for (i = 1; i <= nlines; i++) {
        s = line[i]

        # --- weights footer ------------------------------------------------
        if (index(s, "are weighted by group") > 0 && index(s, "not weighted") == 0) {
            inweights = 1; saw_weight_hdr = 1
            continue
        }
        if (inweights) {
            if (s ~ /^Total[ \t]/) { inweights = 0; continue }
            if (match(s, /[0-9]*\.?[0-9]+%[ \t]*$/)) {
                pct  = substr(s, RSTART); sub(/%.*/, "", pct)
                name = trim(substr(s, 1, RSTART - 1))
                if (name != "" && name != "Group") wout[++nw] = "W" OFS name OFS pct
            }
            continue
        }

        # --- score lines -----------------------------------------------------
        p = index(s, MARK)
        if (p == 0) continue
        rest = substr(s, p + length(MARK))

        # Only "<num> / <num>" counts. "- / 10" (ungraded) doesn't match,
        # so it is skipped: not a zero, just absent.
        if (!match(rest, /^[ \t]*[0-9]*\.?[0-9]+[ \t]*\/[ \t]*[0-9]*\.?[0-9]+/)) continue
        split(substr(rest, RSTART, RLENGTH), part, "/")
        earned = part[1] + 0; possible = part[2] + 0

        # Walk upward past filler to find the group-name line.
        j = i - 1
        while (j >= 1 && is_filler(line[j])) j--
        grp = (j >= 1) ? trim(line[j]) : ""
        if (grp == "") { grp = "(unknown)"; print "warn: no group for line " i > "/dev/stderr" }

        aout[++na] = "A" OFS grp OFS earned OFS possible
    }

    if (saw_weight_hdr && nw == 0)
        print "warn: weighted page but no weight rows parsed" > "/dev/stderr"

    for (k = 1; k <= nw; k++) print wout[k]
    for (k = 1; k <= na; k++) print aout[k]
}
