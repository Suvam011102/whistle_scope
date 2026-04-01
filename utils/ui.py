"""Shared Streamlit UI helpers for the WhistleScope dashboard."""

import streamlit as st


def apply_global_styles():
    """Inject the shared dark theme and component styling."""
    st.markdown(
        """
        <style>
            :root {
                --bg-deep: #0a0a0a;
                --bg-panel: #121212;
                --bg-panel-alt: #181818;
                --bg-card: rgba(24, 24, 24, 0.96);
                --bg-card-soft: rgba(30, 30, 30, 0.94);
                --text-strong: #f5f7fa;
                --text-muted: #a8b0bb;
                --text-inverse: #f5f7fa;
                --accent: #1ed760;
                --accent-soft: rgba(30, 215, 96, 0.16);
                --border-soft: rgba(255, 255, 255, 0.08);
            }
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(30, 215, 96, 0.09), transparent 24%),
                    radial-gradient(circle at top right, rgba(77, 171, 247, 0.08), transparent 26%),
                    linear-gradient(180deg, #090909 0%, #111111 100%);
                color: var(--text-strong);
            }
            [data-testid="stAppViewContainer"] {
                background: transparent;
            }
            [data-testid="stHeader"] {
                background: transparent !important;
                height: 0;
                border: 0;
            }
            [data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at top, rgba(30, 215, 96, 0.08), transparent 28%),
                    linear-gradient(180deg, #0c0c0c 0%, #151515 100%);
                border-right: 1px solid rgba(255, 255, 255, 0.06);
            }
            [data-testid="stSidebar"] * {
                color: var(--text-inverse);
            }
            [data-testid="stSidebar"] svg {
                fill: currentColor;
            }
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1.1rem;
            }
            [data-testid="stSidebarNav"] {
                display: none;
            }
            .sidebar-nav {
                background: rgba(255, 255, 255, 0.025);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 18px;
                padding: 0.55rem;
                margin: 0 0 1rem 0;
            }
            .sidebar-nav-label {
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.16em;
                color: rgba(30, 215, 96, 0.92);
                margin-bottom: 0.4rem;
                text-align: center;
            }
            .sidebar-nav [data-testid="stPageLink"] a {
                border-radius: 14px;
                margin-bottom: 0.22rem;
                background: transparent;
            }
            .sidebar-nav [data-testid="stPageLink"] a:hover {
                background: rgba(30, 215, 96, 0.11);
            }
            .sidebar-nav [data-testid="stPageLinkCurrent"] a {
                background: linear-gradient(135deg, rgba(30, 215, 96, 0.18), rgba(30, 215, 96, 0.06));
                border: 1px solid rgba(30, 215, 96, 0.22);
            }
            [data-testid="stSidebarUserContent"] {
                padding-top: 0.2rem;
            }
            .block-container {
                padding-top: 1.6rem;
                padding-bottom: 2.4rem;
                max-width: 1320px;
            }
            [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stMarkdownContainer"],
            [data-testid="stMarkdownContainer"],
            [data-testid="stText"],
            p,
            li,
            label,
            h1,
            h2,
            h3,
            h4,
            h5,
            h6,
            span {
                color: var(--text-strong);
            }
            .stMarkdown,
            .stCaption,
            .stMetric,
            .stDataFrame,
            .stAlert,
            .stPlotlyChart,
            .stExpander,
            .stTextInput,
            .stTextArea,
            .stSelectbox,
            .stMultiSelect,
            .stSlider,
            .stDataFrameGlideDataEditor,
            .stTable {
                color: var(--text-strong);
            }
            .stDataFrame, .stTable {
                background: rgba(24, 24, 24, 0.9);
                border-radius: 18px;
            }
            .stInfo, .stSuccess, .stWarning, .stError {
                color: var(--text-strong);
            }
            [data-testid="stMetricValue"],
            [data-testid="stMetricLabel"],
            [data-testid="stMetricDelta"] {
                color: var(--text-strong);
            }
            [data-testid="stMarkdownContainer"] a {
                color: #7dd3fc;
            }
            [data-testid="stMarkdownContainer"] strong {
                color: #ffffff;
            }
            .stSelectbox label,
            .stMultiSelect label,
            .stSlider label,
            .stTextInput label,
            .stTextArea label,
            .stToggle label {
                color: var(--text-inverse);
            }
            [data-testid="stSidebar"] .stSelectbox label,
            [data-testid="stSidebar"] .stMultiSelect label,
            [data-testid="stSidebar"] .stSlider label,
            [data-testid="stSidebar"] .stTextInput label,
            [data-testid="stSidebar"] .stTextArea label,
            [data-testid="stSidebar"] .stToggle label,
            [data-testid="stSidebar"] .stCaption {
                color: rgba(247, 241, 231, 0.88);
            }
            .stSelectbox div[data-baseweb="select"] > div,
            .stMultiSelect div[data-baseweb="select"] > div,
            .stTextInput input,
            .stTextArea textarea {
                background: rgba(28, 28, 28, 0.96);
                color: var(--text-strong);
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
            [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
            [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div,
            [data-testid="stSidebar"] .stTextInput input,
            [data-testid="stSidebar"] .stTextArea textarea {
                background: rgba(255, 255, 255, 0.08);
                color: var(--text-inverse);
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
            [data-baseweb="tag"] {
                background: rgba(30, 215, 96, 0.18) !important;
                color: #effff4 !important;
                border: 1px solid rgba(30, 215, 96, 0.22) !important;
            }
            [data-testid="stSidebar"] [data-baseweb="tag"] {
                background: rgba(30, 215, 96, 0.16) !important;
                color: #effff4 !important;
            }
            .stSlider [data-baseweb="slider"] > div > div {
                background: var(--accent);
            }
            .stButton > button,
            .stDownloadButton > button {
                border-radius: 999px;
                border: 1px solid rgba(255, 255, 255, 0.12);
                background: linear-gradient(135deg, #1a1a1a, #222222);
                color: var(--text-inverse);
                transition: transform 0.16s ease, box-shadow 0.16s ease;
                box-shadow: 0 10px 24px rgba(0, 0, 0, 0.24);
            }
            .stButton > button:hover,
            .stDownloadButton > button:hover {
                transform: translateY(-1px);
                border-color: rgba(30, 215, 96, 0.28);
                box-shadow: 0 14px 28px rgba(0, 0, 0, 0.3);
            }
            .hero-card {
                padding: 1.55rem 1.6rem;
                border-radius: 24px;
                background: linear-gradient(135deg, rgba(18, 18, 18, 0.98), rgba(28, 28, 28, 0.98));
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 22px 60px rgba(0, 0, 0, 0.28);
                color: var(--text-inverse);
                margin-bottom: 1.1rem;
            }
            .hero-kicker {
                text-transform: uppercase;
                letter-spacing: 0.22em;
                font-size: 0.74rem;
                color: var(--accent);
                margin-bottom: 0.35rem;
            }
            .hero-title {
                font-size: 2.2rem;
                line-height: 1.05;
                font-weight: 800;
                margin-bottom: 0.6rem;
                color: #ffffff;
            }
            .hero-copy {
                font-size: 1rem;
                max-width: 46rem;
                color: rgba(245, 247, 250, 0.8);
            }
            .stat-card {
                background: var(--bg-card);
                border: 1px solid var(--border-soft);
                border-radius: 20px;
                padding: 1rem 1.1rem;
                box-shadow: 0 14px 34px rgba(0, 0, 0, 0.16);
                min-height: 124px;
                margin-bottom: 0.85rem;
            }
            .stat-label {
                font-size: 0.8rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #9fb0a7;
                margin-bottom: 0.35rem;
            }
            .stat-value {
                font-size: 1.9rem;
                font-weight: 800;
                color: #ffffff;
                margin-bottom: 0.2rem;
            }
            .stat-help {
                font-size: 0.92rem;
                color: #a8b0bb;
            }
            .section-card {
                background: var(--bg-card);
                border-radius: 22px;
                padding: 1.2rem 1.25rem;
                border: 1px solid var(--border-soft);
                box-shadow: 0 18px 34px rgba(0, 0, 0, 0.14);
                margin-bottom: 1rem;
            }
            .story-card {
                background: linear-gradient(180deg, rgba(24, 24, 24, 0.98), rgba(30, 30, 30, 0.98));
                border-radius: 20px;
                border: 1px solid var(--border-soft);
                padding: 1rem;
                min-height: 156px;
                margin-bottom: 0.85rem;
            }
            .story-title {
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--accent);
                margin-bottom: 0.5rem;
            }
            .story-body {
                font-size: 1rem;
                line-height: 1.5;
                color: #d6dbe1;
            }
            .section-intro {
                background: var(--bg-card-soft);
                border: 1px solid var(--border-soft);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                margin: 0.35rem 0 0.9rem 0;
                box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
            }
            .section-title {
                font-size: 1rem;
                font-weight: 800;
                color: #ffffff;
                margin-bottom: 0.25rem;
            }
            .section-copy {
                font-size: 0.95rem;
                line-height: 1.5;
                color: var(--text-muted);
            }
            .insight-chip {
                display: inline-block;
                padding: 0.34rem 0.68rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: #eefbf2;
                font-size: 0.78rem;
                margin-right: 0.35rem;
                margin-bottom: 0.35rem;
            }
            .sidebar-shell {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
            }
            .sidebar-kicker {
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.18em;
                color: rgba(30, 215, 96, 0.92);
                margin-bottom: 0.35rem;
            }
            .sidebar-icon {
                width: 1.7rem;
                height: 1.7rem;
                margin-bottom: 0.55rem;
                color: var(--text-inverse);
            }
            .sidebar-title {
                font-size: 1.2rem;
                font-weight: 800;
                color: var(--text-inverse);
                margin-bottom: 0.35rem;
            }
            .sidebar-copy {
                font-size: 0.92rem;
                line-height: 1.45;
                color: rgba(247, 241, 231, 0.76);
            }
            .js-plotly-plot .plotly .gtitle,
            .js-plotly-plot .plotly .xtitle,
            .js-plotly-plot .plotly .ytitle,
            .js-plotly-plot .plotly .legendtitletext,
            .js-plotly-plot .plotly .xtick text,
            .js-plotly-plot .plotly .ytick text {
                fill: #d8dee6 !important;
            }
            @media (max-width: 900px) {
                .block-container {
                    padding-top: 1rem;
                }
                .hero-title {
                    font-size: 1.8rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_intro(title, copy):
    """Render the dashboard-only sidebar header card."""
    icon = """
    <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 5.5h16M4 12h16M4 18.5h16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
        <path d="M6 4v2.8M12 10.5v3M18 16.8v2.7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
    </svg>
    """
    st.markdown(
        f"""
        <div class="sidebar-shell">
            <div class="sidebar-icon">{icon}</div>
            <div class="sidebar-kicker">Control Room</div>
            <div class="sidebar-title">{title}</div>
            <div class="sidebar-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_navigation():
    """Render a custom navigation block with stable, professional page labels."""
    st.sidebar.markdown("<div class='sidebar-nav'><div class='sidebar-nav-label'>Navigation</div>", unsafe_allow_html=True)
    st.sidebar.page_link("app.py", label="◫ Dashboard")
    st.sidebar.page_link("pages/league_pulse.py", label="◌ League Pulse")
    st.sidebar.page_link("pages/referee_fingerprints.py", label="◇ Referee Fingerprints")
    st.sidebar.page_link("pages/home_away_bias.py", label="△ Home-Away Bias")
    st.sidebar.page_link("pages/var_impact.py", label="▷ VAR Impact")
    st.sidebar.page_link("pages/analyst_brief.py", label="▤ Analyst Brief")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)


