
# utils/mettle_projection.py

def get_mettle_projection(row):
    base_proj = row.get("RotoWire Projection", 0)
    if base_proj == 0:
        return 0

    adjustment = 0.0
    tags = row.get("tags", [])

    # --- Tag-based adjustments ---
    for tag in tags:
        if tag == "High Hit Rate":
            adjustment += 0.03
        if tag == "Streaking":
            adjustment += 0.02
        if tag == "Line Moved ↑":
            adjustment += 0.02
        if tag == "Cold":
            adjustment -= 0.03
        if tag == "Phantom Line":
            adjustment -= 0.05
        if tag == "Distortion Risk":
            adjustment -= 0.05
        if tag == "Market Disagreement":
            adjustment -= 0.02

    mettle_proj = base_proj * (1 + adjustment)

    # --- Vegas consensus adjustment ---
    try:
        dk_line = float(row.get("DraftKings Line", 0))
        fd_line = float(row.get("FanDuel Line", 0))
        caesars_line = float(row.get("Caesars Line", 0))
        mgm_line = float(row.get("BetMGM Line", 0))

        vegas_lines = [dk_line, fd_line, caesars_line, mgm_line]
        vegas_lines = [l for l in vegas_lines if l > 0]

        if len(vegas_lines) >= 2:
            vegas_consensus = sum(vegas_lines) / len(vegas_lines)

            # Adjust if Mettle Projection is off Vegas Consensus by 1.5+
            if mettle_proj > vegas_consensus + 1.5:
                mettle_proj = mettle_proj * 0.98
            elif mettle_proj < vegas_consensus - 1.5:
                mettle_proj = mettle_proj * 1.02
    except:
        pass

    return round(mettle_proj, 2)
