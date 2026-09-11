import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "airplane_crashes_raw.csv"

def load_raw_data(path=RAW_PATH):
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df

if __name__ == "__main__":
    load_raw_data()