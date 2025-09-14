"""Helper to force-load .env into the current process environment.
Run from a notebook with `%run scripts/reload_env.py` or import and call `reload_env()`.
"""
import os
from dotenv import dotenv_values, load_dotenv

def reload_env():
    try:
        load_dotenv(override=True)
    except TypeError:
        for k, v in dotenv_values('.env').items():
            if v is not None:
                os.environ[k] = v
    print('Reloaded .env into os.environ')
    print('RAINFALL_URL =', os.getenv('RAINFALL_URL'))
    print('RAINFALL_STATION_NAME =', os.getenv('RAINFALL_STATION_NAME'))
    print('START_YEAR =', os.getenv('START_YEAR'))
    print('END_YEAR =', os.getenv('END_YEAR'))
    print('HUMIDITY_URL =', os.getenv('HUMIDITY_URL'))

if __name__ == '__main__':
    reload_env()
