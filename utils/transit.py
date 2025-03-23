# utils/transit.py

from datetime import datetime
import swisseph as swe
from utils.geolocation import get_lat_lon_timezone

def get_transits(dob: str, tob: str, pob: str):
    birth_datetime = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
    geo = get_lat_lon_timezone(pob)

    current_jd = swe.julday(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day)
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    planet_codes = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS, "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE, "Ketu": swe.TRUE_NODE
    }

    transit_data = {}
    for planet in planets:
        code = planet_codes[planet]
        lon, _, _ = swe.calc_ut(current_jd, code)
        transit_data[planet] = {"longitude": lon[0]}

    return {
        "location": geo,
        "transits": transit_data
    }

def get_daily_global_transits():
    current_jd = swe.julday(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day)
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    planet_codes = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS, "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE, "Ketu": swe.TRUE_NODE
    }

    transit_data = {}
    for planet in planets:
        code = planet_codes[planet]
        lon, _, _ = swe.calc_ut(current_jd, code)
        transit_data[planet] = {"longitude": lon[0]}

    return {
        "transits": transit_data,
        "timestamp": datetime.utcnow().isoformat()
    }
