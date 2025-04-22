
import streamlit as st
import pandas as pd
from utils.edge_calculator import calculate_edge
from utils.prop_filters import filter_valid_props

def run_nba_pick6(files=None):
    st.header("NBA Pick6 Analysis")
    if files is None:
        files = st.file_uploader("Upload 6 NBA stat category CSVs", type="csv", accept_multiple_files=True)
    if files and len(files) == 6:
        stat_types = ["PTS", "REB", "AST", "PRA", "PR", "PA"]
        dfs = []
        for file, stat in zip(files, stat_types):
            df = pd.read_csv(file)
            df["Stat Type"] = stat
            dfs.append(df)
        df = pd.concat(dfs, ignore_index=True)
        valid = filter_valid_props(df)
        scored = calculate_edge(valid)
        top = scored.sort_values(by="Abs Edge", ascending=False).head(20)
        st.subheader("Top 20 NBA Props")
        st.dataframe(top[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])
    else:
        st.warning("Please upload all 6 stat types: PTS, REB, AST, PRA, PR, PA.")
