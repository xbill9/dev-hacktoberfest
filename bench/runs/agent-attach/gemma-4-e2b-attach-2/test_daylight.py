import pytest
from datetime import date, datetime
from daylight import sun_times

@pytest.fixture
def london_day():
    # Date: 2026-06-21
    d = date(2026, 6, 21)
    lat = 51.5
    lon = -0.13
    return lat, lon, d

def test_london_times(london_day):
    lat, lon, d = london_day
    sunrise, sunset = sun_times(lat, lon, d)

    # Expected ranges for London (51.5 N, -0.13 E) on 2026-06-21:
    # Sunrise UTC: between 03:35 and 03:55
    # Sunset UTC: between 20:10 and 20:30

    # Check sunrise range
    expected_sunrise_min = 3 * 60 + 35
    expected_sunrise_max = 3 * 60 + 55
    
    # Check sunset range
    expected_sunset_min = 20 * 60 + 10
    expected_sunset_max = 20 * 60 + 30

    # Check if calculated sunrise is within the range
    assert expected_sunrise_min <= sunrise.hour * 60 + sunrise.minute <= expected_sunrise_max, f"Sunrise {sunrise} out of range [{expected_sunrise_min}, {expected_sunrise_max}]"
    
    # Check if calculated sunset is within the range
    assert expected_sunset_min <= sunset.hour * 60 + sunset.minute <= expected_sunset_max, f"Sunset {sunset} out of range [{expected_sunset_min}, {expected_sunset_max}]"

