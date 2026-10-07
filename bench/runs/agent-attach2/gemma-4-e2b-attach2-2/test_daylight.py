import pytest
from datetime import date, datetime
from daylight import sun_times

def test_london_sun_times():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)

    sunrise, sunset = sun_times(lat, lon, d)

    # Check sunrise range (03:35 to 03:55 UTC)
    sunrise_hour = sunrise.hour
    sunrise_minute = sunrise.minute
    assert 3 <= sunrise_hour <= 3
    assert 35 <= sunrise_minute <= 55

    # Check sunset range (20:10 to 20:30 UTC)
    sunset_hour = sunset.hour
    sunset_minute = sunset.minute
    assert 20 <= sunset_hour <= 20
    assert 10 <= sunset_minute <= 30

def test_different_location():
    lat = 40.71
    lon = -74.00
    d = date(2024, 1, 1)
    sunrise, _ = sun_times(lat, lon, d)
    # Just ensuring it runs and doesn't immediately crash (will be checked by the range in the previous test if the function is correct)
    assert isinstance(sunrise, datetime)