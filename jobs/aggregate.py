"""
PySpark Aggregation Script
Aggregates silver data to gold layer (business metrics)
"""
import os
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_spark_session():
    """Create and configure Spark session"""
    spark = SparkSession.builder \
        .appName("SalesAggregation") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    return spark


def aggregate_silver_to_gold(spark, silver_path, gold_path, run_date=None):
    """
    Aggregate silver data to gold layer

    Aggregations:
    - Daily sales by region
    - Customer metrics
    - Product performance
    """
    if run_date is None:
        run_date = datetime.now().strftime("%Y-%m-%d")

    logger.info(f"Starting aggregation for date: {run_date}")

    # Read silver data
    logger.info(f"Reading silver data from: {silver_path}")
    df = spark.read.parquet(silver_path)

    logger.info(f"Silver record count: {df.count()}")

    # Aggregation 1: Daily sales by region
    daily_sales_by_region = df.groupBy("order_date", "region").agg(
        F.countDistinct("order_id").alias("total_orders"),
        F.sum("amount").alias("total_revenue"),
        F.sum("quantity").alias("total_quantity"),
        F.avg("amount").alias("avg_order_value"),
        F.countDistinct("customer_id").alias("unique_customers")
    )

    # Aggregation 2: Customer metrics
    customer_metrics = df.groupBy("customer_id").agg(
        F.count("order_id").alias("total_orders"),
        F.sum("amount").alias("total_spend"),
        F.avg("amount").alias("avg_order_value"),
        F.min("order_date").alias("first_order_date"),
        F.max("order_date").alias("last_order_date")
    )

    # Aggregation 3: Product performance
    product_metrics = df.groupBy("product_id").agg(
        F.count("order_id").alias("total_orders"),
        F.sum("quantity").alias("total_quantity"),
        F.sum("amount").alias("total_revenue"),
        F.avg("unit_price").alias("avg_unit_price")
    )

    # Write to gold
    gold_base = os.path.join(gold_path, run_date)

    logger.info("Writing daily sales by region to gold")
    daily_sales_by_region.write.mode("overwrite").parquet(
        os.path.join(gold_base, "daily_sales_by_region")
    )

    logger.info("Writing customer metrics to gold")
    customer_metrics.write.mode("overwrite").parquet(
        os.path.join(gold_base, "customer_metrics")
    )

    logger.info("Writing product metrics to gold")
    product_metrics.write.mode("overwrite").parquet(
        os.path.join(gold_base, "product_metrics")
    )

    logger.info(f"Aggregations written to gold: {gold_base}")

    # Print sample data
    logger.info("\nSample daily sales by region:")
    daily_sales_by_region.show(5, truncate=False)

    return gold_base


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aggregate silver to gold")
    parser.add_argument("--silver-path", required=True, help="Silver data path")
    parser.add_argument("--gold-path", required=True, help="Gold output path")
    parser.add_argument("--run-date", help="Run date (YYYY-MM-DD)")
    args = parser.parse_args()

    spark = create_spark_session()
    try:
        aggregate_silver_to_gold(spark, args.silver_path, args.gold_path, args.run_date)
    finally:
        spark.stop()
