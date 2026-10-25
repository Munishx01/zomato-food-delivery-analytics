"""Generate a SYNTHETIC Zomato-style food delivery dataset (not real Zomato data).
Deliberately injects a few data-quality issues (duplicates, nulls, messy casing)
so that data_cleaning.py has real work to do. Seeded for reproducibility."""
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"; RAW.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(42)

CITIES = ["Hyderabad", "Mumbai", "Bangalore", "Pune", "Jaipur", "Delhi"]
CITY_W = [.22, .20, .18, .14, .13, .13]
AREAS = ["North", "South", "East", "West", "Central"]
TYPES = ["Casual Dining", "Cloud Kitchen", "Quick Service", "Cafe"]
TYPE_RATING = {"Casual Dining": 4.2, "Cloud Kitchen": 3.9, "Quick Service": 3.8, "Cafe": 3.6}
CUISINES = ["Pizza", "Chinese", "Biryani", "Healthy", "Mughlai", "Beverages",
            "Street Food", "Desserts", "North Indian", "South Indian"]
CUIS_W = [.17, .14, .15, .06, .11, .07, .09, .07, .08, .06]
CUIS_PRICE = {"Pizza": 520, "Chinese": 430, "Biryani": 480, "Healthy": 410, "Mughlai": 500,
              "Beverages": 180, "Street Food": 220, "Desserts": 260, "North Indian": 450, "South Indian": 300}
PAY = ["Cash on Delivery", "Credit Card", "Debit Card", "UPI", "Wallet"]
PAY_W = [.18, .15, .12, .45, .10]

n_rest = 60
rest = pd.DataFrame({
    "restaurant_id": [f"R{i:03d}" for i in range(1, n_rest + 1)],
    "restaurant_name": [f"Restaurant {i:02d}" for i in range(1, n_rest + 1)],
    "restaurant_type": rng.choice(TYPES, n_rest, p=[.35, .25, .25, .15]),
    "city": rng.choice(CITIES, n_rest, p=CITY_W),
    "area": rng.choice(AREAS, n_rest),
    "primary_cuisine": rng.choice(CUISINES, n_rest, p=CUIS_W),
})
rest["restaurant_rating"] = np.clip(
    rest["restaurant_type"].map(TYPE_RATING) + rng.normal(0, .3, n_rest), 3.0, 5.0).round(1)

n = 1200
dates = pd.to_datetime("2025-11-01") + pd.to_timedelta(rng.integers(0, 334, n), unit="D") \
        + pd.to_timedelta(rng.integers(10 * 60, 23 * 60, n), unit="m")
rid = rng.choice(rest["restaurant_id"], n)
cuisine = rest.set_index("restaurant_id").loc[rid, "primary_cuisine"].values
qty = rng.choice([1, 2, 3, 4, 5], n, p=[.2, .3, .25, .15, .1])
unit = np.array([CUIS_PRICE[c] for c in cuisine]) / 2.2 * rng.uniform(.8, 1.25, n)
amount = (qty * unit).round(2)
disc = np.where(rng.random(n) < .45, amount * rng.uniform(.05, .25, n), 0).round(2)
deliv = rng.choice([0, 20, 30, 40], n, p=[.1, .3, .4, .2]).astype(float)
pack = rng.choice([5, 10, 15, 20], n, p=[.2, .4, .3, .1]).astype(float)
tax = ((amount - disc) * .05).round(2)
orders = pd.DataFrame({
    "order_id": [f"ORD{100000 + i}" for i in range(n)],
    "order_timestamp": dates, "restaurant_id": rid, "cuisine": cuisine,
    "payment_mode": rng.choice(PAY, n, p=PAY_W),
    "order_status": rng.choice(["Delivered", "Cancelled", "Refunded"], n, p=[.90, .07, .03]),
    "item_quantity": qty, "order_amount": amount, "discount": disc,
    "delivery_fee": deliv, "packaging_fee": pack, "tax": tax,
    "delivery_vehicle_id": [f"V{v:02d}" for v in rng.integers(1, 41, n)],
})
orders = orders.sort_values("order_timestamp").reset_index(drop=True)

orders = pd.concat([orders, orders.sample(15, random_state=1)], ignore_index=True)
orders.loc[rng.choice(len(orders), 12, replace=False), "payment_mode"] = None
orders.loc[rng.choice(len(orders), 20, replace=False), "order_status"] = "delivered "
rest_out = rest.copy()
idx = rest_out.sample(4, random_state=3).index
rest_out.loc[idx, "city"] = rest_out.loc[idx, "city"].str.lower() + " "

rest_out.to_csv(RAW / "restaurants_raw.csv", index=False)
orders.to_csv(RAW / "orders_raw.csv", index=False)
print("restaurants:", len(rest_out), "order rows (incl. injected dupes):", len(orders))
