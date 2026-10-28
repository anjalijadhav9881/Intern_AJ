# E-commerce Sales Analysis

A complete beginner data-analysis project in Python: it loads a sales CSV, cleans it, calculates
business metrics, draws three charts with Matplotlib and writes a Markdown report with insights.

## Project overview
**Goal:** find out what sells, when it sells and where, using one year of order data (2025).

Questions answered:
1. Which product categories earn the most revenue?
2. How does revenue change month by month?
3. How is revenue split between regions?

**Pipeline:** `load -> validate -> clean -> analyze -> visualize -> report`

## Setup instructions
```bash
# 1. (optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. (optional) regenerate the practice dataset
python generate_data.py

# 4. run the analysis
python main.py
# or analyse another file with the same columns:
python main.py --data path/to/your_sales.csv
```
Outputs: charts in `visualizations/`, the report in `report/analysis_report.md`,
and the cleaned data in `data/sales_data_clean.csv`.

## Code structure
```
ecommerce_sales_analysis/
|-- README.md
|-- main.py                  # the whole pipeline (one function per stage)
|-- generate_data.py         # builds the 100-row practice dataset
|-- requirements.txt
|-- data/
|   |-- sales_data.csv       # raw input (100 rows x 5 columns)
|   `-- sales_data_clean.csv # output of the cleaning step
|-- visualizations/          # bar, line and pie chart PNGs
|-- report/
|   `-- analysis_report.md   # numbers + charts + written insights
`-- tests/
    `-- test_analysis.py     # 9 automated tests
```

| Function in `main.py` | Job |
|---|---|
| `load_data` | read the CSV, check the file and columns exist |
| `clean_data` | trim/standardise text, parse dates, drop duplicates, missing and invalid rows, add `revenue` |
| `analyze` | totals, average order value, revenue by category / region / month |
| `plot_bar`, `plot_line`, `plot_pie` | the three charts |
| `build_report` | writes the Markdown report with data-driven insights |

## Dataset
`data/sales_data.csv` has 100 rows and 5 columns: `date`, `product_category`, `units_sold`,
`unit_price`, `region`. It is synthetic and seeded, with a few deliberate problems for the cleaning
step (a missing price, a negative quantity, duplicate rows, inconsistent capitalisation, stray spaces).

## Screenshots
| Bar chart | Line chart | Pie chart |
|---|---|---|
| ![bar](visualizations/revenue_by_category.png) | ![line](visualizations/monthly_revenue_trend.png) | ![pie](visualizations/revenue_share_by_region.png) |

## Technical details
- **Libraries:** pandas (data), Matplotlib (charts).
- **Cleaning rules:** exact duplicate rows are dropped; rows with a missing or unparseable value are
  dropped; rows with `units_sold <= 0` or `unit_price <= 0` are dropped; text is stripped and title-cased.
- **Metric:** `revenue = units_sold * unit_price`; monthly figures use `date.to_period("M")`.
- **Error handling:** a custom `DataError` covers a missing file, an empty file, bad CSV, missing columns,
  and no valid rows after cleaning. `main()` logs the message and exits with code 1 instead of a traceback.
- **Chart design:** one colour for single-series charts, a fixed categorical order for the pie, direct
  value labels, light gridlines, titles and axis labels on every chart.

## Testing evidence
```bash
python -m unittest discover -s tests -v     # or: pytest -v
```
```
Ran 9 tests ... OK
```
Covered: text standardisation and revenue calculation, removal of duplicates / missing / invalid rows,
unparseable dates, empty-after-cleaning, metric calculation, missing file, missing columns, empty file,
and a full end-to-end run that checks the report and three PNGs are created.

## Key findings (from this dataset)
See `report/analysis_report.md` for the full report. Headlines: Electronics earns about 69% of revenue,
revenue peaks in June, and the East region is the largest at about 42%.

## Possible improvements
Add a category-by-month heatmap, compare year-over-year growth, or build a Streamlit dashboard.
