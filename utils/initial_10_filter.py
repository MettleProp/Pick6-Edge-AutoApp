def get_initial_10(df):
    import pandas as pd

    valid_stats = ["PRA", "PR", "PTS+AST", "PTS+REB", "PTS", "REB", "AST", "Fantasy", "Strikeouts", "Outs"]

    deduped = df.drop_duplicates(subset=["Player", "Stat Type"])

    # Safety fallback in case 'Stat Type' is missing
    if "Stat Type" not in deduped.columns:
        deduped["Stat Type"] = ""

    filtered = deduped[deduped["Stat Type"].isin(valid_stats)]

    # Tiebreaker by best edge
    sorted_df = filtered.sort_values(by=["Player", "Edge"], ascending=[True, False])

    best_per_player = sorted_df.drop_duplicates(subset=["Player"])

    return best_per_player.reset_index(drop=True)