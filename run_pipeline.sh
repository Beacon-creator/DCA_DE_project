#!/bin/bash
# run_pipeline.sh - Netflix ETL pipeline

set -e  # exit if any command fails

LOG_FILE="/app/pipeline.log"

echo "[$(date)] Starting Netflix pipeline..." >> "$LOG_FILE"

# Step 1: Run data cleaning (loads raw data + preprocessing)
echo "[$(date)] Running data cleaning..." >> "$LOG_FILE"
python /app/scripts/data_cleaning.py >> "$LOG_FILE" 2>&1

# Step 2: Load data into PostgreSQL and run validation
echo "[$(date)] Loading data and running validation..." >> "$LOG_FILE"
python /app/scripts/insert_data.py >> "$LOG_FILE" 2>&1

echo "[$(date)] Netflix pipeline completed successfully." >> "$LOG_FILE"
