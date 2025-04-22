import streamlit as st
import pandas as pd

# Core logic imports
from utils.unified_extractor import extract_and_normalize_props
from utils.edge_calculator import calculate_edge
from utils.prop_filters import filter_valid_props
from utils.initial_10_filter import get_initial_10
from utils.tdbu_engine import compute_tdbu_score

# Summary card display
from summary.summary_card import render_summary_card, render_summary_result_card


def run_nba_pick6(files=None):
    st.header("NBA Pick6 Analysis")

    # Step 1 – Upload Files
    if files is None:
        files = st.file_uploader("Upload 6 full RotoWire prop CSVs", type="csv", accept_multiple_files=True)

    if files and len(files) == 6:
        # Step 2 – Normalize props
        all_props = extract_and_normalize_props(files)

        # Step 3 – Filter valid props
        valid = filter_valid_props(all_props)

        # Step 4 – Calculate edge
        scored = calculate_edge(valid)

        # Step 5 – Score props with full TDBU model
        tdbu_ranked = compute_tdbu_score(scored)

        # Step 6 – Show Top 20 table
        best_per_player = tdbu_ranked.sort_values(by=["Confidence Score", "Abs Edge"], ascending=False).drop_duplicates(subset=["Player"])
        top20 = best_per_player.head(20).reset_index(drop=True)

        st.subheader("Top 20 Props (Best per Player, TDBU Scored)")
        st.dataframe(top20[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge", "Confidence Score"]])

        # Step 7 – Initial 10
        initial10 = get_initial_10(top20)

        st.subheader("Initial 10 Finalists")
        st.dataframe(initial10[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])

        # Step 8 – Prop.cash Screenshot Uploads + Tagging
        summary_outputs = []
        st.subheader("Prop.cash Screenshots and Apply Tags")

        for idx, row in initial10.iterrows():
            summary = render_summary_card(row["Player"], idx)
            summary_outputs.append(summary)

        st.session_state["summary_cards"] = summary_outputs

        # Step 9 – Show Final OG-style Summary Cards
        st.subheader("Final Summary Cards")
        for summary in st.session_state.get("summary_cards", []):
            render_summary_result_card(summary)

    else:
        st.warning("Please upload 6 RotoWire prop CSVs for NBA from today’s slate.")