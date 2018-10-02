import statistics
import json
import requests
import re

notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
intervals = ["PO", "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7"]
consonance = [12, 7, 5, 9, 4, 3, 8, 2, 10, 1, 11, 6]

scales = []

for s in range(1, 2048, 2):
    binScale = ("{:0>12b}".format(s))[::-1]
    notesInScale = []
    for i, v in enumerate(binScale):
        if v == "1":
            notesInScale.append(notes[i])
    numNotes = binScale.count("1")
    intervals = [len(x) + 1 for x in binScale.split("1")][1:]
    intStDev = statistics.pstdev(intervals)
    diss = 0
    count = 0
    # print("Scale {}, Intervals {}".format(s, str(intervals)))
    for i in range(len(intervals)):
        # print("Interval {}".format(i))
        for j in range(1, len(intervals) - i + 1):
            count += 1
            total = 0
            for k in range(i, i + j):
                total += intervals[k]
            diss += consonance.index(total)
            # print("Length of chain: {}, total interval: {}, dissonance: {}".format(j, total, curDiss))
    diss /= count
    # r = requests.get("https://www.scales-chords.com/fscale_res_en.php?rn1=C&rn2=D&rn3=D%23%2FEb&rn4=F&rn5=G&rn6=A&rn7=A%23%2FBb&rn8=&rn9=&normal=1&greek=1&greekalt=1&other=1&etnic=1&c1=&t1=&c2=&t2=&c3=&t3=")
    # if r.status_code == 200:
    #     p1 = r.text.find("/scaleinfo.php?skey=C&sname=")
    #     p2 = r.text.find("\"", p1)
    #     name = r.text[p1 + 28:p2]
    # else:
    #     name = ""
    # scale = { "id": s, "binary": binScale, "notes": notesInScale, "intervals": intervals, "stdev": intStDev, "diss": diss, "name": name }
    scale = { "id": s, "binary": binScale, "notes": notesInScale, "intervals": intervals, "stdev": intStDev, "diss": diss }
    scales.append(scale)

print("<html><body><table><tr><th>ID<th>Binary<th>Notes<th>#Notes<th>Intervals<th>Std. Dev.<th>Dissonance</tr>")
for s in sorted(sorted(scales, key=lambda kk: kk["stdev"]), key=lambda k: k["diss"]):
    # print("<tr><td>{:}<td>{}<td>{}<td>{}<td>{}<td>{:.3f}<td>{:.3f}<td>{}</tr>".format(s["id"], s["binary"], str(s["notes"]), len(s["notes"]), str(s["intervals"]), s["stdev"], s["diss"], s["name"]))
    print("<tr><td>{:}<td>{}<td>{}<td>{}<td>{}<td>{:.3f}<td>{:.3f}</tr>".format(s["id"], s["binary"], str(s["notes"]), len(s["notes"]), str(s["intervals"]), s["stdev"], s["diss"]))
print("</table></body></html>")
