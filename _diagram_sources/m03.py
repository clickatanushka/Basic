from style import *
plt.rcParams["font.family"] = ["Liberation Sans", "DejaVu Sans"]   # DejaVu supplies the ₹ glyph
import numpy as np
from math import erf

OUT = "out/m03_s{:02d}.png"


def s04():  # the data-type tree
    fig, ax = canvas()
    box(ax, 5.4, 5.9, 2.4, 0.75, "Data", color=BLUE, fs=22, bold=True)
    box(ax, 2.8, 4.35, 3.2, 0.75, "Categorical", color=TEAL, fs=20, bold=True)
    box(ax, 8.2, 4.35, 3.2, 0.75, "Numerical", color=ORANGE, fs=20, bold=True)
    arrow(ax, 4.9, 5.52, 3.2, 4.73)
    arrow(ax, 5.9, 5.52, 7.8, 4.73)
    text(ax, 3.55, 5.1, "labels / groups", fs=15, color=MUTED, ha="right", va="bottom")
    text(ax, 7.35, 5.1, "counts / amounts", fs=15, color=MUTED, ha="left", va="bottom")
    leaves = [(1.4, "Nominal", "city, payment", "no order:\nDelhi, Pune · COD, UPI\nbinary (returned) = 2 groups", TEAL, 2.3),
              (4.1, "Ordinal", "rating", "has order:\n1 < 2 < 3 < 4 < 5", TEAL, 3.3),
              (6.9, "Discrete", "quantity", "counted:\n1, 2, 3 items", ORANGE, 7.7),
              (9.6, "Continuous", "revenue", "measured:\n₹1,249.50", ORANGE, 8.7)]
    for x, name, col, ex, c, px in leaves:
        box(ax, x, 2.85, 2.55, 1.0, f"{name}\n({col})", color=c, fs=18, bold=False)
        arrow(ax, px, 3.97, x, 3.35)
        text(ax, x, 1.75, ex, fs=15, color=MUTED, va="center")
    # side note: ID-like columns are labels
    box(ax, 13.45, 3.9, 4.4, 4.3, "", color=CORAL, ls="--")
    text(ax, 13.45, 5.65, "order_id = O10001", fs=19, bold=True, color=CORAL)
    text(ax, 13.45, 5.05, "→ label!", fs=21, bold=True, color=RED)
    text(ax, 13.45, 4.05, "Also labels: customer ID,\nPIN code, mobile number", fs=16)
    text(ax, 13.45, 3.05, "They look like numbers,\nbut they only identify.", fs=16)
    text(ax, 13.45, 2.15, "Adding or averaging\nthem = nonsense.", fs=17, bold=True, color=RED)
    pill(ax, 8, 0.5, "Type decides the maths:  labels → count & %   ·   numbers → add, average, spread")
    save(fig, OUT.format(4))


