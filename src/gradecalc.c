/*
 * gradecalc.c -- read clean TSV from parse_canvas.awk, compute grades.
 *
 * Input (stdin), tab-separated:
 *   W <group> <weight_percent>
 *   A <group> <earned> <possible>
 *
 * Weighted course  : final = sum(w * earned/possible) / sum(w), over groups
 *                    that actually have graded points (Canvas rescales
 *                    when a group is empty).
 * Unweighted course: final = total earned / total possible.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_GROUPS 64
#define NAME_LEN   128
#define LINE_LEN   512

typedef struct {
    char   name[NAME_LEN];
    double weight;      // percent, e.g. 30.0
    int    has_weight;
    double earned;
    double possible;
} Group;

static Group groups[MAX_GROUPS];
static int   ngroups = 0;

static Group *find_or_add(const char *name)
{
    for (int i = 0; i < ngroups; i++)
        if (strcmp(groups[i].name, name) == 0)
            return &groups[i];

    if (ngroups == MAX_GROUPS) {
        fprintf(stderr, "error: more than %d groups\n", MAX_GROUPS);
        exit(1);
    }
    Group *g = &groups[ngroups++];
    memset(g, 0, sizeof *g);
    snprintf(g->name, NAME_LEN, "%s", name);
    return g;
}

/* Split s in place on tabs; returns field count (at most max). */
static int split_tabs(char *s, char *f[], int max)
{
    int n = 0;
    f[n++] = s;
    for (char *p = s; *p && n < max; p++)
        if (*p == '\t') { *p = '\0'; f[n++] = p + 1; }
    return n;
}

static int parse_num(const char *s, double *out)
{
    char *end;
    *out = strtod(s, &end);
    return end != s;
}

int main(void)
{
    char buf[LINE_LEN];
    long lineno = 0;

    while (fgets(buf, sizeof buf, stdin)) {
        lineno++;
        buf[strcspn(buf, "\r\n")] = '\0';
        if (buf[0] == '\0') continue;

        char *f[4];
        int n = split_tabs(buf, f, 4);

        if (strcmp(f[0], "W") == 0 && n == 3) {
            double w;
            if (!parse_num(f[2], &w)) { fprintf(stderr, "line %ld: bad weight\n", lineno); continue; }
            Group *g = find_or_add(f[1]);
            g->weight = w;
            g->has_weight = 1;
        } else if (strcmp(f[0], "A") == 0 && n == 4) {
            double e, p;
            if (!parse_num(f[2], &e) || !parse_num(f[3], &p)) {
                fprintf(stderr, "line %ld: bad score\n", lineno);
                continue;
            }
            Group *g = find_or_add(f[1]);
            g->earned   += e;
            g->possible += p;
        } else {
            fprintf(stderr, "line %ld: unrecognized record\n", lineno);
        }
    }

    if (ngroups == 0) { fprintf(stderr, "error: no assignments found\n"); return 1; }

    int weighted = 0;
    for (int i = 0; i < ngroups; i++)
        if (groups[i].has_weight) weighted = 1;

    double total_e = 0, total_p = 0;   /* unweighted path */
    double wsum = 0, used_w = 0;       /* weighted path   */

    for (int i = 0; i < ngroups; i++) {
        Group *g = &groups[i];
        total_e += g->earned;
        total_p += g->possible;

        if (weighted && !g->has_weight && g->possible > 0)
            fprintf(stderr, "warn: group '%s' has no weight; ignored\n", g->name);

        if (weighted) printf("%-24s %6.2f%%   ", g->name, g->has_weight ? g->weight : 0.0);
        else          printf("%-24s %7s   ", g->name, "n/a");

        if (g->possible > 0)
            printf("%g / %g  (%.2f%%)\n", g->earned, g->possible, 100.0 * g->earned / g->possible);
        else
            printf("%g / %g  (no graded work)\n", g->earned, g->possible);

        if (weighted && g->has_weight && g->possible > 0) {
            wsum   += g->weight * (g->earned / g->possible);
            used_w += g->weight;
        }
    }

    double final;
    if (weighted) {
        if (used_w <= 0) { fprintf(stderr, "error: no weighted group has graded work\n"); return 1; }
        final = 100.0 * wsum / used_w;
    } else {
        if (total_p <= 0) { fprintf(stderr, "error: zero points possible\n"); return 1; }
        final = 100.0 * total_e / total_p;
    }

    printf("Final grade: %.2f%%\n", final);
    return 0;
}
