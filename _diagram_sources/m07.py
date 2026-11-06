import numpy as np
from style import *

OUT = "out/m07_s{:02d}.png"
MONO = "DejaVu Sans Mono"


def stick(ax, x, y, color=INK):
    """Stick figure with feet at y (about 1.0 tall)."""
    ax.add_patch(Circle((x, y + 0.85), 0.15, fc="white", ec=color, lw=2.2))
    ax.plot([x, x], [y + 0.7, y + 0.3], color=color, lw=2.2)
    ax.plot([x - 0.25, x, x + 0.25], [y + 0.45, y + 0.6, y + 0.45], color=color, lw=2.2)
    ax.plot([x - 0.2, x, x + 0.2], [y, y + 0.3, y], color=color, lw=2.2)


def cylinder(ax, x, y, w, h, color, label):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=TINT[color], ec="none"))
    ax.add_patch(Ellipse((x, y - h / 2), w, 0.45, fc=TINT[color], ec=color, lw=2))
    ax.add_patch(Rectangle((x - w / 2 + 0.02, y - h / 2), w - 0.04, 0.05, fc=TINT[color], ec="none"))
    ax.plot([x - w / 2, x - w / 2], [y - h / 2, y + h / 2], color=color, lw=2)
    ax.plot([x + w / 2, x + w / 2], [y - h / 2, y + h / 2], color=color, lw=2)
    ax.add_patch(Ellipse((x, y + h / 2), w, 0.45, fc=TINT[color], ec=color, lw=2))
    text(ax, x, y - 0.1, label, fs=19, bold=True, color=color)


def s04():  # pipeline source -> user
    fig, ax = canvas()
    ym = 3.7
    srcs = ["ShopKart app", "Payments", "CRM"]
    for s, y in zip(srcs, [5.0, 3.7, 2.4]):
        box(ax, 1.65, y, 2.5, 0.85, s, color=BLUE, fs=18)
        arrow(ax, 2.95, y, 3.95, ym + (y - ym) * 0.35, color=LINE)
    text(ax, 1.65, 1.55, "source systems", fs=17, color=MUTED, bold=True)
    steps = [("Extract", 4.85, TEAL), ("Transform", 7.35, ORANGE), ("Load", 9.85, PURPLE)]
    for name, x, c in steps:
        ax.add_patch(Circle((x, ym), 0.88, fc=TINT[c], ec=c, lw=2.5))
        text(ax, x, ym, name, fs=18, bold=True, color=c)
    arrow(ax, 5.75, ym, 6.45, ym, lw=2.5)
    arrow(ax, 8.25, ym, 8.95, ym, lw=2.5)
    arrow(ax, 10.75, ym, 11.4, ym, lw=2.5)
    text(ax, 7.35, 2.45, "clean, merge,\nadd revenue", fs=17, color=ORANGE, bold=True)
    cylinder(ax, 12.45, ym, 1.9, 1.9, BLUE, "warehouse")
    people = [("analyst", 5.0), ("scientist", 3.55), ("manager", 2.1)]
    for name, y in people:
        stick(ax, 14.2, y - 0.5)
        text(ax, 14.55, y - 0.05, name, fs=16, ha="left")
        arrow(ax, 13.45, ym + (y - ym) * 0.3, 13.85, y - 0.05 + (ym - y) * 0.05, color=LINE)
    # bracket under the whole line
    ax.plot([0.4, 0.4, 15.6, 15.6], [1.35, 1.2, 1.2, 1.35], color=LINE, lw=1.8)
    pill(ax, 8, 0.6, "runs every night at 2 am", color=CORAL)
    save(fig, OUT.format(4))


