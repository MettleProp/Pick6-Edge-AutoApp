
def filter_valid_props(df):
    import pandas as pd

    # ✅ 1. Drop duplicate columns that can cause reindexing issues
    df = df.loc[:, ~df.columns.duplicated()]

    # ✅ 2. Optional: debug print to see current structure
    # print("Filter Props Columns:", df.columns.tolist())

    # ✅ 3. Filter out any rows with missing Line or Projection values
    df = df[df["Line"].notnull()]
    df = df[df["RotoWire Projection"].notnull()]

    return df.reset_index(drop=True)