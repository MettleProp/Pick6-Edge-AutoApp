
import pandas as pd
from utils.rotowire_miner import mine_rotowire_data

def extract_and_normalize_props(files):
    raw_dataframes = [pd.read_csv(file) for file in files]

    # Step 1: mine player-level metadata
    player_metadata = mine_rotowire_data(raw_dataframes)

    # Step 2: combine all props
    combined_df = pd.concat(raw_dataframes)
    combined_df = combined_df.drop_duplicates()

    # Step 3: rename columns to unify formats
    combined_df = combined_df.rename(columns={
        "Player Name": "Player",
        "Market Name": "Stat Type",
        "Stat": "Stat Type",
        "StatType": "Stat Type",
        "Prop Type": "Stat Type",
        "Category": "Stat Type",
        "Proj": "RotoWire Projection",
        "Projection": "RotoWire Projection"
        # ❌ "Prediction" is excluded — often unreliable in MLB
    })

    # Step 4: normalize Stat Type values (handle Fantasy Score variations)
    combined_df["Stat Type"] = combined_df["Stat Type"].str.strip().str.title()
    combined_df["Stat Type"] = combined_df["Stat Type"].replace({
        "Fantasy Score": "Fantasy",
        "Fpts": "Fantasy",
        "Fpts Score": "Fantasy"
    })

    # Step 5: ensure critical columns exist
    if "Stat Type" not in combined_df.columns:
        combined_df["Stat Type"] = ""
    if "Line" not in combined_df.columns:
        combined_df["Line"] = 0.0
    if "RotoWire Projection" not in combined_df.columns:
        combined_df["RotoWire Projection"] = 0.0

    # Step 6: enrich each row with mined metadata
    def enrich_row(row):
        meta = player_metadata.get(row["Player"], {})
        for key, value in meta.items():
            row[key] = value
        return row

    enriched_df = combined_df.apply(enrich_row, axis=1)

    return enriched_df.reset_index(drop=True)