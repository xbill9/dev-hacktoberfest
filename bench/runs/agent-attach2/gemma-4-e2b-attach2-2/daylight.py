import math
from datetime import datetime, timedelta

def sun_times(lat: float, lon: float, d: datetime.date) -> tuple[datetime.datetime, datetime.datetime]:
    # 1. Day of year (doy)
    doy = d.timetuple().tm_yday

    # Gamma in radians
    gamma = 2 * math.pi / 365 * (doy - 1)

    # 2. Equation of time, in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                        - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))

    # 3. Solar declination, in radians
    decl = (0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
            - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
            - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma))

    # Convert latitude to radians for subsequent calculations
    lat_rad = math.radians(lat)

    # 4. Hour angle at sunrise/sunset
    # 90.833 degrees accounts for refraction
    ha_rad = math.acos(math.cos(math.radians(90.833)) / (math.cos(lat_rad) * math.cos(decl) - math.tan(lat_rad) * math.tan(decl)))

    ha_degrees = math.degrees(ha_rad)

    # 5. Times in minutes after 00:00 UTC on that date.
    # Longitude in degrees, east positive, so west longitudes are negative.
    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    # sunset = 720 - 4*(longitude - ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime

    # Build the datetime
    midnight = datetime.combine(d, datetime.min.time())
    sunrise_dt = midnight + timedelta(minutes=sunrise_minutes)
    sunset_dt = midnight + timedelta(minutes=sunset_minutes)

    return sunrise_dt, sunset_dt
