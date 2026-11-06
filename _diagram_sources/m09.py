from style import *
import numpy as np
plt.rcParams["font.family"] = ["Liberation Sans", "DejaVu Sans"]   # DejaVu supplies the ₹ glyph

OUT = "out/m09_s{:02d}.png"


def s05():  # learning from past orders: X and y
    fig, ax = canvas()
    cols = ["city", "delivery_days", "COD?", "returned"]
    rows = [["Pune", 7, "Yes", "Yes"], ["Delhi", 3, "No (UPI)", "No"], ["Mumbai", 6, "Yes", "No"],
            ["Pune", 10, "Yes", "Yes"], ["Bengaluru", 3, "No", "No"]]
    cw = [2.2, 2.4, 1.8, 1.9]
    x0, y0, rh = 0.6, 5.0, 0.56
    hl = {(0, 3): TINT[CORAL], (3, 3): TINT[CORAL]}
    table(ax, x0, y0, cols, rows, cw, rh=rh, color=BLUE, fs=17, highlight=hl)
    # bracket over X columns
    xa, xb = x0 + 0.05, x0 + sum(cw[:3]) - 0.05
    yb = y0 + 0.15
    ax.plot([xa, xa, xb, xb], [yb, yb + 0.2, yb + 0.2, yb], color=BLUE, lw=2.5)
    ax.plot([(xa + xb) / 2] * 2, [yb + 0.2, yb + 0.35], color=BLUE, lw=2.5)
    text(ax, (xa + xb) / 2, yb + 0.65, "X  (features)", fs=19, bold=True, color=BLUE)
    # circle y column
    cx = x0 + sum(cw[:3]) + cw[3] / 2
    n = len(rows) + 1
    ax.add_patch(Ellipse((cx, y0 - rh * n / 2), cw[3] + 0.35, rh * n + 0.45, fc="none", ec=CORAL, lw=3))
    text(ax, cx, yb + 0.65, "y  (target)", fs=19, bold=True, color=CORAL)
    text(ax, x0 + sum(cw) / 2, y0 - rh * n - 0.5, "5 past orders, 2 returned  →  the model learns from these",
         fs=16, color=MUTED)
    # new row
    nx0 = 10.0
    text(ax, nx0 + 2.85, 4.35, "New order (today)", fs=19, bold=True, color=ORANGE)
    table(ax, nx0, 3.95, ["city", "delivery", "COD?", "returned"], [["Pune", 6, "Yes", "?"]],
          [1.5, 1.5, 1.1, 1.6], rh=0.56, color=ORANGE, fs=17, highlight={(0, 3): "white"})
    text(ax, nx0 + 4.1 + 0.8, 3.95 - 0.56 * 1.5, "?", fs=26, bold=True, color=CORAL)
    arrow(ax, 9.3, 3.3, 9.9, 3.3, lw=2.5, color=INK)
    text(ax, nx0 + 2.85, 2.35, "We know X, the model predicts y", fs=16, color=MUTED)
    pill(ax, 8, 0.6, "Past rows teach the pattern  X → y.   New row: fill in returned = ?")
    save(fig, OUT.format(5))


