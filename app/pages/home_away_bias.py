import streamlit as st
import plotly.express as px

st.set_page_config("Home-Away Pressure", page_icon="⚽", layout="wide")

from analysis.bias import compute_home_bias
from analysis.insights import build_team_bias_table
from utils.session import ensure_session_state
from utils.ui import apply_global_styles, render_empty_analysis_state, render_hero, render_section_intro, render_sidebar_navigation, style_figure, render_view_switcher

ensure_session_state()
apply_global_styles()
render_sidebar_navigation()

df = st.session_state["df"]
min_matches = st.session_state["min_matches"]

render_hero(
    "Home-away bias explorer",
    "Look at structural bias from two angles: referee-team foul differentials and club-level home versus away drawing patterns.",
    chips=["Distribution view", "Team lens", "Foul differential"],
)

result = compute_home_bias(df, min_matches)
bias_df = result["data"]
team_bias = build_team_bias_table(df, min_matches)

metric1, metric2 = st.columns(2)
metric1.metric("Mean Bias (Away - Home)", round(result["mean_bias"], 2))
metric2.metric("p-value", round(result["p_value"], 4))

active_view = render_view_switcher(
    "home_away_pressure",
    {
        "distribution": "Bias Distribution",
        "clubs": "Club Edge",
    },
)

if active_view == "distribution":
    render_section_intro(
        "Referee-team bias distribution",
        "Positive values mean away teams are called for more fouls than home teams within the grouped sample. The dashed line marks neutral territory.",
    )
    fig = px.histogram(
        bias_df,
        x="HomeBias",
        nbins=40,
        title="Referee-team foul differential distribution",
    )
    fig.add_vline(x=0, line_dash="dash")
    style_figure(fig)
    st.plotly_chart(fig, width="stretch")
    if not bias_df.empty:
        bias_summary = (
            bias_df["HomeBias"]
            .describe()[["mean", "std", "min", "25%", "50%", "75%", "max"]]
            .round(2)
            .rename_axis("metric")
            .reset_index(name="value")
        )
        st.dataframe(bias_summary, width="stretch", hide_index=True)
elif active_view == "clubs":
    if team_bias.empty:
        st.info("No teams meet the current threshold for a club-level bias table.")
    else:
        render_section_intro(
            "Club-level home edge",
            "This ranking highlights which clubs draw the strongest home whistle advantage relative to their away matches.",
        )
        fig2 = px.bar(
            team_bias.head(12),
            x="Team",
            y="drawn_bias",
            color="matches",
            title="Teams with the strongest home foul-drawn edge",
        )
        fig2.update_layout(xaxis_tickangle=-35)
        style_figure(fig2)
        st.plotly_chart(fig2, width="stretch")
        st.dataframe(
            team_bias[["Team", "matches", "drawn_bias", "committed_bias"]].head(12).round(2),
            width="stretch",
            hide_index=True,
        )
else:
    render_empty_analysis_state("Press a button above to open the bias distribution or the club-edge ranking.")

st.markdown(
    "Positive values mean away sides are whistled more often than home sides. "
    "The extra team chart helps separate referee-level bias from club-context effects like crowd pressure or tactical style."
)
