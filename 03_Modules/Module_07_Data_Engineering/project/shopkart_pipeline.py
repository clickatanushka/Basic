"""
ShopKart data pipeline (Module 7, Video 7.2)
=============================================
Extract -> Transform -> Quality checks -> Load, then an incremental load of new orders.

How to run in Google Colab:
  1. Upload this file and the data files to the Files panel:
     orders_raw.csv, customers.csv, products.csv, new_orders_2026_01.csv
  2. In a code cell type:   !python shopkart_pipeline.py

What it produces:
  - shopkart_warehouse.db  : SQLite "warehouse" with a star schema
                             (fact_orders, dim_customer, dim_product, dim_date)
  - shopkart_clean.csv     : the 2025 orders, cleaned and merged (same file as Module 6)
  - pipeline_log.txt       : what happened, step by step
"""

import sqlite3
from datetime import datetime

import pandas as pd

# ---------------------------------------------------------------
# Settings: file names in one place, so they are easy to change
# ---------------------------------------------------------------
ORDERS_FILE = "orders_raw.csv"
CUSTOMERS_FILE = "customers.csv"
PRODUCTS_FILE = "products.csv"
NEW_ORDERS_FILE = "new_orders_2026_01.csv"
WAREHOUSE_DB = "shopkart_warehouse.db"
CLEAN_CSV = "shopkart_clean.csv"
LOG_FILE = "pipeline_log.txt"

run_log = []   # every log() message is also stored here


def log(message):
    """Print a message with the time, and remember it for the run log."""
    line = datetime.now().strftime("%H:%M:%S") + "  " + message
    print(line)
    run_log.append(line)


# ---------------------------------------------------------------
# E: EXTRACT - read the source files as they are (no changes)
# ---------------------------------------------------------------
def extract(orders_file=ORDERS_FILE):
    orders = pd.read_csv(orders_file)
    customers = pd.read_csv(CUSTOMERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    log(f"EXTRACT  {orders_file}: {len(orders)} rows | customers: {len(customers)} | products: {len(products)}")
    return orders, customers, products


# ---------------------------------------------------------------
# T: TRANSFORM - the Module 6 cleaning, merges and new columns
# ---------------------------------------------------------------
def transform(orders, customers, products):
    df = orders.copy()

    # 1. Remove exact duplicate rows
    df = df.drop_duplicates()

    # 2. One spelling per city
    df["city"] = df["city"].astype(str).str.strip().str.title()
    df["city"] = df["city"].replace({"New Delhi": "Delhi", "Bangalore": "Bengaluru", "Bombay": "Mumbai",
                                     "Madras": "Chennai", "Calcutta": "Kolkata"})

    # 3. Prices like "₹1,299" -> 1299
    df["unit_price"] = (df["unit_price"].astype(str)
                        .str.replace("₹", "", regex=False)
                        .str.replace(",", "", regex=False)
                        .astype(float).astype(int))

    # 4. Dates: read YYYY-MM-DD first, then fill the gaps with DD-MM-YYYY
    #    (never format="mixed", dayfirst=True: it flips ISO dates like 2025-01-02)
    text_dates = df["order_date"].astype(str)
    df["order_date"] = pd.to_datetime(text_dates, format="%Y-%m-%d", errors="coerce").fillna(
                       pd.to_datetime(text_dates, format="%d-%m-%Y", errors="coerce"))

    # 5. Payment mode: one spelling for UPI, blanks -> "Unknown"
    df["payment_mode"] = df["payment_mode"].replace({"upi": "UPI"}).fillna("Unknown")

    # 6. Blank discount means no discount
    df["discount"] = df["discount"].astype(float).fillna(0.0)

    # 7. Returned: Yes/No -> Y/N
    df["returned"] = df["returned"].replace({"Yes": "Y", "No": "N"})

    # 8. Quantity 99 is a typo for 1 (real bulk orders of 10 are kept)
    df.loc[df["quantity"] == 99, "quantity"] = 1

    # 9. rating stays blank where the customer did not rate

    # Merge product and customer details (LEFT joins keep every order)
    df = df.merge(products[["product_id", "product_name", "category", "cost_price"]], on="product_id", how="left")
    df = df.merge(customers[["customer_id", "gender", "age", "membership"]], on="customer_id", how="left")

    # New columns
    df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
    df["profit"] = df["revenue"] - df["quantity"] * df["cost_price"]
    df["order_month"] = df["order_date"].dt.month

    log(f"TRANSFORM  {len(orders)} raw rows -> {len(df)} clean rows, {df.shape[1]} columns")
    return df


# ---------------------------------------------------------------
# QUALITY CHECKS - stop the pipeline if the data looks wrong
# ---------------------------------------------------------------
def quality_checks(df, expected_rows):
    checks = {
        "row count = unique orders in source": len(df) == expected_rows,
        "no duplicate order_id": df["order_id"].is_unique,
        "no missing keys (order_id, customer_id, product_id, order_date)":
            df[["order_id", "customer_id", "product_id", "order_date"]].notnull().all().all(),
        "every product found in products.csv": df["category"].notnull().all(),
        "every customer found in customers.csv": df["membership"].notnull().all(),
        "unit_price > 0": (df["unit_price"] > 0).all(),
        "quantity between 1 and 10": df["quantity"].between(1, 10).all(),
    }
    failed = [name for name, ok in checks.items() if not ok]
    for name, ok in checks.items():
        print("   ", "PASS" if ok else "FAIL", "-", name)
    if failed:
        log(f"QUALITY CHECKS FAILED: {failed}")
        raise ValueError("Data quality check failed: " + "; ".join(failed) + ". Nothing was loaded.")
    log(f"QUALITY CHECKS  all {len(checks)} passed")


# ---------------------------------------------------------------
# Helpers that shape the clean table into star-schema tables
# ---------------------------------------------------------------
def make_dim_date(df):
    """One row per order date, with handy calendar columns."""
    dates = pd.Series(df["order_date"].drop_duplicates().sort_values())
    dim_date = pd.DataFrame({
        "date_key": dates.dt.strftime("%Y%m%d").astype(int),   # 2025-01-31 -> 20250131
        "date": dates.dt.strftime("%Y-%m-%d"),
        "year": dates.dt.year,
        "month": dates.dt.month,
        "month_name": dates.dt.month_name(),
        "quarter": dates.dt.quarter,
        "weekday": dates.dt.day_name(),
        "is_weekend": dates.dt.dayofweek >= 5,
    })
    return dim_date.reset_index(drop=True)


def make_fact_orders(df):
    """The fact table: one row per order, keys + numbers only (no product names, no customer names)."""
    fact = df[["order_id", "customer_id", "product_id", "quantity", "unit_price", "discount",
               "city", "payment_mode", "delivery_days", "rating", "returned", "revenue", "profit"]].copy()
    fact.insert(1, "date_key", df["order_date"].dt.strftime("%Y%m%d").astype(int))
    return fact


# ---------------------------------------------------------------
# L: LOAD - write the warehouse (star schema) and the clean CSV
# ---------------------------------------------------------------
def load(df, customers, products):
    fact_orders = make_fact_orders(df)
    dim_customer = customers.copy()      # all 800 customers, even those who never ordered
    dim_product = products.copy()        # all 60 products
    dim_date = make_dim_date(df)

    conn = sqlite3.connect(WAREHOUSE_DB)
    fact_orders.to_sql("fact_orders", conn, if_exists="replace", index=False)
    dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)
    dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
    conn.close()

    df.to_csv(CLEAN_CSV, index=False)
    log(f"LOAD  {WAREHOUSE_DB}: fact_orders {len(fact_orders)}, dim_customer {len(dim_customer)}, "
        f"dim_product {len(dim_product)}, dim_date {len(dim_date)} rows | {CLEAN_CSV} {df.shape}")


