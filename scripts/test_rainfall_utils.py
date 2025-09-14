import os
import tempfile
from scripts.rainfall_utils import load_rainfall_csv, validate_csv_header
import datetime


def test_validate_and_load():
    csv_text = """datetime,rainfall_mm,humidity_pct
2023-01-01 00:00,1.5,60
2023-01-01 01:00,,61
2023-01-01 02:00,0.0,
badrow,abc,def
"""
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'test.csv')
        with open(p, 'w', encoding='utf8') as f:
            f.write(csv_text)
        ok, msg = validate_csv_header(p)
        assert ok, msg
        data = load_rainfall_csv(p)
        # should load 3 valid rows
        assert len(data) == 3
        assert data[0][0] == datetime.datetime(2023, 1, 1, 0, 0)
        assert data[0][1] == 1.5
        assert data[0][2] == 60.0
        assert data[1][1] is None
        assert data[2][2] is None
