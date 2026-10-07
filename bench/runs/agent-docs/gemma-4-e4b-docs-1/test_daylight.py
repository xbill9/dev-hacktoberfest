import datetime
import pytest
from daylight import sun_times

def test_london_june_sol():
    """
    Tests sun_times function for London (51.5, -0.13) on 2026-06-21.
    Sunrise should be between 03:35 and 03:55 UTC.
    Sunset should be between 20:10 and 20:30 UTC.
    """
    lat = 51.5
    lon = -0.13
    d = datetime.date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    
    # Define time boundaries in seconds for comparison
    # Sunrise: 03:35:00 to 03:55:00
    sunrise_start = datetime.datetime.combine(d, datetime.time(3, 35, 0))
    sunrise_end = datetime.datetime.combine(d, datetime.time(3, 55, 0))
    
    # Sunset: 20:10:00 to 20:30:00
    sunset_start = datetime.datetime.combine(d, datetime.time(20, 10, 0))
    sunset_end = datetime.datetime.combine(d, datetime.time(20, 30, 0))
    
    assert sunrise is not None
    assert sunrise_start <= sunrise <= sunrise_end, f"Sunrise {sunrise} out of range"
    
    assert sunset is not None
    assert sunset_start <= sunset <= sunset_end, f"Sunset {sunset} out of range"

