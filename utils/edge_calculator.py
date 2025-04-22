
def calculate_edge(df):
    df["Edge"] = df["RotoWire Projection"] - df["Line"]
    df["Abs Edge"] = df["Edge"].abs()
    return df
