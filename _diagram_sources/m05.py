from style import *
plt.rcParams["font.family"] = ["Liberation Sans", "DejaVu Sans"]   # fallback only for glyphs like ₹

OUT = "out/m05_s{:02d}.png"


def s08():  # variables are labelled boxes
    fig, ax = canvas()
    vars_ = [("order_id", '"O10006"', "str", TEAL), ("city", '"Delhi"', "str", TEAL),
             ("quantity", "2", "int", ORANGE), ("unit_price", "1440", "int", ORANGE)]
    for i, (name, val, typ, c) in enumerate(vars_):
        x = 2.3 + 3.8 * i
        # the code line
        text(ax, x - 0.2, 5.72, name, fs=19, ha="right", va="baseline")
        text(ax, x, 5.72, "=", fs=22, bold=True, color=c, va="baseline")
        text(ax, x + 0.2, 5.72, val, fs=19, ha="left", va="baseline")
        # value travelling down from '=' into the box
        arrow(ax, x, 5.6, x, 4.35, color=c, lw=2.5, ms=20)
        text(ax, x + 0.15, 4.95, "goes INTO", fs=14, color=MUTED, ha="left")
        # open-top box
        bx, by, bw, bh = x - 1.4, 2.75, 2.8, 1.45
        ax.plot([bx, bx, bx + bw, bx + bw], [by + bh, by, by, by + bh], color=c, lw=3)
        ax.add_patch(Rectangle((bx, by), bw, bh, fc=TINT[c], ec="none"))
        text(ax, x, by + 0.62, val, fs=22, bold=True)
        # label tag on the outside
        box(ax, x, by - 0.38, 2.2, 0.48, name, color=c, fill=c, fs=17, bold=True, tc="white")
        text(ax, x, by - 0.88, typ, fs=15, color=MUTED)
    box(ax, 8, 1.15, 13.2, 0.62, "", color=BLUE)
    text(ax, 8, 1.15, "revenue = quantity × unit_price × (1 − discount)  =  2 × 1440 × 0.95  =  2736.0",
         fs=19, bold=True)
    pill(ax, 8, 0.38, "A variable is a labelled box: name outside, value inside.  '=' puts the value in.", fs=16)
    save(fig, OUT.format(8))


def s14():  # a list with positions
    fig, ax = canvas()
    vals = ["1737.6", "570.0", "2145.1", "3434.0", "3486.6", "2736.0"]
    x0, bw, y, bh = 2.75, 2.1, 3.65, 1.1
    text(ax, 0.35, y, "order_amounts", fs=18, bold=True, ha="left")
    text(ax, 2.5, y, "=", fs=20, bold=True)
    for i, v in enumerate(vals):
        c = CORAL if i < 3 else BLUE
        ax.add_patch(Rectangle((x0 + bw * i, y - bh / 2), bw, bh, fc=TINT[c], ec=INK, lw=2))
        text(ax, x0 + bw * (i + 0.5), y, v, fs=21, bold=True)
        text(ax, x0 + bw * (i + 0.5), y - 1.0, str(i), fs=21, bold=True, color=BLUE)
    text(ax, x0 + bw * 5.5, y - 1.75, "-1", fs=21, bold=True, color=PURPLE)
    text(ax, 0.35, y - 1.0, "position", fs=17, color=BLUE, ha="left")
    text(ax, 0.35, y - 1.75, "from the end", fs=17, color=PURPLE, ha="left")
    # bracket over boxes 0-2
    bl, br, yb = x0 + 0.08, x0 + 3 * bw - 0.08, y + bh / 2 + 0.2
    ax.plot([bl, bl, br, br], [yb, yb + 0.25, yb + 0.25, yb], color=CORAL, lw=3)
    ax.plot([(bl + br) / 2] * 2, [yb + 0.25, yb + 0.45], color=CORAL, lw=3)
    text(ax, (bl + br) / 2, yb + 0.85, "order_amounts[0:3]  →  [1737.6, 570.0, 2145.1]", fs=19, bold=True,
         color=CORAL)
    text(ax, x0 + bw * 3.5, yb + 0.5, "3 is the stop:\nnot included", fs=17, color=MUTED)
    pill(ax, 8, 0.5, "Python counts from 0.  [0:3] gives positions 0, 1, 2.  [-1] is the last item.", color=BLUE)
    save(fig, OUT.format(14))


def diamond(ax, x, y, w, h, s, color=BLUE, lw=2.5):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)], closed=True,
                         fc=TINT[color], ec=color, lw=lw))
    text(ax, x, y, s, fs=18, bold=True)


