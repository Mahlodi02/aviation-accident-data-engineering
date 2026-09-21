import pandas as pd
from db import get_engine

EXPECTED_ROW_COUNT = 5268
VALID_CATEGORIES = {
    "Hijacking/Sabotage", "War/Conflict", "Mid-Air Collision",
    "Maintenance", "Weather", "Pilot Error", "Unknown", "Other"
}

def run_checks(df):
    checks_passed = 0
    checks_failed = 0

    def check(description, condition):
        nonlocal checks_passed, checks_failed
        if condition:
            print(f"PASS: {description}")
            checks_passed += 1
        else:
            print(f"FAIL: {description}")
            checks_failed += 1

    check(f"Row count is {EXPECTED_ROW_COUNT}", len(df) == EXPECTED_ROW_COUNT)
    check("No nulls in cause_category", df['cause_category'].isnull().sum() == 0)
    check("All cause_category values are recognized",
          set(df['cause_category'].unique()).issubset(VALID_CATEGORIES))
    check("No negative Fatalities", (df['Fatalities'].dropna() >= 0).all())
    check("No negative Aboard", (df['Aboard'].dropna() >= 0).all())
    check("No negative Ground", (df['Ground'].dropna() >= 0).all())

    dates = pd.to_datetime(df['Date'], errors='coerce')
    check("No crash dates in the future", (dates.dropna() <= pd.Timestamp.now()).all())

    print(f"\n{checks_passed} passed, {checks_failed} failed")
    return checks_failed == 0

if __name__ == "__main__":
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM crashes", engine)
    run_checks(df)