"""E-commerce Sales Analysis - complete pipeline: load -> clean -> analyze -> visualize -> report.

Usage:
    python main.py                       # uses data/sales_data.csv
    python main.py --data path/to.csv    # use another file with the same columns
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # render to files; no display needed
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = BASE_DIR / "data" / "sales_data.csv"
VIZ_DIR = BASE_DIR / "visualizations"
REPORT_DIR = BASE_DIR / "report"

REQUIRED_COLUMNS = ["date", "product_category", "units_sold", "unit_price", "region"]

# Colours: validated categorical palette, fixed order (blue, orange, aqua, yellow, magenta)
BLUE = "#2a78d6"
CATEGORICAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
INK, INK_SOFT, GRID = "#0b0b0b", "#52514e", "#e4e3df"

log = logging.getLogger("sales_analysis")


class DataError(Exception):
    """Raised when the input data cannot be used."""


# --------------------------------------------------------------------------- load
def load_data(path: Path) -> pd.DataFrame:
    """Load the CSV and validate that the expected columns exist."""
    path = Path(path)
    if not path.exists():
        raise DataError(f"Data file not found: {path}. Run `python generate_data.py` first.")
    try:
        df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as exc:
        raise DataError(f"Could not read {path.name}: {exc}") from exc
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise DataError(f"Missing required columns: {missing}")
    if df.empty:
        raise DataError("The data file has no rows.")
    log.info("Loaded %d rows, %d columns", *df.shape)
    return df


# -------------------------------------------------------------------------- clean
def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Return (clean dataframe, log of what was fixed/removed)."""
    df = df[REQUIRED_COLUMNS].copy()
    report = {"rows_in": len(df)}

    for col in ("product_category", "region"):
        df[col] = df[col].astype("string").str.strip().str.title()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before - len(df)

    before = len(df)
    df = df.dropna(subset=REQUIRED_COLUMNS)
    report["missing_removed"] = before - len(df)

    before = len(df)
    df = df[(df["units_sold"] > 0) & (df["unit_price"] > 0)]
    report["invalid_removed"] = before - len(df)

    if df.empty:
        raise DataError("No valid rows left after cleaning.")

    df = df.assign(
        units_sold=df["units_sold"].astype(int),
        revenue=(df["units_sold"] * df["unit_price"]).round(2),
        month=df["date"].dt.to_period("M"),
    ).reset_index(drop=True)
    report["rows_out"] = len(df)
    log.info("Cleaning: %s", report)
    return df, report


# ------------------------------------------------------------------------ analyze
def analyze(df: pd.DataFrame) -> dict:
    """Compute headline metrics and the grouped tables used by the charts."""
    by_category = df.groupby("product_category")["revenue"].sum().sort_values(ascending=False)
    by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    monthly = df.groupby("month")["revenue"].sum().sort_index()
    units_by_category = df.groupby("product_category")["units_sold"].sum().sort_values(ascending=False)

    total = df["revenue"].sum()
    return {
        "total_revenue": total,
        "orders": len(df),
        "avg_order_value": df["revenue"].mean(),
        "units": int(df["units_sold"].sum()),
        "by_category": by_category,
        "by_region": by_region,
        "monthly": monthly,
        "units_by_category": units_by_category,
        "top_category": by_category.index[0],
        "top_category_share": by_category.iloc[0] / total * 100,
        "best_month": monthly.idxmax(),
        "worst_month": monthly.idxmin(),
        "top_region": by_region.index[0],
        "top_region_share": by_region.iloc[0] / total * 100,
        "q4_share": monthly[monthly.index.month >= 10].sum() / total * 100,
        "date_min": df["date"].min(),
        "date_max": df["date"].max(),
    }


# ---------------------------------------------------------------------- visualize
def _style(ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=14, fontweight="bold", color=INK, loc="left", pad=14)
    ax.set_xlabel(xlabel, color=INK_SOFT)
    ax.set_ylabel(ylabel, color=INK_SOFT)
    ax.tick_params(colors=INK_SOFT)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)


def _money(x, _pos=None) -> str:
    return f"${x:,.0f}"


def plot_bar(by_category: pd.Series, out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = range(len(by_category))
    bars = ax.bar(x, by_category.values, color=BLUE, width=0.6)
    ax.set_xticks(list(x), list(by_category.index))
    _style(ax, "Revenue by product category", "Product category", "Revenue (USD)")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(_money))
    for b in bars:
        ax.annotate(_money(b.get_height()), (b.get_x() + b.get_width() / 2, b.get_height()),
                    ha="center", va="bottom", fontsize=9, color=INK, xytext=(0, 3),
                    textcoords="offset points")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_line(monthly: pd.Series, out: Path) -> Path:
    labels = [p.strftime("%b") for p in monthly.index]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = list(range(len(labels)))
    ax.plot(x, monthly.values, color=BLUE, linewidth=2, marker="o", markersize=7,
            markeredgecolor="white", markeredgewidth=1.5)
    ax.set_xticks(x, labels)
    _style(ax, "Monthly revenue trend", "Month (2025)", "Revenue (USD)")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(_money))
    ax.set_ylim(bottom=0)
    peak = monthly.values.argmax()
    ax.annotate(f"Peak: {_money(monthly.values[peak])}", (x[peak], monthly.values[peak]),
                xytext=(0, 12), textcoords="offset points", ha="center", fontsize=9, color=INK)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_pie(by_region: pd.Series, out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7.5, 6))
    wedges, _texts, autotexts = ax.pie(
        by_region.values, labels=by_region.index, colors=CATEGORICAL[: len(by_region)],
        autopct="%1.1f%%", startangle=90, counterclock=False, pctdistance=0.72,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"color": INK, "fontsize": 11},
    )
    for t in autotexts:
        t.set_fontweight("bold")
    ax.set_title("Share of revenue by region", fontsize=14, fontweight="bold", color=INK, pad=14)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


