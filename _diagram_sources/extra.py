"""Two board segments with no 'draw live' slide: M03 slide 13 (SD in four steps) and M07 slide 6 (ETL vs ELT)."""
from style import *


def m03_s13():  # SD of City Y in four steps
    fig, ax = canvas()
    text(ax, 8, 6.0, "City Y delivery days:  1,  2,  4,  6,  7", fs=20, bold=True)
    steps = [("1", "Mean", "Find the average", "(1+2+4+6+7) ÷ 5\n= 20 ÷ 5\n= 4", TEAL),
             ("2", "Gaps", "Each value minus the mean", "1−4, 2−4, 4−4,\n6−4, 7−4\n→ −3, −2, 0, 2, 3", ORANGE),
             ("3", "Square", "Square gaps, add, ÷ (n − 1)", "9, 4, 0, 4, 9\ntotal 26\n26 ÷ 4 = 6.5", CORAL),
             ("4", "Root", "Square root = SD", "√6.5\n= 2.55 days", BLUE)]
    for i, (n, name, sub, calc, col) in enumerate(steps):
        x = 2.05 + i * 3.95
        box(ax, x, 3.2, 3.5, 4.0, color=col)
        ax.add_patch(Circle((x - 1.25, 4.75), 0.3, fc=col, ec="none"))
        text(ax, x - 1.25, 4.75, n, fs=18, bold=True, color="white")
        text(ax, x - 0.8, 4.75, name, fs=21, bold=True, ha="left")
        text(ax, x, 4.15, sub, fs=15, color=MUTED)
        text(ax, x, 2.75, calc, fs=19)
        if i < 3:
            arrow(ax, x + 1.8, 3.2, x + 2.15, 3.2, color=LINE, lw=2.5)
    text(ax, 9.95, 1.6, "= variance", fs=15, color=CORAL, bold=True)
    pill(ax, 8, 0.55, "Step 3 result (6.5) is the variance.  Sheets does all four steps with =STDEV(range).", color=INK)
    save(fig, "out/m03_s13.png")


def m07_s06():  # ETL vs ELT as two pipelines
    fig, ax = canvas()
    def cyl(x, y, w, col=BLUE):
        ax.add_patch(Ellipse((x + w / 2, y - 0.6), w, 0.4, fc=TINT[col], ec=col, lw=2, zorder=1))
        ax.add_patch(Rectangle((x, y - 0.6), w, 1.15, fc=TINT[col], ec="none", zorder=2))
        ax.plot([x, x], [y - 0.6, y + 0.55], color=col, lw=2, zorder=3)
        ax.plot([x + w, x + w], [y - 0.6, y + 0.55], color=col, lw=2, zorder=3)
        ax.add_patch(Ellipse((x + w / 2, y + 0.55), w, 0.4, fc=TINT[col], ec=col, lw=2, zorder=3))
        text(ax, x + w / 2, y + 0.12, "warehouse", fs=16, bold=True, zorder=4)
    def lane(y, label, sub, order, col, notes):
        text(ax, 0.35, y + 0.25, label, fs=26, bold=True, color=col, ha="left")
        text(ax, 0.35, y - 0.3, sub, fs=15, color=MUTED, ha="left")
        box(ax, 2.95, y, 2.0, 1.0, "sources\napp\npayments · CRM", color=LINE, fill="white", fs=14)
        x = 3.95
        prev = None
        for step in order:
            if step == "dotL":   # dotted arrow from E straight into the warehouse
                arrow(ax, x + 0.05, y, x + 1.95, y, color=col, lw=3, ls=(0, (2, 2)))
                text(ax, x + 1.0, y + 0.35, "L: load raw", fs=15, bold=True, color=col)
                x += 2.0; prev = step
                continue
            if prev != "dotL":
                arrow(ax, x + 0.05, y, x + 0.45, y, color=LINE, lw=2.5); x += 0.5
            prev = step
            if step == "W":
                cyl(x, y, 2.3); x += 2.3
            else:
                ax.add_patch(Circle((x + 0.5, y), 0.5, fc=col, ec="none"))
                text(ax, x + 0.5, y, step, fs=24, bold=True, color="white"); x += 1.0
        text(ax, 11.55, y, notes, fs=16, ha="left")
        return x
    lane(4.65, "ETL", "transform first", ["E", "T", "L", "W"], TEAL,
         "• Clean first, then load\n• ShopKart in this module:\n   pandas cleans, then we load")
    lane(1.95, "ELT", "load first", ["E", "dotL", "W"], ORANGE,
         "• Raw data lands in the warehouse first\n• Cleaning happens inside it, with SQL\n• Common with cloud warehouses:\n   cheap storage, very fast SQL")
    ax.add_patch(Circle((8.05, 1.68), 0.27, fc=ORANGE, ec="none", zorder=5))
    text(ax, 8.05, 1.68, "T", fs=16, bold=True, color="white", zorder=6)
    text(ax, 8.42, 1.68, "with SQL", fs=15, color=ORANGE, bold=True, ha="left", zorder=6)
    ax.plot([0.35, 15.65], [3.3, 3.3], color=LINE, lw=1, ls=":")
    pill(ax, 8, 0.45, "Same three letters, different order. Neither is wrong.", color=INK)
    save(fig, "out/m07_s06.png")


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    m03_s13(); m07_s06()
