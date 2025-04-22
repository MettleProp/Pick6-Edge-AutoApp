import streamlit as st
from nba.logic import run_nba_pick6
from mlb.logic import run_mlb_pick6
from dfs.logic import run_dfs

st.set_page_config(page_title="Pick6 + DFS Edge App", layout="wide")
st.title("Pick6 + DFS Edge App")

tab = st.sidebar.radio("Choose Mode", ["Pick6", "DFS"])
sport = st.sidebar.radio("Sport", ["NBA", "MLB"])

if tab == "Pick6":
    if sport == "NBA":
        run_nba_pick6()
    else:
        run_mlb_pick6()
elif tab == "DFS":
    run_dfs()