def table_sizes():
    """Count the rows in every warehouse table."""
    conn = sqlite3.connect(WAREHOUSE_DB)
    sizes = {t: int(pd.read_sql(f"SELECT COUNT(*) AS n FROM {t}", conn)["n"][0])
             for t in ["fact_orders", "dim_customer", "dim_product", "dim_date"]}
    conn.close()
    return sizes


# ---------------------------------------------------------------
# INCREMENTAL LOAD - add only orders the warehouse has not seen
# ---------------------------------------------------------------
def incremental_load(new_file):
    log(f"INCREMENTAL LOAD  starting with {new_file}")
    new_raw, customers, products = extract(new_file)
    new_df = transform(new_raw, customers, products)
    quality_checks(new_df, expected_rows=new_raw["order_id"].nunique())

    conn = sqlite3.connect(WAREHOUSE_DB)
    loaded_ids = set(pd.read_sql("SELECT order_id FROM fact_orders", conn)["order_id"])
    to_add = new_df[~new_df["order_id"].isin(loaded_ids)]          # keep only order_ids we have not loaded
    skipped = len(new_df) - len(to_add)

    make_fact_orders(to_add).to_sql("fact_orders", conn, if_exists="append", index=False)

    # add calendar rows for dates the warehouse does not have yet
    known_dates = set(pd.read_sql("SELECT date_key FROM dim_date", conn)["date_key"])
    new_dates = make_dim_date(to_add)
    new_dates = new_dates[~new_dates["date_key"].isin(known_dates)]
    new_dates.to_sql("dim_date", conn, if_exists="append", index=False)
    conn.close()

    log(f"INCREMENTAL LOAD  {len(new_raw)} rows in file, {len(new_raw) - len(new_df)} duplicate rows removed | "
        f"added {len(to_add)} new orders | skipped {skipped} already in warehouse | "
        f"added {len(new_dates)} new dates")
    return len(to_add), skipped


# ---------------------------------------------------------------
# A question for the warehouse: revenue by category and month
# ---------------------------------------------------------------
REVENUE_QUERY = """
SELECT d.year, d.month, p.category,
       COUNT(*)                 AS orders,
       ROUND(SUM(f.revenue), 2) AS revenue
FROM fact_orders AS f
JOIN dim_product AS p ON f.product_id = p.product_id
JOIN dim_date    AS d ON f.date_key   = d.date_key
GROUP BY d.year, d.month, p.category
ORDER BY d.year, d.month, revenue DESC
"""


def run_pipeline():
    log("PIPELINE START")
    orders, customers, products = extract()
    clean = transform(orders, customers, products)
    quality_checks(clean, expected_rows=orders["order_id"].nunique())
    load(clean, customers, products)
    added, skipped = incremental_load(NEW_ORDERS_FILE)
    log(f"WAREHOUSE TABLES  {table_sizes()}")

    conn = sqlite3.connect(WAREHOUSE_DB)
    result = pd.read_sql(REVENUE_QUERY, conn)
    conn.close()
    print("\nRevenue by category and month (last 10 rows):")
    print(result.tail(10).to_string(index=False))
    print("Revenue 2025: ₹", round(result.loc[result["year"] == 2025, "revenue"].sum(), 2),
          "| Revenue Jan 2026: ₹", round(result.loc[result["year"] == 2026, "revenue"].sum(), 2))
    log("PIPELINE END  success")

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(run_log) + "\n")
    print("\nRun log saved to", LOG_FILE)


if __name__ == "__main__":
    run_pipeline()
