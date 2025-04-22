import pandas as pd

# Mapping RotoWire market names to simplified stat types
STAT_TYPE_MAP = {
    "Points": "PTS",
    "Rebounds": "REB",
    "Assists": "AST",
    "Points + Rebounds + Assists": "PRA",
    "Points + Rebounds": "PR",
    "Points + Assists": "PA",
    "Hits+Runs+RBI": "HRRBI",
    "Total Bases": "TB",
    "Outs Recorded": "Outs",
    "Strikeouts": "Strikeouts",
    "Walks": "Walks",
    "Earned Runs": "ER"
}

def extract_and_normalize_props(uploaded_files):
    combined = []
    for file in uploaded_files:
        df = pd.read_csv(file)
        if "Market Name" in df.columns:
            df["Stat Type"] = df["Market Name"].map(STAT_TYPE_MAP)
        combined.append(df)

    all_props = pd.concat(combined, ignore_index=True)
    all_props = all_props[all_props["Stat Type"].notnull()]  # Drop rows we can’t classify

    return all_props.reset_index(drop=True)