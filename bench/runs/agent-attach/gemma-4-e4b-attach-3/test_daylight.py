import pytest
from datetime import date, time
from daylight import sun_times

def test_london_sun_times():
    # lat=51.5, lon=-0.13 (London) on 2026-06-21
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    
    # sunrise UTC is between 03:35 and 03:55
    assert time(3, 35) <= sunrise.time() <= time(3, 55)
    # sunset UTC is between 20:10 and 20:30
    assert time(20, 10) <= sunset.time() <= time(20, 30)
