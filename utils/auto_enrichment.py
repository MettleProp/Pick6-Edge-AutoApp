
def apply_enrichments(row):
    tags = []

    # 1. Phantom Line / Distortion Risk
    try:
        sportsbook_line = float(row.get("DraftKings Line", 0))
        pick6_line = float(row.get("Line", 0))
        if abs(pick6_line - sportsbook_line) > 1.5:
            tags.append("Phantom Line")
        if abs(pick6_line - sportsbook_line) > 2.0:
            tags.append("Distortion Risk")
    except:
        pass

    # 2. Lean Agreement Check (safely parse lean string)
    lean_raw = row.get("Lean", "")
    lean = str(lean_raw).strip().lower() if isinstance(lean_raw, str) else ""
    edge = row.get("Edge", 0)
    if lean == "more" and edge < 0:
        tags.append("Market Disagreement")
    elif lean == "less" and edge > 0:
        tags.append("Market Disagreement")
    elif (lean == "more" and edge > 0) or (lean == "less" and edge < 0):
        tags.append("Lean Aligned")

    # 3. Hit Rate Pattern Tags
    try:
        last5 = float(row.get("Hit Rate: Last 5", 0))
        if last5 >= 80:
            tags.append("Streaking")
        elif last5 <= 40:
            tags.append("Cold")
    except:
        pass

    # 4. Line Movement Tags
    try:
        line_change = float(row.get("Line Change", 0))
        if line_change > 0.5:
            tags.append("Line Moved ↑")
        elif line_change < -0.5:
            tags.append("Line Moved ↓")
        if abs(line_change) > 1.5:
            tags.append("Distortion Risk")
    except:
        pass

    return tags