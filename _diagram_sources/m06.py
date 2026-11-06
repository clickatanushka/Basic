from style import *

OUT = "out/m06_s{:02d}.png"


def s03():  # anatomy of a DataFrame
    fig, ax = canvas()
    cols = ["order_id", "city", "quantity", "unit_price"]
    rows = [("O10001", "Delhi", 6, 362), ("O10002", "Chennai", 2, 300),
            ("O10003", "DELHI", 1, 2258), ("O10004", "Lucknow", 2, 2020)]
    cw = [2.3, 2.3, 2.3, 2.3]
    x0, y0, rh = 4.2, 4.75, 0.62
    table(ax, x0, y0, cols, rows, cw, rh=rh, color=BLUE, fs=18)
    # index
    for i in range(4):
        text(ax, x0 - 0.45, y0 - rh * (i + 1.5), str(i), fs=19, bold=True, color=TEAL)
    ax.add_patch(FancyBboxPatch((x0 - 0.75, y0 - rh * 5 - 0.05), 0.6, rh * 4 + 0.1,
                                boxstyle="round,pad=0,rounding_size=0.1", fc="none", ec=TEAL, lw=2, ls="--"))
    text(ax, 2.1, y0 - rh * 3, "index\n0, 1, 2, 3", fs=18, color=TEAL, bold=True)
    arrow(ax, 2.95, y0 - rh * 3, x0 - 0.85, y0 - rh * 3, color=TEAL)
    # circle a column -> Series
    cx = x0 + cw[0] + cw[1] / 2
    ax.add_patch(Ellipse((cx, y0 - rh * 2.5), cw[1] + 0.35, rh * 5 + 0.55, fc="none", ec=CORAL, lw=3))
    text(ax, 14.2, 1.25, "one column = a Series", fs=19, color=CORAL, bold=True)
    text(ax, 14.2, 0.75, "df[\"city\"]", fs=17, color=MUTED)
    arrow(ax, 12.65, 1.25, cx + 0.55, 1.4, color=CORAL, rad=-0.15)
    # shape label on top
    tw = sum(cw)
    ax.plot([x0, x0 + tw], [5.3, 5.3], color=PURPLE, lw=2)
    for xx in (x0, x0 + tw):
        ax.plot([xx, xx], [5.18, 5.42], color=PURPLE, lw=2)
    text(ax, x0 + tw / 2, 5.75, "df.shape = (rows, columns) = (4, 4)", fs=20, bold=True, color=PURPLE)
    text(ax, x0 + tw + 0.15, y0 - rh / 2, "← column names", fs=16, color=MUTED, ha="left")
    pill(ax, 7, 0.55, "DataFrame = index + named columns.  Each column is a Series.", color=CORAL)
    save(fig, OUT.format(3))


def s20():  # pd.cut on a number line
    fig, ax = canvas()
    X = lambda v: 1.0 + (v - 17) * (14.0 / 43)
    yl = 3.0
    ax.plot([X(17), X(60)], [yl, yl], color=INK, lw=2.5)
    for v in range(17, 61):
        big = v in (17, 20, 30, 40, 50, 60) or v % 5 == 0
        ax.plot([X(v), X(v)], [yl - (0.12 if big else 0.06), yl + (0.12 if big else 0.06)], color=INK, lw=1.2)
    for v in (17, 20, 30, 40, 50, 60):
        text(ax, X(v), yl - 0.42, str(v), fs=17)
    # bins
    bins = [17, 25, 35, 45, 60]
    labels = ["18-25", "26-35", "36-45", "46-60"]
    colors = [TEAL, ORANGE, BLUE, PURPLE]
    for a, b, lab, c in zip(bins[:-1], bins[1:], labels, colors):
        ax.add_patch(Rectangle((X(a), yl + 0.35), X(b) - X(a), 0.75, fc=TINT[c], ec=c, lw=2))
        text(ax, (X(a) + X(b)) / 2, yl + 0.72, lab, fs=20, bold=True, color=c)
        # open left, closed right
        ax.add_patch(Circle((X(a) + 0.0, yl), 0.1, fc="white", ec=c, lw=2, zorder=5))
    for v in (25, 35, 45, 60):
        ax.add_patch(Circle((X(v), yl), 0.1, fc=INK, ec=INK, zorder=6))
    for v in (25, 35, 45):
        ax.plot([X(v), X(v)], [yl - 0.25, yl + 1.25], color=RED, lw=3)
        text(ax, X(v), yl + 1.5, f"cut {v}", fs=17, bold=True, color=RED)
    # 25 callout
    text(ax, X(25) - 0.2, 1.55, "age 25 → \"18-25\"  (right edge included)", fs=18, color=TEAL, bold=True, ha="left")
    arrow(ax, X(25) - 0.05, 1.8, X(25) - 0.05, yl - 0.7, color=TEAL)
    text(ax, 13.0, 1.55, "●  included    ○  excluded", fs=17, color=MUTED)
    text(ax, 8, 5.45, "pd.cut(age, bins=[17, 25, 35, 45, 60], labels=[\"18-25\", \"26-35\", \"36-45\", \"46-60\"])",
         fs=17, color=INK, family="DejaVu Sans Mono")
    pill(ax, 8, 0.6, "Bins are (left, right]:  25 goes to 18-25,  26 starts 26-35")
    save(fig, OUT.format(20))


