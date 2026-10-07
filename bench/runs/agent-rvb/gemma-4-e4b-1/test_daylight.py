import pytest
import datetime
from daylight import sun_times

def test_london_summer_solstice():
    # London coordinates
    lat = 51.5
    lon = -0.13
    # Summer Solstice 2026
    d = datetime.date(2026, 6, 21)
    
    # Calculate times
    sunrise, sunset = sun_times(lat, lon, d)
    
    # Expected ranges (UTC)
    # Sunrise between 03:35 and 03:55
    # Sunset between 20:10 and 20:30
    
    # Check sunrise range: 03:35:00 to 03:55:00
    start_sunrise = datetime.datetime(d.year, d.month, d.day, 3, 35, 0, tzinfo=datetime.timezone.utc)
    end_sunrise = datetime.datetime(d.year, d.month, d.day, 3, 55, 0, tzinfo=datetime.timezone.utc)
    
    assert start_sunrise <= sunrise <= end_sunrise, f"Sunrise {sunrise} not in expected range [03:35, 03:55]"
    
    # Check sunset range: 20:10:00 to 20:30:00
    start_sunset = datetime.datetime(d.year, d.month, d.day, 20, 10, 0, tzinfo=datetime.timezone.utc)
    end_sunset = datetime.datetime(d.year, d.month, d.day, 20, 30, 0, tzinfo=datetime.timezone.utc)
    
    assert start_sunset <= sunset <= end_sunset, f"Sunset {sunset} not in expected range [20:10, 20:30]"
