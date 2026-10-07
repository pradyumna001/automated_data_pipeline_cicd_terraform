"""
Data Extraction Script
Lands raw data from source to bronze layer
"""
import os
from datetime import datetime
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
SOURCE_DIR = "../data"
BRONZE_DIR = "../data/bronze/sales"
SOURCE_FILE = "sample_sales.csv"


def extract_to_bronze(source_file, bronze_dir, run_date=None):
    """
    Extract data from source and land in bronze layer

    Args:
        source_file: Path to source CSV file
        bronze_dir: Target bronze directory
        run_date: Run date for partitioning (YYYY-MM-DD)
    """
    if run_date is None:
        run_date = datetime.now().strftime("%Y-%m-%d")

    logger.info(f"Starting extraction for date: {run_date}")

    # Create bronze directory if not exists
    os.makedirs(bronze_dir, exist_ok=True)

    # Read source data
    source_path = os.path.join(SOURCE_DIR, source_file)
    logger.info(f"Reading source file: {source_path}")

    df = pd.read_csv(source_path)
    logger.info(f"Extracted {len(df)} records")

    # Add metadata
    df['ingestion_timestamp'] = datetime.now().isoformat()
    df['run_date'] = run_date

    # Write to bronze (partitioned by run_date)
    bronze_file = os.path.join(bronze_dir, f"sales_{run_date}.csv")
    df.to_csv(bronze_file, index=False)

    logger.info(f"Data landed to bronze: {bronze_file}")
    logger.info(f"Bronze file size: {os.path.getsize(bronze_file)} bytes")

    return bronze_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract data to bronze layer")
    parser.add_argument("--run-date", help="Run date (YYYY-MM-DD)")
    args = parser.parse_args()

    extract_to_bronze(SOURCE_FILE, BRONZE_DIR, args.run_date)
