from style import *
plt.rcParams["font.family"] = ["Liberation Sans", "DejaVu Sans"]   # fallback only for glyphs like ₹ and ★

OUT = "out/m04_s{:02d}.png"


def cross(ax, x, y, s=0.16, color=RED, lw=3):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=lw, solid_capstyle="round")
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=lw, solid_capstyle="round")


def s05():  # ShopKart schema
    fig, ax = canvas()
    RH, top, HH = 0.4, 6.3, 0.5

    def ent(x, name, cols, color):
        ax.add_patch(Rectangle((x - 1.75, top - HH), 3.5, HH, fc=color, ec=color))
        text(ax, x, top - HH / 2, name, fs=19, bold=True, color="white")
        bh = RH * len(cols) + 0.1
        ax.add_patch(Rectangle((x - 1.75, top - HH - bh), 3.5, bh, fc=TINT[color], ec=color, lw=2))
        ys = {}
        for i, (c, tag) in enumerate(cols):
            y = top - HH - 0.25 - RH * i
            t = text(ax, x - 1.55, y, c, fs=15, ha="left", bold=tag == "PK")
            if tag == "PK":
                ax.plot([x - 1.55, x - 1.55 + 0.118 * len(c)], [y - 0.15, y - 0.15], color=INK, lw=1.5)
            if tag:
                text(ax, x + 1.55, y, tag, fs=14, ha="right", bold=True, color=color)
            ys[c] = y
        return ys, top - HH - bh

    c, cb = ent(2.4, "customers", [("customer_id", "PK"), ("name", ""), ("gender", ""), ("age", ""), ("city", ""),
                                   ("signup_date", ""), ("membership", "")], TEAL)
    o, _ = ent(8, "orders", [("order_id", "PK"), ("order_date", ""), ("customer_id", "FK"), ("product_id", "FK"),
                             ("quantity", ""), ("unit_price", ""), ("discount", ""), ("city", ""),
                             ("payment_mode", ""), ("delivery_days", ""), ("rating", ""), ("returned", "")], ORANGE)
    p, pb = ent(13.6, "products", [("product_id", "PK"), ("product_name", ""), ("category", ""), ("list_price", ""),
                                   ("cost_price", "")], PURPLE)
    arrow(ax, 6.25, o["customer_id"], 4.15, c["customer_id"], lw=2.5)
    text(ax, 6.15, o["customer_id"] - 0.12, "many", fs=16, color=CORAL, bold=True, va="top", ha="right")
    text(ax, 4.45, c["customer_id"] + 0.28, "1", fs=18, color=CORAL, bold=True)
    arrow(ax, 9.75, o["product_id"], 11.85, p["product_id"], lw=2.5)
    text(ax, 9.85, o["product_id"] - 0.12, "many", fs=16, color=CORAL, bold=True, va="top", ha="left")
    text(ax, 11.55, p["product_id"] + 0.28, "1", fs=18, color=CORAL, bold=True)
    text(ax, 2.4, cb - 0.65, "PK = primary key\n(underlined, never repeats)", fs=16, color=MUTED)
    text(ax, 13.6, pb - 0.65, "FK = foreign key\n(points to another table's PK)", fs=16, color=MUTED)
    text(ax, 2.4, 1.05, "Each fact stored once:\nno name typed 20 times", fs=16, bold=True, color=TEAL)
    pill(ax, 13.6, 1.4, "One customer → many orders", fs=16)
    pill(ax, 13.6, 0.65, "One product → many orders", fs=16)
    save(fig, OUT.format(5))


