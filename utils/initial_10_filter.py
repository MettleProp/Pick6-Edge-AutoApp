
def get_initial_10(df):
    import pandas as pd

    valid_stats = [
        "PRA", "PR", "PTS+AST", "PTS+REB", "PTS+REB+AST",
        "PTS", "REB", "AST",
        "Fantasy", "Strikeouts", "Outs",
        "3PM", "Blocks", "Steals"
    ]

    # Ensure "Stat Type" column exists
    if "Stat Type" not in df.columns:
        df["Stat Type"] = ""

    # Drop duplicates on player + stat type
    deduped = df.drop_duplicates(subset=["Player", "Stat Type"])

    # Filter to only valid stat types
    filtered = deduped[deduped["Stat Type"].isin(valid_stats)]

    # Sort and keep highest edge per player
    sorted_df = filtered.sort_values(by=["Player", "Edge"], ascending=[True, False])
    best_per_player = sorted_df.drop_duplicates(subset=["Player"])

    return best_per_player.reset_index(drop=True)