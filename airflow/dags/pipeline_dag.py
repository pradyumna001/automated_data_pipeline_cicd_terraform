"""
Airflow DAG for End-to-End Data Pipeline
Orchestrates: Extract → Transform → Aggregate
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os

# Default arguments
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2026, 10, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'sales_pipeline',
    default_args=default_args,
    description='End-to-End Sales Data Pipeline',
    schedule_interval='@daily',  # Run daily
    catchup=False,
    tags=['etl', 'sales', 'pipeline'],
)

# Paths (adjust for your environment)
PROJECT_DIR = "/opt/airflow/dags/../.."
PYTHON_PATH = os.path.join(PROJECT_DIR, "jobs")
DATA_DIR = os.path.join(PROJECT_DIR, "data")


def extract_task(**context):
    """Extract data to bronze layer"""
    from jobs.extract import extract_to_bronze
    import sys
    sys.path.insert(0, PYTHON_PATH)

    run_date = context['ds']  # Execution date (YYYY-MM-DD)
    bronze_dir = os.path.join(DATA_DIR, "bronze/sales")

    extract_to_bronze("sample_sales.csv", bronze_dir, run_date)


def transform_task(**context):
    """Transform bronze to silver"""
    from jobs.transform import transform_bronze_to_silver
    from pyspark.sql import SparkSession
    import sys
    sys.path.insert(0, PYTHON_PATH)

    run_date = context['ds']
    bronze_path = os.path.join(DATA_DIR, "bronze/sales", f"sales_{run_date}.csv")
    silver_path = os.path.join(DATA_DIR, "silver")

    spark = SparkSession.builder.appName("Transform").getOrCreate()
    try:
        transform_bronze_to_silver(spark, bronze_path, silver_path, run_date)
    finally:
        spark.stop()


def aggregate_task(**context):
    """Aggregate silver to gold"""
    from jobs.aggregate import aggregate_silver_to_gold
    from pyspark.sql import SparkSession
    import sys
    sys.path.insert(0, PYTHON_PATH)

    run_date = context['ds']
    silver_path = os.path.join(DATA_DIR, "silver", f"sales_cleaned_{run_date}")
    gold_path = os.path.join(DATA_DIR, "gold")

    spark = SparkSession.builder.appName("Aggregate").getOrCreate()
    try:
        aggregate_silver_to_gold(spark, silver_path, gold_path, run_date)
    finally:
        spark.stop()


# Task definitions
extract = PythonOperator(
    task_id='extract_to_bronze',
    python_callable=extract_task,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform_to_silver',
    python_callable=transform_task,
    dag=dag,
)

aggregate = PythonOperator(
    task_id='aggregate_to_gold',
    python_callable=aggregate_task,
    dag=dag,
)

# Task dependencies
extract >> transform >> aggregate
