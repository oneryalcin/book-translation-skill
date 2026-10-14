#!/usr/bin/env python3
"""Group reviewer edit lists by chapter group for the final-editor stage.

usage: prepare_final.py RU.md TR.md OUT_DIR EDITS1.md [EDITS2.md ...] [--max-bytes 60000]

Edit files use the strict format:
### E<n>
OLD: <verbatim substring of RU.md, unique>
NEW: <replacement>
WHY: <reason>
Lens is taken from the edit file name (e.g. out_voice.md -> voice).
Chapters are split on lines starting with '## '. RU and TR must have the same
number of '## ' sections (front matter counts as section 0).
Writes OUT_DIR/G{n}_ru.md, G{n}_tr.md, G{n}_edits.md and prints a summary.
"""
import re, sys, os

def parse(fn):
    t = open(fn).read()
    return [(m.group(1), m.group(2).strip(), m.group(3).strip(), m.group(4).strip())
            for m in re.finditer(r'### (E\d+)\s*\nOLD: (.*?)\nNEW: (.*?)\nWHY: (.*?)(?=\n### E|\Z)', t, re.S)]

def main():
    a = sys.argv[1:]
    maxb = 60000
    if '--max-bytes' in a:
        i = a.index('--max-bytes'); maxb = int(a[i + 1]); del a[i:i + 2]
    ru_f, tr_f, out, *edit_files = a
    ru = open(ru_f).read(); tr = open(tr_f).read()
    rp = re.split(r'(?m)^(?=## )', ru); tp = re.split(r'(?m)^(?=## )', tr)
    if len(rp) != len(tp):
        sys.exit(f"section count differs: ru={len(rp)} tr={len(tp)}")
    # group adjacent sections up to maxb bytes of RU
    groups, cur, size = [], [], 0
    for i, p in enumerate(rp):
        b = len(p.encode())
        if cur and size + b > maxb:
            groups.append(cur); cur, size = [], 0
        cur.append(i); size += b
    if cur: groups.append(cur)
    offs, pos = [], 0
    for p in rp:
        offs.append((pos, pos + len(p))); pos += len(p)
    sec_group = {i: g for g, idx in enumerate(groups) for i in idx}
    buckets = {g: [] for g in range(len(groups))}
    bad = 0
    for ef in edit_files:
        lens = re.sub(r'^(out_)?|\.md$', '', os.path.basename(ef))
        for eid, old, new, why in parse(ef):
            if ru.count(old) != 1:
                bad += 1; print(f"UNMATCHED {ef} {eid}"); continue
            i = ru.index(old)
            s = [k for k, (x, y) in enumerate(offs) if x <= i < y][0]
            buckets[sec_group[s]].append((i, lens, eid, old, new, why))
    os.makedirs(out, exist_ok=True)
    for g, idx in enumerate(groups, 1):
        open(f"{out}/G{g}_ru.md", "w").write("".join(rp[i] for i in groups[g - 1]))
        open(f"{out}/G{g}_tr.md", "w").write("".join(tp[i] for i in groups[g - 1]))
        with open(f"{out}/G{g}_edits.md", "w") as f:
            for i, lens, eid, old, new, why in sorted(buckets[g - 1]):
                f.write(f"### {lens}:{eid}\nOLD: {old}\nNEW: {new}\nWHY: {why}\n\n")
        heads = [rp[i].split('\n')[0][:40] for i in groups[g - 1]]
        print(f"G{g}: {len(buckets[g-1])} edits, sections {heads}")
    print("unmatched:", bad)

main()
