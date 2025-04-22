
def filter_valid_props(df):
    return df[
        (df["Line"].notnull()) &
        (df["RotoWire Projection"].notnull()) &
        (df["Site"].str.lower() == "pick6")
    ]