def s23():  # split -> apply -> combine
    fig, ax = canvas()
    C = {"Delhi": TEAL, "Chennai": ORANGE, "Lucknow": BLUE, "Pune": PURPLE}
    rows = [("Delhi", "1737.6"), ("Chennai", "570"), ("Delhi", "2145.1"), ("Lucknow", "3434"),
            ("Chennai", "3486.6"), ("Delhi", "2736"), ("Pune", "14098.95"), ("Pune", "2079")]
    hl = {(i, None): TINT[C[r[0]]] for i, r in enumerate(rows)}
    rh = 0.56
    table(ax, 0.3, 5.75, ["city", "revenue"], rows, [1.8, 1.8], rh=rh, color=BLUE, fs=17, highlight=hl)
    piles = [("Delhi", "1737.6 + 2145.1 + 2736", "6618.7"),
             ("Chennai", "570 + 3486.6", "4056.6"),
             ("Lucknow", "3434", "3434"),
             ("Pune", "14098.95 + 2079", "16177.95")]
    ys = [4.95, 3.75, 2.55, 1.35]
    for (city, vals, tot), y in zip(piles, ys):
        c = C[city]
        box(ax, 6.55, y, 3.9, 1.0, color=c)
        text(ax, 6.55, y + 0.23, city, fs=18, bold=True, color=c)
        text(ax, 6.55, y - 0.22, vals, fs=16)
        arrow(ax, 8.55, y, 9.1, y, color=c)
        box(ax, 10.3, y, 2.2, 0.8, f"sum = {tot}", color=c, fs=16, bold=True)
    # split arrow
    arrow(ax, 3.95, 3.15, 4.5, 3.15, lw=2.5)
    text(ax, 6.55, 5.95, "1. SPLIT: one pile per city", fs=18, bold=True, color=MUTED)
    text(ax, 10.3, 5.95, "2. APPLY: sum", fs=18, bold=True, color=MUTED)
    text(ax, 14.05, 5.95, "3. COMBINE", fs=18, bold=True, color=MUTED)
    # combine table
    ct = [("Chennai", "4056.6"), ("Delhi", "6618.7"), ("Lucknow", "3434"), ("Pune", "16177.95")]
    table(ax, 12.35, 4.6, ["city", "revenue"], ct, [1.65, 1.75], rh=0.55, color=BLUE, fs=17,
          highlight={(i, None): TINT[C[r[0]]] for i, r in enumerate(ct)})
    for y in ys:
        arrow(ax, 11.45, y, 12.3, 3.2 + (y - 3.15) * 0.3, color=LINE, lw=2)
    text(ax, 14.05, 1.35, "= SUMIFS for every city\n= GROUP BY in SQL", fs=16, color=MUTED, bold=True)
    pill(ax, 8, 0.4, "df.groupby(\"city\")[\"revenue\"].sum()   8 rows → 4 rows", color=CORAL)
    save(fig, OUT.format(23))


def s28():  # two LEFT joins
    fig, ax = canvas()
    def tbox(x, y, w, h, name, sub, cols, c):
        ax.add_patch(Rectangle((x - w / 2, y + h / 2 - 0.6), w, 0.6, fc=c, ec=c))
        text(ax, x, y + h / 2 - 0.3, name, fs=20, bold=True, color="white")
        ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h - 0.6, fc=TINT[c], ec=c, lw=2))
        text(ax, x, y + h / 2 - 0.95, sub, fs=18, bold=True, color=c)
        text(ax, x, y - 0.35, cols, fs=16, color=INK)
    tbox(2.4, 3.9, 3.6, 3.1, "customers", "800 rows", "customer_id\ngender, age\ncity, membership", TEAL)
    tbox(8.0, 3.9, 3.6, 3.1, "orders", "5,000 rows", "order_id\ncustomer_id\nproduct_id\nquantity, unit_price", ORANGE)
    tbox(13.6, 3.9, 3.6, 3.1, "products", "60 rows", "product_id\nproduct_name\ncategory\ncost_price", PURPLE)
    arrow(ax, 6.2, 3.9, 4.25, 3.9, lw=2.5)
    text(ax, 5.22, 4.25, "on customer_id", fs=16, bold=True, color=TEAL)
    text(ax, 5.22, 3.55, "how=\"left\"", fs=16, color=MUTED)
    arrow(ax, 9.8, 3.9, 11.75, 3.9, lw=2.5)
    text(ax, 10.78, 4.25, "on product_id", fs=16, bold=True, color=PURPLE)
    text(ax, 10.78, 3.55, "how=\"left\"", fs=16, color=MUTED)
    text(ax, 8, 1.75, "LEFT join: keep every order", fs=20, bold=True, color=ORANGE)
    text(ax, 8, 1.3, "and attach customer / product details where they match", fs=16, color=MUTED)
    pill(ax, 8, 0.7, "rows before = rows after = 5,000", fs=22)
    save(fig, OUT.format(28))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s03(); s20(); s23(); s28()
