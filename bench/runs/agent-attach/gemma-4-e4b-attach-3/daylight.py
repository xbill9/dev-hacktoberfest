import math
from datetime import date, datetime, timedelta

def sun_times(lat: float, lon: float, d: date) -> tuple[datetime, datetime]:
    doy = d.timetuple().tm_yday
    
    # 1. Day of year doy
    gamma = (2 * math.pi / 365) * (doy - 1)

    # 2. Equation of time, in minutes
    eqtime = 229.18 * (0.000075 + 0.001868*math.cos(gamma) - 0.032077*math.sin(gamma) - 0.014615*math.cos(2*gamma) - 0.040849*math.sin(2*gamma))

    # 3. Solar declination, in radians
    decl = 0.006918 - 0.399912*math.cos(gamma) + 0.070257*math.sin(gamma) - 0.006758*math.cos(2*gamma) + 0.000907*math.sin(2*gamma) - 0.002697*math.cos(3*gamma) + 0.00148*math.sin(3*gamma)

    # Convert latitude to radians
    lat_rad = math.radians(lat)
    
    # 4. Hour angle at sunrise/sunset, with lat in radians.
    # Note: 90.833 degrees accounts for refraction and the size of the solar disk.
    try:
        ha_rad = math.acos((math.cos(math.radians(90.833)) / (math.cos(lat_rad) * math.cos(decl))) - (math.tan(lat_rad) * math.tan(decl)))
    except ValueError:
        # Handle cases where the argument to acos is outside [-1, 1] (e.g., polar regions)
        # In such cases, sunrise/sunset might not occur, or the math fails.
        # We'll raise an error for now, assuming valid inputs for the test case.
        # A more robust solution would return None or raise a specific error.
        raise ValueError("Invalid astronomical parameters for given location/date.")

    ha_degrees = math.degrees(ha_rad)

    # 5. Times in minutes after 00:00 UTC
    # Longitude in degrees, east positive, so west longitudes are negative.
    # lon is already in degrees.

    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime

    # Convert minutes to datetime object for midnight UTC on that date
    # The result can be below 0 or at/above 1440.
    
    # Calculate total minutes since start of the year (doy-1 * 1440)
    start_of_day_minutes = (doy - 1) * 1440
    
    sunrise_total_minutes = start_of_day_minutes + sunrise_minutes
    sunset_total_minutes = start_of_day_minutes + sunset_minutes
    
    # Create datetime object from total minutes offset from the start of the year (Jan 1 00:00 UTC)
    # Since we are only dealing with time components relative to the day, 
    # let's simplify: take the base date (d) and add the calculated minutes offset.
    
    sunrise_timedelta = timedelta(minutes=sunrise_minutes)
    sunset_timedelta = timedelta(minutes=sunset_minutes)

    # Since the result can cross day boundaries (e.g., sunrise minutes < 0 or > 1440), 
    # we need to adjust the date accordingly.
    
    # We calculate the time based on the date 'd'. If the minutes are outside [0, 1440), we adjust the date.
    
    def get_dt_from_minutes(minutes_offset, base_date):
        # Calculate how many days to add/subtract
        days_offset = math.ceil(minutes_offset / 1440)
        
        # Calculate time within the day (0 to 1439.99...)
        time_within_day_minutes = minutes_offset % 1440
        if time_within_day_minutes < 0:
            time_within_day_minutes += 1440
            
        new_date = base_date + timedelta(days=days_offset)
        
        # Calculate hours, minutes, seconds from the remaining minutes
        hours = int(time_within_day_minutes // 60)
        minutes = int(time_within_day_minutes % 60)
        
        return datetime(new_date.year, new_date.month, new_date.day, hours, minutes, 0)

    sunrise_dt = get_dt_from_minutes(sunrise_minutes, d)
    sunset_dt = get_dt_from_minutes(sunset_minutes, d)

    return sunrise_dt, sunset_dt