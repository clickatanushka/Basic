from style import *

OUT = "out/m02_s{:02d}.png"


def grid(ax, x0, top, cells, cw=(0.95, 0.95, 1.75), rh=0.7, hl=None, color=BLUE):
    """Spreadsheet grid with A/B/C letters and 1/2/3 row numbers. cells[r][c]. hl = {(r, c): colour}."""
    hl = hl or {}
    rn = 0.45
    hh = 0.45
    ax.add_patch(Rectangle((x0, top - hh), rn, hh, fc="#EEF0F4", ec=LINE, lw=1))
    x = x0 + rn
    xc = []
    for j, w in enumerate(cw):
        ax.add_patch(Rectangle((x, top - hh), w, hh, fc="#EEF0F4", ec=LINE, lw=1))
        text(ax, x + w / 2, top - hh / 2, "ABC"[j], fs=16, bold=True, color=MUTED)
        xc.append((x, w)); x += w
    yc = []
    for i, row in enumerate(cells):
        y = top - hh - rh * (i + 1)
        ax.add_patch(Rectangle((x0, y), rn, rh, fc="#EEF0F4", ec=LINE, lw=1))
        text(ax, x0 + rn / 2, y + rh / 2, str(i + 1), fs=16, bold=True, color=MUTED)
        for j, v in enumerate(row):
            cx, w = xc[j]
            c = hl.get((i, j))
            ax.add_patch(Rectangle((cx, y), w, rh, fc=TINT[c] if c else "white", ec=c or LINE, lw=2 if c else 1))
            text(ax, cx + w / 2, y + rh / 2, v, fs=17)
        yc.append(y + rh / 2)
    return xc, yc


def s13():  # relative vs absolute references
    fig, ax = canvas()
    top, cw, rh = 5.45, (0.8, 0.8, 1.6), 0.6

    def drag(xc, yc, color):
        xr = xc[2][0] + xc[2][1] + 0.15
        arrow(ax, xr, yc[0], xr, yc[1] + 0.05, color=color, lw=2.5, rad=-0.5)
        arrow(ax, xr, yc[1], xr, yc[2] + 0.05, color=color, lw=2.5, rad=-0.5)

    # panel 1: relative (A = quantity, B = price)
    text(ax, 2.2, 6.0, "1. Relative:  =A1*B1", fs=19, bold=True, color=TEAL)
    xc, yc = grid(ax, 0.3, top, [["2", "499", "=A1*B1"], ["1", "1299", "=A2*B2"], ["3", "799", "=A3*B3"]],
                  cw=cw, rh=rh, hl={(0, 2): TEAL, (1, 2): TEAL, (2, 2): TEAL})
    drag(xc, yc, TEAL)
    text(ax, 2.2, 2.75, "qty × price: A1 → A2 → A3\neach row uses its own values", fs=16, color=MUTED)

    # panel 2: the same formula breaks when B1 is a fixed rate
    text(ax, 7.5, 6.0, "2. Tax rate in B1:  =A1*B1", fs=19, bold=True, color=RED)
    xc, yc = grid(ax, 5.6, top, [["499", "18%", "=A1*B1"], ["1299", "", "=A2*B2 → 0"], ["799", "", "=A3*B3 → 0"]],
                  cw=cw, rh=rh, hl={(0, 1): CORAL, (1, 2): CORAL, (2, 2): CORAL})
    drag(xc, yc, RED)
    bx, bw = xc[1]
    for y in yc[1:]:   # cross out the empty B2 and B3
        ax.plot([bx + 0.15, bx + bw - 0.15], [y - 0.2, y + 0.2], color=RED, lw=3)
        ax.plot([bx + 0.15, bx + bw - 0.15], [y + 0.2, y - 0.2], color=RED, lw=3)
    text(ax, 7.5, 2.75, "B2, B3 are empty → zero!\nwrong answer, no error", fs=16, color=RED, bold=True)

    # panel 3: pin B1
    text(ax, 12.8, 6.0, "3. Pin it:  =A1*\\$B\\$1", fs=19, bold=True, color=GREEN)
    xc, yc = grid(ax, 10.9, top, [["499", "18%", "=A1*\\$B\\$1"], ["1299", "", "=A2*\\$B\\$1"], ["799", "", "=A3*\\$B\\$1"]],
                  cw=cw, rh=rh, hl={(0, 1): CORAL, (0, 2): GREEN, (1, 2): GREEN, (2, 2): GREEN})
    drag(xc, yc, GREEN)
    text(ax, 12.8, 2.75, "A1 → A2 → A3, but \\$B\\$1 stays B1", fs=16, color=MUTED)

    # bottom: the rule + F4 cycle
    box(ax, 3.55, 1.25, 6.7, 1.55, "", color=PURPLE)
    text(ax, 0.45, 1.72, "\\$ before the letter  →  pins the column", fs=17, ha="left")
    text(ax, 0.45, 1.25, "\\$ before the number  →  pins the row", fs=17, ha="left")
    text(ax, 0.45, 0.78, "both \\$  →  pins the whole cell", fs=17, ha="left")
    text(ax, 11.0, 1.9, "Press F4 to cycle", fs=18, bold=True, color=PURPLE)
    refs = ["A1", r"\$A\$1", r"A\$1", r"\$A1"]
    xs = [8.0, 10.0, 12.0, 14.0]
    for i, r in enumerate(refs):
        box(ax, xs[i], 1.05, 1.15, 0.62, r, color=PURPLE, fs=18, bold=True)
        if i < 3:
            arrow(ax, xs[i] + 0.6, 1.05, xs[i + 1] - 0.6, 1.05, color=PURPLE, lw=2, ms=14)
    arrow(ax, xs[3], 0.72, xs[0], 0.72, color=PURPLE, lw=1.8, rad=-0.12, ls=(0, (4, 3)), ms=14)
    pill(ax, 14.75, 1.9, '\\$ = "do not move"', color=CORAL, fs=17)
    save(fig, OUT.format(14))


