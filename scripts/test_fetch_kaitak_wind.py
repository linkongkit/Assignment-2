import datetime
from fetch_kaitak_wind import parse_station_block_lines


def test_parse_station_block_lines_sample():
    sample = [
        "Mean Wind Speed (km/h) - Kai Tak",
        "Year,Month,Day,Value,Completeness",
        "2010,1,1,12.3,C",
        "2010,1,2,10.0,C",
        "",
        "Mean Wind Speed (km/h) - Another Station",
        "Year,Month,Day,Value,Completeness",
        "2010,1,1,5.0,C",
    ]
    recs = parse_station_block_lines(sample, 'KaiTak', 2010, 2010)
    assert len(recs) == 2
    assert recs[0]['date'] == datetime.date(2010, 1, 1)
    assert abs(recs[0]['mean_wspd'] - 12.3) < 1e-6
    assert 'Kai Tak' in recs[0]['station']
