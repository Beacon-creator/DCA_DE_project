FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install cron and netcat (for waiting on PostgreSQL)
RUN apt-get update && apt-get install -y procps cron netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy and enable cronjob 
COPY cronjob /etc/cron.d/pipeline_cron
RUN sed -i 's/\r$//' /etc/cron.d/pipeline_cron \
    && chmod 0644 /etc/cron.d/pipeline_cron \
    && crontab /etc/cron.d/pipeline_cron

# ensure the pipeline script is executable
RUN chmod +x /app/run_pipeline.sh

# Start cron in foreground when container starts
CMD ["cron", "-f"]
