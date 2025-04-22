def filter_valid_props(df):
    # Base filtering: non-null lines, projections, and Pick6 only
    df = df[
        (df["Line"].notnull()) &
        (df["RotoWire Projection"].notnull()) &
        (df["Site"].str.lower() == "pick6")
    ].copy()

    # Stat-type-based projection sanity checks
    valid_ranges = {
        "Hits+Runs+RBI": (0.5, 3.5),
        "Total Bases": (0.5, 4.0),
        "Walks": (0.0, 2.5),
        "Strikeouts": (0.0, 12.0),
        "Outs Recorded": (14, 24),
        "Earned Runs": (0.0, 5.0),
        "PTS": (5, 45),
        "REB": (1, 20),
        "AST": (1, 15),
        "PRA": (5, 60),
        "PR": (5, 40),
        "PA": (5, 40)
    }

    def is_within_range(row):
        stat = row["Stat Type"]
        proj = row["RotoWire Projection"]
        if stat in valid_ranges:
            lo, hi = valid_ranges[stat]
            return lo <= proj <= hi
        return True  # pass through if stat type isn't defined

    df = df[df.apply(is_within_range, axis=1)].copy()

    return df