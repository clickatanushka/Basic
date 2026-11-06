"""Rewrite handwriting-board wording in the course .docx files: board segments are now diagram slides.

usage: python patch_docs.py COURSE_ROOT OUT_ROOT   (reads 01_Course_Guide/*.docx and 03_Modules/*/*.docx)
"""
import glob, os, re, sys, zipfile, html

src, dst = sys.argv[1:3]
VERBS = r"(?:draw|redraw|write|add|mark|label|shade|fill|underline|circle|trace|number|bracket|cross out|cross|mirror)\b\s*"
SUBS = [  # applied in order to every <w:t> text
    (r"\[Board: on the pipeline drawing, draw a dotted arrow.*?\]",
     "[Diagram: point to the ELT lane – load first, then T with SQL inside the warehouse]"),
    (r"\[Board: " + VERBS, "[Diagram: point to "),
    (r"\[Board: ", "[Diagram: point to "),
    (r"(\[Diagram: [^\]]*)", lambda m: re.sub(r"\b(?:re)?draw(?:s)?\b\s*|\bwrite\b\s*|\badd\b\s*|\bmark\b\s*", "",
                                            re.sub(r"\bunderline (\w+)", r"\1 (underlined)", m.group(1)))),
    (r"\[Slide (\d+) [→–-] Board\]", r"[Slide \1 – diagram]"),
    (r"\[Slide (\d+), switch to handwriting board\]", r"[Slide \1 – diagram]"),
    (r"\[Board\]", "[Diagram]"),
    (r"(Slides? [\d–]+) [→–] (?:handwriting )?board: ", r"\1 – diagram: "),
    (r"(Slides? [\d–]+)(:| –) draw (?:the )?", r"\1 – diagram: "),
    (r' \(add "L before T" arrow on the board drawing\)', " (ELT diagram)"),
    (r",? ?W = handwriting board \(pen tablet\)", ""),
    # guides and prose
    (r'W – Handwriting board: pen tablet or iPad for (anything that builds step by step.*?)\. The slide decks contain a .Handwriting board – draw live. slide listing exactly what to draw\.',
     r"Diagram slides: \1 is a finished diagram slide in the deck. Nothing is drawn live; point to each part as you explain it."),
    (r"Pen tablet or iPad for the W segments \(.*?\)\.", "No pen tablet needed: every drawing is now a finished diagram slide in the deck."),
    (r"Practise the three board drawings \((.*?)\) once on the pen tablet;", r"Rehearse the three diagram slides (\1);"),
    (r"practise the three board drawings", "rehearse the three diagram slides"),
    (r"practise every board drawing on paper", "rehearse every diagram slide"),
    (r"demos and drawing", "demos and diagrams"),
    (r"\(slides, then board, then screen\)", "(slides, then screen)"),
    (r"with slides or the board", "with slides and diagram slides"),
    (r"draw it on the board from the five numbers", "show the box plot diagram (slide 15)"),
    (r"We will draw ideas on the board", "We will see ideas as diagrams"),
    (r"the diagram we draw on the board", "the diagram on the slide"),
    (r"Board in 5\.4: draw the colon", "Diagram in 5.4: point to the colon"),
    (r"5\.3 board: write 0–5 under the boxes\.", "5.3 diagram: positions 0–5 are under the boxes."),
    (r"Prepare the board examples:", "The diagram slides already show the examples:"),
    (r"Let me draw this\. I'll write the brief at the top… and circle two words",
     "Here is the question tree. The brief is at the top… with two words circled"),
    (r"Let me draw it", "Let me show it"), (r"Let me draw", "Let me show you"),
    (r"Let's draw the decision\.", "Here is the decision."),
    (r"Under Transform, I'll write:", "Under Transform:"), (r"Under it I'll write:", "Under it:"),
    (r"Exactly what we drew\.", "Exactly what the diagram shows."),
    (r"I underline it\.", "It's underlined."),
    (r"Taught mostly on the handwriting board", "Taught mostly with diagram slides"),
    (r"mostly on a whiteboard", "mostly with diagrams"),
    (r"(?i)slides (and|\+) (?:the )?(?:handwriting )?board", r"slides \1 diagram slides"),
    (r"board and slides only", "diagram slides and slides only"),
    (r"Star schema drawn on the board", "Star schema diagram"),
    (r"\(board drawing\)", "(diagram)"),
    (r"on the board", "on a diagram slide"),
    (r"(?i)\bboard segment", "diagram slide"),
    (r"\bBoard (mini )?example", "Diagram example"), (r"\bboard example", "diagram example"),
    (r"our board customer", "our diagram customer"), (r"from the board", "from the diagram"),
    (r"exactly as on the board", "exactly as on the diagram"),
    (r"\(board: ", "(diagram: "), (r"\(board\)", "(diagram)"), (r"\bBoard: ", "Diagram: "),
    (r"execution-order board", "execution-order diagram"), (r"LEFT JOIN board", "LEFT JOIN diagram"),
    (r"\b(\d\.\d) board:", r"\1 diagram:"), (r"Board in (\d\.\d)\.", r"Diagram in \1."),
]
CELL = [  # whole short cells: segment tags and shot-plan format codes
    (r"^(S ?\+ ?W|W ?\+ ?S|W)$", "S"), (r"^W ?\+ ?R$", "S+R"), (r"^R ?\+ ?W$", "R+S"),
    (r"^((?:[A-Za-z ]+ \+ )?)(?:Handwriting board|Board|board)((?: \+ [A-Za-z ]+)?)$", r"\1Diagram slides\2"),
]


def fix(t):
    raw = html.unescape(t)
    for a, b in CELL:
        if re.search(a, raw.strip()):
            raw = re.sub(a, b, raw.strip()); break
    else:
        for a, b in SUBS:
            raw = re.sub(a, b, raw)
    return html.escape(raw, quote=False)


PARA = {  # paragraphs whose wording spans several runs: replace the whole paragraph text
    "W – Handwriting board": "W – Diagram slides: anything that builds step by step, such as how a JOIN matches rows, how a pipeline "
                             "moves data, or how a train/test split works, is a finished diagram slide in the deck. Nothing is drawn "
                             "live; point to each part as you explain it.",
}


def fix_para(p):
    text = "".join(html.unescape(t) for t in re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))
    for key, new in PARA.items():
        if text.startswith(key):
            first = [True]
            def put(m):
                v = html.escape(new, quote=False) if first[0] else ""
                first[0] = False
                return m.group(1) + v + m.group(3)
            return re.sub(r"(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)", put, p)
    return p


files = sorted(glob.glob(os.path.join(src, "01_Course_Guide", "*.docx")) + glob.glob(os.path.join(src, "03_Modules", "*", "*.docx")))
for f in files:
    zin = zipfile.ZipFile(f)
    xml = zin.read("word/document.xml").decode()
    xml2 = re.sub(r"<w:p[ >].*?</w:p>", lambda m: fix_para(m.group(0)), xml, flags=re.S)
    new = re.sub(r"(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)", lambda m: m.group(1) + fix(m.group(2)) + m.group(3), xml2)
    if new == xml:
        continue
    out = os.path.join(dst, os.path.relpath(f, src)); os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            zout.writestr(item, new.encode() if item.filename == "word/document.xml" else zin.read(item.filename))
    print("patched", os.path.relpath(f, src))
