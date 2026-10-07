import math
from datetime import datetime, timedelta, timezone

def sun_times(lat: float, lon: float, d: datetime.date) -> tuple[datetime.datetime, datetime.datetime]:
    """
    Calculates sunrise and sunset times in UTC on a given date and location using NOAA equations.
    Returns (sunrise, sunset) in UTC as datetime objects.
    """
    
    # 1. Day of year (doy)
    doy = (d.year - 1900) * 365.25 + d.day
    gamma = 2 * math.pi / 365 * (doy - 1)

    # 2. Equation of time, in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                        - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))

    # 3. Solar declination, in radians
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
            - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
            - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

    # 4. Hour angle at sunrise/sunset, with lat in radians.
    # ha_degrees is calculated in degrees for the next step as per the source equation.
    lat_rad = math.radians(lat)
    
    term1 = math.cos(math.radians(90.833)) / (math.cos(lat_rad) * math.cos(decl))
    term2 = math.tan(lat_rad) * math.tan(decl)
    ha_radians = math.acos(term1 - term2)
    
    # Convert ha_radians to degrees
    ha_degrees = math.degrees(ha_radians)

    # 5. Times in minutes after 00:00 UTC on that date. Longitude in degrees, east positive.
    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime

    # Build the datetime as midnight UTC on the date plus a timedelta of that many minutes.
    start_of_day_utc = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=timezone.utc)
    
    sunrise_time = start_of_day_utc + timedelta(minutes=sunrise_minutes)
    sunset_time = start_of_day_utc + timedelta(minutes=sunset_minutes)

    return sunrise_time, sunset_time