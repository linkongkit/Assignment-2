#!/usr/bin/env python3
"""Fetch HKO rainfall station-block CSV and extract Kai Tak daily rainfall.

Writes `rainfall_processed.csv` with columns: datetime,rainfall_mm
Then regenerates `7.svg` by invoking `scripts/make_7_svg.py`.
"""
import os
import sys
import datetime
import re
import csv

try:
    from scraping_utils import get_url
except Exception:
    print("Error: please run with PYTHONPATH='.' so scraping_utils can be imported")
    raise


def parse_station_block_lines(lines, station_substr, start_year, end_year):
    recs = []
    i = 0
    n = len(lines)
    def _norm(s):
        return re.sub(r'[^0-9a-z]', '', (s or '').lower())
    target = _norm(station_substr)
    while i < n:
        line = lines[i].strip()
        if line and target in _norm(line):
            station_name = line.strip()
            # skip to header
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            if i >= n:
                break
            i += 1
            while i < n:
                row_line = lines[i].strip()
                if not row_line:
                    i += 1
                    break
                if not row_line[0].isdigit():
                    break
                parts = [p.strip() for p in row_line.split(',')]
                try:
                    y = int(parts[0]); m = int(parts[1]); d = int(parts[2])
                    val_str = parts[3] if len(parts) > 3 else ''
                    num = re.sub(r'[^0-9\.-]', '', val_str)
                    v = float(num) if num not in (None, '') else None
                    date_obj = datetime.date(y,m,d)
                    if start_year <= date_obj.year <= end_year:
                        recs.append({'date': date_obj, 'rainfall_mm': v, 'station': station_name})
                except Exception:
                    pass
                i += 1
            continue
        i += 1
    return recs


def main():
    url = os.getenv('RAINFALL_URL') or 'https://data.weather.gov.hk/weatherAPI/cis/csvfile/SE/ALL/daily_SE_RF_ALL.csv'
    station = os.getenv('RAINFALL_STATION_NAME') or 'Kaitak'
    start_year = int(os.getenv('START_YEAR', '2010'))
    end_year = int(os.getenv('END_YEAR', '2025'))

    print(f'Fetching rainfall CSV from: {url}')
    text = get_url(url, 'daily_SE_RF_ALL.csv')
    lines = text.splitlines()
    recs = parse_station_block_lines(lines, station, start_year, end_year)

    out = 'rainfall_processed.csv'
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['datetime','rainfall_mm'])
        for r in recs:
            if r['rainfall_mm'] is None:
                mm = ''
            else:
                mm = f"{r['rainfall_mm']:.1f}"
            w.writerow([r['date'].isoformat(), mm])

    print(f'Wrote {out} with {len(recs)} records')

    # regenerate 7.svg
    print('Regenerating 7.svg')
    os.system('.venv/bin/python scripts/make_7_svg.py')


if __name__ == '__main__':
    main()
