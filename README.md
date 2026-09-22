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
# Meesho Reseller Pipeline & Agentic Workflow

## Overview
This repository contains the end-to-end analytics and mock agentic pipeline for monitoring Meesho reseller performance, automated category growth tracking, guardrail validation, and stakeholder message drafting.

---

## 1. How to Regenerate Data & Run the Pipeline in Order

To run the entire pipeline locally from scratch with **zero API keys required**, execute the scripts in the following exact sequence:

1. **Part 1 (SQL Analytics & Data Generation):**
   ```bash
   python part1_sql/run_queries.py
   # Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end automated analytics, data validation, reliable narrative generation, and agentic monitoring pipeline built for Meesho's reseller-operations team.

## Project Structure & Deliverables

meesho-reseller-project/
├── data/
│   ├── generate_dataset.py
│   ├── meesho_reseller.db
│   ├── resellers.csv
│   └── orders.csv
├── part1_sql/
│   ├── run_queries.py
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

---

## 1. How to Regenerate the Dataset and Run Every Part in Order

To run the entire pipeline locally from scratch, execute the scripts in the following exact sequence:

1. **Dataset Generation:**
   ```bash
   python data/generate_dataset.py