
def get_initial_10(df):
    import pandas as pd

    valid_stats = [
        "PRA", "PR", "PTS+AST", "PTS+REB",
        "PTS", "REB", "AST",
        "Fantasy", "Strikeouts", "Outs"
    ]

    # Ensure "Stat Type" exists to avoid KeyError
    if "Stat Type" not in df.columns:
        df["Stat Type"] = ""

    # Optional debug: print actual columns
    # print("Initial 10 Input Columns:", df.columns.tolist())

    # Drop duplicates on Player + Stat Type
    deduped = df.drop_duplicates(subset=["Player", "Stat Type"])

    # Filter for only valid stat types
    filtered = deduped[deduped["Stat Type"].isin(valid_stats)]

    # Sort so best edge appears first for each player
    sorted_df = filtered.sort_values(by=["Player", "Edge"], ascending=[True, False])

    # One best prop per player
    best_per_player = sorted_df.drop_duplicates(subset=["Player"])

    return best_per_player.reset_index(drop=True)