from style import *

# Liberation Sans has no ₹ glyph: fall back to matplotlib's bundled DejaVu Sans for that one character
plt.rcParams["font.family"] = ["Liberation Sans", "DejaVu Sans"]

OUT = "out/m08_s{:02d}.png"


def bars(fig, ax, x0, y0, w, h, ymin, ymax, ticks, tag, note, ncolor):
    """Bar chart drawn as a styled inset at canvas inches (x0, y0, w, h)."""
    a = fig.add_axes([x0 / W, y0 / H, w / W, h / H])
    a.patch.set_alpha(0)
    vals = [23.2, 22.6]
    a.bar([0, 1], [v - ymin for v in vals], bottom=ymin, width=0.55, color=[TEAL, ORANGE], zorder=2)
    for i, v in enumerate(vals):
        a.text(i, v + (ymax - ymin) * 0.03, f"₹{v} L", ha="center", va="bottom", fontsize=17, fontweight="bold")
    a.set_xlim(-0.6, 1.6); a.set_ylim(ymin, ymax)
    a.set_xticks([0, 1]); a.set_xticklabels(["Delhi", "Bengaluru"], fontsize=17)
    a.set_yticks(ticks); a.set_yticklabels([f"{t:g}" for t in ticks], fontsize=15)
    for sp in ("top", "right"):
        a.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        a.spines[sp].set_color(INK); a.spines[sp].set_linewidth(1.6)
    a.tick_params(length=5, width=1.4)
    # title + verdict above the chart
    text(ax, x0 + w / 2, 6.0, tag, fs=19, bold=True)
    text(ax, x0 + w / 2, 5.55, note, fs=16, color=ncolor, bold=True)
    # circle the axis start (tick label at the bottom of the y-axis)
    ax.add_patch(Ellipse((x0 - 0.2, y0), 0.75, 0.48, fc="none", ec=RED, lw=2.8))
    return a


def s05():  # one fact, two pictures
    fig, ax = canvas()
    bars(fig, ax, 1.6, 1.75, 4.6, 3.3, 0, 26, [0, 5, 10, 15, 20, 25], "Version A: y-axis starts at 0",
         "bars look almost equal (honest)", GREEN)
    text(ax, 1.4, 1.2, "starts at 0", fs=15, color=RED, bold=True)
    bars(fig, ax, 10.6, 1.75, 4.6, 3.3, 22, 23.45, [22, 22.4, 22.8, 23.2], "Version B: y-axis starts at 22",
         "Delhi's bar looks twice as tall (misleading)", RED)
    text(ax, 10.4, 1.2, "starts at 22", fs=15, color=RED, bold=True)
    # middle: what the numbers really say
    box(ax, 8.2, 3.4, 2.6, 1.6, "same data:\nDelhi is only\n₹0.6 L ahead\n(about 3%)", color=BLUE, fs=16)
    pill(ax, 8, 0.55, "Rule 1: bars start at 0", fs=19)
    save(fig, OUT.format(5))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s05()
