import pandas as pd


#define a function to load data to accepts string and returns a DataFrame
def load_data(filepath: str) -> pd.DataFrame:
    """
    Loading the data into a Pandas DataFrame with try except.
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except FileNotFoundError:
        print("File not found. Please check the path.")
        return pd.DataFrame()

if __name__ == "__main__":
    # Path to raw dataset
    raw_file = "data/netflix_titles.csv"

    # calling the function to Load dataset
    df = load_data(raw_file)

    # Print first few rows of the dataframe
    print(df.head())

