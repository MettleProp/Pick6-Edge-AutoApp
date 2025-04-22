
import streamlit as st
from nba.logic import run_nba_pick6
from mlb.logic import run_mlb_pick6
from dfs.logic import run_dfs

st.set_page_config(page_title="Mettle Pick6 + DFS App", layout="wide")
st.title("Mettle Pick6 + DFS App")

mode = st.sidebar.radio("Select Mode", ["Pick6", "DFS"])
sport = None

if mode == "Pick6":
    sport = st.sidebar.radio("Sport", ["Auto", "NBA", "MLB"])
    if sport == "NBA":
        run_nba_pick6()
    elif sport == "MLB":
        run_mlb_pick6()
    else:
        st.info("Upload stat-type CSVs and the app will auto-detect the sport.")
        uploaded_files = st.file_uploader("Upload 6 stat-category CSVs", type="csv", accept_multiple_files=True)
        if uploaded_files and any("Outs" in f.name or "Strikeouts" in f.name for f in uploaded_files):
            run_mlb_pick6(uploaded_files)
        elif uploaded_files and any("PTS" in f.name or "REB" in f.name for f in uploaded_files):
            run_nba_pick6(uploaded_files)
        else:
            st.warning("Waiting for recognizable file names or structure...")
elif mode == "DFS":
    run_dfs()
