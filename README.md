# Meesho Reseller Growth Pipeline

An end-to-end local pipeline for reseller data generation, SQL analytics, revenue validation, narrative masking, and agentic category monitoring.

## Project Structure

```text
data/
   generate_dataset.py       Generate CSV files and the SQLite database
part1_sql/
   run_queries.py            Generate analytics CSV outputs
   output/                   Generated query results
part2_engine/
   growth_engine.py          Growth calculations and feed validation
   test_growth_engine.py     Growth and validation tests
   fixtures/                 Valid and corrupted feed examples
part3_narrative/
   masking.py                Reseller aliasing and leak detection
   test_masking.py           Masking tests
part4_agent/
   mock_agent_runner.py      Human-approval workflow simulation
   test_mock_agent_runner.py Agent workflow tests
```

## Requirements

- Python 3.10 or newer
- No external packages are required

## Run From Scratch

Run these commands from the project root:

```bash
python data/generate_dataset.py
python part1_sql/run_queries.py
python -m unittest discover -v
python part4_agent/mock_agent_runner.py
python -m part3_narrative.test_masking
```

The first command creates `data/resellers.csv`, `data/orders.csv`, and `data/meesho_reseller.db`. The SQL command writes analytics CSV files under `part1_sql/output/`.

The agent validates its current feed before calculating Month-on-Month growth. Invalid input produces a hard stop. Valid flagged categories are sorted by absolute growth, limited to the top three, and held for human approval rather than sent automatically.

## Feed Contract

Revenue feeds must contain these columns in order:

```text
month,category,revenue,n_orders
```

Use `part2_engine/fixtures/monthly_category_revenue.csv` for a valid example and `part2_engine/fixtures/corrupted_feed.csv` for validation failure cases.

## Outputs

- `monthly_category_revenue.csv`: monthly revenue and order count by category
- `region_revenue.csv`: revenue and order count by region
- `top_resellers.csv`: top resellers above the configured spend threshold
- `zero_order_resellers.csv`: resellers without orders
- `june_delivered_aov.csv`: June delivered average order value