FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy and enable cron job
COPY pipeline_cron /etc/cron.d/pipeline_cron
RUN chmod 0644 /etc/cron.d/pipeline_cron
RUN crontab /etc/cron.d/pipeline_cron

# Make sure the shell script is executable
RUN chmod +x /app/run_pipeline.sh

# Start cron in foreground when container starts
CMD ["cron", "-f"]
