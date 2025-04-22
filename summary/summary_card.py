import streamlit as st

def render_summary_card(player_name, index):
    st.markdown(f"### {index+1}. {player_name}")

    col1, col2 = st.columns(2)
    with col1:
        shot1 = st.file_uploader(f"Upload Trend Screenshot for {player_name}", type=["png", "jpg", "jpeg"], key=f"{player_name}_trend")
    with col2:
        shot2 = st.file_uploader(f"Upload Notes Screenshot for {player_name}", type=["png", "jpg", "jpeg"], key=f"{player_name}_notes")

    tags = st.multiselect(
        f"Apply Tags for {player_name}",
        ["Volatile", "Distorted", "Role Up", "Role Down", "Playoff Motivation"],
        key=f"{player_name}_tags"
    )

    override_score = st.slider(
        f"Confidence Override for {player_name} (Optional)", 1, 10, value=0, key=f"{player_name}_override"
    )

    return {
        "player": player_name,
        "trend_img": shot1,
        "notes_img": shot2,
        "tags": tags,
        "override": override_score
    }