def s11():  # exam analogy: train/test split
    fig, ax = canvas()
    box(ax, 2.1, 3.65, 3.2, 3.0, "5,000\norders\n\n13.7% returned\n(685)", color=BLUE, fs=20)
    # train / test boxes
    box(ax, 7.4, 4.85, 4.0, 1.6, "4,000  practice questions\nTRAIN  (80%)\n13.7% returned (548)", color=TEAL, fs=17)
    box(ax, 7.4, 2.15, 4.0, 1.6, "1,000  hidden exam questions\nTEST  (20%)\n13.7% returned (137)", color=ORANGE, fs=17)
    arrow(ax, 3.7, 4.3, 5.4, 4.85, lw=2.5)
    arrow(ax, 3.7, 3.0, 5.4, 2.3, lw=2.5)
    # model and score
    box(ax, 13.4, 4.85, 3.0, 1.2, "Model", color=PURPLE, fs=22, bold=True)
    arrow(ax, 9.4, 4.85, 11.9, 4.85, lw=2.5, color=TEAL)
    text(ax, 10.65, 5.15, "studies ONLY this", fs=16, color=TEAL, bold=True)
    box(ax, 13.4, 2.15, 3.0, 1.2, "Score\n(accuracy)", color=CORAL, fs=19, bold=True)
    arrow(ax, 13.4, 4.25, 13.4, 2.75, lw=2.5, color=PURPLE)
    text(ax, 13.55, 3.5, "predicts", fs=16, color=PURPLE, ha="left")
    arrow(ax, 9.4, 2.15, 11.9, 2.15, lw=2.5, color=ORANGE)
    text(ax, 10.65, 2.45, "score ONLY here", fs=16, color=ORANGE, bold=True)
    text(ax, 10.65, 1.8, "never studied", fs=15, color=MUTED)
    pill(ax, 8, 0.55, "stratify: 13.7% returns in both boxes (train and test)")
    save(fig, OUT.format(11))


def s15():  # best straight line
    fig, ax = canvas()
    ox, oy, xw, yh = 1.6, 2.0, 8.6, 3.95     # axes box in canvas units
    qmax, rmax = 9, 12000
    X = lambda q: ox + q / qmax * xw
    Y = lambda r: oy + r / rmax * yh
    ax.plot([ox, ox + xw + 0.2], [oy, oy], color=INK, lw=2)
    ax.plot([ox, ox], [oy, oy + yh + 0.2], color=INK, lw=2)
    for q in range(1, 9):
        ax.plot([X(q)] * 2, [oy, oy - 0.08], color=INK, lw=1.5)
        text(ax, X(q), oy - 0.3, str(q), fs=15)
    for r in [4000, 8000, 12000]:
        ax.plot([ox, ox - 0.08], [Y(r)] * 2, color=INK, lw=1.5)
        text(ax, ox - 0.15, Y(r), f"₹{r:,}", fs=15, ha="right")
    text(ax, ox - 0.15, oy, "₹0", fs=15, ha="right")
    text(ax, ox + xw / 2, oy - 0.75, "quantity", fs=18, bold=True)
    text(ax, 0.35, oy + yh / 2, "revenue", fs=18, bold=True, rotation=90)
    q = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    r = np.array([3300, 2000, 5200, 4200, 7400, 6000, 9800, 8300])
    b, a = np.polyfit(q, r, 1)
    xs = np.array([0.5, 8.6])
    ax.plot(X(xs), Y(a + b * xs), color=TEAL, lw=3.5, zorder=2)
    for qi, ri in zip(q, r):
        yl = a + b * qi
        arrow(ax, X(qi), Y(ri), X(qi), Y(yl), color=CORAL, lw=2, ms=14)
    ax.scatter(X(q), Y(r), s=110, color=BLUE, zorder=3, edgecolor="white", lw=1.5)
    # legend panel
    lx = 11.2
    ax.scatter([lx], [5.2], s=110, color=BLUE)
    text(ax, lx + 0.35, 5.2, "one order (dot)", fs=17, ha="left")
    ax.plot([lx - 0.25, lx + 0.25], [4.35, 4.35], color=TEAL, lw=3.5)
    text(ax, lx + 0.35, 4.35, "best straight line", fs=17, ha="left")
    arrow(ax, lx, 3.75, lx, 3.25, color=CORAL, ms=14)
    text(ax, lx + 0.35, 3.5, "error = actual − line", fs=17, ha="left")
    text(ax, lx - 0.25, 2.45, "Best line = smallest\ntotal (squared) error", fs=17, ha="left", color=MUTED)
    pill(ax, 6.0, 0.5, "revenue = intercept + slope × quantity", color=CORAL)
    save(fig, OUT.format(15))


