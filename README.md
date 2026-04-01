# WhistleScope

WhistleScope is a Streamlit analytics application for exploring Premier League refereeing patterns across multiple seasons.
It combines league-level summaries, referee style analysis, home-away bias checks, VAR-era comparisons, and a written analyst brief in a darker, app-style interface.

## Features

- Dashboard-first workflow with a custom sidebar and guided navigation
- Filterable multi-season dataset powered by the processed EPL match data in `data/processed/epl_master.csv`
- Referee analysis focused on strictness, foul volume, and card behavior
- Home-away bias views for both referee-team distributions and club-level patterns
- VAR impact analysis across fouls, cards, and cards-per-foul efficiency
- Analyst brief page with both a compact summary table and a narrative write-up
- Button-driven page sections so analyses load on demand instead of all at once

## Project Structure

```text
ref_insights/
├── analysis/
│   ├── bias.py
│   ├── data_loader.py
│   ├── insights.py
│   ├── referee.py
│   └── var_impact.py
├── app/
│   ├── app.py
│   └── pages/
│       ├── analyst_brief.py
│       ├── home_away_bias.py
│       ├── league_pulse.py
│       ├── referee_fingerprints.py
│       └── var_impact.py
├── data/
│   ├── processed/
│   └── raw/
├── utils/
│   ├── session.py
│   └── ui.py
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.11+ recommended
- A local virtual environment is strongly recommended

## Installation

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Running the App

```powershell
.\venv\Scripts\activate
streamlit run app\app.py
```

Once the app opens:

- Use the dashboard to choose the active seasons and minimum referee-match threshold
- Use the sidebar navigation to move between analysis modules
- Press the on-page action buttons to open the specific chart or insight view you want

## Data Notes

- The app reads from `data/processed/epl_master.csv`
- Derived fields such as `TotalFouls`, `TotalCards`, `CardsPerFoul`, `Result`, and `VAR_Era` are created in the loader
- The current data pipeline assumes season labels like `2019_20`

## Core Modules

- `analysis/data_loader.py`: Loads the processed dataset and derives core analytical fields
- `analysis/referee.py`: Computes referee-level match, foul, and card statistics
- `analysis/bias.py`: Measures home-away foul bias using grouped samples and a one-sample t-test
- `analysis/var_impact.py`: Summarizes enforcement differences before and after VAR
- `analysis/insights.py`: Builds summary metrics, trend tables, story cards, and reusable insight tables
- `utils/ui.py`: Centralizes theme styling, sidebar navigation, empty states, and chart formatting

## Development Notes

- Page modules under `app/pages/` follow `snake_case` naming for maintainability
- Shared UI helpers are centralized to keep page code small and consistent
- Plotly chart styling is applied through a shared helper to preserve readability in the dark theme
- Session state is used to retain filters and page-specific view selections

## Suggested Next Improvements

- Add automated tests for analysis helpers
- Move repeated statistical assumptions into a dedicated validation layer
- Add export options for PNG/PDF summaries
- Add referee clustering or segmentation for style archetypes
