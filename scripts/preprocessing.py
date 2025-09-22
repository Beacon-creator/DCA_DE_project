import pandas as pd

def preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the Netflix dataset.
    - Handle missing values
    - Convert datatypes
    - Extract features
    - Drop unnecessary columns
    """
    # --- HANDLE CATEGORICAL/TEXT MISSING VALUES ---
    df.fillna({
        "director": "Unknown",
        "cast": "Unknown",
        "country": "Unknown",
        "date_added": "Unknown",
        "rating": "Unknown",
        "duration": "Unknown"
    }, inplace=True)

    # --- FIX DATATYPES ---
    # Convert 'date_added' to datetime
     # Strip whitespace and convert
    df["date_added"] = df["date_added"].astype(str).str.strip()
    df["date_added"] = pd.to_datetime(
            df["date_added"].astype(str),
            errors="coerce"
    )

    # Extract year, month, day as integers
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")
    df["day_added"] = df["date_added"].dt.day.astype("Int64")

    # Split 'duration' into numeric + unit
    df["duration_value"] = (
        df["duration"].str.extract(r"(\d+)").astype(float).astype("Int64")
    )
    df["duration_unit"] = df["duration"].str.extract(r"([a-zA-Z]+)").astype(str)

    # Drop unnecessary column
    df.drop(columns=["duration"], inplace=True)

    # Clean up string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    df["country"] = df["country"].str.title()
    df["rating"] = df["rating"].str.upper()
    
     # --- RENAME cast column as it's a reserved name ---
    if "cast" in df.columns:
        df.rename(columns={"cast": "cast_members"}, inplace=True)

    # --- SET show_id AS INDEX ---
    df.set_index("show_id", inplace=True)

    return df
