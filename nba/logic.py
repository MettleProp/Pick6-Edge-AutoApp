
import streamlit as st
import pandas as pd

from utils.unified_extractor import extract_and_normalize_props
from utils.edge_calculator import calculate_edge
from utils.prop_filters import filter_valid_props
from utils.initial_10_filter import get_initial_10
from utils.tdbu_engine import compute_tdbu_score
from utils.core_verdict_engine import assign_verdicts
from utils.combo_builder import build_combos

from summary.summary_card import render_summary_card, render_summary_result_card


def run_nba_pick6(files=None):
    st.header("NBA Pick6 Analysis")

    if files is None:
        files = st.file_uploader("Upload 6 full RotoWire prop CSVs", type="csv", accept_multiple_files=True)

    if files and len(files) == 6:
        all_props = extract_and_normalize_props(files)
        valid = filter_valid_props(all_props)
        scored = calculate_edge(valid)
        tdbu_ranked = compute_tdbu_score(scored, sport="NBA")

        best_per_player = tdbu_ranked.sort_values(by=["Confidence Score", "Abs Edge"], ascending=False).drop_duplicates(subset=["Player"])
        top20 = best_per_player.head(20).reset_index(drop=True)

        st.subheader("Top 20 Props (Best per Player, TDBU Scored)")

        # Safe display with debug column listing
        st.write("Top20 Columns:", list(top20.columns))
        expected_cols = ["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge", "Confidence Score"]
        available_cols = [col for col in expected_cols if col in top20.columns]
        st.dataframe(top20[available_cols])

        initial10 = get_initial_10(top20)

        st.subheader("Initial 10 Finalists")
        st.dataframe(initial10[["Player", "Team", "Stat Type", "Line", "RotoWire Projection", "Edge"]])

        st.subheader("Prop.cash Screenshots and Apply Tags")
        summary_outputs = []
        for idx, row in initial10.iterrows():
            summary = render_summary_card(row["Player"], idx, row)
            summary["team"] = row["Team"]
            summary_outputs.append(summary)

        st.session_state["summary_cards"] = summary_outputs

        st.subheader("Final Summary Cards")
        for summary in summary_outputs:
            render_summary_result_card(summary)

        # Core 5 + 1 Verdicts
        verdicts = assign_verdicts(summary_outputs)

        st.subheader("Core 5 + 1 Verdicts")

        # Safe verdict display
        verdict_df_raw = pd.DataFrame(verdicts)
        st.write("Verdict Columns:", list(verdict_df_raw.columns))

        expected_verdict_cols = ["player", "stat_type", "line", "projection", "edge", "score", "verdict"]
        available_verdict_cols = [col for col in expected_verdict_cols if col in verdict_df_raw.columns]
        verdict_df = verdict_df_raw[available_verdict_cols]

        st.dataframe(verdict_df)

        # Combo Builder
        pick2_combos, pick6_entry = build_combos(verdicts)

        st.subheader("Top 10 Pick2 Combos")
        combo_df = pd.DataFrame(pick2_combos)
        st.dataframe(combo_df[["Player 1", "Player 2", "Avg Score", "Tags", "Verdict"]])

        st.subheader("Recommended Pick6 Combo")
        st.write("Players:", pick6_entry["Players"])
        st.write("Avg Score:", pick6_entry["Avg Score"])
        st.write("Total Edge:", pick6_entry["Total Edge"])
        if pick6_entry["Flagged"]:
            st.warning("One or more players in this Pick6 has 'Volatile' or 'Distorted' tags.")
        else:
            st.success("Pick6 combo passes tag check.")

    else:
        st.warning("Please upload 6 RotoWire prop CSVs for NBA from today’s slate.")