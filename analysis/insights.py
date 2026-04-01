"""High-level analytical summaries used across the Streamlit pages."""

import pandas as pd

from analysis.bias import compute_home_bias
from analysis.referee import compute_referee_stats
from analysis.var_impact import compute_var_impact


def build_overview_metrics(df):
    """Return dashboard-level KPI metrics for the current filtered dataset."""
    return {
        "matches": int(len(df)),
        "referees": int(df["Referee"].nunique()),
        "teams": int(pd.unique(pd.concat([df["HomeTeam"], df["AwayTeam"]])).size),
        "seasons": int(df["Season"].nunique()),
        "avg_fouls": float(df["TotalFouls"].mean()),
        "avg_cards": float(df["TotalCards"].mean()),
        "avg_goals": float(df["TotalGoals"].mean()),
        "home_win_rate": float((df["Result"] == "Home win").mean()),
    }


def build_trend_table(df):
    """Aggregate league-level trend metrics by season."""
    trend = (
        df.groupby("Season")
        .agg(
            matches=("Season", "size"),
            avg_fouls=("TotalFouls", "mean"),
            avg_cards=("TotalCards", "mean"),
            avg_goals=("TotalGoals", "mean"),
            home_bias=("HomeBias", "mean"),
        )
        .reset_index()
    )
    return trend.sort_values("Season")


def build_team_bias_table(df, min_matches):
    """Compute club-level home-versus-away foul drawing and committing deltas."""
    home = (
        df.groupby("HomeTeam")
        .agg(home_matches=("HomeTeam", "size"), home_fouls_drawn=("AF", "mean"), home_fouls_committed=("HF", "mean"))
        .rename_axis("Team")
    )
    away = (
        df.groupby("AwayTeam")
        .agg(away_matches=("AwayTeam", "size"), away_fouls_drawn=("HF", "mean"), away_fouls_committed=("AF", "mean"))
        .rename_axis("Team")
    )
    team_bias = home.join(away, how="outer").fillna(0).reset_index()
    team_bias["matches"] = team_bias["home_matches"] + team_bias["away_matches"]
    team_bias = team_bias[team_bias["matches"] >= min_matches].copy()
    team_bias["drawn_bias"] = team_bias["home_fouls_drawn"] - team_bias["away_fouls_drawn"]
    team_bias["committed_bias"] = team_bias["away_fouls_committed"] - team_bias["home_fouls_committed"]
    return team_bias.sort_values("drawn_bias", ascending=False)


def build_story_cards(df, min_matches):
    """Build compact narrative insights for the dashboard and summary pages."""
    ref_stats = compute_referee_stats(df, min_matches)
    bias = compute_home_bias(df, min_matches)
    var_summary, _ = compute_var_impact(df)
    trend = build_trend_table(df)
    team_bias = build_team_bias_table(df, min_matches)

    strictest = ref_stats.sort_values("avg_fouls", ascending=False).iloc[0] if not ref_stats.empty else None
    most_lenient = ref_stats.sort_values("avg_fouls", ascending=True).iloc[0] if not ref_stats.empty else None
    most_home_friendly = team_bias.iloc[0] if not team_bias.empty else None

    post_var_delta = 0.0
    if len(var_summary) >= 2:
        pre = var_summary[var_summary["VAR_Era"] == "Pre-VAR"]
        post = var_summary[var_summary["VAR_Era"] == "Post-VAR"]
        if not pre.empty and not post.empty:
            post_var_delta = float(post["avg_cards_per_foul"].iloc[0] - pre["avg_cards_per_foul"].iloc[0])

    latest_trend = trend.iloc[-1] if not trend.empty else None

    return {
        "strictest_referee": strictest,
        "lenient_referee": most_lenient,
        "home_bias": bias,
        "most_home_friendly_team": most_home_friendly,
        "post_var_cards_per_foul_delta": post_var_delta,
        "latest_trend": latest_trend,
    }


def build_llm_context(df, min_matches):
    """Serialize the active data slice into a compact text context block."""
    metrics = build_overview_metrics(df)
    stories = build_story_cards(df, min_matches)
    trend = build_trend_table(df).round(3)
    ref_stats = compute_referee_stats(df, min_matches).sort_values("avg_fouls", ascending=False).round(3)
    team_bias = build_team_bias_table(df, min_matches).round(3)
    var_summary, _ = compute_var_impact(df)

    strictest = stories["strictest_referee"]
    lenient = stories["lenient_referee"]
    team = stories["most_home_friendly_team"]

    lines = [
        "WhistleScope dataset context:",
        f"- Matches: {metrics['matches']}",
        f"- Referees: {metrics['referees']}",
        f"- Teams: {metrics['teams']}",
        f"- Seasons: {metrics['seasons']}",
        f"- Avg fouls per match: {metrics['avg_fouls']:.2f}",
        f"- Avg cards per match: {metrics['avg_cards']:.2f}",
        f"- Avg goals per match: {metrics['avg_goals']:.2f}",
        f"- Home win rate: {metrics['home_win_rate']:.1%}",
        f"- Mean home bias (away fouls minus home fouls): {stories['home_bias']['mean_bias']:.2f}",
        f"- Home bias p-value: {stories['home_bias']['p_value']:.4f}",
    ]

    if strictest is not None:
        lines.append(
            f"- Strictest referee by average fouls: {strictest['Referee']} ({strictest['avg_fouls']:.2f} fouls, {int(strictest['matches'])} matches)"
        )
    if lenient is not None:
        lines.append(
            f"- Most lenient referee by average fouls: {lenient['Referee']} ({lenient['avg_fouls']:.2f} fouls, {int(lenient['matches'])} matches)"
        )
    if team is not None:
        lines.append(
            f"- Team with strongest home drawn-foul edge: {team['Team']} ({team['drawn_bias']:.2f})"
        )

    lines.extend(
        [
            "",
            "Season trend table:",
            trend.to_csv(index=False),
            "",
            "Top referee rows:",
            ref_stats.head(10).to_csv(index=False),
            "",
            "Team bias rows:",
            team_bias.head(10).to_csv(index=False),
            "",
            "VAR summary:",
            var_summary.round(3).to_csv(index=False),
        ]
    )

    return "\n".join(lines)
