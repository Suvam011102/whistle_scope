import streamlit as st
import plotly.express as px

st.set_page_config("League Pulse", page_icon="⚽", layout="wide")

from analysis.insights import build_overview_metrics, build_story_cards, build_trend_table
from utils.session import ensure_session_state
from utils.ui import (
    apply_global_styles,
    render_empty_analysis_state,
    render_hero,
    render_section_intro,
    render_sidebar_navigation,
    render_stat_card,
    render_story_card,
    style_figure,
    render_view_switcher,
)

ensure_session_state()
apply_global_styles()
render_sidebar_navigation()

df = st.session_state["df"]
min_matches = st.session_state["min_matches"]

metrics = build_overview_metrics(df)
stories = build_story_cards(df, min_matches)
trend = build_trend_table(df)

render_hero(
    "Executive summary with signal, not ceremony",
    "This page now loads directly from the active filter and highlights the most useful macro patterns without making you click through empty states.",
    chips=["Always-on summary", "Season trends", "Story-first layout"],
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_stat_card("Matches", metrics["matches"], "Filtered match sample")
with c2:
    render_stat_card("Teams", metrics["teams"], "Distinct clubs represented")
with c3:
    render_stat_card("Avg Cards", f"{metrics['avg_cards']:.2f}", "Cards per match")
with c4:
    render_stat_card("Avg Goals", f"{metrics['avg_goals']:.2f}", "Scoring climate")

story1, story2, story3 = st.columns(3)
with story1:
    latest_trend = stories["latest_trend"]
    body = "Trend insights will appear when at least one season is selected."
    if latest_trend is not None:
        body = (
            f"In {latest_trend['Season']}, the league averaged {latest_trend['avg_fouls']:.1f} fouls and "
            f"{latest_trend['avg_cards']:.1f} cards per match."
        )
    render_story_card("Latest Season", body)
with story2:
    render_story_card(
        "Home Advantage Context",
        f"Home sides win {metrics['home_win_rate']:.0%} of the filtered matches. "
        "That’s a useful anchor when interpreting whether whistle patterns simply mirror game state."
    )
with story3:
    render_story_card(
        "Referee Spread",
        "The downstream pages now work as a connected analysis flow: league trend first, referee profiles second, bias checks third, then a synthesized report."
    )

active_view = render_view_switcher(
    "league_pulse",
    {
        "trend": "Season Trend",
        "scatter": "Match Map",
    },
)

if active_view == "trend":
    render_section_intro(
        "Season enforcement trend",
        "This view shows how foul and card averages move season by season, which helps separate structural league shifts from one-off referee variance.",
    )
    fig1 = px.line(
        trend,
        x="Season",
        y=["avg_fouls", "avg_cards"],
        markers=True,
        title="Seasonal enforcement trend",
    )
    fig1.update_layout(legend_title_text="Metric")
    style_figure(fig1)
    st.plotly_chart(fig1, width="stretch")
    st.dataframe(trend.round(2), width="stretch", hide_index=True)
elif active_view == "scatter":
    render_section_intro(
        "Match control versus discipline",
        "Each point is a match. The scatter helps you see whether high-foul matches also escalate into high-card matches, and whether the VAR era changed that relationship.",
    )
    fig2 = px.scatter(
        df,
        x="TotalFouls",
        y="TotalCards",
        color="VAR_Era",
        hover_data=["HomeTeam", "AwayTeam", "Referee", "Season"],
        title="Match control intensity vs discipline",
    )
    style_figure(fig2)
    st.plotly_chart(fig2, width="stretch")
    scatter_insights = (
        df.groupby("VAR_Era")
        .agg(
            matches=("VAR_Era", "size"),
            avg_fouls=("TotalFouls", "mean"),
            avg_cards=("TotalCards", "mean"),
        )
        .reset_index()
    )
    st.dataframe(scatter_insights.round(2), width="stretch", hide_index=True)
else:
    render_empty_analysis_state("Press a button above to open the season trend or the match map.")