def s20():  # decision tree
    fig, ax = canvas()
    box(ax, 8, 5.6, 3.6, 0.75, "City = Pune?", color=BLUE, fs=20, bold=True)
    box(ax, 4.3, 3.75, 4.6, 1.05, "~31% returned\nthen asks: delivery > 9 days?", color=BLUE, fs=18)
    box(ax, 11.7, 3.75, 3.4, 1.05, "Fashion?", color=BLUE, fs=20, bold=True)
    arrow(ax, 7.0, 5.22, 5.0, 4.28, lw=2.5)
    arrow(ax, 9.0, 5.22, 11.0, 4.28, lw=2.5)
    text(ax, 5.55, 4.95, "Yes", fs=17, bold=True, color=GREEN)
    text(ax, 10.45, 4.95, "No", fs=17, bold=True, color=CORAL)
    leaves = [(2.4, "more questions …", MUTED, "Yes"), (6.2, "more questions …", MUTED, "No"),
              (9.8, "Fashion: ~19% returned", ORANGE, "Yes"), (13.6, "Everything else: ~10%", GREEN, "No")]
    for i, (lx, s, c, lab) in enumerate(leaves):
        px = 4.3 if i < 2 else 11.7
        if i < 2:
            box(ax, lx, 1.95, 3.0, 0.8, s, color=c, fill="white", fs=17, tc=MUTED, ls="--")
        else:
            box(ax, lx, 1.95, 3.6, 0.8, s, color=c, fs=17, bold=True)
        arrow(ax, px + (-0.8 if lx < px else 0.8), 3.22, lx, 2.37, lw=2.5)
        mx = (px + (-0.8 if lx < px else 0.8) + lx) / 2
        text(ax, mx + (-0.4 if lx < px else 0.4), 2.85, lab, fs=16, bold=True,
             color=GREEN if lab == "Yes" else CORAL)
    text(ax, 0.35, 5.6, "Q1", fs=16, color=MUTED, ha="left", bold=True)
    text(ax, 0.35, 3.75, "Q2", fs=16, color=MUTED, ha="left", bold=True)
    text(ax, 0.35, 1.95, "leaf", fs=16, color=MUTED, ha="left", bold=True)
    pill(ax, 8, 0.55, "max_depth = number of questions in a row   (we'll use max_depth = 4)")
    save(fig, OUT.format(20))


def s27():  # confusion matrix
    fig, ax = canvas()
    gx, gy, cw, ch = 3.4, 5.2, 3.5, 1.85
    text(ax, gx + cw, 6.05, "PREDICTED", fs=18, bold=True, color=MUTED)
    text(ax, gx + cw / 2, 5.5, "said kept", fs=17, bold=True, va="baseline")
    text(ax, gx + 1.5 * cw, 5.5, "said returned", fs=17, bold=True, va="baseline")
    text(ax, 0.6, gy - ch, "ACTUAL", fs=18, bold=True, color=MUTED, rotation=90)
    text(ax, gx - 0.2, gy - ch / 2, "kept", fs=17, bold=True, ha="right")
    text(ax, gx - 0.2, gy - 1.5 * ch, "returned", fs=17, bold=True, ha="right")
    cells = [(0, 0, "True negative", "kept, said kept", GREEN), (0, 1, "False positive", "false alarm", ORANGE),
             (1, 0, "False negative", "missed return", CORAL), (1, 1, "True positive", "caught it!", TEAL)]
    for r, c, a, b, col in cells:
        x = gx + cw * (c + 0.5); y = gy - ch * (r + 0.5)
        box(ax, x, y, cw - 0.1, ch - 0.1, color=col, r=0.06)
        text(ax, x, y + 0.3, a, fs=22, bold=True, color=col)
        text(ax, x, y - 0.35, b, fs=18)
    lx = 11.2
    text(ax, lx, 4.75, "Rows: what really happened", fs=17, ha="left", bold=True)
    text(ax, lx, 4.15, "Columns: what the model said", fs=17, ha="left", bold=True)
    text(ax, lx, 3.3, "Diagonal = model was right", fs=17, ha="left", color=TEAL, bold=True)
    text(ax, lx, 2.7, "False positive = flag a good order", fs=17, ha="left", color=ORANGE)
    text(ax, lx, 2.1, "False negative = return slips past", fs=17, ha="left", color=CORAL)
    pill(ax, 8, 0.6, "Rows = actual,  columns = predicted")
    save(fig, OUT.format(27))


