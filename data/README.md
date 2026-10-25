# Data
**All data is SYNTHETIC. It is not Zomato data.** No suitable public dataset could be downloaded in the authoring
environment (Kaggle and similar hosts were not reachable), so `python/generate_synthetic_data.py` (seed 42) creates it:
60 restaurants, 1,200 orders (Nov 2025 – Sep 2026), plus deliberately injected quality issues (15 duplicate rows,
12 null payment modes, inconsistent casing) for the cleaning step.
- `raw/` generated files; `processed/` output of `python/data_cleaning.py`.
- Not included in the data (so those analyses are unsupported): customer IDs, real vehicle fleet size, order-level ratings.
- To use a real dataset, keep the column names in `docs/methodology.md` and rerun the pipeline.
Zomato is a trademark of its owner; this project is an independent portfolio piece with no affiliation.
