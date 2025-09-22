FROM python:3.11-slim

# set workdir
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files (optional, volumes also mount them)
COPY . .

# default command (can be overridden by docker compose run)
CMD ["python", "scripts/preprocessing.py"]
# CMD ["python", "scripts/data_cleaning.py"]