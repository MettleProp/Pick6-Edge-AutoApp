def filter_valid_props(df):
    # Base filtering
    df = df[
        (df["Line"].notnull()) &
        (df["RotoWire Projection"].notnull()) &
        (df["Site"].str.lower() == "pick6")
    ].copy()

    # Stat-type-specific expected ranges
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

    def is_valid(row):
        stat = row.get("Stat Type") or row.get("Stat") or ""
        line = row["Line"]
        proj = row["RotoWire Projection"]
        if stat in valid_ranges:
            lo, hi = valid_ranges[stat]
            return lo <= line <= hi and lo <= proj <= hi
        return True

    df = df[df.apply(is_valid, axis=1)].copy()
    return df