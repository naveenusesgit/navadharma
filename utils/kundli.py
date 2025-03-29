import swisseph as swe
from datetime import datetime

# Set the ephemeris path (optional, if not using .se1 files)
swe.set_ephe_path('/usr/share/ephe')  # This can be changed or removed

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Ketu': swe.TRUE_NODE,
}


def get_planet_positions(jd, latitude, longitude):
    planet_positions = {}
    for name, planet_id in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, planet_id)
        planet_positions[name] = round(lon, 2)
    return planet_positions


def generate_kundli_chart(jd, latitude, longitude):
    """
    Generate a basic kundli chart with planetary positions.
    """
    positions = get_planet_positions(jd, latitude, longitude)
    return {
        "chart": {
            "planet_positions": positions
        },
        "meta": {
            "julian_day": jd,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "generated_at": datetime.utcnow().isoformat()
        }
    }