def s32():  # train vs test curves
    fig, ax = canvas()
    ox, oy, xw, yh = 1.6, 2.0, 9.4, 3.95
    lo, hi = 0.70, 1.00
    X = lambda d: ox + (d - 1) / 14 * xw
    Y = lambda v: oy + (v - lo) / (hi - lo) * yh
    ax.plot([ox, ox + xw + 0.2], [oy, oy], color=INK, lw=2)
    ax.plot([ox, ox], [oy, oy + yh + 0.2], color=INK, lw=2)
    for d in [1, 3, 5, 7, 9, 11, 13, 15]:
        ax.plot([X(d)] * 2, [oy, oy - 0.08], color=INK, lw=1.5)
        text(ax, X(d), oy - 0.3, str(d), fs=15)
    for v in [0.7, 0.8, 0.9, 1.0]:
        ax.plot([ox, ox - 0.08], [Y(v)] * 2, color=INK, lw=1.5)
        text(ax, ox - 0.15, Y(v), f"{int(v*100)}%", fs=15, ha="right")
    text(ax, ox + xw / 2, oy - 0.75, "tree depth (max_depth)", fs=18, bold=True)
    text(ax, 0.35, oy + yh / 2, "accuracy", fs=18, bold=True, rotation=90)
    d = np.arange(1, 16)
    train = np.array([.80, .84, .87, .89, .91, .93, .95, .96, .97, .98, .99, .995, 1, 1, 1])
    test = np.array([.79, .83, .85, .86, .86, .855, .85, .84, .83, .82, .81, .80, .79, .785, .78])
    ax.fill_between(X(d), Y(test), Y(train), color=TINT[CORAL], zorder=1)
    ax.plot(X(d), Y(train), color=BLUE, lw=3.5, marker="o", ms=6, zorder=3)
    ax.plot(X(d), Y(test), color=ORANGE, lw=3.5, marker="o", ms=6, zorder=3)
    ax.plot([X(4)] * 2, [oy, Y(0.97)], color=MUTED, lw=1.5, ls="--")
    text(ax, X(4), Y(0.985), "best depth", fs=15, color=MUTED)
    text(ax, X(12.2), Y(0.89), "gap =\noverfitting", fs=17, bold=True, color=CORAL)
    text(ax, X(2.2), Y(0.74), "underfit", fs=18, bold=True, color=PURPLE)
    text(ax, X(13), Y(0.74), "overfit", fs=18, bold=True, color=CORAL)
    lx = 12.0
    ax.plot([lx, lx + 0.6], [4.9, 4.9], color=BLUE, lw=3.5)
    text(ax, lx + 0.8, 4.9, "train accuracy", fs=17, ha="left")
    ax.plot([lx, lx + 0.6], [4.2, 4.2], color=ORANGE, lw=3.5)
    text(ax, lx + 0.8, 4.2, "test accuracy", fs=17, ha="left")
    text(ax, lx, 2.9, "Train climbs to 100%\n(memorising).\nTest stalls, then falls.", fs=16,
         ha="left", color=MUTED)
    pill(ax, 8, 0.5, "Pick the depth where TEST is highest, not train")
    save(fig, OUT.format(32))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    for f in (s05, s11, s15, s20, s27, s32):
        f()
