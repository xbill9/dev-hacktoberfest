import pytest
from datetime import date, time
from daylight import sun_times

def test_london_solar_times():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)

    sunrise, sunset = sun_times(lat, lon, d)

    # Check if sunrise is within the expected range (03:35 to 03:55 UTC)
    sunrise_hour = sunrise.hour
    sunrise_minute = sunrise.minute
    
    assert 3 <= sunrise_hour <= 4, f"Sunrise hour {sunrise_hour} outside expected range (3-4)"
    assert 35 <= sunrise_minute <= 55, f"Sunrise minute {sunrise_minute} outside expected range (35-55)"

    # Check if sunset is within the expected range (20:10 to 20:30 UTC)
    sunset_hour = sunset.hour
    sunset_minute = sunset.minute
    
    assert 20 <= sunset_hour <= 21, f"Sunset hour {sunset_hour} outside expected range (20-21)"
    assert 10 <= sunset_minute <= 30, f"Sunset minute {sunset_minute} outside expected range (10-30)"