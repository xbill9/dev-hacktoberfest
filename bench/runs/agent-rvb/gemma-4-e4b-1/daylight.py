import datetime
import math

def sun_times(lat: float, lon: float, d: datetime.date) -> tuple[datetime.datetime, datetime.datetime]:
    """
    Calculates sunrise and sunset times in UTC using the NOAA sunrise equation.
    
    :param lat: Latitude in decimal degrees.
    :param lon: Longitude in decimal degrees.
    :param d: Date object (year, month, day).
    :return: A tuple containing (sunrise_utc, sunset_utc) as datetime objects in UTC.
    """
    # Convert longitude to radians
    lon_rad = math.radians(lon)
    
    # Day of the year (n)
    n = d.timetuple().tm_yday
    
    # Calculate solar mean anomaly (M) and equation of center (C)
    # M = (360/365.25) * (n - 81)
    m = (360 / 365.25) * (n - 81)
    # C = (1.915/12) * sin(M) + 0.072 * sin(2M) + 0.0036 * sin(3M)
    c = (1.915 / 12) * math.sin(m) + 0.072 * math.sin(2 * m) + 0.0036 * math.sin(3 * m)
    
    # Calculate solar mean longitude (L)
    l = m + c
    
    # Calculate obliquity of the ecliptic (epsilon)
    # epsilon = (3/4) * sin(L) * sin((90/360) * L)
    epsilon = (3 / 4) * math.sin(l) * math.sin((90 / 360) * l)
    
    # Calculate ecliptic latitude (beta)
    # beta = asin(sin(l) * sin(epsilon))
    beta = math.asin(math.sin(l) * math.sin(epsilon))
    
    # Calculate the declination of the sun (delta)
    # delta = sin(beta)
    delta = math.sin(beta)
    
    # Calculate the hour angle (H) for sunrise/sunset
    # cos(H) = (cos(lat) - sin(lat) * sin(delta)) / (cos(lat) * cos(epsilon))
    lat_rad = math.radians(lat)
    cos_H_num = math.cos(lat_rad) - math.sin(lat_rad) * math.sin(delta)
    cos_H_den = math.cos(lat_rad) * math.cos(epsilon)
    
    # Handle potential division by zero or rounding issues near the poles/equinox
    if abs(cos_H_den) < 1e-9:
        raise ValueError("Calculation failed: cos_H_den is near zero.")
        
    cos_H = cos_H_num / cos_H_den
    
    if cos_H > 1.0:
        H = math.pi / 2  # Sun is always above the horizon
    elif cos_H < -1.0:
        H = -math.pi / 2 # Sun never rises/sets (polar night)
    else:
        H = math.acos(cos_H)

    # Calculate time offset from local solar noon (in hours)
    # H is in radians. 15 degrees = 1 hour.
    time_offset_hours = (H * 180 / math.pi) / 15.0

    # Solar Noon in UTC, adjusted for longitude
    T_noon_utc = 12 + (lon / 15.0)

    # Sunrise/Sunset in hours from 00:00 UTC
    sunrise_utc_hours = T_noon_utc - time_offset_hours
    sunset_utc_hours = T_noon_utc + time_offset_hours
    
    # Convert hours to datetime object for a specific date, assuming UTC
    start_of_day_utc = datetime.datetime(d.year, d.month, d.day, tzinfo=datetime.timezone.utc)
    
    # Ensure times are positive and within a 24-hour day for standard interpretation
    if sunrise_utc_hours < 0:
        sunrise = start_of_day_utc + datetime.timedelta(hours=sunrise_utc_hours + 24)
    else:
        sunrise = start_of_day_utc + datetime.timedelta(hours=sunrise_utc_hours)

    if sunset_utc_hours >= 24:
        sunset = start_of_day_utc + datetime.timedelta(hours=sunset_utc_hours - 24)
    else:
        sunset = start_of_day_utc + datetime.timedelta(hours=sunset_utc_hours)
    
    return sunrise, sunset
