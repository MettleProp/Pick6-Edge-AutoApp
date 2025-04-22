import streamlit as st
import pandas as pd

from utils.unified_extractor import extract_and_normalize_props
from utils.edge_calculator import calculate_edge
from utils.prop_filters import filter_valid_props
from utils.initial_10_filter import get_initial_10
from utils.tdbu_engine import compute_tdbu_score

from summary.summary_card import render_summary_card, render_summary_result_card


def run_nba_pick6(files=None):
    st.header("NBA Pick6 Analysis")

    if files is None:
        files = st.file_uploader("Upload 6 full RotoWire prop CSVs", type="csv", accept_multiple_files=True)

    if files and len(files) == 6:
        all_props = extract_and_normalize_props(files)
        valid = filter_valid_props(all_props)
        scored = calculate_edge(valid)
        tdbu_ranked = compute_tdbu_score(scored)

        best_per_player = tdbu_ranked.sort_values(by=["Confidence Score", "Abs Edge"], ascending=False).drop_duplicates(subset=["Player"])
        top20 = best_per_player.head(20).reset_index(drop=True)

        st.subheader("Top 20 Props (Best per Player, TDBU Scored)")
        st.dataframe(top20[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge", "Confidence Score"]])

        initial10 = get_initial_10(top20)

        st.subheader("Initial 10 Finalists")
        st.dataframe(initial10[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])

        st.subheader("Prop.cash Screenshots and Apply Tags")

        summary_outputs = []
        for idx, row in initial10.iterrows():
            summary = render_summary_card(row["Player"], idx, row)
            summary_outputs.append(summary)

        st.session_state["summary_cards"] = summary_outputs

        st.subheader("Final Summary Cards")
        for summary in st.session_state.get("summary_cards", []):
            render_summary_result_card(summary)

    else:
        st.warning("Please upload 6 RotoWire prop CSVs for NBA from today’s slate.")