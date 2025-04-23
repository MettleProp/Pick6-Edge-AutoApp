def compute_tdbu_score(df, sport="NBA"):
    df = df.copy()

    # Pitcher-specific logic (MLB only)
    if sport == "MLB":
        pitcher_stats = ["Strikeouts", "Outs", "Earned Runs", "Hits Allowed"]
        df["Is Pitcher"] = df["Stat Type"].isin(pitcher_stats)
    else:
        df["Is Pitcher"] = False

    # Core Score: baseline = edge + confidence influence
    df["Base Score"] = df["Edge"]

    # Confidence bump: projection > line → higher trust
    df["Confidence Score"] = (
        abs(df["RotoWire Projection"] - df["Line"]) * 0.5
    )

    # Final blend
    df["TDBU Score"] = (
        df["Base Score"]
        + df["Confidence Score"]
        + df["Is Pitcher"].astype(int) * 0.5  # slight bump for pitcher props
    )

    return df.sort_values(by="TDBU Score", ascending=False).reset_index(drop=True)
