
import streamlit as st
from nba.logic import run_nba_pick6
from mlb.logic import run_mlb_pick6
from app_pages import slate_result_form

st.set_page_config(page_title="Pick6 Edge App", layout="wide")
st.sidebar.title("Pick6 Navigation")

page = st.sidebar.selectbox(
    "Choose a Page:",
    ["NBA Pick6", "MLB Pick6", "Post-Slate Result Tracker"]
)

if page == "NBA Pick6":
    run_nba_pick6()
elif page == "MLB Pick6":
    run_mlb_pick6()
elif page == "Post-Slate Result Tracker":
    slate_result_form.run()  # ✅ correctly calls the form's run() function