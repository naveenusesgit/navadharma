import swisseph as swe
from datetime import datetime
from .astro_utils import get_planet_positions  # You already have this

PLANETS = [
    swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER,
    swe.VENUS, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO
]

PLANET_NAMES = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter",
    "Venus", "Saturn", "Uranus", "Neptune", "Pluto"
]

def get_current_transits(lat, lon, timezone_offset=0):
    now = datetime.utcnow()
    jd_now = swe.julday(now.year, now.month, now.day, now.hour)

    swe.set_topo(lon, lat, 0)

    transit_data = {}

    for i, planet in enumerate(PLANETS):
        lon, lat_, dist = swe.calc_ut(jd_now, planet)
        transit_data[PLANET_NAMES[i]] = round(lon, 2)

    return transit_data

def compare_transits_with_natal(transits, natal):
    influence_report = []

    for planet, transit_lon in transits.items():
        natal_lon = natal.get(planet)
        if natal_lon:
            diff = (transit_lon - natal_lon + 360) % 360
            if 0 <= diff <= 10:
                influence_report.append(f"{planet} is conjunct natal position (within {round(diff, 1)}°)")
            elif 170 <= diff <= 190:
                influence_report.append(f"{planet} is opposite natal position (around {round(diff, 1)}°)")
            elif abs(diff - 90) <= 10 or abs(diff - 270) <= 10:
                influence_report.append(f"{planet} is square natal position ({round(diff, 1)}°)")

    return influence_report