def s20():  # GROUP BY makes buckets
    fig, ax = canvas()
    col = {"Delhi": TEAL, "Chennai": ORANGE, "Pune": PURPLE}
    rows = [("O10001", "Delhi", 1737.60), ("O10002", "Chennai", 570.00), ("O10003", "Delhi", 2145.10),
            ("O10005", "Chennai", 3486.60), ("O10006", "Delhi", 2736.00), ("O10008", "Pune", 14098.95)]
    rh, ty = 0.55, 5.6
    text(ax, 2.5, 5.9, "6 order rows", fs=18, bold=True, color=MUTED)
    hl = {(i, None): TINT[col[c]] for i, (_, c, _) in enumerate(rows)}
    table(ax, 0.3, ty, ["order_id", "city", "revenue"], [(o, c, f"{v:,.2f}") for o, c, v in rows],
          [1.35, 1.35, 1.7], rh=rh, fs=16, color=BLUE, highlight=hl)
    text(ax, 9.2, 5.9, "GROUP BY city: drop each row into its city's bucket", fs=16, bold=True, color=MUTED)
    tray = {"Delhi": 4.95, "Chennai": 3.6, "Pune": 2.25}
    x0, x1, th = 6.3, 12.2, 1.05
    for city, yc in tray.items():
        c = col[city]
        ax.add_patch(Rectangle((x0, yc - th / 2), x1 - x0, th, fc=TINT[c], ec="none"))
        ax.plot([x0, x1, x1, x0], [yc + th / 2, yc + th / 2, yc - th / 2, yc - th / 2], color=c, lw=3)
        text(ax, 7.15, yc, city, fs=19, bold=True, color=c)
        vals = [(o, v) for o, cc, v in rows if cc == city]
        for i, (o, v) in enumerate(vals):
            box(ax, 8.65 + 1.17 * i, yc, 1.1, 0.5, o, color=c, fill="white", fs=14)
        text(ax, 12.45, yc + 0.22, f"COUNT = {len(vals)}", fs=17, bold=True, ha="left")
        text(ax, 12.45, yc - 0.22, f"SUM = ₹{sum(v for _, v in vals):,.2f}", fs=17, bold=True, ha="left")
    seen = {}
    for i, (o, city, _) in enumerate(rows):
        y = ty - rh * (i + 1.5)
        k = seen.get(city, 0); seen[city] = k + 1
        n = sum(1 for r in rows if r[1] == city)
        ey = tray[city] + (0.3 - 0.3 * k if n == 3 else (0.15 - 0.3 * k if n == 2 else 0))
        arrow(ax, 4.75, y, x0 + 0.15, ey, color=col[city], lw=2.2, ms=14)
        ax.add_patch(Circle((4.75, y), 0.06, fc=col[city], ec="none"))
    box(ax, 8.0, 3.675, 15.8, 5.15, color=CORAL, fill="none", lw=2.5, ls="--", r=0.3)
    text(ax, 13.9, 1.1, "6 rows in → 3 rows out", fs=18, bold=True, color=CORAL,
         bbox=dict(fc="white", ec="none", pad=4))
    pill(ax, 7.0, 0.45, "SELECT only the bucket label or an aggregate, not order_id (Delhi's bucket has three)", fs=16)
    save(fig, OUT.format(20))


