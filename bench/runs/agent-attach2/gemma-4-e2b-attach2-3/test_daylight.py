import pytest
from datetime import date, datetime
from daylight import sun_times

def test_london_times():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)
    
    sunrise_dt, sunset_dt = sun_times(lat, lon, d)
    
    # Check sunrise time hour (must be 3)
    sunrise_hour = sunrise_dt.hour
    assert sunrise_hour == 3, f"Sunrise hour {sunrise_hour} is not 3."
    
    # Check sunset time hour (must be 20)
    sunset_hour = sunset_dt.hour
    assert sunset_hour == 20, f"Sunset hour {sunset_hour} is not 20."

