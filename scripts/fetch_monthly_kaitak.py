#!/usr/bin/env python3
"""Fetch HKO daily rainfall CSV, filter Kaitak station, aggregate monthly rainfall (2010-2025).
Writes CSV and creates a simple plot.
"""
import os
import csv
import datetime
import requests
import dotenv
import matplotlib.pyplot as plt
from collections import defaultdict

dotenv.load_dotenv()
RAINFALL_URL = os.getenv('RAINFALL_URL')
STATION = os.getenv('RAINFALL_STATION_NAME', 'Kaitak')
START_YEAR = int(os.getenv('START_YEAR', '2010'))
END_YEAR = int(os.getenv('END_YEAR', '2025'))

OUT_CSV = f'kaitak_monthly_rainfall_{START_YEAR}_{END_YEAR}.csv'

if not RAINFALL_URL:
    raise SystemExit('RAINFALL_URL not set in .env')

print(f'Fetching rainfall CSV from: {RAINFALL_URL}')
resp = requests.get(RAINFALL_URL, timeout=30)
resp.raise_for_status()
text = resp.text

# The HKO CSV likely has header rows; parse using csv.reader
reader = csv.reader(text.splitlines())
rows = list(reader)

# Try to find header row containing known column names (e.g., "Station", "Date", "Rainfall")
header = None
for i, r in enumerate(rows[:5]):
    if any('Station' in c or 'station' in c for c in r) and any('Date' in c or 'date' in c for c in r):
        header = rows[i]
        data_rows = rows[i+1:]
        break

if header is None:
    # Fallback: assume first row is header
    header = rows[0]
    data_rows = rows[1:]

col_index = {name: idx for idx, name in enumerate(header)}
# Print header mapping
print('Detected header columns:', col_index)

# Common column names to find
possible_station_cols = [c for c in header if 'station' in c.lower() or 'site' in c.lower()]
possible_date_cols = [c for c in header if 'date' in c.lower()]
possible_rain_cols = [c for c in header if 'rain' in c.lower() or 'rf' in c.lower()]

if not possible_station_cols or not possible_date_cols or not possible_rain_cols:
    print('Warning: could not confidently detect station/date/rain columns automatically. Inspect header above.')

# Choose columns
station_col = possible_station_cols[0] if possible_station_cols else header[0]
date_col = possible_date_cols[0] if possible_date_cols else header[1]
rain_col = possible_rain_cols[0] if possible_rain_cols else header[-1]

si = col_index[station_col]
di = col_index[date_col]
rn = col_index[rain_col]

monthly = defaultdict(float)
counted = 0
for r in data_rows:
    if len(r) <= max(si, di, rn):
        continue
    station = r[si].strip()
    if station.lower() != STATION.lower():
        continue
    date_str = r[di].strip()
    try:
        # try common date formats
        if '-' in date_str:
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        elif '/' in date_str:
            dt = datetime.datetime.strptime(date_str, '%d/%m/%Y')
        else:
            dt = datetime.datetime.strptime(date_str, '%Y%m%d')
    except Exception:
        # skip unparsable
        continue
    if dt.year < START_YEAR or dt.year > END_YEAR:
        continue
    rain_val = r[rn].strip()
    # normalize numeric rainfall (empty or non-numeric treated as 0)
    try:
        rv = float(rain_val) if rain_val != '' else 0.0
    except ValueError:
        rv = 0.0
    key = (dt.year, dt.month)
    monthly[key] += rv
    counted += 1

print(f'Processed {counted} daily records for station {STATION}')

# Write monthly CSV
with open(OUT_CSV, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['year','month','monthly_rainfall_mm'])
    for (y,m), total in sorted(monthly.items()):
        writer.writerow([y,m,f'{total:.2f}'])

print(f'Wrote monthly CSV: {OUT_CSV}')

# Quick plot
if monthly:
    years = sorted(set(y for y,m in monthly.keys()))
    # Create a timeline of months
    timeline = []
    values = []
    for y in range(START_YEAR, END_YEAR+1):
        for m in range(1,13):
            timeline.append(datetime.datetime(y,m,1))
            values.append(monthly.get((y,m), 0.0))
    plt.figure(figsize=(14,6))
    plt.bar(timeline, values, width=20)
    plt.title(f'Monthly Rainfall - {STATION} ({START_YEAR}-{END_YEAR})')
    plt.xlabel('Month')
    plt.ylabel('Monthly Rainfall (mm)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'monthly_rainfall_{STATION}_{START_YEAR}_{END_YEAR}.png')
    print('Saved plot PNG')
else:
    print('No monthly data to plot')
