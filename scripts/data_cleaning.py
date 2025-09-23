import os
from load_data import load_data
from preprocessing import preprocessing

# Base directory -> /app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

if __name__ == "__main__":
    raw_file = os.path.join(DATA_DIR, "netflix_titles.csv")

    print(f"Loading raw dataset from {raw_file}...")
    raw_df = load_data(raw_file)

    print("Cleaning dataset...")
    cleaned_df = preprocessing(raw_df)

    # --- SAVE CLEANED DATA ---
    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, "cleaned_netflix.csv")
    cleaned_df.to_csv(output_path)

    print(f"\nCleaned dataset saved to: {output_path}")
    print("\n--- CLEANED DATA SAMPLE ---")
    print(cleaned_df.head())
