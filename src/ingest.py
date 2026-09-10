import pandas as pd

RAW_PATH = "data/raw/airplane_crashes_raw.csv"

def load_raw_data(path=RAW_PATH):
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns:", list(df.columns))
    print(df.head())
    return df

def explore_data(df):
    print(f"Missing values per column")
    print(df.isnull().sum())

    print("\n Summary of the first 5 rows")
    for i, summary in enumerate(df['Summary'].dropna().head(5)):
        print(f"{i+1}. {summary}\n")

        
if __name__ == "__main__":
    df = load_raw_data()
    explore_data(df)