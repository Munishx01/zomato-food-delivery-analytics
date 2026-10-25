# Methodology
1. `generate_synthetic_data.py` builds restaurants + orders (amount = quantity x cuisine-based unit price with noise; tax = 5% of amount after discount).
2. `data_cleaning.py`: trim/standardise text, title-case cities, normalise status casing, drop 15 exact duplicate rows, fill 12 null payment modes with "Unknown" (not guessed), assert non-negative amounts / valid foreign keys / ratings 1–5, flag 4 IQR outliers on order_amount (kept).
3. `eda_analysis.py` computes independent KPIs (`docs/kpi_summary.csv`) used to cross-check SQL (`run_sql_validation.py`): all KPI values matched exactly.
4. Power BI model, M and DAX are documented in `powerbi/` (unvalidated; see README).
Definitions: *Vehicle Count* = distinct delivery vehicles with >=1 order in the period. *Total Order Amount* = pre-discount item subtotal across all statuses.
