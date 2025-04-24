
def generate_auto_tags(row, sport="NBA"):
    tags = []

    # RotoWire mining tags
    if row.get("Appearances", 0) >= 3:
        tags.append("Multi-Stat Core")
    if row.get("Has Round Projection"):
        tags.append("Low Confidence")
    if row.get("Is Close To Line"):
        tags.append("Projection Trap")
    if row.get("Big Projection Gap"):
        tags.append("Sharp")

    # ✅ MLB-specific volatility tag for Fantasy Score props
    if sport == "MLB" and row.get("Stat Type") == "Fantasy":
        tags.append("High Variance")

    # Projection + edge logic
    edge = row.get("Edge", 0)
    if abs(edge) > 1.5 and abs(row["RotoWire Projection"] - row["Line"]) < 1.0:
        tags.append("Volatile")
    if row["RotoWire Projection"] < row["Line"] - 1.0:
        tags.append("Distorted")
    if "PTS" in row.get("Stat Type", "") and row["RotoWire Projection"] > row["Line"] + 2:
        tags.append("Streaking")
    if 0 < edge < 0.7:
        tags.append("Narrow Misses")

    # Hit rate insights
    if row.get("Weighted Hit Rate", 0) >= 65:
        tags.append("High Hit Rate")
    if row.get("Hit Rate Factor", 0) <= -30:
        tags.append("Cold")

    return tags