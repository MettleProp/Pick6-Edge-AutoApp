# TEMP: Force refresh on Streamlit

import streamlit as st
from nba.logic import run_nba_pick6
from mlb.logic import run_mlb_pick6
from dfs.logic import run_dfs


def detect_sport_from_files(files):
    """
    Determine whether the uploaded stat files correspond to NBA or MLB by scanning filenames and content.
    Returns "NBA", "MLB", or None if uncertain.
    """
    found_nba = False
    found_mlb = False
    nba_terms = ["points", "rebounds", "assists", "3pt", "three-pointer", "fantasy score", "pra"]
    mlb_terms = ["rbi", "earned run", "total bases", "pitcher strikeouts", "hits allowed", "singles", "outs", "hits+runs+rbi"]

    for file in files:
        fname_lower = file.name.lower()
        if "nba" in fname_lower:
            found_nba = True
        if "mlb" in fname_lower:
            found_mlb = True

        try:
            content_bytes = file.read()
            file.seek(0)
        except Exception:
            try:
                content_bytes = file.getvalue()
            except Exception:
                content_bytes = b""

        content_lower = content_bytes.decode("utf-8", errors="ignore").lower()
        if any(term in content_lower for term in nba_terms):
            found_nba = True
        if any(term in content_lower for term in mlb_terms):
            found_mlb = True

    if found_nba and not found_mlb:
        return "NBA"
    if found_mlb and not found_nba:
        return "MLB"
    return None

# Main App
st.set_page_config(page_title="Mettle Pick6 + DFS App", layout="wide")
st.title("Mettle Pick6 + DFS App")

mode = st.sidebar.radio("Select Mode", ["Pick6", "DFS"])
sport = None

if mode == "Pick6":
    sport = st.sidebar.selectbox("Sport", ["Auto", "NBA", "MLB"])
    st.header("Pick6 Mode")

    uploaded_files = st.file_uploader("Upload 6 stat-category CSVs", type="csv", accept_multiple_files=True)

    if uploaded_files is None or len(uploaded_files) == 0:
        st.info("Please upload 6 CSV files to analyze Pick6 predictions.")
    elif len(uploaded_files) != 6:
        st.error("Please upload exactly 6 CSV files for Pick6 mode.")
    else:
        if sport == "Auto":
            detected_sport = detect_sport_from_files(uploaded_files)
            if detected_sport == "NBA":
                st.success("Detected sport: NBA")
                run_nba_pick6(uploaded_files)
            elif detected_sport == "MLB":
                st.success("Detected sport: MLB")
                run_mlb_pick6(uploaded_files)
            else:
                st.warning("Sport could not be determined automatically. Please select NBA or MLB and try again.")
        elif sport == "NBA":
            run_nba_pick6(uploaded_files)
        elif sport == "MLB":
            run_mlb_pick6(uploaded_files)

elif mode == "DFS":
    st.header("DFS Mode")
    uploaded_file = st.file_uploader("Upload DFS CSV file", type="csv")
    if uploaded_file is None:
        st.info("Please upload a CSV file to analyze DFS predictions.")
    else:
        run_dfs(uploaded_file)

