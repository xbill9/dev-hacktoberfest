from datetime import datetime, date
import math
import calendar

def sun_times(lat: float, lon: float, d: date) -> tuple[datetime.datetime, datetime.datetime]:
    # 1. Day of year
    doy = calendar.dayofyear(d)
    gamma = 2 * math.pi / 365 * (doy - 1)
    
    # 2. Equation of time in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                       - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    
    # 3. Solar declination in radians
    decl = (0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
            - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
            - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma))
    
    # Convert latitude and declination to degrees for ha calculation if necessary, 
    # but the formula uses radians for cos/sin, so we use lat/decl as radians.
    lat_rad = math.radians(lat)
    decl_rad = math.radians(decl)

    # 4. Hour angle at sunrise/sunset, in degrees
    # ha = arccos( cos(radians(90.833)) / (cos(lat)*cos(decl)) - tan(lat)*tan(decl) )
    ha_rad = math.acos(math.cos(math.radians(90.833)) / (math.cos(lat_rad) * math.cos(decl_rad) - math.tan(lat_rad) * math.tan(decl_rad)))
    ha_degrees = math.degrees(ha_rad)

    # 5. Times in minutes after 00:00 UTC
    # sunrise = 720 - 4*(longitude + ha_degrees) - eqtime
    # sunset = 720 - 4*(longitude - ha_degrees) - eqtime
    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime

    # Build datetime object
    sunrise_dt = datetime(d.year, d.month, d.day, 0, sunrise_minutes % 1440, 0)
    sunset_dt = datetime(d.year, d.month, d.day, 0, sunset_minutes % 1440, 0)
    
    # The result can be below 0 or at/above 1440 (the event falls on the previous or next UTC day).
    # Python's datetime handles day overflow automatically when constructing the date component.
    
    return sunrise_dt, sunset_dt