#!/usr/bin/env python3
"""Generate `7.svg` summarising rainfall and wind data.

This script reads `kaitak_wind_2010_2025.csv` and `rainfall_processed.csv` (if present)
and creates a simple SVG `7.svg` that shows:
 - left: a bar for mean wind speed (Kai Tak)
 - right: a bar for total rainfall over the period (if rainfall data available)

The SVG is intentionally simple so it's easy to edit later.
"""
import csv
import datetime
import os
import statistics


def read_wind(csv_path):
    rows = []
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                d = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
            except Exception:
                continue
            v = row.get('mean_wspd')
            try:
                v = float(v) if v not in (None, '') else None
            except Exception:
                v = None
            rows.append({'date': d, 'mean_wspd': v})
    return rows


def read_rainfall(csv_path):
    # rainfall_processed.csv expected format: datetime,rainfall_mm,humidity_pct
    rows = []
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            dt = row.get('datetime')
            try:
                d = datetime.datetime.strptime(dt[:10], '%Y-%m-%d')
            except Exception:
                continue
            v = row.get('rainfall_mm')
            try:
                v = float(v) if v not in (None, '') else 0.0
            except Exception:
                v = 0.0
            rows.append({'datetime': d, 'rainfall_mm': v})
    return rows


def make_svg(mean_wind, total_rain):
    # simple layout
    width = 600
    height = 240
    left_x = 50
    right_x = 350
    svg = [f'<?xml version="1.0" encoding="UTF-8"?>', f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg.append(f'<text x="{width/2}" y="24" font-size="18" text-anchor="middle" font-family="Arial" font-weight="bold">Rainfall & Wind Summary (Kai Tak)</text>')

    # Wind bar (left)
    max_w = max(mean_wind * 1.4, 1) if mean_wind is not None else 1
    bar_h = 120
    wind_bar_h = (mean_wind / max_w) * bar_h if mean_wind is not None else 0
    svg.append(f'<text x="{left_x+50}" y="60" font-size="14" text-anchor="middle">Mean Wind (km/h)</text>')
    svg.append(f'<rect x="{left_x}" y="{100 + (bar_h - wind_bar_h)}" width="100" height="{wind_bar_h}" fill="#1f77b4" stroke="#0b3d66" stroke-width="1"/>')
    svg.append(f'<text x="{left_x+50}" y="{100 + bar_h + 20}" font-size="12" text-anchor="middle">{mean_wind:.2f} km/h</text>' if mean_wind is not None else f'<text x="{left_x+50}" y="{100 + bar_h + 20}" font-size="12" text-anchor="middle">No data</text>')

    # Rain bar (right)
    svg.append(f'<text x="{right_x+50}" y="60" font-size="14" text-anchor="middle">Total Rainfall (mm)</text>')
    max_r = max(total_rain * 1.1, 1) if total_rain is not None else 1
    rain_bar_h = (total_rain / max_r) * bar_h if total_rain is not None else 0
    svg.append(f'<rect x="{right_x}" y="{100 + (bar_h - rain_bar_h)}" width="100" height="{rain_bar_h}" fill="#ff7f0e" stroke="#8a3e00" stroke-width="1"/>')
    svg.append(f'<text x="{right_x+50}" y="{100 + bar_h + 20}" font-size="12" text-anchor="middle">{int(total_rain)} mm</text>' if total_rain is not None else f'<text x="{right_x+50}" y="{100 + bar_h + 20}" font-size="12" text-anchor="middle">No data</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def main():
    wind_rows = read_wind('kaitak_wind_2010_2025.csv')
    rain_rows = read_rainfall('rainfall_processed.csv')

    mean_wind = None
    total_rain = None
    if wind_rows:
        vals = [r['mean_wspd'] for r in wind_rows if r['mean_wspd'] is not None]
        if vals:
            mean_wind = statistics.mean(vals)
    if rain_rows:
        total_rain = sum(r['rainfall_mm'] for r in rain_rows)

    svg_text = make_svg(mean_wind if mean_wind is not None else 0.0, total_rain if total_rain is not None else 0.0)
    with open('7.svg', 'w') as f:
        f.write(svg_text)
    print('Wrote 7.svg')


if __name__ == '__main__':
    main()
