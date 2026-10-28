# Python Programming & Data Analysis Portfolio 

Welcome to my Python learning repository! This portfolio documents my structured progression from absolute beginner programming concepts to data analysis using real-world libraries.

---

Clean Data

The cleaning process includes:

Removing duplicate records.

Converting date and numerical columns to appropriate data types.

Removing rows with missing essential information.

Excluding invalid quantities and prices.

Recalculating total sales using quantity multiplied by price.

Correcting inconsistent sales totals before analysis.

4. Analyze Sales

The program calculates important sales metrics and groups the data by product and region.

5. Generate Report

The program generates a Markdown report containing the main metrics, product performance, regional revenue, data-cleaning summary, and key findings.

 Key Metrics

The project calculates:

Metric

Description

Total Revenue

Sum of all valid sales

Total Units Sold

Sum of product quantities

Average Sale

Average revenue per valid sales record

Highest Sale

Largest individual sales amount

Lowest Sale

Smallest individual sales amount

Best-Selling Product

Product with the highest total quantity sold

Highest-Revenue Product

Product generating the most revenue

Highest-Revenue Region

Region generating the most revenue

 Sample Results

Based on the included 20-record dataset:

Metric

Result

Total Revenue

₹29,15,257.00

Total Units Sold

103

Number of Records

20

Average Sale

₹1,45,762.85

Highest Sale

₹3,73,932.00

Lowest Sale

₹4,195.00

Best-Selling Product

Laptop

Quantity of Best-Selling Product

43 units

Highest-Revenue Product

Laptop

Highest-Revenue Region

South

South Region Revenue

₹10,88,182.00

Note: These results apply to the provided sample dataset.

 Key Findings

The dataset contains 20 sales records across five product categories.

Total revenue from the dataset is ₹29,15,257.

Laptop is the best-selling product by quantity, with 43 units sold.

Laptop also generates the highest product revenue.

The South region contributes the highest revenue.

Regional grouping helps compare sales performance across different locations.

Data cleaning improves the reliability of the analysis.

 Testing and Validation

The project can be tested using the following cases:

Test Case

Expected Result

Load a valid CSV file

Dataset loads successfully

Check dataset dimensions

20 rows and 7 columns before cleaning

Check duplicate records

Duplicate count is displayed

Check missing values

Missing-value counts are displayed

Validate sales calculations

Total sales equal quantity multiplied by price

Analyze product performance

Product quantity and revenue summaries are generated

Analyze regional performance

Revenue is grouped by region

Generate the report

analysis_report.md is created

Error Handling

The program checks whether the dataset exists, validates required columns, handles invalid numeric values, and stops with a clear error if no valid sales records remain after cleaning.

 Screenshots

Add screenshots of your own program execution to the screenshots/ directory.

