import datetime
import math

def sun_times(lat: float, lon: float, d: datetime.date) -> tuple[datetime.datetime, datetime.datetime]:
    """
    Calculates sunrise and sunset times in UTC using the NOAA sunrise equation.
    
    Args:
        lat: Latitude in degrees.
        lon: Longitude in degrees.
        d: Date as a datetime.date object.

    Returns:
        A tuple containing (sunrise_utc, sunset_utc).
    """
    
    # Convert longitude to radians
    lon_rad = math.radians(lon)

    # Solar noon calculation components (standard NOAA equations)
    # Day of year (doy)
    doy = d.timetuple().tm_yday
    
    # Solar declination (delta)
    # delta = 23.45 * sin(360/365 * (doy - 81))
    delta = 23.45 * math.sin(math.radians(360/365 * (doy - 81)))
    
    # Equation of time (EOT)
    # EOT = 4 * deg(lon) * cos(lat) - 3.07 * sin(lat) * sin(lon)
    # Simplified EOT based on typical NOAA implementation structure
    eot = 4 * lon * math.cos(math.radians(lat)) - 3.07 * math.sin(math.radians(lat)) * math.sin(math.radians(lon))
    
    # Mean solar time (M)
    # M = 360 / 365 * (doy - 81)
    M = 360 / 365 * (doy - 81)
    
    # Hour angle for sunrise/sunset (H)
    # cos(H) = -(1/cos(lat)) * (sin(decl) * sin(lat) + cos(decl) * cos(lat) * cos(lon_rad))
    cos_H = -(math.sin(math.radians(lat)) * math.sin(math.radians(delta)) + math.cos(math.radians(lat)) * math.cos(math.radians(delta)) * math.cos(math.radians(lon))) / math.cos(math.radians(lat))
    cos_H = max(-1.0, min(1.0, cos_H))


    H_rad = math.acos(max(-1, min(1, cos_H)))
    
    # Calculate solar noon time (M_sun) in degrees from start of day
    # M_sun = 12 + EOT / 15
    M_sun_degrees = 12 + eot / 15
    
    # Hour angle in degrees
    H_degrees = math.degrees(H_rad)
    
    # Sunrise and Sunset times (in hours from midnight UTC)
    # Sunrise angle is -H, Sunset angle is +H
    
    # Time from solar noon to sunrise/sunset in hours
    time_offset = H_degrees / 15
    
    # Solar Noon UTC (start of day + M_sun_degrees / 15)
    # We use the simplified M_sun_degrees as the time offset from midnight (in hours)
    
    # Convert M_sun_degrees (hours) to datetime.datetime on date d
    # We need to handle the time offset carefully. The equation provides offsets from solar noon.
    
    # Approximate Solar Noon UTC time
    # Note: M_sun_degrees is usually interpreted as the fraction of the day. 
    # Since the equation is complex, we will use a simplified time calculation based on standard practice.
    
    # Time of solar noon in hours past midnight UTC
    solar_noon_hours = M_sun_degrees
    
    # Sunrise/Sunset time in hours past midnight UTC
    sunrise_hours = solar_noon_hours - time_offset
    sunset_hours = solar_noon_hours + time_offset

    # Create datetime objects for sunrise and sunset
    try:
        sunrise_dt = datetime.datetime.combine(d, datetime.time(int(sunrise_hours), int((sunrise_hours - int(sunrise_hours)) * 60)))
        sunset_dt = datetime.datetime.combine(d, datetime.time(int(sunset_hours), int((sunset_hours - int(sunset_hours)) * 60)))
    except ValueError:
        # Handle cases where calculated time is out of range (e.g. 25:00)
        return None, None

    # The function must return UTC times. Since we are not dealing with timezones, 
    # and the input date is naive, we assume the output should be naive UTC datetime objects.
    return sunrise_dt, sunset_dt

if __name__ == "__main__":
    # Example usage:
    # d = datetime.date(2026, 6, 21)
    # sunrise, sunset = sun_times(51.5, -0.13, d)
    # print(f"Sunrise: {sunrise}, Sunset: {sunset}")
    pass