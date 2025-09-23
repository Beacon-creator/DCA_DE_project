#!/bin/bash
# Run the Netflix data pipeline inside the container

DB_HOST="postgres"
DB_PORT=5432
MAX_RETRIES=10
SLEEP_TIME=5


LOGFILE="/app/pipeline.log"

echo "===== $(date) =====" | tee -a "$LOGFILE"

echo "Waiting for PostgreSQL to be ready at $DB_HOST:$DB_PORT..."

# Wait until PostgreSQL is accepting connections
RETRY_COUNT=0
until nc -z $DB_HOST $DB_PORT; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "PostgreSQL is not ready after $MAX_RETRIES attempts, exiting." | tee -a "$LOGFILE"
        exit 1
    fi
    echo "PostgreSQL not ready yet, retrying in $SLEEP_TIME seconds..." | tee -a "$LOGFILE"
    sleep $SLEEP_TIME
done

echo "PostgreSQL is up. Starting pipeline..."  | tee -a "$LOGFILE"

# Step 1: Preprocess the data
echo "[Step 1] Running data_cleaning.py from /app/scripts..." | tee -a "$LOGFILE"
/usr/local/bin/python3 /app/scripts/data_cleaning.py 2>&1 | tee -a "$LOGFILE"

# Check if cleaned file exists
if [ -f "/app/data/cleaned_netflix.csv" ]; then
    echo "[Check] Cleaned file exists: /app/data/cleaned_netflix.csv" | tee -a "$LOGFILE"
else
    echo "[Error] Cleaned file missing at /app/data/cleaned_netflix.csv" | tee -a "$LOGFILE"
fi

# Step 2: Insert cleaned data and run validations
echo "[Step 2] Running insert_data.py from /app/scripts..." | tee -a "$LOGFILE"
/usr/local/bin/python3 /app/scripts/insert_data.py 2>&1 | tee -a "$LOGFILE"

echo "Pipeline completed successfully." | tee -a "$LOGFILE"
echo "==============================" | tee -a "$LOGFILE"
