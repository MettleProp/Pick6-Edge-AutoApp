
def generate_auto_tags(row):
    tags = []

    # VOLATILE: if edge is high but projection is close to line
    if abs(row["Edge"]) > 1.5 and abs(row["RotoWire Projection"] - row["Line"]) < 1.0:
        tags.append("Volatile")

    # DISTORTED: if projection is far below line
    if row["RotoWire Projection"] < row["Line"] - 1.0:
        tags.append("Distorted")

    # STREAKING: fake it for now — later we use Prop.cash logs
    if "PTS" in row["Stat Type"] and row["RotoWire Projection"] > row["Line"] + 2:
        tags.append("Streaking")

    # NARROW MISSES: flag if edge is low but still projected over
    if 0 < row["Edge"] < 0.7:
        tags.append("Narrow Misses")

    # LINE SPIKE: manual for now — add auto detection later
    if row.get("Line Moved", False):
        tags.append("Line Moved ↑")

    return tags