"""Replace every 'HANDWRITING BOARD – DRAW LIVE' slide with its finished diagram image.

usage: python patch_decks.py SRC_MODULES_DIR DST_MODULES_DIR
Diagram for deck NN slide SS is out/mNN_sSS.png. Video-title slides' 'Handwriting board' tag becomes 'Diagram slides'.
"""
import glob, os, re, shutil, sys
from pptx import Presentation
from pptx.util import Emu

src, dst = sys.argv[1:3]
missing = []
NOTES = [(r"(?:Handwriting b|B)oard segment(?: 1)?", "Diagram slide"), (r"Draw slowly;", "Go slowly;"),
         (r"Draw left to right, slowly\.", "Walk through it left to right, slowly."),
         (r"Draw arrows on board after this slide\.", "Point to the two arrows: rules + data → answers vs data + answers → rules."),
         (r"then board", "then diagram slide")]
EXTRA = {("03", 13), ("07", 6)}   # SD in four steps, ETL vs ELT
for deck in sorted(glob.glob(os.path.join(src, "*", "4_Slides_Module*.pptx"))):
    mod = re.search(r"Module(\d+)", deck).group(1)
    prs = Presentation(deck)
    n = 0
    for i, slide in enumerate(prs.slides, 1):
        if slide.has_notes_slide:   # speaker notes: board segments are now diagram slides
            for p in slide.notes_slide.notes_text_frame.paragraphs:
                for r in p.runs:
                    t = r.text
                    for a, b in NOTES:
                        t = re.sub(a, b, t)
                    r.text = t
        shapes = list(slide.shapes)
        for sh in shapes:   # title-slide segment tags
            if sh.has_text_frame and sh.text_frame.text.strip() == "Handwriting board":
                sh.text_frame.paragraphs[0].runs[0].text = "Diagram slides"
                for r in sh.text_frame.paragraphs[0].runs[1:]: r.text = ""
        label = [s for s in shapes if s.has_text_frame and "DRAW LIVE" in s.text_frame.text]
        if (mod, i) in EXTRA:   # board segment without a draw-live slide: redraw the whole body
            png = f"out/m{mod}_s{i:02d}.png"
            title = min((s for s in shapes if s.has_text_frame and s.text_frame.text.strip()), key=lambda s: s.top)
            for s in shapes:
                if s is not title and "Slide Number" not in s.name:
                    s._element.getparent().remove(s._element)
            slide.shapes.add_picture(png, Emu(548640), Emu(1325880), width=Emu(11094415))
            n += 1
            continue
        if not label:
            continue
        png = f"out/m{mod}_s{i:02d}.png"
        if not os.path.exists(png):
            missing.append(png); continue
        title = min((s for s in shapes if s.has_text_frame and s.text_frame.text.startswith("Draw")), key=lambda s: s.top)
        t = title.text_frame.paragraphs[0]
        new = re.sub(r"^Draw:\s*", "", t.runs[0].text); t.runs[0].text = new if new.startswith("pd.") else new[:1].upper() + new[1:]
        frame = [s for s in shapes if s.shape_type == 1 and s.top > title.top + title.height - 10]  # dashed box
        bullets = [s for s in shapes if s.has_text_frame and s is not title and s not in label
                   and s.top > title.top and "Slide Number" not in s.name]
        for s in {id(s): s for s in label + frame + bullets}.values():
            s._element.getparent().remove(s._element)
        left, top, width = Emu(548640), Emu(1325880), Emu(11094415)
        slide.shapes.add_picture(png, left, top, width=width)
        n += 1
    out = os.path.join(dst, os.path.relpath(deck, src))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prs.save(out)
    print(f"Module {mod}: {n} board slides replaced -> {out}")
if missing:
    print("MISSING:", *missing, sep="\n  ")
