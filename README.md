# Tides & Temperature Scraping + Visualization (Assignment 2)

This repository contains utilities and example scripts for crawling, parsing and visualizing climate and tidal data for a short course project. The code demonstrates simple web scraping (with local caching), parsing HTML/JSON responses, converting scraped tide tables into CSV, and plotting results using Matplotlib. There are also small SVG drawing experiments.

Contents
--------
- `scraping_utils.py` – helper functions: `get_url` (fetch + local cache) and `parse` (HTML or JSON).
- `plot_tides.py` – example script that scrapes a tide table page, extracts times/heights and plots them with Matplotlib.
- `tides_csv.py` – similar logic to `plot_tides.py` but writes parsed tide records to `tides.csv`.
- `multi_city_temp.py` – example that loads multiple city climate JSON pages and prints simple data from each.
- `draw_svg.py`, `geometric-shapes.svg`, `irregular-polygon.svg`, `tide-chart.svg` – small drawing examples using `drawsvg` and shipped SVGs.
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

2. Create a `.env` file at the repository root with the environment variables used by the scripts. Example `.env` values used by `plot_tides.py` / `tides_csv.py`:

```ini
URL=https://example.com/tide-table
YEAR=2023
FILENAME=crawled-page-{year}.html
ROW_XPATH=//table[@id="tide-table"]/tbody/tr
COL_XPATH=./td
# For multi_city_temp.py
MULTICITY_URL=https://example.com/api/city/{city_id}
```

How the main scripts work
-------------------------
- `scraping_utils.get_url(url, filename)` fetches a URL and saves the response to `filename` if it does not already exist; otherwise it reads the local file. This is convenient for debugging and avoiding repeated network calls.
- `scraping_utils.parse(page, mode)` returns an `lxml` HTML tree when `mode=='html'` or a parsed JSON object when `mode=='json'`.
- `plot_tides.py` (example): uses `ROW_XPATH`/`COL_XPATH` to locate tide rows and columns, extracts date/time pairs and tide heights, then plots a time-series using Matplotlib.
- `tides_csv.py`: collects the same parsed records and appends them into a local `tides.csv` file with the format `YYYY-MM-DD HH:MM,value`.
- `multi_city_temp.py`: reads multiple JSON endpoints defined by `MULTICITY_URL` and prints some climate data keys for each city.

Running examples
----------------
- Plot tides (opens a Matplotlib window):

```bash
source .venv/bin/activate
python plot_tides.py
```

- Generate `tides.csv` from the scraped page:

```bash
python tides_csv.py
```

- Run the multi-city climate demo:

```bash
python multi_city_temp.py
```

Dependencies
------------
Dependencies are listed in `requirements.txt`. The main ones are:
- `requests` — HTTP client
- `lxml` — HTML parsing
- `python-dotenv` — load `.env` variables
- `drawsvg` — optional SVG drawing examples
- `matplotlib` — plotting

Notes, assumptions, and next steps
---------------------------------
- The scripts expect the caller to provide correct XPath expressions and working URLs via environment variables. Example pages are included to allow offline testing.
- CSV writing in `tides_csv.py` appends to `tides.csv`; if you want a fresh file, remove the old file first.
- Error handling is minimal — consider adding robust validation for missing/invalid data, network timeouts, and CSV header handling for production use.

If you want, I can:
- add a minimal `requirements.txt` pinning exact versions,
- add a small `Makefile` or `tasks.json` to simplify running each demo,
- improve `scraping_utils` to return structured records and add unit tests.

License
-------
No license specified. If you plan to publish this project, consider adding a `LICENSE` file (e.g., MIT).

Author / Context
----------------
Course assignment: SD5913 Creative Programming for Designers and Artists — Assignment 2.
