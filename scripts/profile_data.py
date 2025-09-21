import pandas as pd
from load_data import load_data


def profile_dataset(df: pd.DataFrame, name: str):
    """
    Generic function to profile a dataset (raw or cleaned).
    """
    if df.empty:
        print(f"{name} dataset is empty. Exiting...")
        return

    print(f"\n--- {name.upper()} DATASET INFO ---")
    print(df.info())

    # Missing values
    print(f"\n{name} - NULL VALUES")
    print(df.isnull().sum().sort_values(ascending=False).head(10))

    # Duplicates
    print(f"\n{name} - DUPLICATES")
    print("Total duplicates:", df.duplicated().sum())

    # Sample records
    print(f"\n{name} - SAMPLE RECORDS")
    print(df.head(5))

    # Ratings distribution
    if "rating" in df.columns:
        print(f"\n{name} - RATINGS DISTRIBUTION")
        print(df["rating"].value_counts(dropna=False).head(10))

    # Duration distribution (only in raw data)
    if "duration" in df.columns:
        print(f"\n{name} - DURATION EXAMPLES")
        print(df["duration"].value_counts().head(10))


def profile_raw():
    raw_file = "data/netflix_titles.csv"
    print("\n Profiling RAW dataset...")
    df = load_data(raw_file)
    profile_dataset(df, "RAW")


def profile_cleaned():
    cleaned_file = "data/cleaned_netflix.csv"
    print("\n Profiling CLEANED dataset...")
    try:
        df = pd.read_csv(cleaned_file, index_col="show_id")
        profile_dataset(df, "CLEANED")
    except FileNotFoundError:
        print(" Cleaned file not found. Run data_cleaning.py first.")


if __name__ == "__main__":
    profile_raw()
    profile_cleaned()
