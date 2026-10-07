import datetime
import math

def sun_times(lat: float, lon: float, d: datetime.date) -> tuple[datetime.datetime, datetime.datetime]:
    # Calculate mean anomaly (M)
    M = (360 / 365.2422) * (d.timetuple().tm_yday - 81) * 0.98564736629

    # Calculate mean longitude (L)
    L = (270.4505883 + 360.985647366 * (d.timetuple().tm_yday - 81) / 365.2422) * math.pi / 180.0

    # Calculate equation of center (C)
    C = 1.915 * math.sin(L) + 0.020 * math.sin(2 * L)

    # Solar declination (delta)
    delta = 23.45 * math.asin(math.sin(L) * math.cos(math.pi / 180.0))

    # Hour angle (H) calculation: cos(H) = -tan(latitude) * tan(delta)
    cos_H = -math.tan(math.radians(lat)) * math.tan(delta)
    
    # Clamp cos_H to [-1, 1] to avoid domain error in acos due to floating point inaccuracies
    cos_H = max(min(cos_H, 1.0), -1.0)
    
    H = math.acos(cos_H) # Hour angle in radians

    # Time difference from solar noon (in hours)
    time_diff_from_noon = H / (15 * math.pi / 180.0)

    # Solar Noon Time in local time (approximation: 12:00)
    solar_noon_local_hour = 12
    
    # Local sunrise/sunset times
    local_sunrise_hour_float = solar_noon_local_hour - time_diff_from_noon
    local_sunset_hour_float = solar_noon_local_hour + time_diff_from_noon

    # Convert hours to minutes and round
    def round_time(h_float):
        h_int = int(h_float)
        m_float = (h_float - h_int) * 60
        m_int = int(round(m_float))
        return h_int, m_int

    # Local time objects
    sr_h, sr_m = round_time(local_sunrise_hour_float)
    ss_h, ss_m = round_time(local_sunset_hour_float)

    # Apply longitude correction to get UTC
    # Time shift due to longitude (hours): lon / 15
    time_shift = lon / 15.0
    
    # UTC times
    utc_sunrise_hour = round(sr_h - time_shift)
    utc_sunrise_minute = round(sr_m)
    
    utc_sunset_hour = round(ss_h - time_shift)
    utc_sunset_minute = round(ss_m)

    # Handle wrap around (if UTC time falls on previous/next day)
    # For simplicity, we assume the day is the same as input date for both
    
    return datetime.datetime(d.year, d.month, d.day, utc_sunrise_hour, utc_sunrise_minute), \
           datetime.datetime(d.year, d.month, d.day, utc_sunset_hour, utc_sunset_minute)

if __name__ == '__main__':
    # Example usage (London: 51.5, -0.13, 2026-06-21)
    lat = 51.5
    lon = -0.13
    date = datetime.date(2026, 6, 21)
    sunrise, sunset = sun_times(lat, lon, date)
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
