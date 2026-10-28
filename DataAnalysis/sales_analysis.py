"""
Project: Sales Data Analysis
Description: Uses the pandas library to load, clean, and analyze a sales dataset,
             computing critical revenue metrics and generating a clean report.
"""

import pandas as pd

def main():
    print("=" * 50)
    print("        AUTOMATED SALES DATA ANALYSIS REPORT        ")
    print("=" * 50 + "\n")

    # Step 1: Load the dataset
    try:
        df = pd.read_csv('sales_data.csv')
    except FileNotFoundError:
        print(" Error: 'sales_data.csv' file not found. Ensure it is in the same directory.")
        return

    # Step 2: Explore & Clean Data
    print(f"-> Initial dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Clean duplicates and handle missing values if any
    initial_count = len(df)
    df = df.dropna().drop_duplicates()
    cleaned_count = len(df)
    if initial_count > cleaned_count:
        print(f"-> Cleaned data: Removed {initial_count - cleaned_count} duplicate/null rows.")
    else:
        print("-> Data integrity check passed: No missing values or duplicates found.")

    # Step 3: Calculate Metrics
    total_revenue = df['Total_Sales'].sum()
    average_order_value = df['Total_Sales'].mean()
    
    # Find best-selling product by total quantity sold
    product_sales = df.groupby('Product')['Quantity'].sum()
    best_product_qty = product_sales.idxmax()
    best_product_qty_val = product_sales.max()

    # Find best-selling product by total revenue generated
    product_revenue = df.groupby('Product')['Total_Sales'].sum()
    best_product_rev = product_revenue.idxmax()
    best_product_rev_val = product_revenue.max()

    # Step 4: Display Formatted Report Output
    print("\n" + "~" * 50)
    print(" EXECUTIVE SUMMARY METRICS:")
    print(f"• Total Store Revenue     : ₹{total_revenue:,.2f}")
    print(f"• Average Order Value     : ₹{average_order_value:,.2f}")
    print(f"• Top Product (by Volume) : {best_product_qty} ({best_product_qty_val} units sold)")
    print(f"• Top Product (by Revenue): {best_product_rev} (₹{best_product_rev_val:,.2f})")
    print("~" * 50)

if __name__ == "__main__":
    main()