import os
import pandas as pd
from sqlalchemy import create_engine, text

def insert_to_db(cleaned_csv: str, db_url: str, table_name: str = "netflix_titles_table"):
    """
    Load cleaned Netflix dataset into PostgreSQL using SQLAlchemy.
    
    Args:
        cleaned_csv (str): Path to the cleaned CSV file.
        db_url (str): SQLAlchemy database connection URL.
        table_name (str): Target table name in PostgreSQL.
    """
    print("Reading cleaned dataset...")
    df = pd.read_csv(cleaned_csv, index_col="show_id")
    df.reset_index(inplace=True)  # ensure show_id is a proper column

    print(f"Loaded {len(df)} rows from {cleaned_csv}")

    # Create SQLAlchemy engine
    print("Connecting to PostgreSQL...")
    engine = create_engine(db_url)

    with engine.begin() as conn:
        # Run create_tables.sql to ensure schema exists
        print("Ensuring table exists...")
        with open("sql/create_tables.sql", "r") as f:
            create_sql = f.read()
        conn.execute(text(create_sql))

        # Insert data into PostgreSQL
        print(f"Inserting data into '{table_name}'...")
        df.to_sql(table_name, conn, if_exists="append", index=False)

        # --- Validation queries ---
        print("Running validation checks...")

        row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        print(f" Total rows in table: {row_count}")

        nulls_check = conn.execute(text("""
            SELECT 
                SUM(CASE WHEN show_id IS NULL THEN 1 ELSE 0 END) AS null_show_id,
                SUM(CASE WHEN title IS NULL THEN 1 ELSE 0 END) AS null_title,
                SUM(CASE WHEN type IS NULL THEN 1 ELSE 0 END) AS null_type
            FROM {table_name};
        """.format(table_name=table_name))).first()

        if nulls_check:
            print(" Null check results:")
            print(dict(nulls_check._mapping))
        else:
            print(" No results from null check query.")


    print("Data successfully loaded and validated!")

if __name__ == "__main__":
    # Example connection string (adjust for your setup)
    # Format: postgresql+psycopg2://username:password@host:port/database
    DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://my_postgres:password_postgres@localhost:5432/netflix_titles_db")

    cleaned_file = "data/cleaned_netflix.csv"
    insert_to_db(cleaned_file, DB_URL)
