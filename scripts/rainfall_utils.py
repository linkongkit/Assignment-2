"""Small helper utilities to load and validate rainfall_processed.csv

Functions:
- load_rainfall_csv(path) -> list of (datetime, rainfall_mm_or_None, humidity_pct_or_None)
- validate_csv_header(path) -> (bool, message)
"""
from __future__ import annotations
import csv
import datetime
from typing import List, Tuple, Optional

def load_rainfall_csv(path: str) -> List[Tuple[datetime.datetime, Optional[float], Optional[float]]]:
    """Load a CSV with header: datetime,rainfall_mm,humidity_pct

    Rows with unparsable datetimes are skipped. Numeric conversion errors are treated as None.
    """
    data = []
    with open(path, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        # Basic header check
        hdr = reader.fieldnames or []
        expected = {'datetime', 'rainfall_mm', 'humidity_pct'}
        if not expected.issubset(set(hdr)):
            raise ValueError(f"CSV header missing required fields: {expected - set(hdr)}")
        for row in reader:
            dt_str = (row.get('datetime') or '')[:16]
            try:
                dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
            except Exception:
                # skip rows with bad datetime
                continue
            rainfall = None
            humidity = None
            rv = row.get('rainfall_mm')
            hv = row.get('humidity_pct')
            if rv not in (None, ''):
                try:
                    rainfall = float(rv)
                except Exception:
                    rainfall = None
            if hv not in (None, ''):
                # strip percent sign if present
                hv_clean = ''.join(c for c in hv if (c.isdigit() or c in '.-'))
                if hv_clean != '':
                    try:
                        humidity = float(hv_clean)
                    except Exception:
                        humidity = None
            data.append((dt, rainfall, humidity))
    return data


def validate_csv_header(path: str) -> Tuple[bool, str]:
    """Return (True, '') if header looks correct, otherwise (False, message)."""
    with open(path, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        try:
            hdr = next(reader)
        except StopIteration:
            return False, 'CSV is empty'
        hdr_set = set(hdr)
        required = {'datetime', 'rainfall_mm', 'humidity_pct'}
        missing = required - hdr_set
        if missing:
            return False, f'Missing columns: {missing}'
        return True, ''
