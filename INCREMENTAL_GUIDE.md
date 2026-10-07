# Incremental Learning Guide

This guide helps you learn the pipeline components incrementally, from simple to complex.

## Learning Path

### Level 1: Core Pipeline (Local Execution) ⭐
**Time: 30 minutes**
**Focus: Understand data flow and ETL patterns**

**What you'll learn:**
- Medallion architecture (Bronze → Silver → Gold)
- PySpark transformations
- Data quality checks
- Idempotent processing

**Files to explore:**
- `jobs/extract.py` - Data ingestion
- `jobs/transform.py` - Data cleaning and validation
- `jobs/aggregate.py` - Business metrics
- `data/sample_sales.csv` - Source data

**How to run:**
```bash
cd Simple-Pipeline-POC
pip install -r requirements.txt

python jobs/extract.py --run-date 2026-10-07
python jobs/transform.py --bronze-path data/bronze/sales/sales_2026-10-07.csv --silver-path data/silver --run-date 2026-10-07
python jobs/aggregate.py --silver-path data/silver/sales_cleaned_2026-10-07 --gold-path data/gold --run-date 2026-10-07
```

**Validate:**
```bash
python scripts/validate_data.py --run-date 2026-10-07
```

**What to understand:**
- Why is bronze immutable?
- What data quality checks are applied?
- How are aggregations computed?
- Why is Parquet used for silver/gold?

---

### Level 2: Orchestration (Airflow) ⭐⭐
**Time: 1 hour**
**Focus: Automate pipeline execution with scheduling**

**What you'll learn:**
- Airflow DAG structure
- Task dependencies
- Error handling and retries
- Pipeline monitoring

**New files:**
- `airflow/dags/pipeline_dag.py` - Orchestration logic
- `docker/docker-compose.yml` - Airflow infrastructure

**How to run:**
```bash
cd docker
docker-compose up -d

# Access Airflow UI at http://localhost:8080
# Username: admin
# Password: admin

# Trigger the "sales_pipeline" DAG manually
```

**What to understand:**
- How are tasks chained together?
- What happens if a task fails?
- How does Airflow track execution?
- What are retries and why are they important?

---

### Level 3: Infrastructure as Code (Terraform) ⭐⭐⭐
**Time: 2 hours**
**Focus: Automate cloud infrastructure provisioning**

**What you'll learn:**
- Terraform basics
- AWS resource creation
- State management
- Environment-specific configurations

**New files:**
- `terraform/main.tf` - AWS resources
- `terraform/variables.tf` - Configuration
- `terraform/outputs.tf` - Resource outputs

**How to run:**
```bash
cd terraform
terraform init
terraform plan
terraform apply  # Requires AWS credentials
```

**What creates:**
- S3 buckets (bronze, silver, gold, artifacts)
- IAM roles for Glue
- Glue jobs
- CloudWatch alarms
- SNS topics for alerts

**What to understand:**
- Why use IaC instead of manual console?
- How does Terraform state work?
- What are the benefits of versioning infrastructure?
- How do you manage multiple environments?

---

### Level 4: CI/CD Automation (GitHub Actions) ⭐⭐⭐⭐
**Time: 2 hours**
**Focus: Automate testing and deployment**

**What you'll learn:**
- CI/CD pipeline stages
- Quality gates (lint, test)
- Automated Terraform deployment
- Integration testing

**New files:**
- `ci-cd/github-actions.yml` - CI/CD workflow

**How it works:**
1. **Push to GitHub** → Triggers CI/CD
2. **Lint & Test** → Code quality checks
3. **Build** → Package code
4. **Terraform Plan** → Preview changes (PRs)
5. **Terraform Apply** → Deploy infrastructure (main branch)
6. **Integration Test** → End-to-end validation

**What to understand:**
- Why automate testing and deployment?
- What are quality gates?
- How do you safely deploy to production?
- What happens when CI/CD fails?

---

## Summary of Components

| Level | Component | Files | Purpose |
|-------|-----------|-------|---------|
| 1 | Core Pipeline | `jobs/*.py`, `data/*.csv` | ETL logic |
| 2 | Orchestration | `airflow/dags/*.py`, `docker/*.yml` | Scheduling |
| 3 | IaC | `terraform/*.tf` | Infrastructure |
| 4 | CI/CD | `ci-cd/*.yml` | Automation |

## Progress Checklist

### Level 1 - Core Pipeline
- [ ] Run extract script
- [ ] Run transform script
- [ ] Run aggregate script
- [ ] Validate data
- [ ] Understand medallion architecture
- [ ] Modify source data and re-run

### Level 2 - Orchestration
- [ ] Start Docker Compose
- [ ] Access Airflow UI
- [ ] Trigger DAG manually
- [ ] View task logs
- [ ] Understand task dependencies
- [ ] Modify DAG and re-deploy

### Level 3 - IaC
- [ ] Initialize Terraform
- [ ] Run terraform plan
- [ ] Apply Terraform changes
- [ ] View created resources
- [ ] Understand state management
- [ ] Modify variables for different environments

### Level 4 - CI/CD
- [ ] Push to GitHub
- [ ] View CI/CD workflow
- [ ] Understand quality gates
- [ ] Create a pull request
- [ ] Merge to main and deploy
- [ ] View integration tests

## Interview Talking Points

After completing each level, you can say:

**Level 1:**
"I built a data pipeline with medallion architecture, processing data through bronze, silver, and gold layers with PySpark."

**Level 2:**
"I orchestrated the pipeline with Airflow, implementing task dependencies, error handling, and automated retries."

**Level 3:**
"I implemented infrastructure as code with Terraform, provisioning S3 buckets, Glue jobs, and monitoring resources on AWS."

**Level 4:**
"I set up a complete CI/CD pipeline with GitHub Actions, including linting, testing, automated Terraform deployment, and integration tests."

## Tips for Learning

1. **Don't rush**: Complete each level before moving to the next
2. **Experiment**: Modify code and see what breaks
3. **Read the code**: Understand what each line does
4. **Draw diagrams**: Visualize the architecture
5. **Ask questions**: Why was this design chosen?
6. **Document**: Write notes as you learn

## Common Issues

**Java not found for PySpark:**
```bash
export JAVA_HOME=/path/to/java
```

**Docker won't start:**
```bash
docker-compose down
docker-compose up -d --build
```

**Terraform state locked:**
```bash
terraform force-unlock <LOCK_ID>
```

**CI/CD fails:**
- Check GitHub Actions logs
- Verify AWS credentials
- Review test failures

## Next Steps

After completing all levels:
1. Add streaming (Kafka/Kinesis)
2. Implement CDC (Change Data Capture)
3. Add data catalog (Glue/Athena)
4. Implement schema evolution
5. Add comprehensive tests
6. Deploy to production AWS account
7. Set up monitoring dashboards
8. Document operational procedures

---

**Remember**: Each level builds on the previous one. Master the basics before adding complexity!