def s07():  # one bulk order breaks the average
    fig, ax = canvas()
    # left panel
    box(ax, 3.9, 4.0, 7.2, 4.2, "", color=TEAL)
    text(ax, 3.9, 5.65, "5 orders (₹)", fs=20, bold=True, color=TEAL)
    for i, v in enumerate(["500", "700", "800", "900", "1,100"]):
        box(ax, 1.25 + 1.32 * i, 4.8, 1.15, 0.65, v, color=TEAL, fill="white", fs=18, bold=(v == "800"))
    ax.add_patch(Ellipse((1.25 + 1.32 * 2, 4.8), 1.6, 1.05, fc="none", ec=CORAL, lw=2.5))   # circle the middle
    text(ax, 0.75, 3.8, "Mean   = (500+700+800+900+1100) ÷ 5", fs=18, ha="left")
    text(ax, 0.75, 3.25, "          = 4,000 ÷ 5 = 800", fs=18, ha="left")
    text(ax, 0.75, 2.7, "Median = middle value = 800", fs=18, ha="left")
    text(ax, 3.9, 2.2, "mean and median agree", fs=16, color=MUTED)
    # right panel
    box(ax, 12.0, 4.0, 7.4, 4.2, "", color=CORAL)
    text(ax, 12.0, 5.65, "Add one bulk order (phones)", fs=20, bold=True, color=CORAL)
    for i, v in enumerate(["500", "700", "800", "900", "1,100"]):
        mid = v in ("800", "900")
        box(ax, 8.95 + 1.1 * i, 4.8, 0.98, 0.65, v, color=TEAL, fill=TINT[TEAL] if mid else "white", fs=16, bold=mid)
    box(ax, 14.65, 4.8, 1.45, 0.65, "1,50,000", color=RED, fill=TINT[CORAL], fs=16, bold=True, lw=2.5)
    xm = 8.95 + 1.1 * 2.5
    ax.plot([xm, xm], [4.35, 5.25], color=INK, lw=2.5)   # split between the two middle values
    text(ax, 8.65, 3.7, "New mean   = 1,54,000 ÷ 6 = ", fs=19, ha="left")
    t = text(ax, 12.15, 3.7, "25,667", fs=19, ha="left", bold=True, color=RED)
    ax.plot([12.15, 13.25], [3.47, 3.47], color=RED, lw=2); ax.plot([12.15, 13.25], [3.41, 3.41], color=RED, lw=2)
    text(ax, 8.65, 2.95, "New median = (800 + 900) ÷ 2 = ", fs=19, ha="left")
    text(ax, 12.55, 2.95, "850", fs=19, ha="left", bold=True, color=TEAL)
    text(ax, 12.0, 2.3, "the mean describes nobody; the median barely moved", fs=16, color=MUTED)
    arrow(ax, 7.65, 4.0, 8.25, 4.0, lw=2.5)
    pill(ax, 8, 1.15, "Median resists outliers. Mean does not.", fs=20)
    text(ax, 8, 0.38, "Mode = most frequent value  (e.g. most common city, usual number of items)", fs=17, bold=True)
    save(fig, OUT.format(7))


def s12():  # same average, different promise
    fig, ax = canvas()
    X = lambda d: 1.9 + 0.95 * d
    def line(y, label, color, days, stacked):
        text(ax, 0.35, y + 1.2, label, fs=20, bold=True, color=color, ha="left")
        ax.plot([X(0), X(8)], [y, y], color=INK, lw=2)
        for d in range(0, 9):
            ax.plot([X(d), X(d)], [y - 0.08, y + 0.08], color=INK, lw=1.5)
            text(ax, X(d), y - 0.35, str(d), fs=15, color=MUTED)
        seen = {}
        for d in days:
            k = seen.get(d, 0); seen[d] = k + 1
            ax.add_patch(Circle((X(d), y + 0.27 + 0.32 * k), 0.14, fc=color, ec="white", lw=1.2))
        text(ax, X(8) + 0.25, y, "days", fs=15, color=MUTED, ha="left")
    line(4.1, "City X:  4, 4, 4, 4, 4", TEAL, [4] * 5, True)
    line(1.65, "City Y:  1, 2, 4, 6, 7", ORANGE, [1, 2, 4, 6, 7], False)
    # mean marker
    for a, b in ((4.1, 5.95), (1.65, 3.5)):
        ax.plot([X(4), X(4)], [a, b], color=CORAL, lw=2, ls="--", zorder=0)
    text(ax, X(4) + 0.12, 6.12, "mean = 4 for both", fs=16, color=CORAL, bold=True, ha="left")
    # circle the cluster in X
    ax.add_patch(Ellipse((X(4), 4.1 + 0.27 + 0.62), 0.85, 1.7, fc="none", ec=TEAL, lw=2.2, ls="--"))
    text(ax, X(4) + 0.6, 4.75, "all on day 4", fs=15, color=TEAL, bold=True, ha="left")
    # arrows across the spread of Y
    yb = 2.5
    arrow(ax, X(4) - 0.1, yb, X(1), yb, color=ORANGE, lw=2.2)
    arrow(ax, X(4) + 0.1, yb, X(7), yb, color=ORANGE, lw=2.2)
    text(ax, X(5.5), yb + 0.25, "all over the place", fs=15, color=ORANGE, bold=True)
    # stats table
    text(ax, 13.2, 5.75, "Range = max − min", fs=20, bold=True, color=BLUE)
    table(ax, 10.7, 5.25, ["", "City X", "City Y"], [["Mean", "20 ÷ 5 = 4", "20 ÷ 5 = 4"],
                                                    ["Range", "4 − 4 = 0", "7 − 1 = 6"]],
          [1.3, 1.85, 1.85], rh=0.62, color=BLUE, fs=17,
          highlight={(1, 2): TINT[ORANGE], (1, 1): TINT[TEAL]})
    text(ax, 13.2, 2.45, "Range sees only the two extremes:\none bulk order makes ShopKart's\nrevenue range ≈ ₹1.5 lakh", fs=16, color=MUTED)
    pill(ax, 8, 0.55, "Which city would you trust for a birthday gift?", fs=17)
    save(fig, OUT.format(12))


