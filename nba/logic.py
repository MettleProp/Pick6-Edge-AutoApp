import streamlit as st
import pandas as pd
from utils.edge_calculator import calculate_edge
from utils.prop_filters import filter_valid_props
from utils.initial_10_filter import get_initial_10
from utils.tdbu_engine import compute_tdbu_score

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
        tdbu_ranked = compute_tdbu_score(scored)

        st.subheader("Top 20 NBA Props (TDBU Scored)")
        st.dataframe(tdbu_ranked.head(20)[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge", "Confidence Score"]])

        st.subheader("Initial 10 Finalists")
        initial10 = get_initial_10(tdbu_ranked)
        st.dataframe(initial10[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])
    else:
        st.warning("Please upload all 6 stat types: PTS, REB, AST, PRA, PR, PA.")