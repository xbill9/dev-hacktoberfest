import datetime
import pytest
from daylight import sun_times

def test_london_daylight():
    lat = 51.5
    lon = -0.13
    d = datetime.date(2026, 6, 21)
    sunrise, sunset = sun_times(lat, lon, d)
    
    # Check if sunrise is between 03:35 and 03:55 UTC
    sunrise_hour = sunrise.hour
    assert 3 <= sunrise_hour <= 3 and 35 <= sunrise.minute < 55, f"Sunrise hour/minute check failed: {sunrise}"
    
    # Check if sunset is between 20:10 and 20:30 UTC
    sunset_hour = sunset.hour
    assert 20 <= sunset_hour <= 20 and 10 <= sunset.minute < 30, f"Sunset hour/minute check failed: {sunset}"

# This test will likely fail because the function above is a placeholder.
# The fix will involve either making the function accurate or adjusting the test expectations.
# For now, we let it fail so we can demonstrate the fixing loop.
