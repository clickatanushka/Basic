from style import *

OUT = "out/m01_s{:02d}.png"


def s14():  # the data lifecycle
    fig, ax = canvas()
    steps = ["Collect", "Store", "Clean", "Analyse", "Model", "Communicate"]
    eg = ["order placed in\nShopKart app", "saved in the\norders table", "Bombay = Mumbai", "revenue / return\nrate by city", "predict which\norders return", "dashboard for\nmanagers"]
    cols = [BLUE, PURPLE, TEAL, ORANGE, CORAL, GREEN]
    xs = [1.65 + 2.54 * i for i in range(6)]
    bw, by, bh = 2.1, 4.1, 0.8
    for i, (s, e, c) in enumerate(zip(steps, eg, cols)):
        box(ax, xs[i], by, bw, bh, s, color=c, fs=19, bold=True)
        text(ax, xs[i], by - 0.48, e, fs=16, color=MUTED, va="top")
        if i < 5:
            arrow(ax, xs[i] + bw / 2 + 0.02, by, xs[i + 1] - bw / 2 - 0.02, by, lw=2)

    def bracket(ks, y, label, color, up=True, ly=None):
        d = -0.25 if up else 0.25
        ax.plot([xs[ks[0]], xs[ks[-1]]], [y, y], color=color, lw=3, solid_capstyle="round")
        for k in ks:
            ax.plot([xs[k], xs[k]], [y, y + d], color=color, lw=3, solid_capstyle="round")
        text(ax, (xs[ks[0]] + xs[ks[-1]]) / 2, y - 2 * d * 0.85 if ly is None else ly, label, fs=19, bold=True,
             color=color)

    bracket([0, 1, 2], 5.15, "Engineer", BLUE)
    bracket([3, 4, 5], 5.15, "Scientist", PURPLE)
    bracket([2, 3, 5], 2.45, "Analyst", TEAL, up=False, ly=2.0)
    text(ax, 4.2, 2.0, "Cleaning + communicating:\neveryone's job", fs=16, color=MUTED, bold=True)

    # loop back: decisions create new data
    yl, xl, xr = 0.95, 0.32, 15.68
    gap = 2.85   # half-width of the gap left for the label
    ax.plot([xs[5] + bw / 2, xr, xr, 8 + gap], [by, by, yl, yl], color=CORAL, lw=2.5, solid_joinstyle="round")
    ax.plot([8 - gap, xl, xl], [yl, yl, by], color=CORAL, lw=2.5, solid_joinstyle="round")
    arrow(ax, xl, by - 0.01, xs[0] - bw / 2, by, color=CORAL, lw=2.5)
    text(ax, 8, yl, "decision (e.g. faster courier) creates new data", fs=18, bold=True, color=CORAL)
    save(fig, OUT.format(14))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s14()
