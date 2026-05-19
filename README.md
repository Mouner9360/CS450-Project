# Washington State EV Adoption — Interactive Dashboard

> An interactive data storytelling dashboard exploring 280,000+ electric vehicle registrations in Washington State.

![Built with](https://img.shields.io/badge/built%20with-Dash%20%2B%20Plotly-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## Live Demo

**[cs450-project-l8yg.onrender.com](https://cs450-project-l8yg.onrender.com/)**

---

## About

Electric vehicle adoption is reshaping transportation in the U.S., and Washington State is at the forefront. This dashboard makes it easy to explore over 280,000 EV registrations through four interconnected, story-driven visualizations.

Each chart answers a different question — how fast are EVs growing? Who dominates the market? How has battery range improved? Where are EVs concentrated geographically? — and all four update simultaneously through unified interactive controls.

The data comes from the Washington State Department of Licensing and covers model years 1999–2026, with careful cleaning to handle missing values, impute unreported ranges, and ensure narrative consistency.

---

## Features

- **Adoption Over Time** — Area chart showing BEV vs PHEV registrations by model year
- **Market Share** — Horizontal bar chart of top 10 manufacturers (Tesla holds ~41%)
- **Range Evolution** — Line chart of median electric range by year and EV type
- **Geographic Concentration** — Top 10 counties by EV registrations
- **Unified Filters** — Model year range slider, county dropdown, and EV type selector that control all charts simultaneously
- **KPI Cards** — At-a-glance metrics for total vehicles, Tesla share, King County share, BEV share, and unique manufacturers

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Dash 2.18 |
| Charting | Plotly 5.24 |
| Data Processing | Pandas 2.2 |
| Server | Gunicorn 23.0 |
| Styling | Custom CSS (Space Grotesk + Inter, dark theme) |
| Deployment | Render |

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/Mouner9360/CS450-Project.git
cd CS450-Project
pip install -r requirements.txt
```

### Running Locally

```bash
python clean_data.py   # generates ev_clean.csv (one-time)
python app.py           # serves on http://localhost:8050
```

Open [http://localhost:8050](http://localhost:8050) in your browser.

---

## Deployment

Deployed on **Render** with one-click setup:

1. Connect the GitHub repo on Render
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:server`

---

## Key Insights

- EV registrations grew **~11x** between 2015 and 2024
- **Tesla** alone holds **40.9%** of the market — more than the next 8 makers combined
- **King County** contains nearly half (49.2%) of all WA EVs
- BEV share climbed from **70%** (2018) to **88%** (2023)
- Median BEV range nearly **quadrupled** between 2013 (75 mi) and 2020 (291 mi)

---

## Dataset

- **Source**: Washington State Department of Licensing — Electric Vehicle Population Data
- **Size**: ~280,000 rows, 16 columns
- **Coverage**: 1999–2026 model years, 99.75% Washington State

---

## Project Structure

```
ev_dashboard/
├── app.py              # Main Dash application
├── clean_data.py       # Data cleaning script
├── ev_clean.csv        # Cleaned dataset (generated)
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment config (Render)
├── assets/
│   └── styles.css      # Custom dashboard styling
└── previews/           # Chart screenshots
```

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## License

[MIT](LICENSE)

---

## Author

**Mouner Wissa**
- Portfolio: [mouner9360.github.io/portfolio](https://mouner9360.github.io/portfolio)
- LinkedIn: [linkedin.com/in/mouner-wissa-8493a1282](https://www.linkedin.com/in/mouner-wissa-8493a1282/)
- GitHub: [@Mouner9360](https://github.com/Mouner9360)
