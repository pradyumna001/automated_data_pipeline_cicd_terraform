"""
PySpark Transformation Script
Transforms bronze data to silver layer (cleaning, validation)
"""
import os
import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_spark_session():
    """Create and configure Spark session"""
    spark = SparkSession.builder \
        .appName("SalesETL") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    return spark


def transform_bronze_to_silver(spark, bronze_path, silver_path, run_date=None):
    """
    Transform bronze data to silver layer

    Steps:
    1. Read bronze data
    2. Clean data (handle nulls, validate types)
    3. Apply business rules
    4. Filter cancelled orders
    5. Write to silver as Parquet
    """
    if run_date is None:
        run_date = datetime.now().strftime("%Y-%m-%d")

    logger.info(f"Starting transformation for date: {run_date}")

    # Read bronze data
    logger.info(f"Reading bronze data from: {bronze_path}")
    df = spark.read.csv(bronze_path, header=True, inferSchema=True)

    logger.info(f"Bronze record count: {df.count()}")
    logger.info("Bronze schema:")
    df.printSchema()

    # Transformation: Clean and validate
    df_cleaned = df \
        .filter(F.col("status") != "cancelled") \
        .filter(F.col("amount") > 0) \
        .filter(F.col("quantity") > 0) \
        .withColumn("order_date", F.to_date("order_date")) \
        .withColumn("amount", F.col("amount").cast("double")) \
        .withColumn("quantity", F.col("quantity").cast("int")) \
        .withColumn("unit_price", F.col("amount") / F.col("quantity")) \
        .drop("ingestion_timestamp", "run_date")

    # Data quality checks
    null_checks = df_cleaned.select([
        F.sum(F.when(F.col("order_id").isNull(), 1).otherwise(0)).alias("null_order_id"),
        F.sum(F.when(F.col("customer_id").isNull(), 1).otherwise(0)).alias("null_customer_id"),
        F.sum(F.when(F.col("amount").isNull(), 1).otherwise(0)).alias("null_amount"),
    ]).collect()[0]

    logger.info(f"Data quality checks:")
    logger.info(f"  Null order_id: {null_checks['null_order_id']}")
    logger.info(f"  Null customer_id: {null_checks['null_customer_id']}")
    logger.info(f"  Null amount: {null_checks['null_amount']}")

    if null_checks["null_order_id"] > 0:
        raise ValueError("Data quality check failed: null order_id found")

    # Write to silver (Parquet for performance)
    silver_file = os.path.join(silver_path, f"sales_cleaned_{run_date}")
    df_cleaned.write.mode("overwrite").parquet(silver_file)

    logger.info(f"Silver record count: {df_cleaned.count()}")
    logger.info(f"Data written to silver: {silver_file}")

    return silver_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transform bronze to silver")
    parser.add_argument("--bronze-path", required=True, help="Bronze data path")
    parser.add_argument("--silver-path", required=True, help="Silver output path")
    parser.add_argument("--run-date", help="Run date (YYYY-MM-DD)")
    args = parser.parse_args()

    spark = create_spark_session()
    try:
        transform_bronze_to_silver(spark, args.bronze_path, args.silver_path, args.run_date)
    finally:
        spark.stop()
