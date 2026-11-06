from style import *

# Liberation Sans has no ₹ glyph: fall back to matplotlib's bundled DejaVu Sans for that one character
plt.rcParams["font.family"] = ["Liberation Sans", "DejaVu Sans"]

OUT = "out/m10_s{:02d}.png"


def s04():  # turn the brief into questions
    fig, ax = canvas()
    r = fig.canvas.get_renderer()
    # the brief, written word-group by word-group so 'returns' and 'profit' can be circled
    box(ax, 8, 5.7, 15.2, 0.9, "", color=INK, fill="white", lw=1.6)
    def width(t):
        return t.get_window_extent(r).width / fig.dpi

    parts = [("Brief:", "lead"), ("“", ""), ("Returns", "circ"), ("are eating into our", ""), ("profit", "circ"),
             ("– find out where they come from and if we can predict them.”", "")]
    gap, pad = 0.13, 0.2
    ts = []
    for s_, kind in parts:
        ts.append(text(ax, 0, 5.7, s_, fs=18, ha="left", bold=kind != "", color=CORAL if kind == "circ" else INK))
    ws = [width(t) for t in ts]
    total = sum(ws) + gap * (len(ws) - 2) + 4 * pad   # no gap after the opening quote 
    x = 8 - total / 2
    for i, ((s_, kind), t, w) in enumerate(zip(parts, ts, ws)):
        if kind == "circ":
            x += pad
        t.set_x(x)
        if kind == "circ":
            ax.add_patch(Ellipse((x + w / 2, 5.7), w + 0.35, 0.62, fc="none", ec=CORAL, lw=2.5))
            x += pad
        nxt = parts[i + 1][0] if i + 1 < len(parts) else ""
        x += w + (0 if s_ == "“" or nxt == "." else gap)

    heads = [("How big?", 2.75, ORANGE), ("Where?", 8, TEAL), ("Predict?", 13.25, PURPLE)]
    for name, hx, c in heads:
        ax.plot([8, 8, hx, hx], [5.25, 4.85, 4.85, 4.45], color=INK, lw=2, solid_joinstyle="round")
        box(ax, hx, 4.1, 4.6, 0.7, name, color=c, fill=c, tc="white", fs=20, bold=True)
        box(ax, hx, 1.95, 4.6, 3.25, "", color=c, lw=1.6)

    def items(hx, lines, top=3.45, line=0.35, between=0.24):
        y = top
        out = []
        for s_ in lines:
            t = text(ax, hx - 2.1, y, s_, fs=18, ha="left", va="top")
            out.append((t, y))
            y -= line * (s_.count("\n") + 1) + between
        return out

    items(2.75, ["• return rate\n   (% of orders returned)",
                 "• revenue lost to returns =\n   total ₹ revenue of\n   returned orders"], between=0.3)
    text(ax, 2.75 - 2.1, 0.85, "assume full refund; ignore return\nshipping & resale → an estimate", fs=15,
         color=MUTED, ha="left", va="center")
    items(8, ["• city", "• category", "• payment mode", "• delivery days"], between=0.4)
    out = items(13.25, ["• target = returned", "• features known at order\n   time (category, city …)", "• "],
                between=0.22)
    # rating, crossed out and labelled as leakage
    tb, yr = out[-1]
    xr = 13.25 - 2.1 + width(tb) + 0.08
    tr = text(ax, xr, yr, "rating", fs=18, ha="left", va="top")
    wr = width(tr)
    ym = yr - 0.19
    ax.plot([xr - 0.04, xr + wr + 0.06], [ym, ym], color=RED, lw=3)
    text(ax, xr + wr + 0.3, ym, "LEAKAGE", fs=26, bold=True, color=RED, ha="left")
    text(ax, 13.25 - 2.1, ym - 0.85, "given after delivery:\nreturned 2.8 stars, kept 4.1", fs=15, color=MUTED,
         ha="left", va="center")
    save(fig, OUT.format(4))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s04()
