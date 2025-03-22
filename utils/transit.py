from datetime import datetime
from utils.geolocation import get_lat_lon_timezone
import swisseph as swe

def get_transits(dob: str, tob: str, pob: str):
    # Parse datetime
    dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")

    # Get location data
    lat, lon, tz = get_lat_lon_timezone(pob)
    local_dt = dt
    utc_dt = local_dt.astimezone(tz).astimezone(datetime.timezone.utc)

    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)

    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": swe.MEAN_NODE
    }

    transits = {}
    for planet_name, planet_const in planets.items():
        lon, _ = swe.calc_ut(jd_ut, planet_const)
        if planet_name == "Ketu":
            lon = (lon + 180) % 360
        transits[planet_name] = round(lon, 2)

    return {
        "datetime_utc": utc_dt.isoformat(),
        "location": {"lat": lat, "lon": lon},
        "transits": transits
    }

def get_daily_global_transits(date_str=None):
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.utcnow()

    jd = swe.julday(date.year, date.month, date.day)
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": swe.MEAN_NODE
    }

    transits = {}
    for name, planet in planets.items():
        lon, _ = swe.calc_ut(jd, planet)
        if name == "Ketu":
            lon = (lon + 180) % 360
        transits[name] = round(lon, 2)

    return {
        "date": date.strftime("%Y-%m-%d"),
        "transits": transits
    }