def s19():  # star schema
    fig, ax = canvas()

    def ent(x, top, w, name, cols, color, keys=(), rh=0.4):
        ax.add_patch(Rectangle((x - w / 2, top - 0.55), w, 0.55, fc=color, ec=color))
        text(ax, x, top - 0.27, name, fs=19, bold=True, color="white")
        ax.add_patch(Rectangle((x - w / 2, top - 0.55 - rh * len(cols) - 0.1), w, rh * len(cols) + 0.1,
                               fc=TINT[color], ec=color, lw=2))
        ys = {}
        for i, c in enumerate(cols):
            y = top - 0.55 - 0.05 - rh * (i + 0.5)
            text(ax, x - w / 2 + 0.2, y, c, fs=17, ha="left", bold=c in keys,
                 color=INK)
            ys[c] = y
        return ys

    # dim_date: one-line body
    ax.add_patch(Rectangle((4.6, 5.55), 6.8, 0.5, fc=BLUE, ec=BLUE))
    text(ax, 8, 5.8, "dim_date", fs=19, bold=True, color="white")
    ax.add_patch(Rectangle((4.6, 5.05), 6.8, 0.5, fc=TINT[BLUE], ec=BLUE, lw=2))
    text(ax, 5.1, 5.3, "date_key", fs=17, bold=True, ha="left")
    text(ax, 6.55, 5.3, "  month   ·   quarter   ·   weekday", fs=17, ha="left")

    f = ent(8, 4.75, 3.4, "fact_orders",
            ["order_id", "date_key", "customer_id", "product_id", "quantity", "revenue", "profit"], ORANGE,
            keys=("date_key", "customer_id", "product_id"))
    text(ax, 9.55, f["quantity"] - 0.4, "numbers", fs=15, color=ORANGE, bold=True, ha="right")
    c = ent(2.4, 4.3, 3.4, "dim_customer", ["customer_id", "gender", "age", "membership"], TEAL,
            keys=("customer_id",), rh=0.45)
    p = ent(13.6, 4.0, 3.4, "dim_product", ["product_id", "product_name", "category"], PURPLE,
            keys=("product_id",), rh=0.45)
    # lines (the star)
    ax.plot([9.7, 10.4, 10.4], [f["date_key"], f["date_key"], 5.05], color=BLUE, lw=2.8)
    ax.plot([6.3, 5.2, 5.2, 4.1], [f["customer_id"], f["customer_id"], c["customer_id"], c["customer_id"]],
            color=TEAL, lw=2.8)
    ax.plot([9.7, 10.9, 10.9, 11.9], [f["product_id"], f["product_id"], p["product_id"], p["product_id"]],
            color=PURPLE, lw=2.8)
    for (x, y, col) in [(10.4, 5.05, BLUE), (4.1, c["customer_id"], TEAL), (11.9, p["product_id"], PURPLE)]:
        ax.add_patch(Circle((x, y), 0.07, fc=col, ec=col, zorder=5))
    # trace one question with a coloured pen
    def ring(x, y, w):
        ax.add_patch(FancyBboxPatch((x - 0.08, y - 0.19), w, 0.38, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc="none", ec=CORAL, lw=2.6, zorder=6))
    ring(6.42, f["revenue"], 1.15)
    ring(6.42, f["product_id"], 1.4)
    ring(6.42, f["date_key"], 1.15)
    ring(11.92, p["category"], 1.25)
    ring(6.62, 5.3, 0.95)
    arrow(ax, 6.34, f["revenue"], 6.34, f["product_id"] - 0.05, color=CORAL, lw=2.4, rad=-0.6, ls="--")
    arrow(ax, 7.85, f["product_id"] - 0.12, 11.85, p["category"], color=CORAL, lw=2.4, rad=0.12, ls="--")
    arrow(ax, 6.34, f["date_key"], 6.95, 5.08, color=CORAL, lw=2.4, rad=-0.45, ls="--")
    text(ax, 0.4, 5.85, "Question: revenue by", fs=18, color=CORAL, bold=True, ha="left")
    text(ax, 0.4, 5.4, "category and month", fs=18, color=CORAL, bold=True, ha="left")
    text(ax, 13.7, 5.15, "revenue ← fact\ncategory ← dim_product\nmonth ← dim_date\n→ group by, sum",
         fs=16, color=CORAL, bold=True)
    pill(ax, 8, 0.6, "fact = numbers,  dims = descriptions")
    save(fig, OUT.format(19))


