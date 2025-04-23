import pandas as pd

def get_initial_10(df):
    # Filter to one prop per player (highest Abs Edge)
    deduped = df.sort_values(by="Abs Edge", ascending=False).drop_duplicates(subset=["Player"])

    # Filter to valid stat types only (can be adjusted per sport)
    valid_stats = ["PTS", "REB", "AST", "PRA", "PR", "PA", "Hits+Runs+RBI", "Total Bases", "Strikeouts", "Outs Recorded", "Earned Runs", "Walks"]
    print("Columns in deduped:", list(deduped.columns))
    if "Stat Type" not in deduped.columns:
    deduped["Stat Type"] = ""  # fallback to empty if missing

filtered = deduped[deduped["Stat Type"].isin(valid_stats)]

    # Return top 10 props
    return filtered.head(10).reset_index(drop=True)