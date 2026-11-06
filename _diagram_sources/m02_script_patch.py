"""M02 video script: slide numbers after the new slides 11 (dates) and 22 (every formula), plus the 2.4 fixes.

usage: python m02_script_patch.py IN.docx OUT.docx [OUT2.docx ...]
"""
import copy, re, sys
from docx import Document
from docx.oxml.ns import qn

src, outs = sys.argv[1], sys.argv[2:]
d = Document(src)
body = d.element.body


def renum(m):
    n = int(m.group(2))
    return m.group(1) + str(n if n <= 10 else n + 1 if n <= 20 else n + 2)


for t in body.iter(qn("w:t")):
    if t.text == "Slides 21–22":   # 2.4 shot plan: formulas slide, results, recap
        t.text = "Slides 22–24"
        continue
    t.text = re.sub(r"(Slides? )(\d+)", renum, t.text)
    t.text = re.sub(r"(Slides? \d+–)(\d+)", renum, t.text)

paras = d.paragraphs
find = lambda start: next(p for p in paras if p.text.startswith(start))


def set_text(p, old, new):
    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return
    raise SystemExit(f"not found: {old!r} in {p.text[:60]!r}")


def insert_after(p, like, text):
    """New paragraph after p, formatted like paragraph `like` (first run's formatting kept)."""
    el = copy.deepcopy(like._p)
    for r in el.findall(qn("w:r"))[1:]:
        el.remove(r)
    p._p.addnext(el)
    new = next(q for q in d.paragraphs if q._p is el)
    new.runs[0].text = text
    return new


cue = find("[Slide 12]")          # a plain cue paragraph (was [Slide 11], renumbered above)
# Video 2.2: the date slide
m2 = find("[Screen: M2 formula")
prev = m2._p.getprevious()
new = insert_after(next(q for q in d.paragraphs if q._p is prev), cue, "[Slide 11]")

# Video 2.4: check row goes in row 22 (row 21 sits under the Google Sheets table)
set_text(find("[Screen: row 21 total check"), "row 21 total check", "row 22 total check (row 21 left empty)")
set_text(find("Now a habit that separates"), "In row 21,", "In row 22, leaving one empty row under the table,")

board = find("On the left, an order with product ID P048")
set_text(board, 'brings back "Books".', 'brings back "Books": P048 is Wings of Fire, a book.')
set_text(board, 'products!A:A, products!C:C', 'products!$A$2:$A$61, products!$C$2:$C$61')

cat = find("Now the same SUMIFS pattern, by category")
c22 = insert_after(cat, cue, "[Slide 22]")
insert_after(c22, cat, (
    "Before we read the results, here is every formula on our Summary sheet in one place. Pause the video and "
    "check yours against it. At the top: SUM adds up the whole revenue column. COUNTA counts the order IDs, so it "
    "counts orders. Revenue divided by orders is the average order value. COUNTIF counts the Y's in the returned "
    "column, and returns divided by orders is the return rate. The city table always follows the same pattern: "
    "first the column we calculate on, revenue in V. Then a pair: where to look, city in P, and what to look for, "
    "the city name in A11. The ranges have dollar signs so they stay fixed when we fill down; A11 has none, so it "
    "becomes A12, A13. For returns we simply add a second pair: returned equals Y. The check row adds up the table, "
    "and it must match the top numbers. And the category table is the very same five formulas. Only the "
    "where-to-look column changes, from P, the city, to W, the category we brought in with XLOOKUP, and A11 "
    "becomes A25."))

for o in outs:
    d.save(o)
    print("saved", o)
