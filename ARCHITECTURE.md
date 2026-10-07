# Architecture Documentation

## Overview

This POC demonstrates a production-ready end-to-end data pipeline with complete automation.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SOURCE SYSTEM                            │
│                    CSV Files / APIs / DB                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Extraction
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BRONZE LAYER                                │
│              Raw, Immutable Data Storage                        │
│  - Original format preserved                                    │
│  - Added: ingestion_timestamp, run_date                         │
│  - Never modified (append-only)                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ PySpark ETL
                           │ (Cleaning, Validation)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SILVER LAYER                                │
│              Cleaned, Conformed Data                            │
│  - Data type enforcement                                         │
│  - Null handling                                                 │
│  - Business rule application                                    │
│  - Filtered cancelled orders                                    │
│  - Format: Parquet (columnar, compressed)                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ PySpark Aggregation
                           │ (Business Metrics)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       GOLD LAYER                                 │
│              Business-Ready Aggregates                          │
│  - Daily sales by region                                        │
│  - Customer lifetime metrics                                    │
│  - Product performance metrics                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
              ┌─────────┐   ┌─────────┐
              │  BI Tool │   │  ML /   │
              │ (Tableau │   │  Data   │
              │  Power   │   │ Science │
              │   BI)    │   │         │
              └─────────┘   └─────────┘
```

## Key Design Patterns

### 1. Medallion Architecture

```
Bronze (Raw) → Silver (Cleaned) → Gold (Aggregates)
```

**Benefits**:
- Clear separation of concerns
- Easy debugging (can replay from any layer)
- Multiple consumers can use appropriate layer
- Audit trail preserved in bronze

### 2. Idempotency

**Pattern**: Re-running the pipeline for the same date produces the same result

**Implementation**:
- Partition by date
- Overwrite mode (not append)
- Idempotent file naming

### 3. Data Quality Gates

**Pattern**: Validate data at each stage before proceeding

**Implementation**:
- Bronze: Schema validation
- Silver: Null checks, business rules
- Gold: Aggregate completeness

## Data Flow

```
1. EXTRACT (Bronze)
   Source CSV → Read → Add Metadata → Write CSV
   Input:  sample_sales.csv
   Output: data/bronze/sales/sales_YYYY-MM-DD.csv

2. TRANSFORM (Silver)
   Bronze CSV → Read → Clean → Validate → Write Parquet
   Input:  data/bronze/sales/sales_YYYY-MM-DD.csv
   Output: data/silver/sales_cleaned_YYYY-MM-DD/

3. AGGREGATE (Gold)
   Silver Parquet → Read → Aggregate → Write Parquet
   Input:  data/silver/sales_cleaned_YYYY-MM-DD/
   Output: data/gold/YYYY-MM-DD/{daily_sales,customer,product}/
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Data Processing** | PySpark | ETL transformations |
| **Orchestration** | Airflow | Pipeline scheduling |
| **IaC** | Terraform | Infrastructure provisioning |
| **CI/CD** | GitHub Actions | Automated testing & deployment |
| **Containerization** | Docker | Consistent environments |
| **Storage** | Local filesystem (extendable to S3) | Data lake layers |

## Scalability Considerations

### Local → Cloud Migration Path

1. **Replace local filesystem with S3**
   - Change paths from `data/` to `s3://bucket/`
   - Update Terraform to create buckets

2. **Replace local Spark with EMR/Glue**
   - Use Glue for serverless Spark
   - Or EMR for heavy workloads

3. **Replace local Airflow with MWAA**
   - AWS Managed Workflows for Apache Airflow
   - Or self-hosted on ECS

## Learning Outcomes

This POC teaches:
- ✅ Medallion architecture (Bronze/Silver/Gold)
- ✅ ETL best practices
- ✅ Orchestration with Airflow
- ✅ Infrastructure as Code with Terraform
- ✅ CI/CD automation
- ✅ Containerization with Docker
- ✅ Data quality patterns
- ✅ Production-ready design patterns