def s15():  # box plot of delivery days
    fig, ax = canvas()
    X = lambda d: 1.0 + 1.35 * (d - 2)
    ya = 2.55; yb = 3.9
    ax.plot([X(2) - 0.2, X(12) + 0.3], [ya, ya], color=INK, lw=2)
    for d in range(2, 13):
        ax.plot([X(d), X(d)], [ya - 0.09, ya + 0.09], color=INK, lw=1.5)
        text(ax, X(d), ya - 0.38, str(d), fs=16, color=MUTED)
    text(ax, X(12) + 0.45, ya, "days", fs=15, color=MUTED, ha="left")
    # whiskers
    ax.plot([X(2), X(3)], [yb, yb], color=INK, lw=2.2)
    ax.plot([X(5), X(8)], [yb, yb], color=INK, lw=2.2)
    for d in (2, 8):
        ax.plot([X(d), X(d)], [yb - 0.3, yb + 0.3], color=INK, lw=2.2)
    ax.add_patch(Rectangle((X(3), yb - 0.55), X(5) - X(3), 1.1, fc=TINT[TEAL], ec=TEAL, lw=2.5))
    ax.plot([X(4), X(4)], [yb - 0.55, yb + 0.55], color=TEAL, lw=3.5)
    # labels
    text(ax, X(2), yb + 0.75, "min = 2", fs=16)
    text(ax, X(4), yb + 0.85, "median = 4", fs=16, bold=True, color=TEAL)
    text(ax, X(3), yb - 0.85, "Q1 = 3", fs=16)
    text(ax, X(5), yb - 0.85, "Q3 = 5", fs=16)
    text(ax, X(8), yb + 0.6, "fence = 8", fs=16)
    # outliers
    for d in (9, 10, 11, 12):
        ax.add_patch(Circle((X(d), yb), 0.15, fc=CORAL, ec="white", lw=1.2))
    yk = yb + 0.5
    ax.plot([X(9) - 0.2, X(9) - 0.2, X(12) + 0.2, X(12) + 0.2], [yk - 0.1, yk, yk, yk - 0.1], color=CORAL, lw=2)
    text(ax, (X(9) + X(12)) / 2, yk + 0.35, "9, 10, 11, 12 days: 36 orders", fs=17, bold=True, color=CORAL)
    text(ax, (X(9) + X(12)) / 2, yk + 0.85, "these are the late deliveries", fs=17, color=CORAL)
    text(ax, 0.6, 1.4, "IQR = Q3 − Q1 = 5 − 3 = 2      fence = Q3 + 1.5 × IQR = 5 + 3 = 8", fs=16,
         color=MUTED, ha="left")
    pill(ax, 8, 0.6, "Dots past the fence = the late deliveries to investigate")
    save(fig, OUT.format(15))


