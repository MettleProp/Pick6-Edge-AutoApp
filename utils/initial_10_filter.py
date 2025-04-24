
def get_initial_10(df):
    import pandas as pd

    valid_stats = [
        "PRA", "PR", "PTS+AST", "PTS+REB", "PTS+REB+AST",
        "PTS", "REB", "AST",
        "FANTASY", "STRIKEOUTS", "OUTS",
        "3PM", "BLOCKS", "STEALS"
    ]

    if "Stat Type" not in df.columns:
        df["Stat Type"] = ""

    # ✅ Normalize stat types to uppercase
    df["Stat Type"] = df["Stat Type"].astype(str).str.strip().str.upper()

    deduped = df.drop_duplicates(subset=["Player", "Stat Type"])
    filtered = deduped[deduped["Stat Type"].isin(valid_stats)]

    sorted_df = filtered.sort_values(by=["Player", "Edge"], ascending=[True, False])
    best_per_player = sorted_df.drop_duplicates(subset=["Player"])

    return best_per_player.head(10).reset_index(drop=True)
