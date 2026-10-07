# NOAA general solar position equations (sunrise / sunset)

Source: NOAA Global Monitoring Laboratory, "General Solar Position Calculations".
All angles in the trig functions are in **radians** unless marked degrees.

1. Day of year `doy` (1 = Jan 1). Fractional year, evaluated at 12:00 UTC:

       gamma = 2*pi/365 * (doy - 1)

2. Equation of time, in **minutes**:

       eqtime = 229.18 * (0.000075 + 0.001868*cos(gamma) - 0.032077*sin(gamma)
                          - 0.014615*cos(2*gamma) - 0.040849*sin(2*gamma))

3. Solar declination, in **radians**:

       decl = 0.006918 - 0.399912*cos(gamma) + 0.070257*sin(gamma)
              - 0.006758*cos(2*gamma) + 0.000907*sin(2*gamma)
              - 0.002697*cos(3*gamma) + 0.00148*sin(3*gamma)

4. Hour angle at sunrise/sunset, with lat in radians. 90.833 degrees accounts for refraction
   and the size of the solar disk. Convert `ha` to **degrees** for step 5:

       ha = arccos( cos(radians(90.833)) / (cos(lat)*cos(decl)) - tan(lat)*tan(decl) )

5. Times in **minutes after 00:00 UTC** on that date. Longitude in degrees, **east positive**,
   so west longitudes are negative:

       sunrise = 720 - 4*(longitude + ha_degrees) - eqtime
       sunset  = 720 - 4*(longitude - ha_degrees) - eqtime

   The result can be below 0 or at/above 1440 (the event falls on the previous or next UTC day).
   Build the datetime as midnight UTC on the date plus a timedelta of that many minutes.
