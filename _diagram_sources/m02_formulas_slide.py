"""M02: real-data XLOOKUP diagram on slide 21 + new slide 22 'Summary sheet: every formula'.

usage: python m02_formulas_slide.py DECK [PNG]
PNG given -> also swap slide 21's diagram image (live deck). The backup deck has the board slide instead.
"""
import copy, sys
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR

deck = sys.argv[1]
png = sys.argv[2] if len(sys.argv) > 2 else None
prs = Presentation(deck)
assert len(prs.slides) == 31, "deck already patched?"

DRAW = ["Left: orders_clean row 2: product_id P048 in column D, category goes in column W",
        "Right: products table, columns product_id and category (P048 = Wings of Fire)",
        "Arrow 1: look for P048 down product_id",
        "Arrow 2: step across to category, return Books",
        'Write: =XLOOKUP(D2, products!$A$2:$A$61, products!$C$2:$C$61, "Not found")']

# --- slide 21: XLOOKUP diagram -------------------------------------------------------------------------------
s21 = prs.slides[20]
if png:
    pic = next(sh for sh in s21.shapes if sh.shape_type == 13)
    rid = pic._element.blipFill.blip.rEmbed
    s21.part.related_part(rid)._blob = open(png, "rb").read()
    paras = [p for p in s21.notes_slide.notes_text_frame.paragraphs if p.text.startswith("• ")]
    for p, t in zip(paras, DRAW):
        p.runs[0].text = "• " + t
        for r in p.runs[1:]:
            r.text = ""
else:   # backup: the hand-draw list is the slide body
    body = next(sh for sh in s21.shapes if sh.has_text_frame and sh.text_frame.text.startswith("Left:"))
    for p, t in zip(body.text_frame.paragraphs, DRAW):
        p.runs[0].text = t
        for r in p.runs[1:]:
            r.text = ""

# --- new slide 22: every Summary formula -----------------------------------------------------------------------
src = prs.slides[19]   # 'The IFS family': same layout and code panel look
new = prs.slides.add_slide(src.slide_layout)
for sh in list(new.shapes):
    sh._element.getparent().remove(sh._element)
keep = {"Text 0", "codepanel", "Text 3", "Slide Number Placeholder 0"}
for sh in src.shapes:
    if sh.name in keep:
        new.shapes._spTree.append(copy.deepcopy(sh._element))
shapes = {sh.name: sh for sh in new.shapes}
shapes["Text 0"].text_frame.paragraphs[0].runs[0].text = "Summary sheet: every formula"
panel, code = shapes["codepanel"], shapes["Text 3"]
panel.left, panel.top, panel.width, panel.height = Emu(548640), Emu(1325880), Emu(11094415), Emu(4983480)
code.left, code.top, code.width, code.height = Emu(822960), Emu(1463040), Emu(10606000), Emu(4754880)

V, P, U, W = "orders_clean!$V$2:$V$5001", "orders_clean!$P$2:$P$5001", "orders_clean!$U$2:$U$5001", \
    "orders_clean!$W$2:$W$5001"
H = "head"
LINES = [
    (H, "TOP NUMBERS  (B3 to B7)"),
    (f"B3  =SUM({V})", "total revenue"),
    ("B4  =COUNTA(orders_clean!$A$2:$A$5001)", "orders"),
    ("B5  =B3/B4", "average order value"),
    (f'B6  =COUNTIF({U},"Y")', "returned orders"),
    ("B7  =B6/B4", "return rate"),
    (H, "CITY TABLE  (type row 11, fill down to row 20)     V = revenue · P = city_clean · U = returned"),
    (f"B11 =SUMIFS({V}, {P}, A11)", ""),
    (f"C11 =COUNTIFS({P}, A11)", ""),
    (f"D11 =AVERAGEIFS({V}, {P}, A11)", ""),
    (f'E11 =COUNTIFS({P}, A11, {U}, "Y")', ""),
    ("F11 =E11/C11", "format as %"),
    (H, "CHECK ROW  (row 22: leave row 21 empty below the table)"),
    ("B22 =SUM(B11:B20)     C22 =SUM(C11:C20)", "must equal B3 and B4"),
    (H, "CATEGORY TABLE  (first W2 in orders_clean, then row 25, fill down to row 29)"),
    ('W2  =XLOOKUP(D2, products!$A$2:$A$61, products!$C$2:$C$61, "Not found")', ""),
    ("B25:F25  the same five formulas as row 11, with $W$2:$W$5001 in place of", ""),
    ("          $P$2:$P$5001, and A25 in place of A11", ""),
]
tf = code.text_frame
proto = copy.deepcopy(tf.paragraphs[0]._p)
for p in list(tf._txBody.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}p")):
    tf._txBody.remove(p)
COL = 46   # comments line up in one column
for a, b in LINES:
    tf._txBody.append(copy.deepcopy(proto))
    para = tf.paragraphs[-1]
    r = para.runs[0]
    r.font.size = Pt(14)
    if a == H:
        r.text = b
        r.font.bold = True
        r.font.size = Pt(12)
        r.font.color.theme_color = MSO_THEME_COLOR.ACCENT_1
        para.space_before = Pt(0 if len(tf.paragraphs) == 1 else 9)
        para.space_after = Pt(2)
        continue
    r.text = a
    if b:
        c = para.add_run()
        c.text = " " * max(2, COL - len(a)) + "← " + b
        c.font.size = Pt(14)
        c.font.name = "Courier New"
        c.font.color.rgb = RGBColor(0x9A, 0xA3, 0xB2)

notes = new.notes_slide.notes_text_frame
notes.text = ("Video 2.4. Show after the category table is built, before 'What the summary sheet tells us'. "
              "Walk through it top to bottom: every line is a cell in the Summary tab (W2 is in orders_clean). "
              "Students can pause here and copy.")

# move the new slide to position 22
ids = prs.slides._sldIdLst
el = ids[-1]
ids.remove(el)
ids.insert(21, el)
prs.save(deck)
print("patched", deck)