def s20():  # scheduling
    fig, ax = canvas()
    cx, cy, r = 2.6, 4.25, 1.3
    ax.add_patch(Circle((cx, cy), r, fc=TINT[BLUE], ec=INK, lw=3))
    for k in range(12):
        a = np.pi / 2 - k * np.pi / 6
        r1 = r - (0.22 if k % 3 == 0 else 0.13)
        ax.plot([cx + r1 * np.cos(a), cx + (r - 0.04) * np.cos(a)],
                [cy + r1 * np.sin(a), cy + (r - 0.04) * np.sin(a)], color=INK, lw=2.5 if k % 3 == 0 else 1.5)
    for k, lab in [(3, "3"), (6, "6"), (9, "9")]:
        a = np.pi / 2 - k * np.pi / 6
        text(ax, cx + (r - 0.45) * np.cos(a), cy + (r - 0.45) * np.sin(a), lab, fs=15, color=MUTED, bold=True)
    a = np.pi / 2 - 2 * np.pi / 6   # hour hand at 2
    ax.plot([cx, cx + 0.62 * np.cos(a)], [cy, cy + 0.62 * np.sin(a)], color=INK, lw=5, solid_capstyle="round")
    ax.plot([cx, cx], [cy, cy + 0.95], color=INK, lw=3, solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), 0.08, fc=INK))
    text(ax, cx, cy - 0.55, "2:00 am", fs=15, color=CORAL, bold=True)
    # cron line
    fields = ["0", "2", "*", "*", "*"]
    labels = ["minute", "hour", "day", "month", "weekday"]
    xs = [cx - 2.0 + i * 1.0 for i in range(5)]
    for fld, lab, x in zip(fields, labels, xs):
        box(ax, x, 2.15, 0.7, 0.7, fld, color=BLUE, fs=24, bold=True)
        text(ax, x, 1.7, lab, fs=15, color=MUTED, va="top")
    text(ax, cx, 1.0, "0 2 * * *  = every night at 2 am", fs=16, color=INK, bold=True)
    text(ax, cx, 0.55, "Mondays at 6 am:  0 6 * * 1", fs=15, color=MUTED)
    # DAG
    ax.add_patch(FancyBboxPatch((5.35, 3.3), 10.3, 2.05, boxstyle="round,pad=0,rounding_size=0.15",
                                fc="none", ec=LINE, lw=1.8, ls="--"))
    text(ax, 10.5, 5.75, "DAG = tasks + arrows", fs=20, bold=True, color=PURPLE)
    arrow(ax, cx + r + 0.1, cy, 5.75, 4.3, lw=2.5, color=CORAL)
    text(ax, 4.6, 4.6, "triggers", fs=15, color=CORAL, bold=True)
    names = ["extract", "transform", "checks", "load"]
    bx = [7.0, 9.5, 12.0, 14.4]
    for n, x in zip(names, bx):
        box(ax, x, 4.3, 2.0, 0.95, n, color=TEAL if n != "checks" else ORANGE, fs=18, bold=True)
    for a1, a2 in zip(bx[:-1], bx[1:]):
        arrow(ax, a1 + 1.0, 4.3, a2 - 1.0, 4.3, lw=2.2)
    # red cross on checks
    bx_, by_ = 12.95, 4.75
    ax.add_patch(Circle((bx_, by_), 0.3, fc=RED, ec="white", lw=2, zorder=6))
    for s in (1, -1):
        ax.plot([bx_ - 0.14, bx_ + 0.14], [by_ - 0.14 * s, by_ + 0.14 * s], color="white", lw=3.5, zorder=7)
    text(ax, 12.15, 2.95, "checks fail", fs=16, color=RED, bold=True, ha="left")
    arrow(ax, 12.0, 3.8, 12.0, 2.45, color=RED, lw=2.5)
    box(ax, 12.0, 1.95, 3.6, 0.9, "email the engineer", color=CORAL, fs=18, bold=True)
    text(ax, 12.0, 0.95, "cron won't tell anyone. Airflow retries, shows every run, alerts someone.", fs=16, color=MUTED)
    save(fig, OUT.format(20))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s04(); s19(); s20()