def s18():  # three shapes
    fig, ax = canvas()
    base, peak = 2.15, 2.85
    # 1. bell
    cx, sc = 2.85, 0.78
    z = np.linspace(-3, 3, 400); f = np.exp(-z ** 2 / 2)
    xs, ys = cx + z * sc, base + peak * f
    for k, a in ((2, TINT[TEAL]), (1, "#BFE3DE")):
        m = np.abs(z) <= k
        ax.fill_between(xs[m], base, ys[m], color=a, lw=0)
    ax.plot(xs, ys, color=TEAL, lw=3)
    ax.plot([xs[0] - 0.1, xs[-1] + 0.1], [base, base], color=INK, lw=2)
    ax.plot([cx, cx], [base, base + peak], color=CORAL, lw=2, ls="--")
    text(ax, cx, base + peak + 0.3, "mean = median = mode", fs=16, bold=True, color=CORAL)
    for k, y, lab in ((1, 1.75, "68% within 1 SD  (50–70)"), (2, 1.05, "95% within 2 SD  (40–80)")):
        x1, x2 = cx - k * sc, cx + k * sc
        ax.plot([x1, x1, x2, x2], [y + 0.12, y, y, y + 0.12], color=INK, lw=1.8)
        text(ax, cx, y - 0.27, lab, fs=16, bold=True)
    text(ax, cx, 5.95, "Symmetric (bell)", fs=20, bold=True, color=TEAL)
    text(ax, cx, 0.35, "e.g. exam marks: mean 60, SD 10", fs=15, color=MUTED)

    # 2/3. skewed hills (gamma k=2.2)
    def hill(cx, color, title, mirror, example):
        k, th = 2.2, 1.0
        t = np.linspace(0, 11, 500)
        g = t ** (k - 1) * np.exp(-t / th); g = g / g.max()
        span = 4.4; s = span / 11
        x0 = cx - span / 2
        def X(tt):
            return x0 + tt * s if not mirror else x0 + span - tt * s
        xs, ys = X(t), base + peak * g
        ax.fill_between(xs, base, ys, color=TINT[color], lw=0)
        ax.plot(xs, ys, color=color, lw=3)
        ax.plot([x0 - 0.15, x0 + span + 0.15], [base, base], color=INK, lw=2)
        mode, mean = (k - 1) * th, k * th
        med = th * (k - 1 / 3 + 0.02)
        gv = lambda tt: base + peak * (tt ** (k - 1) * np.exp(-tt)) / ((k - 1) ** (k - 1) * np.exp(-(k - 1)))
        for tt, c in ((mode, MUTED), (med, BLUE), (mean, CORAL)):
            ax.plot([X(tt), X(tt)], [base, gv(tt)], color=c, lw=2.4, ls="--" if c != MUTED else ":")
        tx = X(8.0)
        text(ax, tx, base + 0.75, "long tail →" if not mirror else "← long tail", fs=16, color=color, bold=True)
        sg = -1 if mirror else 1
        text(ax, cx - 1.0 * sg, 1.65, "mode", fs=16, color=MUTED, bold=True)
        text(ax, cx, 1.65, "median", fs=16, color=BLUE, bold=True)
        text(ax, cx + 1.0 * sg, 1.65, "mean", fs=16, color=CORAL, bold=True)
        text(ax, cx, 1.05, "mean pulled " + ("right" if not mirror else "left") + " of median", fs=16)
        text(ax, cx, 5.95, title, fs=20, bold=True, color=color)
        text(ax, cx, 0.35, example, fs=15, color=MUTED)
        # arrow: the tail drags the mean away from the median
        ya = base + peak + 0.25
        for tt, c in ((med, BLUE), (mean, CORAL)):
            ax.plot([X(tt), X(tt)], [gv(tt), ya], color=c, lw=1.4, ls=":")
        arrow(ax, X(med), ya, X(mean) + (1.1 if not mirror else -1.1), ya, color=CORAL, lw=2.2)
        text(ax, X(mean) + (1.2 if not mirror else -1.2), ya, "mean pulled by tail",
             fs=15, color=CORAL, bold=True, ha="left" if not mirror else "right")
    hill(8.0, ORANGE, "Right skew (positive)", False, "money: salaries, house prices, order values")
    hill(13.15, PURPLE, "Left skew (negative)", True, "ratings: most give 4–5★, a few give 1–2")
    for xx in (5.45, 10.6):
        ax.plot([xx, xx], [0.5, 6.0], color=LINE, lw=1, ls=":")
    save(fig, OUT.format(18))