def num(ax, x, y, n, color):
    ax.add_patch(Circle((x, y), 0.2, fc=color, ec="none"))
    text(ax, x, y, str(n), fs=15, bold=True, color="white")


def s20():  # how XLOOKUP finds a category
    fig, ax = canvas()
    top = 5.75
    # left: orders_clean sheet, row 2 (the first real order); the category formula lives in column W
    ocols = ["order_id", "order_date", "customer_id", "product_id", "…", "category"]
    ocw = [1.15, 1.4, 1.4, 1.3, 0.45, 1.2]
    ox0 = 0.5
    x = ox0
    for j, w in enumerate(ocw):
        text(ax, x + w / 2, top + 0.24, ["A", "B", "C", "D", "", "W"][j], fs=15, bold=True, color=MUTED)
        x += w
    orh = 0.55
    text(ax, ox0 - 0.2, top - 1.5 * orh, "2", fs=15, bold=True, color=MUTED)
    table(ax, ox0, top, ocols, [["O10001", "2025-01-01", "C0593", "P048", "…", "Books"]], ocw, rh=orh, color=ORANGE,
          fs=15, highlight={(0, 3): TINT[BLUE], (0, 5): TINT[GREEN]})
    yo0 = top - 2 * orh                      # bottom of row 2
    xd = ox0 + sum(ocw[:3]); xe = ox0 + sum(ocw[:5])
    ax.add_patch(Rectangle((xd, yo0), ocw[3], orh, fc="none", ec=BLUE, lw=3))
    ax.add_patch(Rectangle((xe, yo0), ocw[5], orh, fc="none", ec=GREEN, lw=3))
    text(ax, ox0, yo0 - 0.35, "orders_clean sheet", fs=17, bold=True, color=ORANGE, ha="left")
    text(ax, ox0, yo0 - 0.85, "D2 (P048) is what we look up.\nW2 holds the formula and\ngets the answer: Books", fs=16,
         color=MUTED, ha="left", va="top")

    # right: products sheet
    pcols = ["product_id", "product_name", "category"]
    pcw = [1.5, 2.45, 2.2]
    px0 = 9.4
    x = px0
    for j, w in enumerate(pcw):
        text(ax, x + w / 2, top + 0.24, "ABC"[j], fs=15, bold=True, color=MUTED)
        x += w
    rows = [["P001", "Wireless Earbuds", "Electronics"], ["P013", "Cotton T-Shirt", "Fashion"],
            ["P025", "Non-stick Pan", "Home"], ["P048", "Wings of Fire", "Books"]]   # a few of the 60 rows
    rh = 0.5
    table(ax, px0, top, pcols, rows, pcw, rh=rh, color=PURPLE, fs=15,
          highlight={(3, 0): TINT[BLUE], (3, 1): TINT[BLUE], (3, 2): TINT[GREEN]})
    ybot = top - rh * 5
    yrow = ybot + rh / 2
    text(ax, px0 + sum(pcw), ybot - 1.45, "products sheet", fs=17, bold=True, color=PURPLE, ha="right")
    text(ax, px0 + sum(pcw), ybot - 1.85, "60 products in rows 2 to 61 (4 shown)", fs=14, color=MUTED, ha="right")

    # 1: take P048 over and search down product_id
    xv = px0 - 0.28
    yh = yo0 - 0.3
    xs_ = 8.7
    ax.plot([xd + ocw[3] / 2, xd + ocw[3] / 2, xs_, xs_, xv], [yo0, yh, yh, top - rh, top - rh], color=BLUE,
            lw=3, solid_joinstyle="round")
    arrow(ax, xv, top - rh, xv, yrow, color=BLUE, lw=3)
    ax.plot([xv, px0], [yrow, yrow], color=BLUE, lw=3)
    num(ax, 6.65, 3.85, 1, BLUE)
    text(ax, 6.95, 3.85, "look for P048", fs=16, bold=True, color=BLUE, ha="left")
    text(ax, 6.95, 3.4, "down product_id", fs=16, bold=True, color=BLUE, ha="left")
    # 2: step across the row to category
    xa = px0 + pcw[0] / 2
    xb = px0 + pcw[0] + pcw[1] + pcw[2] / 2
    arrow(ax, xa, ybot - 0.05, xb, ybot - 0.05, color=GREEN, lw=3, rad=0.2)
    num(ax, 9.95, ybot - 0.9, 2, GREEN)
    text(ax, 10.25, ybot - 0.9, "step across to category, return Books", fs=16, bold=True, color=GREEN, ha="left")
    # the formula, with its four parts labelled underneath
    yf = 1.3
    f = '=XLOOKUP(D2, products!\\$A\\$2:\\$A\\$61, products!\\$C\\$2:\\$C\\$61, "Not found")'
    xf = 7.0   # left of the products caption
    pill(ax, xf, yf, f, color=CORAL, fs=18)
    r = fig.canvas.get_renderer()
    probe = text(ax, 0, -5, f, fs=18, bold=True, ha="left")
    fw = probe.get_window_extent(r).width / fig.dpi
    x0 = xf - fw / 2

    def xat(sub):   # canvas x of the centre of substring sub
        i = f.index(sub)
        probe.set_text(f[:i]); a = probe.get_window_extent(r).width / fig.dpi
        probe.set_text(f[:i + len(sub)]); b = probe.get_window_extent(r).width / fig.dpi
        return x0 + (a + b) / 2

    parts = [("D2", "what\nto find"), ("products!\\$A\\$2:\\$A\\$61", "where\nto look"), ("products!\\$C\\$2:\\$C\\$61", "what\nto return"),
             ('"Not found"', "if it is\nnot there")]
    for sub, lab in parts:
        ax.plot([xat(sub)] * 2, [yf - 0.3, yf - 0.45], color=CORAL, lw=2)
        text(ax, xat(sub), yf - 0.5, lab, fs=15, bold=True, color=CORAL, va="top")
    probe.remove()
    save(fig, OUT.format(21))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s13(); s20()
