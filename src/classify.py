import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "clean" / "airplane_crashes_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "final" / "airplane_crashes_classified.csv"

CAUSE_KEYWORDS = {
    "Hijacking/Sabotage": ["hijack", "bomb", "sabotage", "terrorist"],
    "War/Conflict": ["shot down", "shootdown", "combat", "hostile fire",
                      "missile", "attack", "war", "military action", "enemy fire"],
    "Mid-Air Collision": ["mid-air collision", "midair collision"],
    "Maintenance": [("engine", "fail"), "mechanical", "corrosion", "turbine",
                     "hydraulic", "structural failure", "disintegration",
                     "malfunction", "fatigue crack", "fatigue failure",
                     "rotor failure", "maintenance", "quality control"],
    "Weather": ["weather", "storm", "crosswind", "high seas", "heavy rain",
                 "fog", "ice", "icing", "snow", "thunderstorm", "turbulence",
                 "wind shear", "downdraft"],
    "Pilot Error": ["pilot error", "failure of the pilot", "error in judgment of the pilot",
                      "error of judgment", "error in judgement", "error of judgement",
                      "pilot failed to", "loss of control", "pilot disorientation",
                      "disoriented", "stalled", "stall", "improper", "did not properly",
                      "did not fully", "action of the pilot", "pilot's decision",
                      "delayed decision", "vfr in ifr", "fuel starvation",
                      "non-stabilized", "unstabilized"],
}

def classify_summary(summary):
    text = str(summary).lower()

    if text == "no summary available":
        return "Unknown", None

    unknown_phrases = ["unknown origin", "cause undetermined", "cause unknown", "undetermined"]
    for phrase in unknown_phrases:
        if phrase in text:
            return "Unknown", phrase

    for category, keywords in CAUSE_KEYWORDS.items():
        for keyword in keywords:
            if isinstance(keyword, tuple):
                if all(part in text for part in keyword):
                    return category, " + ".join(keyword)
            elif keyword in text:
                return category, keyword

    return "Other", None

def classify_data(df):
    results = df['Summary'].apply(classify_summary)
    df['cause_category'] = results.apply(lambda x: x[0])
    df['matched_keyword'] = results.apply(lambda x: x[1])

    print("\nCause category breakdown:")
    print(df['cause_category'].value_counts())
    return df

def save_classified_data(df, path=OUTPUT_PATH):
    df.to_csv(path, index=False)
    print(f"\nSaved classified data to {path}")

if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    df = classify_data(df)
    save_classified_data(df)