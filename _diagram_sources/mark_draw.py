"""Mark every diagram slide as DRAW (hand-drawn while recording) and bring back the handwriting-board notes.

usage: python mark_draw.py BACKUP_MODULES_DIR DECK_MODULES_DIR
Slides show content only: the diagram image is kept, and all recording cues live in the speaker notes.
Notes come back from the backup decks; video title slides' segment pills (Slides / Handwriting board /
Screen recording / Face cam) move into the notes; each diagram slide gets a DRAW line and its draw list.
"""
import copy, glob, os, re, sys
from pptx import Presentation
from pptx.util import Emu

SEGMENTS = {"Slides", "Handwriting board", "Screen recording", "Face cam"}


def prepend(tf, text):
    """Insert a paragraph with this text before the first one in the notes."""
    first = tf.paragraphs[0]._p
    p = copy.deepcopy(first)
    for r in p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r")[1:]:
        p.remove(r)
    first.addprevious(p)
    para = tf.paragraphs[0]
    if para.runs:
        para.runs[0].text = text
    else:
        para.text = text

bak, dst = sys.argv[1:3]
for deck in sorted(glob.glob(os.path.join(dst, "*", "4_Slides_Module*.pptx"))):
    mod = re.search(r"Module(\d+)", deck).group(1)
    old = Presentation(os.path.join(bak, os.path.relpath(deck, dst)))
    prs = Presentation(deck)
    n = 0
    for slide, orig in zip(prs.slides, old.slides):
        if slide.has_notes_slide:   # notes: back to the original board wording, run by run
            for p, q in zip(slide.notes_slide.notes_text_frame.paragraphs, orig.notes_slide.notes_text_frame.paragraphs):
                for r, s in zip(p.runs, q.runs):
                    r.text = s.text
        shapes = list(slide.shapes)   # title-slide segment pills: label box on top of a rounded shape
        pills = [t for t in shapes if t.has_text_frame and t.text_frame.text.strip() in SEGMENTS | {"Diagram slides"}
                 and any(a.shape_type == 1 and (a.left, a.top, a.width) == (t.left, t.top, t.width) for a in shapes)]
        if pills:
            segs = [{"Diagram slides": "Handwriting board"}.get(t.text_frame.text.strip(), t.text_frame.text.strip())
                    for t in sorted(pills, key=lambda t: t.left)]
            for t in pills:
                for a in [a for a in shapes if a.shape_type == 1 and (a.left, a.top, a.width) == (t.left, t.top, t.width)]:
                    a._element.getparent().remove(a._element)
                t._element.getparent().remove(t._element)
            prepend(slide.notes_slide.notes_text_frame, "SEGMENTS: " + " + ".join(segs))
        if not any(sh.shape_type == 13 and sh.top == Emu(1325880) for sh in slide.shapes):
            continue
        for sh in [sh for sh in slide.shapes if sh.name == "DRAW tag"]:   # older runs put the tag on the slide
            sh._element.getparent().remove(sh._element)
        if slide.notes_slide.notes_text_frame.text.startswith("✏ DRAW"):
            continue
        prepend(slide.notes_slide.notes_text_frame, "✏ DRAW THIS SLIDE – hand-draw it live; the slide diagram is your reference")
        # what to draw: the original slide's bullets (or body text for slides that had no draw-live list)
        texts = [s.text_frame.text for s in orig.shapes if s.has_text_frame and s.text_frame.text.strip()
                 and "DRAW LIVE" not in s.text_frame.text and "Slide Number" not in s.name]
        body = texts[1:] if texts else []
        notes = slide.notes_slide.notes_text_frame
        notes.add_paragraph().text = ""
        notes.add_paragraph().text = "What to draw:"
        items = []
        for t in body:
            for line in filter(None, (l.strip() for l in t.splitlines())):
                if items and re.fullmatch(r"\d+", items[-1].split(" – ")[0]) and len(items[-1].split(" – ")) < 3:
                    items[-1] += " – " + line   # numbered step boxes: "1 – Mean – Find the average"
                else:
                    items.append(line)
        for line in items:
            notes.add_paragraph().text = "• " + line
        n += 1
    prs.save(deck)
    print(f"Module {mod}: {n} slides marked DRAW")
