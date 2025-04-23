
def mine_rotowire_data(raw_dataframes):
    from collections import defaultdict

    player_stats = defaultdict(lambda: {
        "Stat Types": set(),
        "Appearances": 0,
        "Has Round Projection": False,
        "Is Close To Line": False,
        "Big Projection Gap": False
    })

    for df in raw_dataframes:
        for _, row in df.iterrows():
            name = row.get("Player")
            stat = row.get("Stat Type")
            proj = row.get("RotoWire Projection", 0)
            line = row.get("Line", 0)

            if not name or not stat:
                continue

            entry = player_stats[name]
            entry["Stat Types"].add(stat)
            entry["Appearances"] += 1

            # Round projection check (e.g. 18.0, 20.0)
            if float(proj) % 1 == 0:
                entry["Has Round Projection"] = True

            # Projection-line distance checks
            diff = abs(float(proj) - float(line))
            if diff < 0.5:
                entry["Is Close To Line"] = True
            if diff > 2.0:
                entry["Big Projection Gap"] = True

    # Finalize: convert stat sets to comma strings
    for p in player_stats:
        player_stats[p]["Stat Types"] = ", ".join(sorted(player_stats[p]["Stat Types"]))

    return player_stats