from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import SUN, MOON, MARS, MERCURY, JUPITER, VENUS, SATURN

# Optional: planets list if needed
FLATLIB_PLANETS = [SUN, MOON, MARS, MERCURY, JUPITER, VENUS, SATURN]

def get_planetary_strength_flatlib(datetime_str, lat, lon, tz_offset):
    """Only for classical 7 planets (Flatlib doesn't support Rahu/Ketu)."""
    date_obj = Datetime(datetime_str, tz_offset)
    pos = GeoPos(lat, lon)
    chart = Chart(date_obj, pos)

    strengths = {}
    for planet in FLATLIB_PLANETS:
        obj = chart.get(planet)
        strengths[planet] = {
            "sign": obj.sign,
            "longitude": obj.lon,
            "house": obj.house,
            "isRetrograde": obj.retro,
        }

    return strengths
