import streamlit as st
import pandas as pd
from utils.edge_calculator import calculate_edge
from utils.prop_filters import filter_valid_props
from utils.initial_10_filter import get_initial_10

def run_mlb_pick6(files=None):
    st.header("MLB Pick6 Analysis")
    if files is None:
        files = st.file_uploader("Upload 6 MLB stat category CSVs", type="csv", accept_multiple_files=True)
    if files and len(files) == 6:
        stat_types = ["Hits+Runs+RBI", "Total Bases", "Strikeouts", "Outs Recorded", "Earned Runs", "Walks"]
        dfs = []
        for file, stat in zip(files, stat_types):
            df = pd.read_csv(file)
            df["Stat Type"] = stat
            dfs.append(df)
        df = pd.concat(dfs, ignore_index=True)
        valid = filter_valid_props(df)
        scored = calculate_edge(valid)

        st.subheader("Top 20 MLB Props by Edge")
        top20 = scored.sort_values(by="Abs Edge", ascending=False).head(20).reset_index(drop=True)
        st.dataframe(top20[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])

        st.subheader("Initial 10 Candidates")
        initial10 = get_initial_10(top20)
        st.dataframe(initial10[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])
    else:
        st.warning("Please upload all 6 stat types: H+R+RBI, TB, Strikeouts, Outs, ER, Walks.")

