
import pandas as pd
from utils.rotowire_miner import mine_rotowire_data

def extract_and_normalize_props(files):
    raw_dataframes = [pd.read_csv(file) for file in files]

    # Step 1: mine player-level metadata
    player_metadata = mine_rotowire_data(raw_dataframes)

    # Step 2: combine all props
    combined_df = pd.concat(raw_dataframes)
    combined_df = combined_df.drop_duplicates()

    # Step 3: rename RotoWire columns to our standard format
    combined_df = combined_df.rename(columns={
        "Player Name": "Player",
        "Market Name": "Stat Type",         # ✅ NEW: handles RotoWire's naming
        "Stat": "Stat Type",
        "StatType": "Stat Type",
        "Prop Type": "Stat Type",
        "Category": "Stat Type",
        "Proj": "RotoWire Projection",
        "Projection": "RotoWire Projection"
    })

    # Step 4: ensure essential columns exist
    if "Stat Type" not in combined_df.columns:
        combined_df["Stat Type"] = ""
    if "Line" not in combined_df.columns:
        combined_df["Line"] = 0.0
    if "RotoWire Projection" not in combined_df.columns:
        combined_df["RotoWire Projection"] = 0.0

    # Step 5: enrich rows with metadata
    def enrich_row(row):
        meta = player_metadata.get(row["Player"], {})
        for key, value in meta.items():
            row[key] = value
        return row

    enriched_df = combined_df.apply(enrich_row, axis=1)

    return enriched_df.reset_index(drop=True)