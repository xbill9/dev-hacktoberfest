import datetime
import pytest
from daylight import sun_times

LAT = 51.5
LON = -0.13
DATE_VALID = datetime.date(2026, 6, 21)
DATE_INVALID = "not_a_date"

def test_sun_times_basic():
    sunrise, sunset = sun_times(LAT, LON, DATE_VALID)
    assert isinstance(sunrise, datetime.datetime)
    assert isinstance(sunset, datetime.datetime)
    assert sunrise.year == 2026
    assert sunset.year == 2026

def test_sun_times_invalid_date():
    with pytest.raises(TypeError):
        sun_times(LAT, LON, DATE_INVALID)

