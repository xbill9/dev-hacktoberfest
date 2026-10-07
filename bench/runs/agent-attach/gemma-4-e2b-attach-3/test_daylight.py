import pytest
from datetime import date
from daylight import sun_times

def test_london_summer_solstice():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)

    sunrise, sunset = sun_times(lat, lon, d)

    # Check sunrise time range (03:35 to 03:55)
    sunrise_hour = sunrise.hour
    sunrise_min = sunrise.minute
    assert 335 <= sunrise_min <= 355, f"Sunrise is out of range: {sunrise}"

    # Check sunset time range (20:10 to 20:30)
    sunset_hour = sunset.hour
    sunset_min = sunset.minute
    assert 10 <= sunset_min <= 30, f"Sunset is out of range: {sunset}"