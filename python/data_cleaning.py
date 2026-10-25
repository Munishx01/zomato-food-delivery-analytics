"""Clean raw synthetic data and export Power BI / SQLite-ready CSVs."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
log = []

rest = pd.read_csv(RAW / "restaurants_raw.csv")
orders = pd.read_csv(RAW / "orders_raw.csv", parse_dates=["order_timestamp"])
log.append(f"Loaded {len(rest)} restaurants, {len(orders)} order rows")

for df in (rest, orders):
    for c in df.select_dtypes(include=["object", "string"]):
        df[c] = df[c].str.strip()
rest["city"] = rest["city"].str.title()
orders["order_status"] = orders["order_status"].str.title()
log.append(f"Missing values before: {orders.isna().sum()[lambda s: s>0].to_dict()}")

d = orders.duplicated().sum(); orders = orders.drop_duplicates()
log.append(f"Removed {d} exact duplicate rows; duplicate order_id remaining: {orders.order_id.duplicated().sum()}")

orders["payment_mode"] = orders["payment_mode"].fillna("Unknown")   # not guessed

assert (orders[["order_amount", "discount", "delivery_fee", "packaging_fee", "tax"]] >= 0).all().all()
assert (orders["discount"] <= orders["order_amount"]).all()
assert orders["restaurant_id"].isin(rest["restaurant_id"]).all()
assert rest["restaurant_rating"].between(1, 5).all()

q1, q3 = orders.order_amount.quantile([.25, .75]); iqr = q3 - q1
orders["is_outlier_amount"] = (orders.order_amount > q3 + 1.5 * iqr).astype(int)
log.append(f"Flagged {orders.is_outlier_amount.sum()} high-value outliers (kept)")

orders["order_date"] = orders["order_timestamp"].dt.date
orders = orders.sort_values("order_timestamp")
orders.to_csv(OUT / "orders_clean.csv", index=False)
rest.to_csv(OUT / "restaurants_clean.csv", index=False)
print("\n".join(log)); print("Clean orders:", len(orders))
