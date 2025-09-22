import os
import pandas as pd
from sqlalchemy import create_engine, text

def insert_and_validate(cleaned_csv: str, db_url: str, table_name: str = "netflix_titles_table"):
    """
    Load cleaned Netflix dataset into PostgreSQL using SQLAlchemy.
    Performs validation after inserting.
    """
    print("Reading cleaned dataset...")
    df = pd.read_csv(cleaned_csv, index_col="show_id")
    df.reset_index(inplace=True)  # ensure show_id is a proper column

    print(f"Loaded {len(df)} rows from {cleaned_csv}")

    # Create SQLAlchemy engine (connect to DB)
    print("Connecting to PostgreSQL...")
    engine = create_engine(db_url)

    with engine.begin() as conn:
        # Run create_tables.sql to ensure schema exists
        print("Ensuring table exists...")
        with open("sql/create_tables.sql", "r") as f:
            create_sql = f.read()
        conn.execute(text(create_sql))

        # Insert data into PostgreSQL
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"Inserting data into '{table_name}'...")

        # --- Validation queries ---
        print("Running validation checks...")

        # Row count
        row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        print(f"   • Total rows in table: {row_count}")

        # Null checks
        nulls_check = conn.execute(text(f"""
            SELECT 
                SUM(CASE WHEN show_id IS NULL THEN 1 ELSE 0 END) AS null_show_id,
                SUM(CASE WHEN title IS NULL THEN 1 ELSE 0 END) AS null_title,
                SUM(CASE WHEN type IS NULL THEN 1 ELSE 0 END) AS null_type
            FROM {table_name};
        """)).mappings().first()

        print("   • Null values check:")
        if nulls_check:
            for col, val in nulls_check.items():
                print(f"       - {col}: {val}")
        else:
            print("       No results from null check query.")

        # Duplicate check
        duplicates = conn.execute(text(f"""
            SELECT show_id, COUNT(*) 
            FROM {table_name}
            GROUP BY show_id
            HAVING COUNT(*) > 1;
        """)).fetchall()

        print("   • Duplicate check:")
        if duplicates:
            print(f"       Found {len(duplicates)} duplicate show_id values.")
        else:
            print("       No duplicate show_id values found.")

    print("Data successfully loaded and validated.")

if __name__ == "__main__":
    # db url using the same credentials in docker-compose.yml
    DB_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://my_postgres:password_postgres@postgres:5432/netflix_titles_db"
    )

    cleaned_file = "data/cleaned_netflix.csv"
    insert_and_validate(cleaned_file, DB_URL)