def s22():  # the correlation scale
    fig, ax = canvas()
    X = lambda r: 8 + 6.5 * r
    yl = 3.0
    # bands
    bands = [(0, 0.1, "none", LINE), (0.1, 0.3, "weak", BLUE), (0.3, 0.6, "moderate", TEAL), (0.6, 1.0, "strong", CORAL)]
    for a, b, lab, c in bands:
        for sgn in ((1,) if a == 0 else (1, -1)):
            x1, x2 = sorted((X(sgn * a if a else -b), X(sgn * b)))
            ax.add_patch(Rectangle((x1, 1.95), x2 - x1, 0.6, fc=TINT.get(c, "#EEF0F3"), ec="white", lw=2))
            text(ax, (x1 + x2) / 2, 2.25, lab, fs=16, bold=True, color=c if c != LINE else MUTED)
    ax.plot([X(-1), X(1)], [yl, yl], color=INK, lw=2.5)
    for r in (-1, -0.6, -0.3, -0.1, 0, 0.1, 0.3, 0.6, 1):
        big = r in (-1, 0, 1)
        ax.plot([X(r), X(r)], [yl - (0.16 if big else 0.1), yl + (0.16 if big else 0.1)], color=INK, lw=2 if big else 1.5)
        lab = {-1: "−1", 1: "+1", 0: "0"}.get(r, f"{r:+.1f}".replace("-", "−"))
        text(ax, X(r), yl + 0.38, lab, fs=18 if big else 15, bold=big, color=INK if big else MUTED)
    # mini scatters
    rng = np.random.default_rng(3)
    def mini(cx, kind, color, label):
        w, h, y0 = 2.5, 1.75, 4.15
        x0 = cx - w / 2
        ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc=TINT[color], ec=color, lw=2))
        ax.plot([x0 + 0.25, x0 + 0.25, x0 + w - 0.2], [y0 + h - 0.15, y0 + 0.2, y0 + 0.2], color=INK, lw=1.5)
        u = rng.uniform(0, 1, 22)
        if kind == "+": v = u + rng.normal(0, 0.015, 22)
        elif kind == "-": v = 1 - u + rng.normal(0, 0.015, 22)
        else: v = rng.uniform(0, 1, 22)
        v = np.clip(v, 0, 1)
        ax.scatter(x0 + 0.45 + u * (w - 0.8), y0 + 0.4 + v * (h - 0.7), s=28, color=color, zorder=3)
        text(ax, cx, y0 - 0.32, label, fs=16, bold=True, color=color)
    mini(1.95, "-", ORANGE, "−1: van speed vs travel time")
    mini(8.0, "0", BLUE, "0: shoe size vs favourite category")
    mini(13.95, "+", TEAL, "+1: no. of books vs parcel weight")
    text(ax, X(-1), 1.55, "← one goes up, the other goes down", fs=16, color=MUTED, ha="left")
    text(ax, X(1), 1.55, "both go up together →", fs=16, color=MUTED, ha="right")
    pill(ax, 5.2, 0.6, "Sign = direction,  size = strength")
    text(ax, 11.4, 0.6, "r = −0.33 ≠ 33%", fs=21, bold=True, color=RED)
    ax.add_patch(Ellipse((11.4, 0.6), 3.3, 0.9, fc="none", ec=RED, lw=2.5))
    text(ax, 13.25, 0.6, "a strength score,\nnot a percentage", fs=15, color=MUTED, ha="left")
    save(fig, OUT.format(22))


