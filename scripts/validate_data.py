"""
Data Validation Script
Validates data quality in each layer
"""
import os
import sys
from datetime import datetime
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate_bronze(bronze_path, run_date):
    """Validate bronze layer data"""
    logger.info(f"Validating bronze layer: {bronze_path}")

    if not os.path.exists(bronze_path):
        raise FileNotFoundError(f"Bronze file not found: {bronze_path}")

    df = pd.read_csv(bronze_path)

    # Validation checks
    checks = {
        'record_count': len(df) > 0,
        'has_order_id': 'order_id' in df.columns,
        'has_ingestion_timestamp': 'ingestion_timestamp' in df.columns,
        'no_null_order_id': df['order_id'].isnull().sum() == 0,
    }

    logger.info(f"Bronze validation results:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        logger.info(f"  {status} {check}: {passed}")

    if not all(checks.values()):
        raise ValueError("Bronze validation failed")

    return True


def validate_silver(silver_path, run_date):
    """Validate silver layer data"""
    logger.info(f"Validating silver layer: {silver_path}")

    if not os.path.exists(silver_path):
        raise FileNotFoundError(f"Silver directory not found: {silver_path}")

    # For Parquet, we'd use PySpark in production
    # For local POC, check directory exists
    checks = {
        'directory_exists': os.path.exists(silver_path),
        'has_parquet_files': len([f for f in os.listdir(silver_path) if f.endswith('.parquet')]) > 0,
    }

    logger.info(f"Silver validation results:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        logger.info(f"  {status} {check}: {passed}")

    if not all(checks.values()):
        raise ValueError("Silver validation failed")

    return True


def validate_gold(gold_path, run_date):
    """Validate gold layer data"""
    logger.info(f"Validating gold layer: {gold_path}")

    if not os.path.exists(gold_path):
        raise FileNotFoundError(f"Gold directory not found: {gold_path}")

    # Check for expected aggregates
    expected_dirs = ['daily_sales_by_region', 'customer_metrics', 'product_metrics']
    checks = {}

    for dir_name in expected_dirs:
        dir_path = os.path.join(gold_path, dir_name)
        checks[f'{dir_name}_exists'] = os.path.exists(dir_path)

    logger.info(f"Gold validation results:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        logger.info(f"  {status} {check}: {passed}")

    if not all(checks.values()):
        raise ValueError("Gold validation failed")

    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate data pipeline")
    parser.add_argument("--run-date", help="Run date (YYYY-MM-DD)")
    args = parser.parse_args()

    run_date = args.run_date or datetime.now().strftime("%Y-%m-%d")
    data_dir = os.path.join(os.path.dirname(__file__), "../data")

    try:
        validate_bronze(
            os.path.join(data_dir, "bronze/sales", f"sales_{run_date}.csv"),
            run_date
        )
        validate_silver(
            os.path.join(data_dir, "silver", f"sales_cleaned_{run_date}"),
            run_date
        )
        validate_gold(
            os.path.join(data_dir, "gold", run_date),
            run_date
        )

        logger.info("✓ All validations passed!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"✗ Validation failed: {e}")
        sys.exit(1)
