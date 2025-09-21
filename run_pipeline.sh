#!/bin/bash
# Run pipeline manually

# Step 1: Build and start containers
docker compose up --build -d

# Step 2: Run preprocessing
docker compose run app python scripts/preprocessing.py

# Step 3: Stop containers
docker compose down