def render_section_intro(title, copy):
    """Render a short explanatory section header above a chart or table."""
    st.markdown(
        f"""
        <div class="section-intro">
            <div class="section-title">{title}</div>
            <div class="section-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_view_switcher(page_key, options, default_key=None):
    """Render a button group and return the currently selected view key."""
    state_key = f"{page_key}_active_view"

    if default_key is None:
        default_key = None

    # Reset invalid stored state while preserving the intentional empty initial state.
    if st.session_state.get(state_key) not in options and st.session_state.get(state_key) is not None:
        st.session_state[state_key] = default_key
    elif state_key not in st.session_state:
        st.session_state[state_key] = default_key

    columns = st.columns(len(options))
    for column, (option_key, label) in zip(columns, options.items()):
        button_type = "primary" if st.session_state[state_key] == option_key else "secondary"
        if column.button(label, key=f"{page_key}_{option_key}", type=button_type, use_container_width=True):
            st.session_state[state_key] = option_key

    return st.session_state[state_key]


def render_empty_analysis_state(message="Choose one of the buttons above to load an analysis view."):
    """Render a neutral empty state before the user selects an analysis view."""
    st.markdown(
        f"""
        <div class="section-card" style="padding: 2rem 1.4rem; text-align: center;">
            <div class="section-title" style="margin-bottom: 0.45rem;">Analysis Ready</div>
            <div class="section-copy">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title, copy, chips=None):
    """Render the primary page hero card."""
    chips_html = ""
    if chips:
        chips_html = "".join(f"<span class='insight-chip'>{chip}</span>" for chip in chips)
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-kicker">WhistleScope</div>
            <div class="hero-title">{title}</div>
            <div class="hero-copy">{copy}</div>
            <div style="margin-top: 0.9rem;">{chips_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig):
    """Apply the shared dark Plotly theme so charts remain readable."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(24,24,24,0.92)",
        font={"color": "#d8dee6"},
        title={"font": {"color": "#ffffff", "size": 18}},
        legend={"font": {"color": "#d8dee6"}, "title": {"font": {"color": "#d8dee6"}}},
        margin={"t": 56, "b": 36, "l": 36, "r": 24},
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.08)",
        color="#cfd6df",
        title_font={"color": "#e8edf2"},
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.08)",
        color="#cfd6df",
        title_font={"color": "#e8edf2"},
    )
    return fig


def render_stat_card(label, value, help_text):
    """Render a KPI card used on the dashboard and summary pages."""
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_story_card(title, body):
    """Render a short narrative insight card."""
    st.markdown(
        f"""
        <div class="story-card">
            <div class="story-title">{title}</div>
            <div class="story-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
