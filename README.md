 # netflix_titles data pipeline project

# created a containerized data pipeline that accepts , processes and stores a dataset (netflix_titles.csv) using a postgres db


# executed project using cron in a container created
# the whole project setup was on docker , code written on vsc

# major langauges are python, postgresSQL, yml

# STEPS
# clone
# build with 'docker compose up --build -d'
# check your logs using 'docker compose exec app cat /app/pipeline.log' , scheldule to work at 5am daily