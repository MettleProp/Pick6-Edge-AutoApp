
import streamlit as st
from utils.result_tracker import (
    evaluate_prop_result,
    evaluate_pick2_combos,
    evaluate_pick6,
    build_slate_log,
    export_slate_to_csv
)
from datetime import date

st.header("Post-Slate Result Tracker")

# Input: Slate date
today = date.today().strftime("%Y-%m-%d")
date_str = st.text_input("Enter slate date (YYYY-MM-DD):", value=today)

# Input: Core 5 + Flex final results
st.subheader("Enter Final Stats for Core 5")
core_props = []
for i in range(5):
    st.markdown(f"### Core {i+1}")
    player = st.text_input(f"Player {i+1}", key=f"player_{i}")
    stat_type = st.selectbox(
        f"Stat Type {i+1}",
        ["PRA", "PTS", "REB", "AST", "PR", "Fantasy", "Strikeouts", "Outs"],
        key=f"stat_{i}"
    )
    line = st.number_input(f"Line {i+1}", key=f"line_{i}")
    result = st.number_input(f"Final Stat {i+1}", key=f"result_{i}")
    outcome = evaluate_prop_result(stat_type, line, result)
    core_props.append({
        "player": player,
        "stat_type": stat_type,
        "line": line,
        "result_val": result,
        "result": outcome
    })

# Input: Flex player
st.subheader("Enter Final Stat for Flex Player")
flex_player = st.text_input("Flex Player", key="flex_player")
flex_stat_type = st.selectbox(
    "Flex Stat Type",
    ["PRA", "PTS", "REB", "AST", "PR", "Fantasy", "Strikeouts", "Outs"],
    key="flex_stat"
)
flex_line = st.number_input("Flex Line", key="flex_line")
flex_result = st.number_input("Flex Final Stat", key="flex_result")
flex_outcome = evaluate_prop_result(flex_stat_type, flex_line, flex_result)
flex = {
    "player": flex_player,
    "stat_type": flex_stat_type,
    "line": flex_line,
    "result_val": flex_result,
    "result": flex_outcome
}

# Score Combos and Pick6
if st.button("Score Slate"):
    st.success("Scoring in progress...")

    combos = evaluate_pick2_combos(core_props)
    pick6_result = evaluate_pick6(core_props, flex)
    slate_log = build_slate_log(date_str, core_props, flex, combos, pick6_result)
    export_slate_to_csv(slate_log)

    st.subheader("Slate Summary")
    st.dataframe(slate_log)

    st.subheader("Pick2 Combo Outcomes")
    st.dataframe(combos)

    st.success("Slate logged successfully and added to slate_log_master.csv")
