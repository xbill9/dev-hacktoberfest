import math
from datetime import datetime, date, timedelta

def sun_times(lat: float, lon: float, d: date) -> tuple[datetime, datetime]:
    # 1. Day of year (doy)
    doy = d.timetuple().tm_yday
    
    # 2. Gamma
    gamma = (2 * math.pi / 365) * (doy - 1)
    
    # 3. Equation of time (in minutes)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                       - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    
    # Convert inputs to radians where necessary for trig functions
    lat_rad = lat * math.pi / 180
    lon_rad = lon * math.pi / 180

    # 4. Solar declination (decl, in radians)
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
    decl_2g = 2 * gamma
    decl_3g = 3 * gamma
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) - 0.006758 * math.cos(decl_2g) + 0.000907 * math.sin(decl_2g) - 0.002697 * math.cos(decl_3g) + 0.00148 * math.sin(decl_3g)
    
    # 5. Hour angle (ha)
    # ha = arccos( cos(radians(90.833)) / (cos(lat)*cos(decl)) - tan(lat)*tan(decl) )
    # Note: The NOAA formula uses lat in radians for cos(lat) and decl in radians.
    # The term cos(radians(90.833)) is cos(90.833 * pi/180)
    
    try:
        cos_ha_numerator = math.cos(90.833 * math.pi / 180)
        cos_ha_denominator = math.cos(lat_rad) * math.cos(decl)
        ha_term = cos_ha_numerator / cos_ha_denominator - (math.tan(lat_rad) * math.tan(decl))
        ha_rad = math.acos(ha_term)
        ha_degrees = math.degrees(ha_rad)
    except ValueError:
        # Handle cases where the argument to acos is out of [-1, 1] (e.g., poles)
        # This indicates the sun never rises or sets on that day, but for simplicity 
        # given the prompt, we'll return None or raise an error if needed.
        # Assuming inputs are within reasonable bounds for calculation.
        return None, None

    # 6. Times in minutes after 00:00 UTC
    # longitude is in degrees, east positive
    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime

    # 7. Datetime construction
    # Base time is midnight UTC on date d
    midnight = datetime.combine(d, datetime.min.time()).replace(tzinfo=None) # Treat as naive UTC for calculation
    
    # Handle day wrapping
    def minutes_to_datetime(minutes):
        minutes = minutes % 1440
        if minutes < 0:
            minutes += 1440
        
        seconds = (minutes % 60) * 60
        minutes_part = minutes // 60
        
        # Calculate the date offset
        days_offset = minutes_part // 24
        time_of_day = datetime.min.time().replace(hour=minutes_part % 24, minute=minutes % 60)
        
        # Since the requirement is "UTC", we assume the initial date 'd' is the target date, 
        # and we adjust the date if necessary.
        new_date = d + timedelta(days=days_offset)
        return datetime.combine(new_date, time_of_day)
        
    # Re-implement minutes_to_datetime based on required return type and handling
    # A simpler approach: total minutes from start of day d
    
    def get_utc_datetime(minutes_from_midnight, base_date):
        total_minutes_in_day = 24 * 60 # 1440
        minutes_from_start_of_d = (minutes_from_midnight + total_minutes_in_day) % total_minutes_in_day
        
        # Calculate days difference
        day_diff = minutes_from_midnight // 1440
        
        # Minutes within the day
        minutes_within_day = int(minutes_from_midnight % 1440)
        
        new_date = base_date + timedelta(days=day_diff)
        
        # Time components
        hour = minutes_within_day // 60
        minute = minutes_within_day % 60
        
        return datetime(new_date.year, new_date.month, new_date.day, hour, minute, 0)

    sunrise_dt = get_utc_datetime(sunrise_minutes, d)
    sunset_dt = get_utc_datetime(sunset_minutes, d)

    return sunrise_dt, sunset_dt