# ------------------------------------------------------------------------- report
def build_report(r: dict, clean_log: dict, charts: dict[str, Path]) -> str:
    cat_rows = "\n".join(
        f"| {c} | ${v:,.0f} | {v / r['total_revenue'] * 100:.1f}% | {int(r['units_by_category'][c])} |"
        for c, v in r["by_category"].items()
    )
    q4_text = (
        f"Q4 (Oct-Dec) contributes {r['q4_share']:.0f}% of revenue, above an even 25% share, "
        "which points to a holiday lift."
        if r["q4_share"] > 30
        else f"Q4 (Oct-Dec) contributes {r['q4_share']:.0f}% of revenue, close to an even 25% share, "
        "so there is no strong holiday lift in this data."
    )
    if r["top_region_share"] > 40:
        region_text = (f"{r['top_region']} is the largest region at {r['top_region_share']:.0f}% of revenue, "
                       "so sales lean noticeably on one market.")
    else:
        region_text = (f"{r['top_region']} is the largest region at {r['top_region_share']:.0f}% of revenue, "
                       "and no single region dominates.")
    insights = [
        f"**{r['top_category']} drives the business**: {r['top_category_share']:.0f}% of revenue "
        f"(${r['by_category'].iloc[0]:,.0f}). The category with the most units is "
        f"{r['units_by_category'].index[0]}, so unit volume and revenue tell different stories.",
        f"**Revenue peaks in {r['best_month'].strftime('%B')}** (${r['monthly'].max():,.0f}) and is "
        f"lowest in {r['worst_month'].strftime('%B')} (${r['monthly'].min():,.0f}). {q4_text}",
        f"**Regional split:** {region_text}",
        f"**Average order value is ${r['avg_order_value']:,.2f}**, pulled up by high-priced "
        f"categories; raising the basket size in low-priced categories is the cheapest growth lever.",
    ]
    return f"""# E-commerce Sales Analysis Report

*Period: {r['date_min']:%d %b %Y} to {r['date_max']:%d %b %Y}*

## 1. Data quality
- Rows loaded: **{clean_log['rows_in']}**
- Duplicates removed: **{clean_log['duplicates_removed']}**
- Rows with missing values removed: **{clean_log['missing_removed']}**
- Rows with invalid quantity/price removed: **{clean_log['invalid_removed']}**
- Rows analysed: **{clean_log['rows_out']}**
- Text columns were trimmed and standardised (e.g. `books` -> `Books`).

## 2. Key metrics
| Metric | Value |
|---|---|
| Total revenue | ${r['total_revenue']:,.2f} |
| Orders | {r['orders']} |
| Units sold | {r['units']} |
| Average order value | ${r['avg_order_value']:,.2f} |

## 3. Revenue by category
| Category | Revenue | Share | Units |
|---|---|---|---|
{cat_rows}

![Revenue by category](../visualizations/{charts['bar'].name})

## 4. Monthly trend
![Monthly revenue](../visualizations/{charts['line'].name})

## 5. Regional split
![Revenue by region](../visualizations/{charts['pie'].name})

## 6. Insights
{chr(10).join(f"{i}. {t}" for i, t in enumerate(insights, 1))}

## 7. Recommendations
- Protect stock and marketing budget for the top category and the peak month.
- Plan promotions for the weakest month to smooth out demand.
- Bundle low-priced items (e.g. Books) with higher-priced ones to lift average order value.

*Limitations: the sample is small and synthetic, so treat these patterns as practice findings.*
"""


# --------------------------------------------------------------------------- main
def run(data_path: Path) -> dict:
    VIZ_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    raw = load_data(data_path)
    df, clean_log = clean_data(raw)
    results = analyze(df)

    charts = {
        "bar": plot_bar(results["by_category"], VIZ_DIR / "revenue_by_category.png"),
        "line": plot_line(results["monthly"], VIZ_DIR / "monthly_revenue_trend.png"),
        "pie": plot_pie(results["by_region"], VIZ_DIR / "revenue_share_by_region.png"),
    }
    report_path = REPORT_DIR / "analysis_report.md"
    report_path.write_text(build_report(results, clean_log, charts), encoding="utf-8")
    df.drop(columns="month").to_csv(BASE_DIR / "data" / "sales_data_clean.csv", index=False)
    log.info("Report written to %s", report_path)
    return {"results": results, "clean_log": clean_log, "report": report_path}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="E-commerce sales analysis")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="path to sales CSV")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        out = run(args.data)
    except DataError as exc:
        log.error("%s", exc)
        return 1
    r = out["results"]
    print(f"\nTotal revenue: ${r['total_revenue']:,.2f} | Orders: {r['orders']} | "
          f"Top category: {r['top_category']}")
    print(f"Report: {out['report']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
