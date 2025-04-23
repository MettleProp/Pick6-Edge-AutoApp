from itertools import combinations

def build_combos(summaries):
    core = [s for s in summaries if s.get("verdict") == "Core"]
    flex = [s for s in summaries if s.get("verdict") == "Flex"]

    pick2_combos = []
    for a, b in combinations(core, 2):
        combo = {
            "Player 1": a["player"],
            "Player 2": b["player"],
            "Avg Score": round((a["score"] + b["score"]) / 2, 2),
            "Same Team": a.get("team") == b.get("team"),
            "Tags": [],
        }

        tags = []
        if a.get("team") == b.get("team"):
            tags.append("Same Team")
        if a.get("score") >= 8 and b.get("score") >= 8:
            tags.append("High Confidence")
        if "Volatile" not in a.get("tags", []) and "Volatile" not in b.get("tags", []):
            tags.append("Low Volatility")
        if a.get("edge", 0) > 2.0 and b.get("edge", 0) > 2.0:
            tags.append("Stacked Edge")

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

    pick6_entry = {
        "Players": [p["player"] for p in core + flex],
        "Avg Score": round(sum(p["score"] for p in core + flex) / 6, 2),
        "Total Edge": round(sum(p["edge"] for p in core + flex), 2),
        "Flagged": any("Volatile" in p.get("tags", []) or "Distorted" in p.get("tags", []) for p in core + flex)
    }

    return pick2_combos, pick6_entry