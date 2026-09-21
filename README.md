# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end automated analytics, data validation, reliable narrative generation, and agentic monitoring pipeline built for Meesho's reseller-operations team.

## Project Structure & Deliverables

```text
meesho-reseller-project/
├── data/
│   ├── generate_dataset.py
│   ├── meesho_reseller.db
│   ├── resellers.csv
│   └── orders.csv
├── part1_sql/
│   ├── run_queries.py (or queries.sql)
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers.csv
│       ├── zero_order_resellers.csv
│       └── june_delivered_aov.csv
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
├── part3_narrative/
│   ├── masking.py
│   ├── narrative_report.md
│   ├── prompt_pack.md
│   └── test_masking.py
├── part4_agent/
│   ├── agent_spec.md
│   └── mock_agent_runner.py
└── README.md