def s22():  # logical order of SQL (Q11)
    fig, ax = canvas()
    lines = [("SELECT", "city, COUNT(*) AS returns", 5), ("FROM", "orders", 1), ("WHERE", "returned = 'Y'", 2),
             ("GROUP BY", "city", 3), ("HAVING", "COUNT(*) >= 60", 4), ("ORDER BY", "returns DESC;", 6)]
    colors = {1: BLUE, 2: TEAL, 3: ORANGE, 4: PURPLE, 5: CORAL, 6: GREEN}
    text(ax, 3.1, 6.1, "Order we TYPE (Q11)", fs=17, bold=True, color=MUTED)
    text(ax, 6.5, 6.1, "Runs", fs=17, bold=True, color=MUTED)
    box(ax, 3.05, 3.95, 5.7, 3.6, color=LINE, fill="white", lw=1.5)
    for i, (kw, rest, n) in enumerate(lines):
        y = 5.45 - 0.6 * i
        text(ax, 0.45, y, kw, fs=17, bold=True, color=colors[n], ha="left")
        text(ax, 2.05, y, rest, fs=17, ha="left")
        ax.add_patch(Circle((6.5, y), 0.25, fc=colors[n], ec="none"))
        text(ax, 6.5, y, str(n), fs=16, bold=True, color="white")
        if n in (2, 5):
            text(ax, 7.0, y, "★", fs=22, color=CORAL)
    text(ax, 11.9, 6.1, "Run order for Q11", fs=17, bold=True, color=MUTED)
    base = 2.45
    xs = [8.25 + 1.4 * k for k in range(6)]
    # 1 FROM: tall table
    def tall(x, h, c, w=0.9):
        ax.add_patch(Rectangle((x - w / 2, base), w, h, fc=TINT[c], ec=c, lw=1.5))
        for r in range(1, int(h / 0.22)):
            ax.plot([x - w / 2, x + w / 2], [base + 0.22 * r] * 2, color=c, lw=0.7)
        ax.add_patch(Rectangle((x - w / 2, base + h - 0.22), w, 0.22, fc=c, ec=c))
    tall(xs[0], 3.0, BLUE)
    text(ax, xs[0], base + 3.3, "5,000 rows", fs=14)
    tall(xs[1], 1.6, TEAL)
    text(ax, xs[1], base + 1.95, "687 returned\nrows", fs=14)
    # 3 GROUP BY / 4 HAVING: 10 city buckets (real return counts, sorted)
    counts = [146, 89, 82, 69, 63, 59, 56, 44, 43, 36]
    for k, c in ((2, ORANGE), (3, PURPLE)):
        for j, n in enumerate(counts):
            bxx = xs[k] - 0.3 + 0.6 * (j % 2)
            byy = base + 0.45 + 0.5 * (4 - j // 2)
            dead = k == 3 and n < 60
            box(ax, bxx, byy, 0.52, 0.4, str(n), color=LINE if dead else c, fill="white", fs=14,
                tc=MUTED if dead else INK, lw=1.5, r=0.06)
            if dead:
                cross(ax, bxx, byy, s=0.17, lw=2.5)
    text(ax, xs[2], base + 3.1, "10 city\nbuckets", fs=14)
    text(ax, xs[3], base + 3.1, "5 cities\nleft", fs=14)
    # 5 SELECT / 6 ORDER BY: small 2-column result
    for k, c in ((4, CORAL), (5, GREEN)):
        tall(xs[k], 1.1, c, w=0.8)
        ax.plot([xs[k]] * 2, [base, base + 1.1], color=c, lw=1.2)
    text(ax, xs[4], base + 1.45, "city,\nreturns", fs=14)
    text(ax, xs[5], base + 1.45, "sorted by\nreturns", fs=14)
    for k, kw in enumerate(["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY"]):
        n, c = k + 1, colors[k + 1]
        ax.add_patch(Circle((xs[k], base - 0.3), 0.2, fc=c, ec="none"))
        text(ax, xs[k], base - 0.3, str(n), fs=15, bold=True, color="white")
        text(ax, xs[k], base - 0.7, kw, fs=15, bold=True, color=c)
        if k < 5:
            arrow(ax, xs[k] + 0.5, base + 0.12, xs[k] + 0.9, base + 0.12, lw=2.5, ms=16)
    text(ax, 8, 1.15, "★  COUNT can't go in WHERE: at step 2 the groups don't exist yet",
         fs=18, bold=True, color=CORAL)
    pill(ax, 8, 0.42, "★  An alias made in SELECT (step 5) can't be used in WHERE (step 2), but can in ORDER BY (step 6)",
         fs=16)
    save(fig, OUT.format(22))


def s28():  # how JOIN matches rows
    fig, ax = canvas()
    rh = 0.42
    orders = [("O10002", "P049", 2), ("O10003", "P020", 1), ("O10004", "P026", 2), ("O10005", "P026", 2)]
    prods = [("P020", "Saree", "Fashion"), ("P026", "Pressure Cooker", "Home"), ("P049", "Face Wash", "Beauty")]
    text(ax, 2.6, 6.08, "orders", fs=18, bold=True, color=ORANGE)
    table(ax, 0.4, 5.85, ["order_id", "product_id", "quantity"], orders, [1.5, 1.6, 1.3], rh=rh, fs=16,
          color=ORANGE, highlight={(2, 1): TINT[CORAL], (3, 1): TINT[CORAL]})
    text(ax, 12.25, 6.08, "products", fs=18, bold=True, color=PURPLE)
    table(ax, 9.3, 5.85, ["product_id", "product_name", "category"], prods, [1.6, 2.6, 1.7], rh=rh, fs=16,
          color=PURPLE, highlight={(1, 0): TINT[CORAL]})
    text(ax, 7.0, 6.08, "orders.product_id = products.product_id", fs=15, bold=True, color=MUTED)
    py = {p[0]: 5.85 - rh * (i + 1.5) for i, p in enumerate(prods)}
    for i, (o, p, _) in enumerate(orders):
        y = 5.85 - rh * (i + 1.5)
        c = CORAL if p == "P026" else INK
        arrow(ax, 4.85, y, 9.25, py[p], color=c, lw=2.2, ms=14)
        ax.add_patch(Circle((4.85, y), 0.06, fc=c, ec="none"))
    jy = 3.1
    text(ax, 4.0, jy + 0.25, "Joined result: 4 rows, one per order", fs=18, bold=True, color=BLUE)
    pinfo = {q[0]: q[1:] for q in prods}
    joined = [(o, q, *pinfo[p]) for o, p, q in orders]
    table(ax, 0.4, jy, ["order_id", "quantity", "product_name", "category"], joined, [1.5, 1.3, 2.6, 1.7], rh=rh,
          fs=16, color=BLUE, highlight={(2, None): TINT[CORAL], (3, None): TINT[CORAL]})
    ry = jy - rh * 4.0
    box(ax, 3.95, ry, 7.35, 0.98, color=CORAL, fill="none", lw=3, r=0.25)
    text(ax, 11.6, 2.55, "Pressure Cooker twice: two orders bought it", fs=17, bold=True, color=CORAL)
    text(ax, 11.6, 2.1, "one product, many orders: correct, not a duplicate", fs=16)
    box(ax, 11.6, 1.2, 4.6, 0.7, "INNER = only matches", color=BLUE, fs=20, bold=True)
    pill(ax, 8, 0.4, "An order with product_id P999 (not in products) disappears from an INNER JOIN", color=BLUE, fs=16)
    save(fig, OUT.format(28))


def s33():  # LEFT JOIN keeps everyone
    fig, ax = canvas()
    rh = 0.4
    cust = [("C0006", "Siddharth"), ("C0007", "Rohan"), ("C0008", "Isha"), ("C0009", "Nisha")]
    ords = [("O10204", "C0006"), ("O10904", "C0007"), ("O11127", "C0009"), ("O11367", "C0007")]
    ty = 5.9
    cx0, ox0 = 2.4, 9.6
    text(ax, cx0 + 1.5, ty + 0.25, "customers", fs=18, bold=True, color=TEAL)
    table(ax, cx0, ty, ["customer_id", "name"], cust, [1.6, 1.4], rh=rh, fs=16, color=TEAL,
          highlight={(2, None): TINT[CORAL]})
    text(ax, ox0 + 1.5, ty + 0.25, "orders", fs=18, bold=True, color=ORANGE)
    table(ax, ox0, ty, ["order_id", "customer_id"], ords, [1.4, 1.6], rh=rh, fs=16, color=ORANGE)
    cy = {c: ty - rh * (i + 1.5) for i, (c, _) in enumerate(cust)}
    for i, (o, c) in enumerate(ords):
        y = ty - rh * (i + 1.5)
        arrow(ax, cx0 + 3.05, cy[c], ox0 - 0.05, y, color=INK, lw=2, ms=14)
        ax.add_patch(Circle((cx0 + 3.05, cy[c]), 0.06, fc=INK, ec="none"))
    cross(ax, cx0 + 3.3, cy["C0008"], s=0.15)
    text(ax, cx0 + 3.6, cy["C0008"], "no order", fs=15, bold=True, color=RED, ha="left")
    cols, cw = ["customer_id", "name", "order_id"], [1.6, 1.4, 1.4]
    nm = dict(cust)
    inner = [("C0006", nm["C0006"], "O10204"), ("C0007", nm["C0007"], "O10904"), ("C0007", nm["C0007"], "O11367"),
             ("C0009", nm["C0009"], "O11127")]
    left = inner[:3] + [("C0008", "Isha", "NULL")] + inner[3:]
    ry = 3.45
    text(ax, 0.3 + 2.2, ry + 0.25, "INNER JOIN result", fs=18, bold=True, color=BLUE)
    table(ax, 0.3, ry, cols, inner, cw, rh=rh, fs=16, color=BLUE)
    text(ax, 6.15, 2.55, "Isha is gone", fs=18, bold=True, color=RED)
    text(ax, 6.15, 2.1, "(4 rows)", fs=16, color=MUTED)
    lx0 = 7.6
    text(ax, lx0 + 2.2, ry + 0.25, "LEFT JOIN result", fs=18, bold=True, color=GREEN)
    table(ax, lx0, ry, cols, left, cw, rh=rh, fs=16, color=GREEN, highlight={(3, None): TINT[CORAL]})
    ny = ry - rh * 4.5
    ax.add_patch(Ellipse((lx0 + 3.0 + 0.7, ny), 1.25, 0.42, fc="none", ec=RED, lw=3))
    text(ax, 12.3, ny + 0.25, "Isha stays,", fs=16, bold=True, color=RED, ha="left")
    text(ax, 12.3, ny - 0.2, "order_id = NULL", fs=16, bold=True, color=RED, ha="left")
    pill(ax, 8, 0.42, "WHERE order_id IS NULL  →  only C0008  (customers who never bought)")
    save(fig, OUT.format(33))


if __name__ == "__main__":
    import os; os.makedirs("out", exist_ok=True)
    s05(); s20(); s22(); s28(); s33()
