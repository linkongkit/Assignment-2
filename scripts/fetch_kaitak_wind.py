#!/usr/bin/env python3
#!/usr/bin/env python3
"""
scripts/fetch_kaitak_wind.py

Fetch Kai Tak daily mean wind speed from the HKO station-block CSV, save a processed
CSV (`kaitak_wind_{start}_{end}.csv`) and a PNG plot (`kaitak_wind_{start}_{end}.png`).

The HKO CSV is organized in station blocks. Each block begins with a title line that
contains the station name (for example: "Mean Wind Speed (km/h) - Kai Tak"), followed
by a header line like: Year,Month,Day,Value,Completeness and then rows with numeric data.

Environment variables (optional):
  WIND_URL - URL to HKO wind CSV (default: HKO SE WSPD CSV)
  WIND_STATION_NAME - Station name substring to filter (default: KaiTak)
  START_YEAR / END_YEAR - year range to include (defaults: 2010-2025)

Usage:
  PYTHONPATH=. .venv/bin/python scripts/fetch_kaitak_wind.py
"""

import os
import sys
import datetime
import re
import csv
import matplotlib.pyplot as plt

try:
    from scraping_utils import get_url
except Exception:
    # If importing fails, provide a helpful message
    print("Error: unable to import 'scraping_utils'. When running from the shell set PYTHONPATH='.'.")
    raise


def parse_station_block_lines(lines, wind_station, start_year, end_year):
    """Parse HKO station-block CSV lines and return a list of records for the chosen station.

    Each matching record is a dict: {'date': date_obj, 'mean_wspd': float|None, 'station': station_name}
    """
    records = []
    i = 0
    n = len(lines)

    def _norm(s: str) -> str:
        # normalize by keeping only alphanumeric characters and lowercasing
        return re.sub(r'[^0-9a-z]', '', (s or '').lower())

    ws_norm = _norm(wind_station)

    while i < n:
        line = lines[i].strip()
        # detect station title line containing the station substring (normalized)
        if line and ws_norm and ws_norm in _norm(line):
            station_name = line.strip()
            # advance to the header line (skip blanks)
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            if i >= n:
                break
            # header_line = lines[i]
            i += 1
            # read data rows until blank line or next non-data line
            while i < n:
                row_line = lines[i].strip()
                if not row_line:
                    i += 1
                    break
                # data rows normally start with a digit (year)
                if not row_line[0].isdigit():
                    break
                parts = [p.strip() for p in row_line.split(',')]
                try:
                    year = int(parts[0])
                    month = int(parts[1])
                    day = int(parts[2])
                    val_str = parts[3] if len(parts) > 3 else ''
                    num = re.sub(r'[^0-9\.-]', '', val_str)
                    wspd_val = float(num) if num not in (None, '') else None
                    date_obj = datetime.date(year, month, day)
                    if start_year <= date_obj.year <= end_year:
                        records.append({'date': date_obj, 'mean_wspd': wspd_val, 'station': station_name})
                except Exception:
                    # skip malformed rows
                    pass
                i += 1
            continue
        i += 1

    return records


def main():
    wind_url = os.getenv('WIND_URL') or 'https://data.weather.gov.hk/cis/csvfile/SE/ALL/daily_SE_WSPD_ALL.csv'
    wind_station = os.getenv('WIND_STATION_NAME') or 'KaiTak'
    start_year = int(os.getenv('START_YEAR', 2010))
    end_year = int(os.getenv('END_YEAR', 2025))

    print(f"Fetching wind CSV from: {wind_url}")
    try:
        csv_text = get_url(wind_url, 'daily_SE_WSPD_ALL.csv')
    except Exception as e:
        print(f"Error fetching CSV: {e}")
        sys.exit(1)

    lines = csv_text.splitlines()
    print(f"Retrieved CSV: {len(lines)} lines")

    records = parse_station_block_lines(lines, wind_station, start_year, end_year)
    print(f"Found {len(records)} matching records for station '{wind_station}' between {start_year} and {end_year}")

    out_csv = f'kaitak_wind_{start_year}_{end_year}.csv'
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['date', 'station', 'mean_wspd'])
        w.writeheader()
        for r in records:
            w.writerow({'date': r['date'].isoformat(), 'station': r['station'], 'mean_wspd': '' if r['mean_wspd'] is None else r['mean_wspd']})

    print(f"Processed CSV written: {out_csv}")

    speeds = [r['mean_wspd'] for r in records if r['mean_wspd'] is not None]
    if speeds:
        dates = [r['date'] for r in records if r['mean_wspd'] is not None]
        plt.figure(figsize=(12, 5))
        plt.plot(dates, speeds, '-o', markersize=3)
        plt.title(f"Daily Mean Wind Speed - {wind_station} ({start_year}-{end_year})")
        plt.xlabel('Date')
        plt.ylabel('Mean Wind Speed (km/h)')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        out_png = f'kaitak_wind_{start_year}_{end_year}.png'
        plt.savefig(out_png)
        print(f"Plot saved: {out_png}")
    else:
        print("No numeric wind speed values to plot")


if __name__ == '__main__':
    main()
            # advance to header line
