#!/bin/bash
# Run the dataset pipeline inside the container

DB_HOST="postgres"
DB_PORT=5432
MAX_RETRIES=10
SLEEP_TIME=5

# condition to wait until PostgreSQL is accepting connections
RETRY_COUNT=0
until nc -z $DB_HOST $DB_PORT; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "PostgreSQL is not ready after $MAX_RETRIES attempts, exiting."
        exit 1
    fi
    echo "PostgreSQL not ready yet, retrying in $SLEEP_TIME seconds..."
    sleep $SLEEP_TIME
done

echo "PostgreSQL is up. Starting pipeline..."

# Step 1: Preprocess the data
echo "[Step 1] Running data_cleaning.py from /app/scripts..."
/usr/local/bin/python3 /app/scripts/data_cleaning.py

# Check if cleaned file exists
if [ -f "/app/data/cleaned_netflix.csv" ]; then
    echo " Cleaned file exists at /app/data/cleaned_netflix.csv"
else
    echo "Cleaned file missing at /app/data/cleaned_netflix.csv"
fi

# Step 2: Insert cleaned data and run validations
echo "Running insert_data.py from /app/scripts "
/usr/local/bin/python3 /app/scripts/insert_data.py

echo "Pipeline completed!"
