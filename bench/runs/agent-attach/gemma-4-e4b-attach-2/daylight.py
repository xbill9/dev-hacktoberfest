import math
import datetime

def sun_times(lat: float, lon: float, d: datetime.date) -> tuple[datetime.datetime, datetime.datetime]:
    doy = d.timetuple().tm_yday

    # 1. Day of year gamma (in radians)
    gamma = (2 * math.pi / 365) * (doy - 1)

    # 2. Equation of time, in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))

    # 3. Solar declination, in radians
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

    # 4. Hour angle at sunrise/sunset (in radians, then converted to degrees)
    # Note: 90.833 degrees accounts for refraction and solar disk size.
    lat_rad = math.radians(lat)
    cos_ha = math.cos(math.radians(90.833)) / (math.cos(lat_rad) * math.cos(decl)) - math.tan(lat_rad) * math.tan(decl)
    
    # Clamp cos_ha to [-1, 1] to prevent math domain errors from floating point inaccuracies
    cos_ha = max(-1, min(1, cos_ha)) 
    
    ha = math.acos(cos_ha)
    ha_degrees = math.degrees(ha)

    # 5. Times in minutes after 00:00 UTC on that date
    # Longitude in degrees, east positive.
    
    # Sunrise and sunset calculation
    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime

    # Build datetime objects
    
    # Calculate timedelta for sunrise
    sunrise_delta = datetime.timedelta(minutes=sunrise_minutes)
    sunrise_utc = datetime.datetime.combine(d, datetime.time.min) + sunrise_delta

    # Calculate timedelta for sunset
    sunset_delta = datetime.timedelta(minutes=sunset_minutes)
    sunset_utc = datetime.datetime.combine(d, datetime.time.min) + sunset_delta
    
    return sunrise_utc, sunset_utc