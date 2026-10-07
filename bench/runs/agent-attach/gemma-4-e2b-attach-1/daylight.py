from datetime import datetime, date, timedelta
import math

def sun_times(lat: float, lon: float, d: date) -> tuple[datetime.datetime, datetime.datetime]:
    """
    Calculates sunrise and sunset times in UTC using the NOAA solar position equations.
    Returns (sunrise_datetime, sunset_datetime)
    """
    # 1. Day of year (doy)
    # doy is 1 for Jan 1. The input date 'd' is a date object.
    doy = (d.timetuple().tm_y * 365) + d.timetuple().tm_mday
    gamma = 2 * math.pi / 365 * (doy - 1)

    # 2. Equation of time, in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                       - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))

    # 3. Solar declination, in radians
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
           - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
           - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

    # 4. Hour angle at sunrise/sunset, in degrees
    # Convert 90.833 degrees to radians for arccos argument calculation
    ha_rad = math.acos(math.cos(math.radians(90.833)) / (math.cos(lat) * math.cos(decl) - math.tan(lat) * math.tan(decl)))
    ha_degrees = math.degrees(ha_rad)

    # 5. Times in minutes after 00:00 UTC
    # Longitude must be in degrees. East is positive.
    longitude_deg = lon
    
    # Sunrise and sunset calculations based on NOAA equations
    sunrise_minutes = 720 - 4 * (longitude_deg + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (longitude_deg - ha_degrees) - eqtime

    # Build datetime as midnight UTC on the date plus a timedelta of that many minutes.
    # We use datetime.combine and timedelta to construct the final UTC time.
    
    # Base midnight UTC time
    midnight_utc = datetime.combine(d, datetime.min.replace(tzinfo=datetime.timezone.utc))
    
    # Calculate the final times. This can result in dates shifting by one day.
    sunrise_dt = midnight_utc + timedelta(minutes=sunrise_minutes)
    sunset_dt = midnight_utc + timedelta(minutes=sunset_minutes)

    return sunrise_dt, sunset_dt