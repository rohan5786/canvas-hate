#!/usr/bin/env python3
"""Regenerates tests/fixtures/*.txt in the shape of a pasted Canvas grades page.
Data = (name, group, due, submitted, status, earned_or_None, possible, details)."""
import os
HDR = "Grades for Test User\nCourse\nArrange By\nName \tDue \tSubmitted \tStatus \tScore \t\tDetails \tSubmission Progress Status\n"
def block(name, grp, due, sub, status, e, p, det):
    s = f"{name}\n{grp}\n\t{due} \t{sub} \t\n"
    if status: s += f"{status}\n\t\n"
    es = "-" if e is None else (f"{e:g}")
    trail = "  " if det == "tail" else ""
    s += f"Click to test a different score {es} / {p:g}{trail}\n"
    s += {"": "\t\t\t\n", "n": "\t\t3 \t\n", "tail": "\t\t\t\n", "n2": "\t\t1\n \n\t\n"}[det]
    return s

unw = [  # sample 1: unweighted, one group
 ("Tell Me About You","Assignments","Sep 2 by 3:30pm","Sep 5 at 12:11pm","late",10,10,""),
 ("Meeting survey","Assignments","Sep 6 by 8pm","","",3,3,""),
 ("What interests you?","Assignments","Sep 8 by 9:30am","Sep 7 at 11:40pm","",10,10,"n"),
 ("Last time!","Assignments","Sep 11 by 11:30am","Sep 14 at 12:17am","late",8.5,10,"n"),
 ("Resume - First Draft","Assignments","Sep 14 by 2:20pm","Sep 14 at 12:03am","",9,10,"n"),
 ("Meeting Cohort Norms","Assignments","Sep 19 by 12pm","","",4.8,5,"n"),
 ("Meeting Cohort Norms #3","Assignments","Oct 17 by 12pm","","",2,5,"n2"),
 ("What else do you want me to say","Assignments","Oct 20 by 10:20am","Oct 20 at 10:06am","",3,3,"tail"),
 ("EXP - Send 2 e-mails","Assignments","Oct 23 by 12:35pm","","",20,20,"tail"),
 ("Meeting Cohort Norms #4","Assignments","Oct 31 by 12pm","","",4.7,5,"n"),
 ("Send 3 more e-mails","Assignments","Nov 6 by 12:30pm","","",30,30,"tail"),
]
bio = [  # sample 2: weighted
 ("Bring summer work","Homework","Sep 7 by 8am","","",10,10,""),
 ("Ap classroom, practice, review: Water quiz","Assessments","Sep 9 by 8am","","",None,10,""),
 ("water Quiz #1","Assessments","Sep 9 by 8am","","",7.5,9,""),
 ("Project tracker 1","Homework","Sep 11 by 8am","Sep 11 at 8:26am","late",5,5,""),
 ("AP Biology Unit 1 test (open)","Assessments","Sep 21 by 8am","","",95,100,""),
 ("Review Endosymbiosis","Homework","Sep 23 by 8am","","",None,5,""),
 ("Review Modules 13-14","Homework","Oct 15 by 8am","","",None,0,""),
 ("Unit 3 Test","Assessments","Nov 2 by 8am","","",97,100,""),
 ("Unit 8: Energy to Ecosystems","Homework","Nov 4 by 8am","","missing",None,10,""),
 ("Animal Behavior/ Exp design","Assessments","Nov 11 by 8am","","",8,9,""),
 ("Unit 8 test","Assessments","Nov 18 by 8am","","",85,100,""),
 ("Banana Lab: completed handout/graph","Homework","","","",10,10,""),
 ("Project Notebook","Homework","","","",20,20,""),
]
out = os.path.join(os.path.dirname(__file__), "fixtures")
os.makedirs(out, exist_ok=True)
with open(f"{out}/unweighted.txt","w") as f:
    f.write(HDR + "".join(block(*a) for a in unw))
    f.write("Assignments \t\t\t\t\n\t\t\t\nCalculation of totals has been disabled\nCourse assignments are not weighted.\n")
with open(f"{out}/weighted.txt","w") as f:
    f.write(HDR + "".join(block(*a) for a in bio))
    f.write("Homework \t\t\t\t\n\t\t\t\nAssessments \t\t\t\t\n\t\t\t\nImported Assignments \t\t\t\t\n\t\t\t\n")
    f.write("Calculation of totals has been disabled\nAssignments are weighted by group:\nGroup \tWeight\n"
            "Homework \t30%\nAssessments \t70%\nImported Assignments \t0%\nTotal \t100%\n")
# CRLF variant of the weighted file (what a Windows paste can look like)
with open(f"{out}/weighted.txt","rb") as f: b = f.read()
with open(f"{out}/weighted_crlf.txt","wb") as f: f.write(b.replace(b"\n", b"\r\n"))

# Independent oracle (does not share code with the C program)
def agg(rows):
    d = {}
    for r in rows:
        if r[5] is None: continue
        e,p = d.get(r[1],(0,0)); d[r[1]] = (e+r[5], p+r[6])
    return d
u = agg(unw); E=sum(v[0] for v in u.values()); P=sum(v[1] for v in u.values())
print("unweighted oracle:", E, "/", P, "=", f"{100*E/P:.2f}")
b = agg(bio); w = {"Homework":30,"Assessments":70}
fin = sum(w[g]*b[g][0]/b[g][1] for g in w)/sum(w.values())
print("weighted oracle:", b, f"{100*fin:.2f}")
