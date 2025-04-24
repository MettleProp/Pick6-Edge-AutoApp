
def score_confidence(summary):
    if summary.get("override", 0) > 0:
        return float(summary["override"])

    score = 5.0
    edge = summary.get("edge", 0)
    tags = summary.get("tags", [])

    # Edge-based scoring
    if edge > 1.0:
        score += 1.0
    if edge > 1.5:
        score += 0.5

    # Penalties
    if "Volatile" in tags:
        score -= 1.0
    if "Distorted" in tags:
        score -= 1.0
    if "Narrow Misses" in tags:
        score -= 0.5
    if "High Variance" in tags:      # ✅ Stronger penalty for Fantasy Score props
        score -= 1.0

    # Bonuses
    if "Streaking" in tags:
        score += 0.5
    if "Line Moved ↑" in tags:
        score += 0.5

    return round(score, 2)


def assign_verdicts(summaries):
    # Step 1: Score all summaries
    for s in summaries:
        s["score"] = score_confidence(s)

    # Step 2: Sort by score (desc)
    sorted_summaries = sorted(summaries, key=lambda s: s["score"], reverse=True)

    # Step 3: Assign verdicts
    for i, s in enumerate(sorted_summaries):
        if i < 5:
            s["verdict"] = "Core"
        elif i == 5:
            s["verdict"] = "Flex"
        else:
            s["verdict"] = "Drop"

    return sorted_summaries