def s21():  # if / elif / else decision
    fig, ax = canvas()
    dw, dh = 3.6, 1.45
    X, Y1, Y2 = 3.2, 4.45, 2.0
    XB = 7.9
    box(ax, X, 6.0, 3.4, 0.55, "revenue = ₹3,434  (O10004)", color=CORAL, fill=CORAL, fs=17, bold=True, tc="white")
    arrow(ax, X, 5.72, X, Y1 + dh / 2, color=CORAL, lw=3.5)
    diamond(ax, X, Y1, dw, dh, "revenue >= 5000?")
    diamond(ax, X, Y2, dw, dh, "revenue >= 1000?")
    # d1 yes -> Big (right)
    arrow(ax, X + dw / 2, Y1, XB - 1.2, Y1, lw=2)
    text(ax, (X + dw / 2 + XB - 1.2) / 2, Y1 + 0.27, "Yes", fs=17, bold=True, color=GREEN)
    box(ax, XB, Y1, 2.4, 0.7, "Big", color=GREEN, fs=20, bold=True)
    # d1 no -> d2 (down, traced)
    arrow(ax, X, Y1 - dh / 2, X, Y2 + dh / 2, color=CORAL, lw=3.5)
    text(ax, X + 0.2, (Y1 + Y2) / 2, "No", fs=17, bold=True, color=RED, ha="left")
    text(ax, X - 0.2, (Y1 + Y2) / 2, "3,434 < 5000", fs=15, bold=True, color=CORAL, ha="right")
    # d2 yes -> Medium (right, traced)
    arrow(ax, X + dw / 2, Y2, XB - 1.3, Y2, color=CORAL, lw=3.5)
    text(ax, (X + dw / 2 + XB - 1.3) / 2, Y2 + 0.27, "Yes", fs=17, bold=True, color=GREEN)
    text(ax, (X + dw / 2 + XB - 1.3) / 2, Y2 - 0.3, "3,434 ≥ 1000", fs=15, bold=True, color=CORAL)
    box(ax, XB, Y2, 2.6, 0.7, "Medium  ✔", color=CORAL, fill=CORAL, fs=20, bold=True, tc="white")
    # d2 no -> Small (down)
    arrow(ax, X, Y2 - dh / 2, X, 0.72, lw=2)
    text(ax, X + 0.2, 1.0, "No", fs=17, bold=True, color=RED, ha="left")
    box(ax, X, 0.45, 2.2, 0.55, "Small", color=PURPLE, fs=20, bold=True)
    # the code
    code = ("if revenue >= 5000:\n    size = \"Big\"\nelif revenue >= 1000:\n    size = \"Medium\"\n"
            "else:\n    size = \"Small\"")
    box(ax, 12.85, 3.9, 4.6, 2.45, color=LINE, fill="white", lw=1.5)
    text(ax, 10.85, 3.9, code, fs=17, color=INK, ha="left", va="center")
    pill(ax, 12.0, 1.0, "₹3,434 → Medium.  Python checks from the top\nand stops at the first yes.", fs=16)
    save(fig, OUT.format(21))


def s23():  # tracing a loop
    fig, ax = canvas()
    amounts = [1737.6, 570.0, 2145.1, 3434.0, 3486.6, 2736.0, 24484.8, 14098.95]
    rows, total, big = [("start", "–", "–", "total = 0", "0")], 0.0, 0
    hl = {}
    for i, a in enumerate(amounts, 1):
        new = round(total + a, 2)
        isbig = a >= 5000
        big += isbig
        fmt = lambda v: str(round(v, 2))
        rows.append((str(i), fmt(a), "Yes" if isbig else "No", f"{fmt(total) if total else '0'} + {fmt(a)} = {fmt(new)}",
                     f"{big - 1} + 1 = {big}" if isbig else str(big)))
        total = new
        if isbig:
            for c in (1, 2, 4):
                hl[(i, c)] = TINT[CORAL]
    table(ax, 0.3, 6.15, ["turn", "amount", ">= 5000?", "total", "big_orders"], rows,
          [1.0, 1.7, 1.6, 4.3, 2.1], rh=0.47, fs=16, color=BLUE, highlight=hl)
    code = ("total = 0\nbig_orders = 0\nfor amount in order_amounts:\n    total = total + amount\n"
            "    if amount >= 5000:\n        big_orders += 1")
    box(ax, 13.45, 4.3, 4.3, 2.1, "", color=LINE, fill="white", lw=1.5)
    text(ax, 11.5, 4.3, code, fs=16, ha="left")
    text(ax, 13.45, 2.95, "total changes EVERY turn", fs=16, bold=True, color=BLUE)
    text(ax, 13.45, 2.55, "big_orders: only when amount >= 5000", fs=16, bold=True, color=CORAL)
    text(ax, 11.0, 6.15 - 0.47 * 8.5, "← the two-Smartphone order", fs=15, bold=True, color=CORAL, ha="left")
    pill(ax, 8, 0.4, "After 8 turns: total = 52693.05,  big_orders = 2")
    save(fig, OUT.format(23))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s08(); s14(); s21(); s23()
