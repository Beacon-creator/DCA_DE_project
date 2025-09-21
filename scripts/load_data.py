import pandas as pd

# Function to load dataset
def load_data(filepath: str) -> pd.DataFrame:
    """
    Loading the dataset into a Pandas DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded has {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except FileNotFoundError:
        print("no file found")
        return pd.DataFrame()

if __name__ == "__main__":
    # Path to the dataset
    raw_file = "data/netflix_titles.csv"

    #calling Load dataset function
    df = load_data(raw_file)

    # Print first few rows of the dataframe
    print(df.head())
