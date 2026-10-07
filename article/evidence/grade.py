import datetime, sys, os
sys.path.insert(0, os.getcwd())
try:
    from daylight import sun_times
    cases = [  # (lat, lon, date, sunrise UTC, sunset UTC) from NOAA solar calculator, +-10 min
        (51.5, -0.13, datetime.date(2026, 6, 21), (3, 43), (20, 21)),
        (40.71, -74.01, datetime.date(2026, 12, 21), (12, 16), (21, 32)),
        (-33.87, 151.21, datetime.date(2026, 3, 20), (19, 58), (8, 4)),
    ]
    ok = 0
    for lat, lon, d, (rh, rm), (sh, sm) in cases:
        r, s = sun_times(lat, lon, d)
        def mins(t): return t.hour * 60 + t.minute
        dr = abs((mins(r) - (rh * 60 + rm) + 720) % 1440 - 720)
        ds = abs((mins(s) - (sh * 60 + sm) + 720) % 1440 - 720)
        ok += dr <= 10 and ds <= 10
    print(f"GRADER {ok}/{len(cases)}")
except Exception as e:
    print(f"GRADER ERROR {type(e).__name__}: {e}")
