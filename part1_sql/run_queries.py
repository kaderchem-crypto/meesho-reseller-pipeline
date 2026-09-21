import sqlite3
import csv
import os

# Connect to the database created in Part 1
db_path = os.path.join("data", "meesho_reseller.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Ensure output directory exists
out_dir = os.path.join("part1_sql", "output")
os.makedirs(out_dir, exist_ok=True)

# Helper function to write query results to CSV
def execute_and_save(query, output_filename):
    cur.execute(query)
    headers = [description[0] for description in cur.description]
    rows = cur.fetchall()
    
    filepath = os.path.join(out_dir, output_filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

# 1. Monthly revenue by category
q1 = """
SELECT month, category, 
       ROUND(SUM(quantity * unit_price), 2) AS revenue, 
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
"""
execute_and_save(q1, "monthly_category_revenue.csv")

# 2. Region-wise total revenue and order count
q2 = """
SELECT r.region, 
       ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue, 
       COUNT(o.order_id) AS n_orders
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region
"""
execute_and_save(q2, "region_revenue.csv")

# 3. Top resellers by total spend (> 50000, top 5)
q3 = """
SELECT r.reseller_id, r.reseller_name, 
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5
"""
execute_and_save(q3, "top_resellers.csv")

# 4. Resellers who have never placed an order
q4 = """
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL
"""
execute_and_save(q4, "zero_order_resellers.csv")

# 5. Average Order Value (AOV) for June, Delivered orders only

q5 = """
SELECT SUM(quantity * unit_price) * 1.0 / COUNT(*) AS aov_june_delivered
FROM orders
WHERE month = 'June' AND status = 'Delivered'
"""
execute_and_save(q5, "june_delivered_aov.csv")

conn.close()
print("Part 1 SQL queries executed successfully and CSVs saved in part1_sql/output/!")