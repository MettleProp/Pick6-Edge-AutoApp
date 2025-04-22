import streamlit as st
import pandas as pd
from utils.unified_extractor import extract_and_normalize_props
from utils.edge_calculator import calculate_edge
from utils.prop_filters import filter_valid_props
from utils.initial_10_filter import get_initial_10
from utils.tdbu_engine import compute_tdbu_score
from summary.summary_card import render_summary_card, render_summary_result_card


def run_mlb_pick6(files=None):
    st.header("MLB Pick6 Analysis")

    if files is None:
        files = st.file_uploader("Upload 6 RotoWire CSV slices", type="csv", accept_multiple_files=True)

    if files and len(files) == 6:
        # Step 1: Combine all uploaded files and normalize stat types
        df = extract_and_normalize_props(files)

        # Step 2: Filter clean props
        valid = filter_valid_props(df)

        # Step 3: Score all props
        scored = calculate_edge(valid)
        tdbu_ranked = compute_tdbu_score(scored)

        # Step 4: Pick best prop per player
        best_per_player = tdbu_ranked.sort_values(by=["Confidence Score", "Abs Edge"], ascending=False).drop_duplicates(subset=["Player"])

        st.subheader("Top 20 MLB Props (Best per Player, TDBU Scored)")
        top20 = best_per_player.head(20).reset_index(drop=True)
        st.dataframe(top20[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge", "Confidence Score"]])

        # Step 5: Initial 10
        st.subheader("Initial 10 Finalists")
        initial10 = get_initial_10(top20)
        st.dataframe(initial10[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])

        # Step 6: Prop.cash upload + tagging
        st.subheader("Upload Prop.cash Screenshots and Apply Tags")
        summary_outputs = []
        for idx, row in initial10.iterrows():
            summary = render_summary_card(row["Player"], idx)
            summary_outputs.append(summary)

        st.session_state["summary_cards"] = summary_outputs

    else:
        st.warning("Please upload 6 RotoWire CSVs for MLB from today’s slate.")
     # Step 7: Show final OG-style Prop Summary Cards
    st.subheader("Final Summary Cards")
    for summary in st.session_state.get("summary_cards", []):
        render_summary_result_card(summary)   
     st.write("DEBUG:", st.session_state.get("summary_cards", []))

 