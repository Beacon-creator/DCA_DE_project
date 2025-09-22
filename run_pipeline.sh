# #!/bin/bash
# set -e

# echo "Starting pipeline..."

# #!/bin/bash
# # Run the Netflix data pipeline inside the container

# # Step 1: Preprocess the data
# python /app/scripts/data_cleaning.py

# # Step 2: Insert cleaned data and run validations
# python /app/scripts/insert_data.py


#!/bin/bash
# Run the Netflix data pipeline inside the container

DB_HOST="postgres"
DB_PORT=5432
MAX_RETRIES=10
SLEEP_TIME=5

echo "Waiting for PostgreSQL to be ready at $DB_HOST:$DB_PORT..."

# Wait until PostgreSQL is accepting connections
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
python /app/scripts/data_cleaning.py

# Step 2: Insert cleaned data and run validations
python /app/scripts/insert_data.py

echo "Pipeline completed successfully."
