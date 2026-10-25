"""Load clean CSVs into in-memory SQLite, run sql/zomato_analysis.sql, print every result."""
from pathlib import Path
import sqlite3, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
con = sqlite3.connect(":memory:")
pd.read_csv(ROOT/"data/processed/orders_clean.csv").drop(columns=["order_date","is_outlier_amount"]).to_sql("orders", con, index=False)
pd.read_csv(ROOT/"data/processed/restaurants_clean.csv").to_sql("restaurants", con, index=False)
sql = "\n".join(l for l in (ROOT/"sql/zomato_analysis.sql").read_text().splitlines() if not l.lstrip().startswith("--"))
stmts = [s.strip() for s in sql.split(";") if "SELECT" in s.upper()]
for i, s in enumerate(stmts, 1):
    df = pd.read_sql_query(s, con); print(f"--- query {i} ({len(df)} rows)"); print(df.head(12).to_string(index=False))
