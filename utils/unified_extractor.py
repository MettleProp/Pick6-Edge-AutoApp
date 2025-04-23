import pandas as pd
from utils.rotowire_miner import mine_rotowire_data

def extract_and_normalize_props(files):
    raw_dataframes = [pd.read_csv(file) for file in files]

    # MINING: extract player-level metadata before normalization
    player_metadata = mine_rotowire_data(raw_dataframes)

    # Combine all props
    combined_df = pd.concat(raw_dataframes)
    combined_df = combined_df.drop_duplicates()

    # Standardize column names
    combined_df = combined_df.rename(columns={
        "Player Name": "Player",
        "Stat": "Stat Type",
        "Proj": "RotoWire Projection"
    })

    # Merge mined metadata into each row
    def enrich_row(row):
        meta = player_metadata.get(row["Player"], {})
        for key, value in meta.items():
            row[key] = value
        return row

    enriched_df = combined_df.apply(enrich_row, axis=1)

    return enriched_df.reset_index(drop=True)