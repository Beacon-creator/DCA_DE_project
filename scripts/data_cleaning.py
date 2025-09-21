import os
from load_data import load_data
from preprocessing import preprocessing

if __name__ == "__main__":
    raw_file = "data/netflix_titles.csv"

    print("Loading raw dataset...")
    raw_df = load_data(raw_file)

    print("Cleaning dataset...")
    cleaned_df = preprocessing(raw_df)

    # --- SAVE CLEANED DATA ---
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cleaned_netflix.csv")
    cleaned_df.to_csv(output_path)

    print(f"\nCleaned dataset saved to: {output_path}")
    print("\n--- CLEANED DATA SAMPLE ---")
    print(cleaned_df.head())
