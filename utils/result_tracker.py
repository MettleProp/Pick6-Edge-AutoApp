
# utils/result_tracker.py
import pandas as pd
from datetime import datetime


def evaluate_prop_result(stat_type, line, result):
    try:
        return "HIT" if float(result) > float(line) else "MISS"
    except:
        return "ERROR"


def evaluate_pick2_combos(core_props):
    from itertools import combinations
    combos = []
    for a, b in combinations(core_props, 2):
        p1_hit = a["result"] == "HIT"
        p2_hit = b["result"] == "HIT"
        outcome = "WIN" if p1_hit and p2_hit else "LOSS"
        combos.append({
            "Player 1": a["player"],
            "Player 2": b["player"],
            "Result": outcome
        })
    return combos


def evaluate_pick6(core_props, flex):
    all_props = core_props + [flex]
    hits = sum(1 for p in all_props if p["result"] == "HIT")
    if hits == 6:
        return "FULL WIN"
    elif hits == 5:
        return "PARTIAL WIN"
    else:
        return "LOSS"


def build_slate_log(date_str, core_props, flex, combos, pick6_outcome, stake_per_pick2=5, stake_pick6=10):
    pick2_wins = sum(1 for c in combos if c["Result"] == "WIN")
    pick2_losses = len(combos) - pick2_wins
    pick2_return = pick2_wins * 15  # $5 to win $15 per win
    pick2_spent = len(combos) * stake_per_pick2

    pick6_return = 0
    if pick6_outcome == "FULL WIN":
        pick6_return = 150
    elif pick6_outcome == "PARTIAL WIN":
        pick6_return = 30

    total_spent = pick2_spent + stake_pick6
    total_return = pick2_return + pick6_return
    net = total_return - total_spent

    return pd.DataFrame([{
        "Date": date_str,
        "Core 5 Hits": sum(1 for p in core_props if p["result"] == "HIT"),
        "Pick2 Wins": pick2_wins,
        "Pick2 Losses": pick2_losses,
        "Pick6 Outcome": pick6_outcome,
        "Spent": total_spent,
        "Returned": total_return,
        "Net": net
    }])


def export_slate_to_csv(log_df, filename="slate_log_master.csv"):
    try:
        old = pd.read_csv(filename)
        combined = pd.concat([old, log_df], ignore_index=True)
    except:
        combined = log_df
    combined.to_csv(filename, index=False)
    return combined
