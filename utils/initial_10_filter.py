
def get_initial_10(df):
    import pandas as pd

    valid_stats = ["PRA", "PR", "PTS+AST", "PTS+REB", "PTS", "REB", "AST", "Fantasy", "Strikeouts", "Outs"]

    # Fix missing column BEFORE deduping
    if "Stat Type" not in df.columns:
        df["Stat Type"] = ""

    deduped = df.drop_duplicates(subset=["Player", "Stat Type"])
    filtered = deduped[deduped["Stat Type"].isin(valid_stats)]

    sorted_df = filtered.sort_values(by=["Player", "Edge"], ascending=[True, False])
    best_per_player = sorted_df.drop_duplicates(subset=["Player"])

    return best_per_player.reset_index(drop=True)
