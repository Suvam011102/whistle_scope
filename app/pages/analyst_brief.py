import streamlit as st
import numpy as np

st.set_page_config("Analyst Brief", page_icon="⚽", layout="wide")

from analysis.referee import compute_referee_stats
from analysis.bias import compute_home_bias
from analysis.insights import build_overview_metrics
from analysis.var_impact import compute_var_impact
from utils.session import ensure_session_state
from utils.ui import apply_global_styles, render_empty_analysis_state, render_hero, render_section_intro, render_sidebar_navigation, render_view_switcher

ensure_session_state()
apply_global_styles()
render_sidebar_navigation()

df = st.session_state["df"]
min_matches = st.session_state["min_matches"]

render_hero(
    "Narrative report",
    "A cleaner written synthesis of the active data slice. This page now generates immediately from the chosen filters and reads more like a briefing note than raw dashboard text.",
    chips=["Auto-generated", "Filter-aware", "Shareable summary"],
)

ref = compute_referee_stats(df, min_matches)
bias = compute_home_bias(df, min_matches)
summary, _ = compute_var_impact(df)
metrics = build_overview_metrics(df)

if ref.empty or summary.empty:
    st.warning("The report needs at least one valid referee sample and VAR summary in the current filter.")
else:
    iqr = np.percentile(ref["avg_fouls"], 75) - np.percentile(ref["avg_fouls"], 25)
    pre = summary[summary["VAR_Era"] == "Pre-VAR"].iloc[0]
    post = summary[summary["VAR_Era"] == "Post-VAR"].iloc[0]
    strictest = ref.sort_values("avg_fouls", ascending=False).iloc[0]
    lenient = ref.sort_values("avg_fouls", ascending=True).iloc[0]

    report = f"""
### Executive framing
The current slice covers **{metrics['matches']} matches** across **{metrics['seasons']} seasons** with **{metrics['referees']} referees**.
Average match intensity sits at **{metrics['avg_fouls']:.2f} fouls** and **{metrics['avg_cards']:.2f} cards**.

### Referee consistency
Referee foul enforcement shows meaningful spread rather than a single league-wide style.
The interquartile range of average fouls is **{iqr:.2f}**, with **{strictest['Referee']}** at the strict end
({strictest['avg_fouls']:.2f} fouls per match) and **{lenient['Referee']}** at the lenient end
({lenient['avg_fouls']:.2f} fouls per match).

### Home-away bias
The average away-minus-home foul differential is **{bias['mean_bias']:.2f}**, with a p-value of **{bias['p_value']:.4f}**.
That points to a modest aggregate bias signal, though the magnitude still looks small enough that team and game-state context matter.

### VAR impact
After VAR, average fouls moved from **{pre.avg_fouls:.2f}** to **{post.avg_fouls:.2f}**,
while cards per foul shifted from **{pre.avg_cards_per_foul:.3f}** to **{post.avg_cards_per_foul:.3f}**.
That pattern suggests a change in disciplinary efficiency, not just more random whistle behavior.

### Bottom line
This filtered sample supports a league story where officiating is broadly consistent at the system level,
but still shaped by individual referee style, mild home-context effects, and a VAR-era recalibration in discipline.
"""

    render_section_intro(
        "Briefing note",
        "This page is designed as a shareable written summary. The table below gives the same story in compact numbers before the prose interpretation.",
    )
    report_table = [
        {"Insight": "Matches", "Value": metrics["matches"]},
        {"Insight": "Referees", "Value": metrics["referees"]},
        {"Insight": "Avg fouls", "Value": round(metrics["avg_fouls"], 2)},
        {"Insight": "Avg cards", "Value": round(metrics["avg_cards"], 2)},
        {"Insight": "Mean bias", "Value": round(bias["mean_bias"], 2)},
        {"Insight": "Bias p-value", "Value": round(bias["p_value"], 4)},
        {"Insight": "Pre-VAR fouls", "Value": round(pre.avg_fouls, 2)},
        {"Insight": "Post-VAR fouls", "Value": round(post.avg_fouls, 2)},
    ]
    active_view = render_view_switcher(
        "analyst_brief",
        {
            "summary": "Summary Table",
            "report": "Written Brief",
        },
    )
    if active_view == "summary":
        st.dataframe(report_table, width="stretch", hide_index=True)
    elif active_view == "report":
        st.markdown(report)
    else:
        render_empty_analysis_state("Press a button above to open the summary table or the written brief.")
    st.download_button(
        "Download report as Markdown",
        data=report,
        file_name="whistlescope_report.md",
        mime="text/markdown",
    )
