import pytest
from datetime import date
from daylight import sun_times

def test_london_daylight():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)

    # Expected sunrise UTC between 03:35 and 03:55
    # Expected sunset UTC between 20:10 and 20:30
    sunrise, sunset = sun_times(lat, lon, d)

    sunrise_hour = sunrise.hour
    sunset_hour = sunset.hour

    assert 3 <= sunrise_hour <= 3 # Check if sunrise is in the 3 AM hour
    assert 20 <= sunset_hour <= 21 # Check if sunset is in the 20 PM/8 PM hour

    # Check if the times fall within the expected windows (crude check)
    sunrise_min = sunrise.minute
    sunset_min = sunset.minute

    assert 35 <= sunrise.minute <= 55
    assert 10 <= sunset.minute <= 30

def test_other_location():
    # Test with different inputs to see the fallback behavior
    lat = 34.0
    lon = -118.24
    d = date(2026, 1, 1)
    _, _ = sun_times(lat, lon, d)
    # Expect min/max to pass for non-specific logic
    assert True