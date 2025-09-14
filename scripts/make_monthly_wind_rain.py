#!/usr/bin/env python3
"""Aggregate monthly rainfall totals and monthly mean wind, then plot dual-axis chart.

Reads:
 - 'kaitak_wind_2010_2025.csv' (date,station,mean_wspd)
 - 'rainfall_processed.csv' (datetime,rainfall_mm)

Writes:
 - 'monthly_wind_rain.png' (PNG)
 - 'monthly_wind_rain.svg' (SVG)
"""
import csv
import datetime
import os
from collections import defaultdict
import matplotlib.pyplot as plt


def load_wind(path):
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                d = datetime.datetime.strptime(row['date'][:10], '%Y-%m-%d')
            except Exception:
                continue
            v = row.get('mean_wspd')
            try:
                v = float(v) if v not in (None, '') else None
            except Exception:
                v = None
            data.append((d, v))
    return data


def load_rain(path):
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                d = datetime.datetime.strptime(row['datetime'][:10], '%Y-%m-%d')
            except Exception:
                continue
            v = row.get('rainfall_mm')
            try:
                v = float(v) if v not in (None, '') else 0.0
            except Exception:
                v = 0.0
            data.append((d, v))
    return data


def aggregate_monthly(wind_data, rain_data):
    # keys are (year, month)
    wind_sums = defaultdict(list)
    rain_sums = defaultdict(float)
    for d, v in wind_data:
        if v is not None:
            wind_sums[(d.year, d.month)].append(v)
    for d, v in rain_data:
        rain_sums[(d.year, d.month)] += v

    months = []
    wind_means = []
    rain_totals = []
    if not wind_data and not rain_data:
        return months, wind_means, rain_totals

    years = sorted(set([d.year for d, _ in wind_data] + [d.year for d, _ in rain_data]))
    start_year = min(years)
    end_year = max(years)
    for y in range(start_year, end_year+1):
        for m in range(1, 13):
            months.append(datetime.datetime(y, m, 1))
            wm = None
            key = (y,m)
            if key in wind_sums and wind_sums[key]:
                wm = sum(wind_sums[key]) / len(wind_sums[key])
            wind_means.append(wm)
            rain_totals.append(rain_sums.get(key, 0.0))

    return months, wind_means, rain_totals


def plot(months, wind_means, rain_totals):
    fig, ax1 = plt.subplots(figsize=(14,5))
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Monthly Rainfall (mm)', color='#ff7f0e')
    ax1.bar(months, rain_totals, width=20, color='#ff7f0e', alpha=0.6)
    ax1.tick_params(axis='y', labelcolor='#ff7f0e')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Mean Wind Speed (km/h)', color='#1f77b4')
    ax2.plot(months, [v if v is not None else float('nan') for v in wind_means], color='#1f77b4', marker='o', markersize=3)
    ax2.tick_params(axis='y', labelcolor='#1f77b4')

    fig.autofmt_xdate()
    plt.title('Monthly Rainfall (bars) and Mean Wind (line) - Kai Tak')
    plt.tight_layout()
    png = 'monthly_wind_rain.png'
    svg = 'monthly_wind_rain.svg'
    plt.savefig(png)
    plt.savefig(svg)
    print('Wrote', png, 'and', svg)


def main():
    wind = load_wind('kaitak_wind_2010_2025.csv')
    rain = load_rain('rainfall_processed.csv')
    months, wind_means, rain_totals = aggregate_monthly(wind, rain)
    plot(months, wind_means, rain_totals)


if __name__ == '__main__':
    main()
