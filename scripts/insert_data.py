import os
import pandas as pd
from sqlalchemy import create_engine, text

def insert_and_validate(cleaned_csv: str, db_url: str, table_name: str = "netflix_titles_table"):
    """
    Load cleaned Netflix dataset into PostgreSQL using SQLAlchemy.
    Ensures table exists via create_tables.sql and runs validation queries
    from validation_queries.sql.
    """
    print("Reading cleaned dataset...")
    df = pd.read_csv(cleaned_csv, index_col="show_id")
    df.reset_index(inplace=True)  # make sure show_id is a proper column

    print(f"Loaded {len(df)} rows from {cleaned_csv}")

    # Create SQLAlchemy engine
    print("Connecting to PostgreSQL...")
    engine = create_engine(db_url)

    with engine.begin() as conn:
        # --- Create tables ---
        print("Ensuring table exists...")
        with open("sql/create_tables.sql", "r") as f:
            create_sql = f.read()
        conn.execute(text(create_sql))

        # --- Insert data ---
        print(f"Inserting data into '{table_name}'...")
        df.to_sql(table_name, conn, if_exists="append", index=False)

        # --- Run validation queries ---
        print("Running validation checks from sql/validation_queries.sql...")
        with open("sql/validation_queries.sql", "r") as f:
            sql_script = f.read()

        # Split queries on semicolons
        queries = [q.strip() for q in sql_script.split(";") if q.strip()]

        for i, query in enumerate(queries, start=1):
            print(f"\nValidation Query {i}: {query[:60]}...")  # show start of query
            result = conn.execute(text(query))

            rows = result.fetchall()
            if rows:
                for row in rows:
                    print(dict(row._mapping))  # convert Row to dict for pretty print
            else:
                print("No rows returned.")

    print("\nData successfully loaded and validated.")

if __name__ == "__main__":
    DB_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://my_postgres:password_postgres@postgres:5432/netflix_titles_db"
    )

    cleaned_file = "data/cleaned_netflix.csv"
    insert_and_validate(cleaned_file, DB_URL)
