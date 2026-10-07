from datetime import datetime, timedelta
import math

def sun_times(lat: float, lon: float, d: datetime.date) -> tuple[datetime, datetime]:
    # Convert date to day of year (doy)
    day_of_year = d.timetuple().tm_yday
    doy_float = day_of_year

    # 1. Day of year
    gamma = 2 * math.pi / 365 * (doy_float - 1)

    # 2. Equation of time, in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                       - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))

    # 3. Solar declination, in radians
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
           - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
           - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

    # 4. Hour angle at sunrise/sunset, with lat in radians.
    ha_rad = math.acos(math.cos(math.radians(90.833)) / (math.cos(lat) * math.cos(decl) - math.tan(lat) * math.tan(decl)))

    # Convert ha to degrees for step 5
    ha_degrees = math.degrees(ha_rad)

    # 5. Times in minutes after 00:00 UTC
    # Longitude in degrees, east positive
    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime

    # Calculate datetime objects
    sunrise_dt = datetime(d.year, d.month, d.day, 0, 0, 0) + timedelta(minutes=sunrise_minutes)
    sunset_dt = datetime(d.year, d.month, d.day, 0, 0, 0) + timedelta(minutes=sunset_minutes)

    return sunrise_dt, sunset_dt