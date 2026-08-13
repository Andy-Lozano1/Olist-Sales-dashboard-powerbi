# 📊 Data Analysis Projects — Olist E-commerce

Data analysis portfolio based on the public Olist dataset (Brazilian e-commerce marketplace, ~100K orders between 2016 and 2018). Includes two different approaches on the same data source: an interactive Power BI dashboard and a Python-based customer retention analysis.

**Author:** Andy Lozano — Systems Engineering Student | Data Analyst
🔗 [LinkedIn](https://www.linkedin.com/in/andy-lozano-guti%C3%A9rrez-16b12a27b/)

---

## 📁 Power BI — Sales Dashboard

Interactive dashboard analyzing the marketplace's sales performance: total revenue, order count, top-selling categories, monthly trend, and geographic distribution by state.

**Process:**
- Data cleaning and transformation in Power Query (filtering delivered orders, fixing data types).
- Product category translation (Portuguese → English) via merged queries.
- Star-schema data model: `order_items` as the fact table, connected to `orders`, `products`, `customers`, `sellers`, and `payments`.
- Visualizations: KPI cards, sales-by-category bar chart, time trend line chart, sales-by-state map, and interactive slicers.

**Key insights:**
- Sales showed sustained growth between 2016 and 2018.
- A small group of product categories drives most of total revenue.
- Sales distribution by state reveals strong geographic concentration, useful for logistics decisions.

📎 File: [`Power BI/Reporte Ecomerce.pbix`](./Power%20BI/Reporte%20Ecomerce.pbix)

---

## 🐍 Python + SQL — Customer Retention Analysis

Cohort analysis measuring what percentage of customers make a second purchase after their first transaction, using PostgreSQL for data extraction and Python (Pandas, Seaborn) for analysis and visualization.

**Process:**
- Data extraction via SQL query against a local PostgreSQL database.
- Built purchase cohorts by first-purchase month and calculated month-over-month retention.
- **Fixed a data issue:** the Olist dataset assigns a unique `customer_id` per *order*, not per customer. The initial analysis used this column, resulting in 0% retention across all months. This was corrected by using `customer_unique_id`, the actual identifier that tracks a customer across purchases.
- Visualized results with a Seaborn heatmap.

**Key insights:**
- Customer retention is extremely low: fewer than 1% of customers make a second purchase within the first 6 months, regardless of registration month.
- This suggests the business relies almost entirely on constant new-customer acquisition.
- Business opportunity: loyalty strategies (post-purchase email marketing, referral programs) could meaningfully improve customer lifetime value.

📎 Files: [`Python Retention/analisis_retencion.py`](./Python%20Retention/analisis_retencion.py) | [`Python Retention/mapa_calor_retencion.png`](./Python%20Retention/mapa_calor_retencion.png)

---

## 🛠️ Tools used
`Power BI` · `Power Query` · `Python (Pandas, Seaborn, Matplotlib)` · `PostgreSQL` · `SQL`

## 📂 Data source
[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)
