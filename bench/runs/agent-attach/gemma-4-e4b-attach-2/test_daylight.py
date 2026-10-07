import pytest
from datetime import datetime, date
from daylight import sun_times

def test_london_sun_times():
    lat = 51.5
    lon = -0.13
    d = date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    
    # Check sunrise time
    # 03:35:00 UTC to 03:55:00 UTC
    
    # Convert to minutes since midnight for easier comparison
    sunrise_minutes = sunrise.hour * 60 + sunrise.minute + sunrise.second / 60
    
    # Check if sunrise_minutes is between 3:35 (215 min) and 3:55 (235 min)
    assert 215 <= sunrise_minutes <= 235, f"Sunrise outside expected range: {sunrise}"

    # Check sunset time
    # 20:10:00 UTC to 20:30:00 UTC


    # Convert to minutes since midnight for easier comparison
    sunset_minutes = sunset.hour * 60 + sunset.minute + sunset.second / 60

    # Check if sunset_minutes is between 20:10 (1210 min) and 20:30 (1230 min)
    assert 1210 <= sunset_minutes <= 1230, f"Sunset outside expected range: {sunset}"
