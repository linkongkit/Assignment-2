"""Load `rainfall_processed.csv` using the helper and print a quick preview/summary.

Usage:
    python3 scripts/load_and_preview.py

Exits with code 0 on success, non-zero on failure.
"""
import sys
import os
from scripts.rainfall_utils import validate_csv_header, load_rainfall_csv

CSV = 'rainfall_processed.csv'

if not os.path.exists(CSV):
    print(f'ERROR: {CSV} not found in current directory. Create it or run the notebook to produce it.')
    sys.exit(2)

ok, msg = validate_csv_header(CSV)
if not ok:
    print(f'ERROR: CSV header invalid: {msg}')
    sys.exit(3)

try:
    data = load_rainfall_csv(CSV)
except Exception as e:
    print(f'ERROR loading CSV: {e}')
    sys.exit(4)

print(f'Loaded {len(data)} records from {CSV}')
if data:
    print('\nSample records (first 10):')
    for dt, rain, hum in data[:10]:
        print(f'  {dt.strftime("%Y-%m-%d %H:%M")}  rain={"" if rain is None else f"{rain:.2f}"} mm  hum={"" if hum is None else f"{hum:.1f}%"}')

# Basic stats
values = [r for _, r, _ in data if r is not None]
if values:
    print(f"\nRainfall stats: count={len(values)}, mean={sum(values)/len(values):.2f}, min={min(values):.2f}, max={max(values):.2f}")
else:
    print('\nNo numeric rainfall values found.')

sys.exit(0)
