import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from db import get_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_top_aircraft_by_cause(engine, top_n=10):
    query = """
        SELECT "Type", cause_category, COUNT(*) as crash_count
        FROM crashes
        WHERE "Type" IN (
            SELECT "Type" FROM crashes
            GROUP BY "Type"
            ORDER BY COUNT(*) DESC
            LIMIT %(top_n)s
        )
        GROUP BY "Type", cause_category
        ORDER BY "Type", crash_count DESC
    """
    return pd.read_sql(query, engine, params={"top_n": top_n})

def plot_aircraft_causes(df, output_path):
    pivot = df.pivot(index="Type", columns="cause_category", values="crash_count").fillna(0)
    pivot["total"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("total", ascending=True).drop(columns="total")

    pivot.plot(kind="barh", stacked=True, figsize=(10, 6))
    plt.title("Crash Cause Breakdown by Aircraft Type (Top 10 Most-Crashed)")
    plt.xlabel("Number of Crashes")
    plt.ylabel("Aircraft Type")
    plt.legend(title="Cause", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved chart to {output_path}")

def get_crashes_by_decade(engine):
    query = 'SELECT "Date", cause_category FROM crashes'
    df = pd.read_sql(query, engine)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['decade'] = (df['Date'].dt.year // 10 * 10).astype('Int64')
    return df.dropna(subset=['decade'])

def plot_causes_by_decade(df, output_path):
    counts = df.groupby(['decade', 'cause_category']).size().unstack(fill_value=0)
    proportions = counts.div(counts.sum(axis=1), axis=0) * 100

    proportions.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab10')
    plt.title("Crash Cause Breakdown by Decade (% of crashes)")
    plt.xlabel("Decade")
    plt.ylabel("Percentage of Crashes")
    plt.legend(title="Cause", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved chart to {output_path}")

    unknown_other_trend = proportions[['Unknown', 'Other']].sum(axis=1)
    print("\n% of crashes classified as Unknown or Other, by decade:")
    print(unknown_other_trend.round(1))

if __name__ == "__main__":
    engine = get_engine()
    df = get_top_aircraft_by_cause(engine)
    print(df)
    plot_aircraft_causes(df, OUTPUT_DIR / "crashes_by_aircraft_type.png")
    plot_causes_by_decade(get_crashes_by_decade(engine), OUTPUT_DIR / "crashes_by_decade.png")