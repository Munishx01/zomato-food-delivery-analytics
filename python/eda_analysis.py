"""EDA + independent KPI summary (cross-check for SQL/DAX) + exploratory charts."""
from pathlib import Path
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
o = pd.read_csv(ROOT / "data/processed/orders_clean.csv", parse_dates=["order_timestamp"])
r = pd.read_csv(ROOT / "data/processed/restaurants_clean.csv")
d = o.merge(r, on="restaurant_id")
kpi = {"total_order_amount": o.order_amount.sum(), "total_items": o.item_quantity.sum(),
       "total_discount": o.discount.sum(), "total_delivery_fee": o.delivery_fee.sum(),
       "total_packaging_fee": o.packaging_fee.sum(), "total_tax": o.tax.sum(),
       "total_orders": o.order_id.nunique(),
       "cancellation_rate_pct": o.order_status.eq("Cancelled").mean() * 100}
(ROOT / "docs").mkdir(exist_ok=True)
pd.Series(kpi).round(2).to_csv(ROOT / "docs/kpi_summary.csv", header=["value"])
print(pd.Series(kpi).round(2))
print(d.groupby("cuisine").order_amount.sum().sort_values(ascending=False).round(0))
print(d.groupby("restaurant_type").restaurant_rating.mean().round(2))
print(o.order_status.value_counts())

out = ROOT / "docs/python_eda_charts"; out.mkdir(exist_ok=True)
d.groupby("cuisine").order_amount.sum().sort_values().plot.barh(color="#E23744", title="Order amount by cuisine")
plt.tight_layout(); plt.savefig(out / "cuisine_amount.png", dpi=150); plt.close()
o.groupby(o.order_timestamp.dt.to_period("M")).delivery_vehicle_id.nunique().plot(
    marker="o", color="#E23744", title="Distinct vehicles per month")
plt.tight_layout(); plt.savefig(out / "vehicles_monthly.png", dpi=150); plt.close()
