import datetime
import pytest
from daylight import sun_times

def test_london_daylight():
    lat = 51.5
    lon = -0.13
    date = datetime.date(2026, 6, 21)
    
    sunrise_utc, sunset_utc = sun_times(lat, lon, date)
    
    assert sunrise_utc.hour == 3 and 35 <= sunrise_utc.minute <= 55
    
    assert sunset_utc.hour == 20 and 10 <= sunset_utc.minute <= 30


# Note: Since the implementation in daylight.py is a placeholder, this test will pass
# based on the mock return value, but the actual NOA implementation is missing.
# The requirement to fix failures will be executed next.
