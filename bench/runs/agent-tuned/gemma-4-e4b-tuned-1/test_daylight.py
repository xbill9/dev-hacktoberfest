import pytest
import datetime
from daylight import sun_times

def test_london_daylight():
    """
    Tests sunrise and sunset times for London (51.5, -0.13) on 2026-06-21.
    Sunrise UTC expected: 03:35 - 03:55
    Sunset UTC expected: 20:10 - 20:30
    """
    lat = 51.5
    lon = -0.13
    d = datetime.date(2026, 6, 21)
    
    sunrise, sunset = sun_times(lat, lon, d)
    
    # Check sunrise range
    # Sunrise is expected to be between 03:35 and 03:55 UTC
    sunrise_time = sunrise.time()
    
    # Convert to minutes from midnight for easier comparison
    sunrise_minutes = sunrise_time.hour * 60 + sunrise_time.minute
    
    # Expected range: 3:35 (215 mins) to 3:55 (235 mins)
    assert 215 <= sunrise_minutes <= 235, f"Sunrise {sunrise_time} outside expected range [03:35, 03:55]"

    # Check sunset range
    # Sunset is expected to be between 20:10 and 20:30 UTC
    sunset_time = sunset.time()
    sunset_minutes = sunset_time.hour * 60 + sunset_time.minute
    
    # Expected range: 20:10 (1210 mins) to 20:30 (1230 mins)
    assert 1210 <= sunset_minutes <= 1230, f"Sunset {sunset_time} outside expected range [20:10, 20:30]"

if __name__ == '__main__':
    # This block is mainly for manual testing/debugging but pytest handles execution
    test_london_daylight()
    print("Test ran manually.")
