# Washington State EV Adoption — Interactive Dashboard

**Data Visualization Project — Part 2: Charts & Dashboard**

An interactive data storytelling web application built with Dash + Plotly,
exploring 280,000+ electric vehicle registrations in Washington State.

## What's inside

Four story-driven charts plus a unified interactive dashboard:

1. **Adoption over time** — BEV vs PHEV registrations by model year
2. **Market share** — Top 10 manufacturers (Tesla holds ~41%)
3. **Range evolution** — Median electric range by year and EV type
4. **Geographic concentration** — Top 10 counties by EV count

Interactive controls:
- Model Year range slider
- County dropdown
- EV Type radio buttons (All / BEV / PHEV)

All four charts update simultaneously based on the active filters.

## Dataset

- **Source**: Washington State Department of Licensing — Electric Vehicle Population Data
- **Size**: ~280,000 rows, 16 columns
- **Coverage**: 1999–2026 model years, 99.75% Washington State

## Data cleaning

- Dropped 12 rows with missing geographic info (insignificant: ~0.004%)
- Dropped 700+ rows missing the Electric Utility field
- Filtered to Washington State only (99.75% of records) for narrative consistency
- Removed 24 incomplete 2027-model-year records
- For Electric Range, `0` values represent "not reported" rather than literal zero,
  so they are imputed with the mean range grouped by (Make, Model Year)
- A separate `Electric Range Reported` column preserves the original NaN structure
  for charts that should only show actual reported values (Chart 3)

## Project structure

```
ev_dashboard/
├── app.py              # Main Dash application
├── clean_data.py       # Data cleaning script
├── ev_clean.csv        # Cleaned dataset (generated)
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment config (Render/Railway)
├── assets/
│   └── styles.css      # Custom dashboard styling
└── README.md
```

## Run locally

```bash
pip install -r requirements.txt
python clean_data.py        # generates ev_clean.csv (one-time)
python app.py               # serves on http://localhost:8050
```

## Deploy

The app is configured for one-click deployment on Render or Railway:

1. Push this folder to a GitHub repo
2. On Render: New Web Service → connect repo → Build: `pip install -r requirements.txt`
   → Start: `gunicorn app:server`
3. Paste the live URL into the IEEE report (page 1)

## Tech stack

- **Dash 2.18** — Python web framework for analytical apps
- **Plotly 5.24** — Interactive charting
- **Pandas 2.2** — Data wrangling
- **Custom CSS** — Space Grotesk + Inter typography, dark theme

## Key insights surfaced

- EV registrations grew **~11x** between 2015 and 2024
- **Tesla** alone holds **40.9%** of the market — more than the next 8 makers combined
- **King County** contains nearly half (49.2%) of all WA EVs
- BEV share of new registrations climbed from **70%** (2018) to **88%** (2023)
- Median BEV range nearly **quadrupled** between 2013 (75 mi) and 2020 (291 mi)
