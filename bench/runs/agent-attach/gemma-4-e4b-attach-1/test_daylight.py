import pytest
from datetime import date, datetime
from daylight import sun_times

def test_sun_times_london():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    
    assert sunrise is not None and sunset is not None

    # Sunrise check (03:35:00 to 03:55:00)
    expected_sunrise_start = datetime.combine(d, datetime.min.time().replace(hour=3, minute=35))
    expected_sunrise_end = datetime.combine(d, datetime.min.time().replace(hour=3, minute=55))
    
    assert expected_sunrise_start <= sunrise <= expected_sunrise_end, f"Sunrise {sunrise} out of bounds. Expected between 03:35 and 03:55."

    # Sunset check (20:10:00 to 20:30:00)
    expected_sunset_start = datetime.combine(d, datetime.min.time().replace(hour=20, minute=10))
    expected_sunset_end = datetime.combine(d, datetime.min.time().replace(hour=20, minute=30))

    assert expected_sunset_start <= sunset <= expected_sunset_end, f"Sunset {sunset} out of bounds. Expected between 20:10 and 20:30."