def s28():  # how an A/B test works
    fig, ax = canvas()
    # visitors
    for i, x in enumerate((0.65, 1.25, 1.85)):
        ax.add_patch(Circle((x, 4.05), 0.2, fc=BLUE, ec="none"))
        ax.add_patch(FancyBboxPatch((x - 0.24, 3.2), 0.48, 0.55, boxstyle="round,pad=0,rounding_size=0.2",
                                    fc=BLUE, ec="none"))
    text(ax, 1.25, 2.75, "Visitors\narrive", fs=17)
    arrow(ax, 2.3, 3.7, 3.05, 3.7, lw=2.5)
    # coin
    ax.add_patch(Circle((3.6, 3.7), 0.5, fc=TINT[ORANGE], ec=ORANGE, lw=3))
    text(ax, 3.6, 3.7, "₹", fs=24, bold=True, color=ORANGE)
    text(ax, 3.6, 2.85, "coin flip", fs=17)
    arrow(ax, 4.05, 3.95, 5.0, 4.85, lw=2.5)
    arrow(ax, 4.05, 3.45, 5.0, 2.55, lw=2.5)
    text(ax, 4.3, 4.75, "Heads", fs=16, bold=True, color=ORANGE)
    text(ax, 4.3, 2.65, "Tails", fs=16, bold=True, color=ORANGE)

    def group(y, title, btn, bfc, color):
        box(ax, 7.1, y, 4.1, 1.75, "", color=color)
        text(ax, 7.1, y + 0.48, title, fs=18, bold=True, color=color)
        ax.add_patch(FancyBboxPatch((7.1 - 1.15, y - 0.62), 2.3, 0.62, boxstyle="round,pad=0,rounding_size=0.15",
                                    fc=bfc, ec="none"))
        text(ax, 7.1, y - 0.31, btn, fs=18, bold=True, color="white")
    group(4.9, "Group A: old grey button", "Proceed", "#A3A9B3", BLUE)
    group(2.5, "Group B: new orange button", "Place order", ORANGE, ORANGE)
    text(ax, 7.1, 3.7, "Only the button differs", fs=17, bold=True)
    text(ax, 7.1, 1.3, "same products · same prices · same days · same delivery promise", fs=15, color=MUTED)
    for y, n in ((4.9, 12), (2.5, 14)):
        arrow(ax, 9.15, y, 10.0, y, lw=2.5)
        box(ax, 11.35, y, 2.7, 1.3, "", color=TEAL)
        text(ax, 11.35, y + 0.3, "Count orders, 2 weeks", fs=15)
        x = 10.35                      # tally marks
        for k in range(n):
            if k % 5 == 4:
                ax.plot([x - 4 * 0.13 - 0.06, x - 0.07], [y - 0.5, y - 0.02], color=TEAL, lw=2)
                x += 0.22
            else:
                ax.plot([x, x], [y - 0.52, y - 0.02], color=TEAL, lw=2); x += 0.13
        arrow(ax, 12.7, y, 13.45, 3.7 + (0.35 if y > 3 else -0.35), lw=2.5)
    box(ax, 14.5, 3.7, 2.0, 1.5, "Compare\nA vs B", color=CORAL, fs=18, bold=True)
    pill(ax, 8, 0.5, "Random split → a real difference must come from the button (or luck)")
    save(fig, OUT.format(28))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    for f in (s04, s07, s12, s15, s18, s22, s28):
        f()
