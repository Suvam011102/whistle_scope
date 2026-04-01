import streamlit as st
import plotly.express as px

st.set_page_config("VAR Era Shift", page_icon="⚽", layout="wide")

from analysis.var_impact import compute_var_impact
from utils.session import ensure_session_state
from utils.ui import apply_global_styles, render_empty_analysis_state, render_hero, render_section_intro, render_sidebar_navigation, style_figure, render_view_switcher

ensure_session_state()
apply_global_styles()
render_sidebar_navigation()

df = st.session_state["df"]

render_hero(
    "VAR era shift analysis",
    "Compare enforcement before and after VAR using a tighter layout that keeps both the summary table and distribution changes on screen.",
    chips=["Pre vs post", "Cards efficiency", "Distribution change"],
)

summary, df_var = compute_var_impact(df)
render_section_intro(
    "VAR summary table",
    "Use this table as the headline readout. It compares the league before and after VAR across fouls, cards, and cards-per-foul efficiency.",
)
st.dataframe(summary.round(3), width="stretch", hide_index=True)

active_view = render_view_switcher(
    "var_shift",
    {
        "cards": "Cards / Match",
        "efficiency": "Cards / Foul",
        "fouls": "Fouls / Match",
    },
)

if active_view == "cards":
    render_section_intro(
        "Cards per match",
        "This chart shows whether the disciplinary volume itself shifted once VAR entered the league.",
    )
    fig1 = px.box(
        df_var,
        x="VAR_Era",
        y="TotalCards",
        color="VAR_Era",
        title="Cards per match",
    )
    style_figure(fig1)
    st.plotly_chart(fig1, width="stretch")
    st.dataframe(
        df_var.groupby("VAR_Era")["TotalCards"].describe()[["mean", "50%", "std"]].round(2).reset_index(),
        width="stretch",
        hide_index=True,
    )
elif active_view == "efficiency":
    render_section_intro(
        "Cards per foul",
        "This is the cleanest measure of disciplinary efficiency. If it rises, referees are converting fewer fouls into proportionally more cards.",
    )
    fig2 = px.box(
        df_var,
        x="VAR_Era",
        y="CardsPerFoul",
        color="VAR_Era",
        title="Cards per foul",
    )
    style_figure(fig2)
    st.plotly_chart(fig2, width="stretch")
    st.dataframe(
        df_var.groupby("VAR_Era")["CardsPerFoul"].describe()[["mean", "50%", "std"]].round(3).reset_index(),
        width="stretch",
        hide_index=True,
    )
elif active_view == "fouls":
    render_section_intro(
        "Fouls per match",
        "This distribution checks whether matches became less whistle-heavy overall in the VAR era.",
    )
    fig3 = px.box(
        df_var,
        x="VAR_Era",
        y="TotalFouls",
        color="VAR_Era",
        title="Fouls per match",
    )
    style_figure(fig3)
    st.plotly_chart(fig3, width="stretch")
    st.dataframe(
        df_var.groupby("VAR_Era")["TotalFouls"].describe()[["mean", "50%", "std"]].round(2).reset_index(),
        width="stretch",
        hide_index=True,
    )
else:
    render_empty_analysis_state("Press a button above to compare cards per match, cards per foul, or fouls per match.")

st.markdown(
    "If cards per foul rise while fouls per match fall, VAR may be pushing officials toward fewer but more decisive disciplinary interventions."
)
