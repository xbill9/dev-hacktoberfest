import pytest
from datetime import date
from daylight import sun_times

def test_sun_times_london():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    
    # Check sunrise range: 03:35 to 03:55 UTC
    sunrise_time = sunrise.time()
    assert 3*60 + 35 <= sunrise_time.hour*60 + sunrise_time.minute <= 3*60 + 55, f"Sunrise out of range: {sunrise_time}"
    
    # Check sunset range: 20:10 to 20:30 UTC
    sunset_time = sunset.time()
    assert 20*60 + 10 <= sunset_time.hour*60 + sunset_time.minute <= 20*60 + 30, f"Sunset out of range: {sunset_time}"

def test_sun_times_polar_day():
    # Example: High latitude, long day (though the formula might struggle)
    # Just ensuring no crash for a different scenario
    lat = 80.0
    lon = 0.0
    d = date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    assert sunrise is None or isinstance(sunrise, datetime)
    assert sunset is None or isinstance(sunset, datetime)
    assert sunset is not None