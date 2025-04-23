
from itertools import combinations
import pandas as pd

def build_combos(summaries):
    core = [s for s in summaries if s.get("verdict") == "Core"]
    flex = [s for s in summaries if s.get("verdict") == "Flex"]

    pick2_combos = []

    # Only build combos if at least 2 Core props exist
    if len(core) >= 2:
        for a, b in combinations(core, 2):
            combo = {
                "Player 1": a.get("player", "N/A"),
                "Player 2": b.get("player", "N/A"),
                "Avg Score": round((a.get("score", 0) + b.get("score", 0)) / 2, 2),
                "Same Team": a.get("team") == b.get("team"),
                "Tags": [],
            }

            # Combo Tags
            tags = []
            if a.get("team") == b.get("team"):
                tags.append("Same Team")
            if a.get("score", 0) >= 8 and b.get("score", 0) >= 8:
                tags.append("High Confidence")
            if "Volatile" not in a.get("tags", []) and "Volatile" not in b.get("tags", []):
                tags.append("Low Volatility")
            if a.get("edge", 0) > 2.0 and b.get("edge", 0) > 2.0:
                tags.append("Stacked Edge")

            # Verdict logic
            if "Same Team" in tags:
                verdict = "Avoid Combo"
            elif "Low Volatility" in tags and "High Confidence" in tags:
                verdict = "Safe Combo"
            elif "Stacked Edge" in tags:
                verdict = "Ceiling Combo"
            else:
                verdict = "Playable"

            combo["Tags"] = ", ".join(tags)
            combo["Verdict"] = verdict
            pick2_combos.append(combo)

    # Pick6 Combo: only build if 5 Core and 1 Flex
    pick6_entry = {
        "Players": [p.get("player", "N/A") for p in core + flex],
        "Avg Score": round(sum(p.get("score", 0) for p in core + flex) / 6, 2) if len(core + flex) == 6 else 0,
        "Total Edge": round(sum(p.get("edge", 0) for p in core + flex), 2) if len(core + flex) == 6 else 0,
        "Flagged": any("Volatile" in p.get("tags", []) or "Distorted" in p.get("tags", []) for p in core + flex)
    }

    combo_df = pd.DataFrame(pick2_combos)
    return combo_df, pick6_entry