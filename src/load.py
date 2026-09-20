import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from db import get_engine


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT /"data" / "final" / "airplane_crashes_classified.csv"

def load_to_postgres(df, engine, table_name="crashes"):
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} row into '{table_name}' table")

if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    engine = get_engine()
    load_to_postgres(df, engine)