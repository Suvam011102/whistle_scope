import streamlit as st
import plotly.express as px

st.set_page_config("Referee Fingerprints", page_icon="⚽", layout="wide")

from analysis.referee import compute_referee_stats
from utils.session import ensure_session_state
from utils.ui import apply_global_styles, render_empty_analysis_state, render_hero, render_section_intro, render_sidebar_navigation, style_figure, render_view_switcher

ensure_session_state()
apply_global_styles()
render_sidebar_navigation()

df = st.session_state["df"]
min_matches = st.session_state["min_matches"]

render_hero(
    "Referee fingerprints",
    "Compare strictness, card behavior, and workload by official. The page now loads directly and ranks the current slice instead of hiding everything behind a button.",
    chips=["Direct ranking", "Fingerprint view", "Trendline included"],
)

ref_stats = compute_referee_stats(df, min_matches)

if ref_stats.empty:
    st.warning("No referees meet the current minimum-match threshold. Lower the sidebar filter to unlock the rankings.")
else:
    leaderboard = ref_stats.sort_values("avg_fouls", ascending=False).reset_index(drop=True)
    active_view = render_view_switcher(
        "referee_fingerprints",
        {
            "leaderboard": "Leaderboard",
            "scatter": "Strictness Map",
            "ranking": "Top Strictest",
        },
    )

    if active_view == "leaderboard":
        render_section_intro(
            "Referee leaderboard",
            "Start with the table to identify which officials consistently call tighter matches and which ones allow more flow.",
        )
        st.dataframe(leaderboard.round(2), width="stretch", hide_index=True)
    elif active_view == "scatter":
        render_section_intro(
            "Strictness versus discipline",
            "The scatter compares average fouls and average cards per referee. Bubble size reflects sample size, so bigger markers deserve more analytical trust.",
        )
        fig1 = px.scatter(
            leaderboard,
            x="avg_fouls",
            y="avg_cards",
            size="matches",
            color="matches",
            hover_name="Referee",
            title="Strictness vs discipline by referee",
        )
        style_figure(fig1)
        st.plotly_chart(fig1, width="stretch")
        st.dataframe(
            leaderboard[["Referee", "matches", "avg_fouls", "avg_cards"]].head(10).round(2),
            width="stretch",
            hide_index=True,
        )
    elif active_view == "ranking":
        render_section_intro(
            "Strictest referees in view",
            "This bar ranking surfaces the officials setting the tone most aggressively in the current filtered sample.",
        )
        fig2 = px.bar(
            leaderboard.head(12),
            x="Referee",
            y="avg_fouls",
            color="avg_cards",
            title="Top 12 strictest referees in the current slice",
        )
        fig2.update_layout(xaxis_tickangle=-35)
        style_figure(fig2)
        st.plotly_chart(fig2, width="stretch")
        st.dataframe(leaderboard.head(12).round(2), width="stretch", hide_index=True)
    else:
        render_empty_analysis_state("Press a button above to open the leaderboard, strictness map, or top-strictest ranking.")

    st.markdown(
        "The table gives you a compact shortlist, while the scatter separates whistle volume from disciplinary escalation. "
        "Large bubbles indicate referees with enough sample size to trust the shape of their profile."
    )
