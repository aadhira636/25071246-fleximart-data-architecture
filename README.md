# FlexiMart Data Architecture Project

**Student Name:** SANTHA AADHIRA
**Student ID:** BITSOM_BA_25071246
**Email:** aadhira636@gmail.com
**Date:** 08-01-2026

## Project Overview

[2-3 sentences describing what you built]

## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 / PostgreSQL 14
- MongoDB 6.0

## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

Key learnings from the FlexiMart Data Architecture assignment include mastering ETL pipelines for data cleaning and loading into relational databases, transitioning from normalized OLTP schemas to star schemas for efficient OLAP analytics. Designing dimension tables enables powerful drill-down queries using GROUP BY on attributes like year/quarter/month, while CTEs and window functions simplify complex aggregations like revenue percentages and customer segmentation. Overall, the project highlighted trade-offs between RDBMS for structured transactions and NoSQL for flexible schemas, emphasizing surrogate keys and conformed dimensions for scalable warehousing.



