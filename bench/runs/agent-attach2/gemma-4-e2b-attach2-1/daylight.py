import math
from datetime import datetime, date, timedelta

def sun_times(lat: float, lon: float, d: date) -> tuple[datetime, datetime]:
    doy = d.timetuple().tm_yday
    
    # 1. Day of year doy
    gamma = 2 * math.pi / 365 * (doy - 1)
    
    # 2. Equation of time, in minutes
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    
    # 3. Solar declination, in radians
    decl = (0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) - 
            0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) - 
            0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma))
    
    # 4. Hour angle at sunrise/sunset, with lat in radians. 90.833 degrees accounts for refraction
    # Convert 90.833 degrees to radians internally for consistency if using math functions, 
    # but the formula uses degrees in the argument to radians() inside.
    ha_degrees = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(math.radians(lat)) * math.cos(decl) - math.tan(math.radians(lat)) * math.tan(decl))))

    # Re-reading the formula from docs: "ha = arccos( cos(radians(90.833)) / (cos(lat)*cos(decl)) - tan(lat)*tan(decl) )"
    # The provided formula in the document has lat/decl as input to cos/tan directly, implying they might expect them in degrees or radians depending on context.
    # Given the context of other equations using gamma (radians), we must assume lat and decl need conversion or the formula implies they should be in radians for the trig functions if the constants are accurate.
    # NOAA equations usually expect latitude and declination in radians for standard math library usage.
    # Let's stick strictly to the documented formula structure, converting lat and decl to radians for safety.
    
    lat_rad = math.radians(lat)
    decl_rad = math.radians(decl)
    
    # Re-calculating ha using standard math library interpretation based on the formula structure provided.
    ha_rad = math.acos(math.cos(math.radians(90.833)) / (math.cos(lat_rad) * math.cos(decl_rad) - math.tan(lat_rad) * math.tan(decl_rad)))
    
    # Convert ha to degrees for step 5 (as per instruction)
    ha_degrees = math.degrees(ha_rad)

    # 5. Times in minutes after 00:00 UTC on that date.
    # Longitude in degrees, east positive, so west longitudes are negative.
    # Convert longitude to degrees if it's not already, but inputs are expected to be degrees per problem statement.
    # We assume lon is in degrees as per typical usage for these formulas when longitude is specified as degrees.
    
    sunrise_minutes = 720 - 4 * (lon + ha_degrees) - eqtime
    sunset_minutes = 720 - 4 * (lon - ha_degrees) - eqtime
    
    # Build the datetime as midnight UTC on the date plus a timedelta of that many minutes.
    
    sunrise_dt = datetime(d.year, d.month, d.day, 0, 0) + timedelta(minutes=sunrise_minutes)
    sunset_dt = datetime(d.year, d.month, d.day, 0, 0) + timedelta(minutes=sunset_minutes)
    
    return sunrise_dt, sunset_dt