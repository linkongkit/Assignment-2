import requests
from lxml import html

import dotenv
import os
import datetime
from scraping_utils import get_url, parse

# Load environment variables
dotenv.load_dotenv()

# Determine filename and year (fallbacks)
year = int(os.getenv('YEAR', 2024))
filename = os.getenv('FILENAME', "crawled-page-{year}.html").format(year=year)

# Fetch and parse page (uses the project's get_url/parse helpers)
page = get_url(os.getenv('URL'), filename)
tree = parse(page, 'html')

# Collect parsed records as (datetime, value)
data = []
row_num = 0

for row in tree.xpath(os.getenv('ROW_XPATH')):
    cols = row.xpath(os.getenv('COL_XPATH'))
    cols = [c.text_content().strip() for c in cols]
    row_string = " ".join(cols).strip()
    if not row_string:
        continue
    row_num += 1
    print(f'Row {row_num}: {row_string}')

    # Minimal parsing example — original script attempted to interpret MM DD HHMM value sequences
    try:
        month = int(cols[0])
        day = int(cols[1])
    except Exception:
        continue

    for i in range(2, len(cols), 2):
        if cols[i] == "":
            continue
        time_digits = ''.join(ch for ch in cols[i] if ch.isdigit())
        if len(time_digits) not in (3, 4):
            continue
        if len(time_digits) == 3:
            time_digits = '0' + time_digits
        hour = int(time_digits[:2])
        minute = int(time_digits[2:])
        try:
            dt = datetime.datetime(year, month, day, hour, minute)
        except ValueError:
            continue
        value = cols[i+1] if i+1 < len(cols) else ''
        print(f'{dt} - {value}')
        data.append((dt, value))

# Print parsed records. Intentionally do not write tide CSVs in this repository copy.
for record in data:
    print(f"{record[0].strftime('%Y-%m-%d %H:%M')},{record[1]}")

# Note: the original example wrote to a tides CSV. That behavior is disabled here to avoid
# keeping tide data as active outputs in the main repo. If you need to re-enable archival
# of parsed tide records, uncomment and review the example write block below and ensure
# the destination path is appropriate for your environment.
# Example (commented):
# with open('archived-tides.csv', 'a', encoding='utf8') as f:
#     f.write(f"{record[0].strftime('%Y-%m-%d %H:%M')},{record[1]}\n")
