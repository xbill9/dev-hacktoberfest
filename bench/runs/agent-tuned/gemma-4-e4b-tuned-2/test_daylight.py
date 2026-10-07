import datetime
import pytest
from daylight import sun_times

def test_london_daylight():
    lat = 51.5
    lon = -0.13
    d = datetime.date(2026, 6, 21)

    sunrise, sunset = sun_times(lat, lon, d)

    # Sunrise check
    assert sunrise is not None
    # Sunrise between 03:35 and 03:55 UTC
    assert 3*60 + 35 <= sunrise.hour * 60 + sunrise.minute <= 3*60 + 55

    # Sunset check
    assert sunset is not None
    # Sunset between 20:10 and 20:30 UTC
    assert 20*60 + 10 <= sunset.hour * 60 + sunset.minute <= 20*60 + 30

# Helper function for time comparison (since the implementation uses rounded hours/minutes)
# This is mainly for debugging the test structure if needed, but the assertion above is direct.
def check_time_range(dt, min_h, min_m, max_h, max_m):
    min_total_minutes = min_h * 60 + min_m
    max_total_minutes = max_h * 60 + max_m
    current_total_minutes = dt.hour * 60 + dt.minute
    assert min_total_minutes <= current_total_minutes <= max_total_minutes, f"Time {dt.isoformat()} outside range"