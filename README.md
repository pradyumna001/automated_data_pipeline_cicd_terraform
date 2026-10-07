# Simple Data Pipeline POC

A production-style data pipeline demonstrating:
- **Data Ingestion**: CSV → Bronze → Silver → Gold
- **Transformation**: PySpark ETL jobs
- **Orchestration**: Airflow DAGs
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions
- **Containerization**: Docker

## 🎯 Incremental Learning Approach

This project is designed to be learned **incrementally**. Start simple and add complexity as you understand each component.

### Learning Path

1. **Level 1: Core Pipeline** (30 min) - Local ETL with PySpark
2. **Level 2: Orchestration** (1 hour) - Airflow scheduling
3. **Level 3: IaC** (2 hours) - Terraform infrastructure
4. **Level 4: CI/CD** (2 hours) - GitHub Actions automation

📖 **Start here**: Read [INCREMENTAL_GUIDE.md](INCREMENTAL_GUIDE.md) for detailed instructions.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Source                              │
│                    sample_sales.csv                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Python Extraction
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Bronze Layer                              │
│              /data/bronze/sales/                             │
│              Raw CSV files (immutable)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ PySpark ETL
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Silver Layer                              │
│              /data/silver/sales_cleaned/                     │
│              Cleaned, validated Parquet                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ PySpark Aggregation
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gold Layer                                │
│              /data/gold/daily_sales/                          │
│              Aggregated business metrics                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │  Query  │   │  BI Tool │
              │  Tools  │   │  (CSV)  │
              └─────────┘   └─────────┘
```

## Project Structure

```
Simple-Pipeline-POC/
├── data/
│   ├── sample_sales.csv   # Source data
│   ├── bronze/            # Raw ingested data
│   ├── silver/            # Cleaned data
│   └── gold/              # Aggregated metrics
├── jobs/
│   ├── extract.py         # Data extraction (Level 1)
│   ├── transform.py       # PySpark ETL (Level 1)
│   └── aggregate.py       # Aggregation (Level 1)
├── scripts/
│   ├── run_local.sh       # Local execution (Level 1)
│   └── validate_data.py   # Data quality checks (Level 1)
├── airflow/
│   └── dags/
│       └── pipeline_dag.py # Airflow orchestration (Level 2)
├── docker/
│   └── docker-compose.yml # Airflow infrastructure (Level 2)
├── terraform/
│   ├── main.tf            # AWS resources (Level 3)
│   ├── variables.tf       # Configuration (Level 3)
│   └── outputs.tf         # Resource outputs (Level 3)
├── ci-cd/
│   └── github-actions.yml # CI/CD pipeline (Level 4)
├── INCREMENTAL_GUIDE.md   # Learning guide ⭐
├── ARCHITECTURE.md        # Detailed architecture
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Quick Start (Level 1 - Core Pipeline)

### Prerequisites

- Python 3.9+
- Java 17 (for PySpark)

### Setup

```bash
cd Simple-Pipeline-POC

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Step 1: Extract to Bronze
python jobs/extract.py --run-date 2026-10-07

# Step 2: Transform to Silver
python jobs/transform.py --bronze-path data/bronze/sales/sales_2026-10-07.csv --silver-path data/silver --run-date 2026-10-07

# Step 3: Aggregate to Gold
python jobs/aggregate.py --silver-path data/silver/sales_cleaned_2026-10-07 --gold-path data/gold --run-date 2026-10-07

# Validate
python scripts/validate_data.py --run-date 2026-10-07
```

## Next Steps

📖 **Read [INCREMENTAL_GUIDE.md](INCREMENTAL_GUIDE.md)** to learn:
- Level 2: Airflow orchestration
- Level 3: Terraform infrastructure
- Level 4: CI/CD automation

## Learning Objectives

This POC demonstrates:
- ✅ Medallion architecture (Bronze/Silver/Gold)
- ✅ Idempotent data processing
- ✅ Data quality checks
- ✅ Orchestration with Airflow
- ✅ Infrastructure as Code
- ✅ CI/CD automation
- ✅ Container-based deployment
- ✅ Production-ready patterns
