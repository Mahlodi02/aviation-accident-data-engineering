import pandas as pd
from pathlib import Path
from ingest import load_raw_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_PATH = PROJECT_ROOT / "data" / "clean" / "airplane_crashes_clean.csv"

def clean_data(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    df['Summary'] = df['Summary'].fillna('No summary available')
    df['Operator'] = df['Operator'].fillna("Unknown")
    df['Type'] = df['Type'].fillna("Unknown")

    keep_cols = ['Date', 'Location', 'Operator', 'Type', 'Aboard', 'Fatalities', 'Ground', 'Summary']
    df_clean = df[keep_cols].copy()

    print(f"Cleaned data: {len(df_clean)} rows, {len(df_clean.columns)} columns")
    return df_clean

def save_clean_data(df_clean, path=CLEAN_PATH):
    df_clean.to_csv(path, index=False)
    print(f"Saved cleaned data to {path}")
    
if __name__ == "__main__":
    df = load_raw_data()
    df_clean = clean_data(df)
    save_clean_data(df_clean)