
def score_confidence(summary):
    # Manual override always takes priority
    if summary.get("override", 0) > 0:
        return float(summary["override"])

    score = 5.0  # Base score

    # Boost for strong edge
    edge = summary.get("edge", 0)
    if edge > 1.0:
        score += 1.0
    if edge > 1.5:
        score += 0.5

    # Penalties from tags
    tags = summary.get("tags", [])
    if "Volatile" in tags:
        score -= 1.0
    if "Distorted" in tags:
        score -= 1.0
    if "Narrow Misses" in tags:
        score -= 0.5

    # Bonuses from tags
    if "Streaking" in tags:
        score += 0.5
    if "Line Moved ↑" in tags:
        score += 0.5

    return round(score, 2)


def assign_verdicts(summaries):
    # Step 1: Add scores to summaries
    for s in summaries:
        s["score"] = score_confidence(s)

    # Step 2: Sort by score
    sorted_summaries = sorted(summaries, key=lambda s: s["score"], reverse=True)

    # Step 3: Assign verdict
    for i, s in enumerate(sorted_summaries):
        if i < 5:
            s["verdict"] = "Core"
        elif i == 5:
            s["verdict"] = "Flex"
        else:
            s["verdict"] = "Drop"

    return sorted_summaries
