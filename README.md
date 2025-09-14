# Scraping & Visualization (Assignment 2)

This repository contains utilities and example scripts for crawling, parsing and visualizing climate and water-level data for a short course project. The code demonstrates simple web scraping (with local caching), parsing HTML/JSON responses, converting scraped tables into CSV, and plotting results using Matplotlib. There are also small SVG drawing experiments.

Contents
--------
- `scraping_utils.py` – helper functions: `get_url` (fetch + local cache) and `parse` (HTML or JSON).
- `multi_city_temp.py` – example that loads multiple city climate JSON pages and prints simple data from each.
- `draw_svg.py`, `geometric-shapes.svg`, `irregular-polygon.svg` – small drawing examples using `drawsvg` and shipped SVGs.
- `city-1.json`, `city-2.json`, `city-3.json` – example JSON outputs for the multi-city climate parsing demo.
- `crawled-page-2023.html`, `test_page.html` – saved HTML pages used by the scraping examples.
- `requirements.txt` – Python packages required.

Quick setup
-----------
1. Create and activate a virtual environment (macOS / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file at the repository root with the environment variables used by the scripts. Example `.env` values used by the data scripts:

```ini
# Assignment 2 — Scraping & Visualisation (rainfall, wind)

This repository started as a set of small scraping and plotting examples for climate and water-level data. It now includes additional scripts to fetch, parse and visualise Hong Kong Observatory (HKO) rainfall and wind data for the Kai Tak station.

Main contents
-------------
- `scraping_utils.py` — helper functions: `get_url(url, filename)` (fetch + cache) and `parse(page, mode)` (HTML or JSON parsing helpers).
- (archived water-level examples removed)
- `multi_city_temp.py` — small multi-city JSON demo.
- `scripts/` — new scripts for the HKO data processing and plotting (see below).
- `week02_notebook.ipynb` — notebook updated to prefer locally generated CSVs and to display the generated plots inline.

New HKO rainfall & wind scripts (Kai Tak)
----------------------------------------
These scripts fetch the HKO station-block CSVs (the HKO files are organised as blocks per station) and produce processed CSVs and plots for the Kai Tak station:

- `scripts/fetch_kaitak_wind.py` — fetches the HKO wind CSV and writes `kaitak_wind_{START}_{END}.csv` and a PNG plot (`kaitak_wind_{START}_{END}.png`).
- `scripts/fetch_daily_rainfall_kaitak.py` — parses the HKO rainfall CSV station block for Kai Tak and writes `rainfall_processed.csv` (daily rows: `datetime,rainfall_mm`), then regenerates `7.svg`.
- `scripts/make_7_svg.py` — generates a simple summary SVG `7.svg` showing mean wind and total rainfall.
- `scripts/make_monthly_wind_rain.py` — aggregates monthly rainfall totals and monthly mean wind and writes `monthly_wind_rain.png` and `monthly_wind_rain.svg` (bar + line dual-axis chart).
- `scripts/test_fetch_kaitak_wind.py` — pytest unit test for the wind parser.
- `scripts/notebook_append_cells.py` — helper used to append display cells to the notebook (used during development).

Environment variables
---------------------
Create a `.env` (gitignored) at the repository root with the following variables (examples included in `.env.example`):

- `RAINFALL_URL` — HKO rainfall CSV endpoint (default used in examples: `https://data.weather.gov.hk/weatherAPI/cis/csvfile/SE/ALL/daily_SE_RF_ALL.csv`)
- `WIND_URL` — HKO wind CSV endpoint (default used in examples: `https://data.weather.gov.hk/cis/csvfile/SE/ALL/daily_SE_WSPD_ALL.csv`)
- `RAINFALL_STATION_NAME` — station substring to filter for rainfall (default `Kaitak`)
- `WIND_STATION_NAME` — station substring for wind (default `KaiTak`)
- `START_YEAR`, `END_YEAR` — year bounds for filtering (defaults: `2010` and `2025`)

Quick setup
-----------
1. Create and activate a virtual environment (macOS / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` in the repo root (or edit `.env.example`) with the keys above.

How to regenerate the processed data and plots
---------------------------------------------
Run these commands from the project root (example with the venv python):

```bash
# Fetch and process wind data for Kai Tak
PYTHONPATH=. .venv/bin/python scripts/fetch_kaitak_wind.py

# Fetch and process rainfall for Kai Tak and regenerate 7.svg
PYTHONPATH=. .venv/bin/python scripts/fetch_daily_rainfall_kaitak.py

# Create monthly aggregated charts (monthly_wind_rain.png and monthly_wind_rain.svg)
.venv/bin/python scripts/make_monthly_wind_rain.py
```

Files produced by the scripts
----------------------------
- `kaitak_wind_{START}_{END}.csv` — daily mean wind for the Kai Tak station.
- `kaitak_wind_{START}_{END}.png` — simple time-series plot of daily mean wind.
- `rainfall_processed.csv` — daily rainfall for Kai Tak in `datetime,rainfall_mm` format.
- `7.svg` — simple summary SVG (mean wind and total rainfall).
- `monthly_wind_rain.png`, `monthly_wind_rain.svg` — monthly aggregated chart (rainfall bars, wind line).

Notebook
--------
`week02_notebook.ipynb` has been updated to prefer loading the generated `kaitak_wind_...csv` and `rainfall_processed.csv` if they are present. The notebook also includes cells that display `monthly_wind_rain.svg` and `7.svg` inline (run the final notebook cells to render them).

Version control notes
---------------------
- Generated assets (the two SVGs `7.svg` and `monthly_wind_rain.svg`, the monthly PNG and selected CSVs) have been added to the `remove-lecturer-notes` branch. If you prefer not to track generated files, remove them and add patterns to `.gitignore`.

Testing
-------
- `pytest` is used for the small parser test (`scripts/test_fetch_kaitak_wind.py`). Install pytest in your venv and run:

```bash
.venv/bin/python -m pytest scripts/test_fetch_kaitak_wind.py
```

Security & reproducibility notes
--------------------------------
- The scripts fetch remote CSVs from HKO — network access is required. The helper `scraping_utils.get_url` caches downloads locally when used.
- Be mindful of large data files if you choose to track raw downloads in git; they increase repository size.

If you want help
---------------
- I can change the visual design (colours, annotations), produce higher-resolution PNGs or export interactive plots, or remove generated files from git and add a small `Makefile` to automate data regeneration.

Course context
--------------
Assignment for SD5913 Creative Programming for Designers and Artists — Assignment 2.
