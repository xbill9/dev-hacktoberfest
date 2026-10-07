import pytest
from datetime import date
from daylight import sun_times

def test_london_daylight():
    # London: lat=51.5, lon=-0.13
    # Date: 2026-06-21
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    
    # Expected range: sunrise between 03:35 and 03:55, sunset between 20:10 and 20:30 UTC
    
    # Check sunrise
    sunrise_hour = sunrise.hour
    if not (3 <= sunrise_hour <= 3) or (3 * 60 + 35 <= sunrise.minute < 3 * 60 + 55):
        pytest.fail(f"Sunrise time {sunrise} does not fall in the expected range (03:35 - 03:55).")
        
    # Check sunset
    sunset_hour = sunset.hour
    if not (20 <= sunset_hour <= 20) or (20 * 60 + 10 <= sunset.minute < 20 * 60 + 30):
        pytest.fail(f"Sunset time {sunset} does not fall in the expected range (20:10 - 20:30).")
        
    # Since the requirements specify "is between", we will check the ranges more loosely.
    # Let's use the provided examples to define the tolerance.
    
    # A more robust check using the specified ranges
    expected_sunrise_min_total = 3 * 60 + 35
    expected_sunrise_max_min_total = 3 * 60 + 55
    
    expected_sunset_min_total = 20 * 60 + 10
    expected_sunset_max_min_total = 20 * 60 + 30

    assert expected_sunrise_min_total <= sunrise.minute < expected_sunrise_max_min_total
    assert expected_sunset_min_total <= sunset.minute < expected_sunset_max_min_total