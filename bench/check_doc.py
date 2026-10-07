"""Implement docs/NOAA_SOLAR.md literally and compare with astral (needs: pip install astral)."""
import datetime as dt, math
from astral import LocationInfo
from astral.sun import sun

def noaa(lat, lon, d):
    g = 2 * math.pi / 365 * (d.timetuple().tm_yday - 1)
    eq = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                   - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    de = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
          + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    la = math.radians(lat)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(la) * math.cos(de))
                                - math.tan(la) * math.tan(de)))
    base = dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc)
    return (base + dt.timedelta(minutes=720 - 4 * (lon + ha) - eq),
            base + dt.timedelta(minutes=720 - 4 * (lon - ha) - eq))

worst = 0
for lat, lon, d in [(51.5, -0.13, dt.date(2026, 6, 21)), (40.71, -74.01, dt.date(2026, 12, 21)),
                    (-33.87, 151.21, dt.date(2026, 3, 20))]:
    r, s = noaa(lat, lon, d)
    a = sun(LocationInfo("x", "x", "UTC", lat, lon).observer, date=d)
    # astral reports the event on the given UTC date; the sheet can land a day either side,
    # so compare time of day (minutes, wrapped), as grade.py does
    def gap(x, y):
        m = abs((x - y).total_seconds()) / 60 % 1440
        return min(m, 1440 - m)
    dr, ds = gap(r, a["sunrise"]), gap(s, a["sunset"])
    worst = max(worst, dr, ds)
    print(f"{lat},{lon} {d}: doc {r:%H:%M}/{s:%H:%M}  astral {a['sunrise']:%H:%M}/{a['sunset']:%H:%M}  diff {dr:.1f}/{ds:.1f} min")
print(f"worst difference: {worst:.1f} min")
