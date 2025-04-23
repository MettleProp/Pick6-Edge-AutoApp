import streamlit as st
from utils.auto_tagger import generate_auto_tags

def render_summary_card(player_name, index, row):
    st.markdown(f"### {index+1}. {player_name}")

    # Auto-generate tags based on row data
    auto_tags = generate_auto_tags(row)

    col1, col2 = st.columns(2)
    with col1:
        shot1 = st.file_uploader(
            f"Upload Trend Screenshot for {player_name}",
            type=["png", "jpg", "jpeg"],
            key=f"{player_name}_trend"
        )
    with col2:
        shot2 = st.file_uploader(
            f"Upload Notes Screenshot for {player_name}",
            type=["png", "jpg", "jpeg"],
            key=f"{player_name}_notes"
        )

    tags = st.multiselect(
        f"Tags for {player_name}",
        ["Volatile", "Distorted", "Role Up", "Role Down", "Playoff Motivation", "Streaking", "Line Moved ↑", "Narrow Misses"],
        default=auto_tags,
        key=f"{player_name}_tags"
    )

    override_score = st.slider(
        f"Confidence Override for {player_name} (Optional)",
        1, 10, value=0,
        key=f"{player_name}_override"
    )

    return {
        "player": player_name,
        "trend_img": shot1,
        "notes_img": shot2,
        "tags": tags,
        "override": override_score,
        "stat_type": row["Stat Type"],
        "line": row["Line"],
        "projection": row["RotoWire Projection"],
        "edge": row["Edge"]
    }

def render_summary_result_card(summary):
    st.markdown("---")
    st.markdown(f"### {summary['player']}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Stat Type:** {summary.get('stat_type', '—')}")
        st.markdown(f"**Line:** {summary.get('line', '—')}")
        st.markdown(f"**Projection:** {summary.get('projection', '—')}")
        st.markdown(f"**Edge:** {summary.get('edge', '—')}")
        st.markdown(f"**Confidence Score:** {summary.get('override', '—') if summary.get('override', 0) > 0 else 'Auto'}")

    with col2:
        st.markdown("**Tags:**")
        if summary.get("tags"):
            for tag in summary["tags"]:
                st.markdown(f"- {tag}")
        else:
            st.markdown("*No tags applied*")

    if summary.get("trend_img"):
        st.image(summary["trend_img"], caption="Trend Screenshot", width=250)
    if summary.get("notes_img"):
        st.image(summary["notes_img"], caption="Notes Screenshot", width=250)
