# Zomato-Style Food Delivery Analytics | Python · SQL · Power Query · Power BI

An end-to-end analytics project on restaurant and food-delivery operations: cleaning (Python), business SQL, and a
documented Power BI model (star schema, Power Query M, DAX) for a six-KPI, five-slicer dashboard.
Independent portfolio project, not affiliated with Zomato.

> **Honest status.** The dataset is **synthetic**. The Python and SQL parts were executed and cross-checked.
> The Power BI report (`.pbix`) and genuine Power BI screenshots are **not included**: Power BI Desktop was not
> available when this was built. Build the report from `powerbi/` (about an hour) and add your own screenshots to `screenshots/`.

## Objectives
Measure order value and fees, cuisine performance, payment mix, city coverage and ratings, order-status outcomes and delivery vehicle activity.

## Dashboard spec (to build in Power BI)
- KPI cards: Total Order Amount, Total Items, Total Discount, Total Delivery Fee, Total Packaging Fee, Total Tax
- Slicers: Restaurant Name, Restaurant Type, City, Payment Mode, Area
- Visuals: cuisine bar, monthly vehicle-count area chart, payment-mode donut, city restaurant-count column (+ avg rating as a separate visual), order status vs item quantity, restaurant-type rating bars

## Structure
`data/` (raw + processed synthetic CSVs) · `python/` (generate, clean, EDA, SQL validation) · `sql/zomato_analysis.sql` (13 queries; SQLite) · `powerbi/` (`data_model.md`, `power_query_steps.md`, `dax_measures.md`) · `docs/` (methodology, insights, KPI summary, exploratory matplotlib charts - not Power BI)

## Key figures (synthetic data)
Total order amount 596,782 · 3,148 items · 1,200 orders · AOV 497.32 · cancellation 6.67% · UPI 45.6% of orders. See `docs/insights.md`.

## Reproduce
```bash
pip install -r requirements.txt
python python/generate_synthetic_data.py
python python/data_cleaning.py
python python/eda_analysis.py
python python/run_sql_validation.py
```
Power BI: load `data/processed/*.csv` using `powerbi/power_query_steps.md`, create relationships per `data_model.md`, add measures from `dax_measures.md`.

## Limitations
Synthetic data; vehicle count is distinct vehicles with orders (no fleet table); order amount includes cancelled orders; Power BI artefacts unvalidated.
