"""Generate data/sales_data.csv (100 rows x 5 columns) for practice.

The data is synthetic and seeded, so it is identical on every run. A few rows are
deliberately messy (a duplicate, a missing value, an invalid quantity, odd
capitalisation) so the cleaning step in main.py has real work to do.

Usage:  python generate_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT_FILE = Path(__file__).resolve().parent / "data" / "sales_data.csv"

CATEGORIES = {  # category: (typical unit price, price spread)
    "Electronics": (320.0, 120.0),
    "Clothing": (45.0, 15.0),
    "Home & Kitchen": (80.0, 30.0),
    "Books": (18.0, 6.0),
    "Sports": (60.0, 25.0),
}
REGIONS = ["North", "South", "East", "West"]


def build_dataset(n_rows: int = 98, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n_rows), unit="D")
    cats = rng.choice(list(CATEGORIES), n_rows, p=[0.22, 0.28, 0.20, 0.14, 0.16])

    prices = [
        max(5.0, round(rng.normal(*CATEGORIES[c]), 2)) for c in cats
    ]
    # Seasonal bump: more units in Nov/Dec
    base_units = rng.integers(1, 6, n_rows)
    units = np.where(dates.month.isin([11, 12]), base_units + rng.integers(1, 4, n_rows), base_units)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "product_category": cats,
            "units_sold": units,
            "unit_price": prices,
            "region": rng.choice(REGIONS, n_rows),
        }
    ).sort_values("date", ignore_index=True)

    # --- deliberate data-quality problems (4 extra rows -> 100 total) ---
    df.loc[5, "product_category"] = df.loc[5, "product_category"].lower()  # inconsistent case
    df.loc[12, "unit_price"] = np.nan                                       # missing value
    df.loc[20, "units_sold"] = -3                                           # invalid quantity
    df = pd.concat([df, df.iloc[[30]]], ignore_index=True)                  # exact duplicate
    extra = df.iloc[[40]].copy()
    extra["region"] = "  " + extra["region"].iloc[0] + " "                  # stray whitespace
    df = pd.concat([df, extra], ignore_index=True)
    return df.iloc[:100]


if __name__ == "__main__":
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = build_dataset()
    data.to_csv(OUT_FILE, index=False)
    print(f"Wrote {len(data)} rows x {data.shape[1]} columns to {OUT_FILE}")
