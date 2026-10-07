#!/bin/bash
# Local execution script for the data pipeline

set -e

echo "=========================================="
echo "End-to-End Data Pipeline - Local Run"
echo "=========================================="

# Configuration
RUN_DATE=${1:-$(date +%Y-%m-%d)}
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Run Date: $RUN_DATE"
echo "Project Directory: $PROJECT_DIR"

# Step 1: Extract to Bronze
echo ""
echo "Step 1: Extracting data to Bronze layer..."
python jobs/extract.py --run-date "$RUN_DATE"

# Step 2: Transform to Silver
echo ""
echo "Step 2: Transforming Bronze to Silver..."
python jobs/transform.py \
    --bronze-path "data/bronze/sales/sales_${RUN_DATE}.csv" \
    --silver-path "data/silver" \
    --run-date "$RUN_DATE"

# Step 3: Aggregate to Gold
echo ""
echo "Step 3: Aggregating Silver to Gold..."
python jobs/aggregate.py \
    --silver-path "data/silver/sales_cleaned_${RUN_DATE}" \
    --gold-path "data/gold" \
    --run-date "$RUN_DATE"

echo ""
echo "=========================================="
echo "Pipeline completed successfully!"
echo "=========================================="
echo ""
echo "Data locations:"
echo "  Bronze: data/bronze/sales/"
echo "  Silver: data/silver/"
echo "  Gold:   data/gold/${RUN_DATE}/"
echo ""
