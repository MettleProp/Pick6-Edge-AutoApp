import pandas as pd

def compute_tdbu_score(df):
    # Normalize base edge
    df["Edge"] = df["RotoWire Projection"] - df["Line"]
    df["Abs Edge"] = df["Edge"].abs()

    # Phantom line flag: unreasonable projections or edge distortion
    df["Phantom Flag"] = (
        (df["Line"] > df["RotoWire Projection"] * 1.4) |
        (df["Line"] < df["RotoWire Projection"] * 0.6)
    )

    # Volatility tagging (placeholder: can evolve later)
    df["Volatility Flag"] = df["Player"].str.contains("Jr|II|III")  # Simple flag example

    # Confidence scoring (1–10)
    df["Confidence Score"] = 5
    df.loc[df["Phantom Flag"], "Confidence Score"] -= 2
    df.loc[df["Volatility Flag"], "Confidence Score"] -= 1
    df.loc[df["Abs Edge"] > 1.0, "Confidence Score"] += 1
    df.loc[df["Abs Edge"] > 1.5, "Confidence Score"] += 1
    df["Confidence Score"] = df["Confidence Score"].clip(1, 10)

    # Sort for output
    return df.sort_values(by=["Confidence Score", "Abs Edge"], ascending=False).reset_index(drop=True)