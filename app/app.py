import sys
from pathlib import Path

import streamlit as st
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from analysis.data_loader import load_data
from analysis.insights import build_overview_metrics, build_story_cards, build_trend_table
from utils.ui import (
    apply_global_styles,
    render_empty_analysis_state,
    render_hero,
    render_sidebar_intro,
    render_sidebar_navigation,
    render_stat_card,
    render_story_card,
    render_view_switcher,
)

st.set_page_config("WhistleScope", page_icon="⚽", layout="wide")


@st.cache_data
def load_cached():
    return load_data()


df = load_cached()
apply_global_styles()

if (Path("app/assets/logo.png")).exists():
    st.sidebar.image(Image.open("app/assets/logo.png"), width=160)

render_sidebar_intro(
    "Dashboard",
    "Use the navigation menu as your workflow. Filters stay visible, while the main canvas handles season slicing and league context.",
)
render_sidebar_navigation()
st.sidebar.markdown("### Filters")
min_matches = st.sidebar.slider("Minimum matches per referee", 5, 35, 15)
st.sidebar.markdown(
    """
    <div class="sidebar-shell">
        <div class="sidebar-kicker">Workflow</div>
        <div class="sidebar-copy">
            Start with <strong>Overview</strong>, compare referee styles, inspect bias patterns,
            then finish with the written analyst brief.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_hero(
    "A sharper control room for referee intelligence",
    "Use the season shelf to shape the sample, then move through the tabs to compare league trends, referee styles, home-away pressure, VAR effects, and the final analyst brief.",
    chips=[
        "Context-first layout",
        f"min {min_matches} matches/referee",
        "Premier League sample",
    ],
)

selected_seasons = st.multiselect(
    "Included seasons",
    sorted(df["Season"].unique()),
    default=st.session_state.get("selected_seasons", sorted(df["Season"].unique())),
)

df = df[df["Season"].isin(selected_seasons)]

st.session_state["df"] = df
st.session_state["min_matches"] = min_matches
st.session_state["selected_seasons"] = selected_seasons

metrics = build_overview_metrics(df)
stories = build_story_cards(df, min_matches)
trend = build_trend_table(df)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_stat_card("Matches", f"{metrics['matches']}", "Current filtered sample")
with c2:
    render_stat_card("Referees", f"{metrics['referees']}", "Unique officials in view")
with c3:
    render_stat_card("Avg Fouls", f"{metrics['avg_fouls']:.1f}", "Match control intensity")
with c4:
    render_stat_card("Home Win Rate", f"{metrics['home_win_rate']:.0%}", "Context for home advantage")

active_view = render_view_switcher(
    "dashboard",
    {
        "stories": "Key Signals",
        "table": "Insight Table",
        "guide": "How To Use",
    },
)

if active_view == "stories":
    s1, s2, s3 = st.columns(3)
    with s1:
        strictest = stories["strictest_referee"]
        body = "Not enough matches in the current filter to rank referees yet."
        if strictest is not None:
            body = (
                f"{strictest['Referee']} leads the strictness table with {strictest['avg_fouls']:.1f} fouls "
                f"and {strictest['avg_cards']:.1f} cards per match across {int(strictest['matches'])} matches."
            )
        render_story_card("Strictness Signal", body)
    with s2:
        bias = stories["home_bias"]
        render_story_card(
            "Bias Snapshot",
            f"The filtered sample shows a mean away-minus-home foul gap of {bias['mean_bias']:.2f}. "
            f"Lower p-values strengthen the case that this pattern is systematic rather than random noise.",
        )
    with s3:
        render_story_card(
            "VAR Shift",
            f"Cards per foul moved by {stories['post_var_cards_per_foul_delta']:+.3f} between the pre-VAR and post-VAR eras, "
            "which is useful for testing whether discipline became more efficient after intervention tech arrived.",
        )
elif active_view == "table":
    st.dataframe(
        trend.round(2),
        width="stretch",
        hide_index=True,
    )
elif active_view == "guide":
    st.markdown(
        """
        <div class="section-card">
            Open the pages in the left navigation to explore league trends, referee fingerprints, team bias patterns,
            VAR-era shifts, and the written analytical report.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    render_empty_analysis_state("Press one of the buttons above to open key signals, the insight table, or the usage guide.")
