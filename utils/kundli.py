import swisseph as swe
from datetime import datetime

# Set ephemeris path if needed
swe.set_ephe_path('/usr/share/ephe')  # You can modify or remove this if not required

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

def get_house_cusps(jd, latitude, longitude):
    """Return house cusps using Placidus (used in KP)."""
    flags = swe.FLG_SWIEPH
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')  # Placidus = 'P'
    house_data = {f"House_{i+1}": round(cusp, 2) for i, cusp in enumerate(cusps)}
    house_data["Ascendant"] = round(ascmc[0], 2)
    return house_data

def generate_kundli_chart(jd, latitude, longitude, tz=5.5, system="vedic"):
    """
    Generate a Kundli chart based on system: 'vedic' or 'kp'.
    """
    chart = {
        "planet_positions": get_planet_positions(jd, latitude, longitude)
    }

    if system.lower() == "kp":
        chart["house_cusps"] = get_house_cusps(jd, latitude, longitude)

    return {
        "chart": chart,
        "meta": {
            "system": system,
            "julian_day": jd,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "timezone": tz,
            "generated_at": datetime.utcnow().isoformat()
        }
    }
