
def get_initial_10(df):
    import pandas as pd

    valid_stats = [
        "PRA", "PR", "PTS+AST", "PTS+REB", "PTS+REB+AST",
        "PTS", "REB", "AST",
        "Fantasy", "Strikeouts", "Outs",
        "3PM", "Blocks", "Steals"
    ]

    # Ensure "Stat Type" column is present
    if "Stat Type" not in df.columns:
        df["Stat Type"] = ""

    # Drop duplicate props by player + stat type
    deduped = df.drop_duplicates(subset=["Player", "Stat Type"])

    # Only keep props with desired stat categories
    filtered = deduped[deduped["Stat Type"].isin(valid_stats)]

    # Pick best prop per player (highest edge)
    sorted_df = filtered.sort_values(by=["Player", "Edge"], ascending=[True, False])
    best_per_player = sorted_df.drop_duplicates(subset=["Player"])

    # ✅ Return only the top 10
    return best_per_player.head(10).reset_index(drop=True)
