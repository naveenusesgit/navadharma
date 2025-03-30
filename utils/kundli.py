import swisseph as swe
from datetime import datetime

# Optional: set ephemeris path
swe.set_ephe_path('/usr/share/ephe')

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

# Nakshatra Dasha system (Vimshottari) - used in KP
DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
    'Mars': 7, 'Rahu': 18, 'Jupiter': 16,
    'Saturn': 19, 'Mercury': 17
}

def get_ayanamsa(jd):
    """Get ayanamsa for metadata display."""
    return swe.get_ayanamsa(jd)

def get_planet_positions(jd, latitude, longitude):
    """Get planetary longitudes (sidereal)."""
    positions = {}
    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)
        positions[name] = round(lon % 360, 4)
    return positions

def get_house_cusps(jd, latitude, longitude):
    """Return Placidus house cusps and ascendant (for KP system)."""
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    house_data = {f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)}
    house_data["Ascendant"] = round(ascmc[0], 4)
    return house_data

def get_sub_lords(jd, system='kp'):
    """Compute sub-lords based on Vimshottari dasha proportion logic."""
    total_span = 360
    degrees_by_lord = [(k, (v / 120) * total_span) for k, v in DASHA_YEARS.items()]

    sublords = {}
    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)

        # Adjust longitude for KP ayanamsa
        if system.lower() == "kp":
            lon -= 23.85675
            if lon < 0:
                lon += 360

        deg = lon % 360
        idx = 0
        while deg > degrees_by_lord[idx][1]:
            deg -= degrees_by_lord[idx][1]
            idx = (idx + 1) % len(degrees_by_lord)

        sublords[name] = degrees_by_lord[idx][0]

    return sublords

def get_ascendant(jd, latitude, longitude):
    """Return the Ascendant degree."""
    _, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return round(ascmc[0], 4)

def generate_kundli_chart(jd, latitude, longitude, tz=5.5, system="vedic"):
    """
    Generate a kundli chart. Supports both 'vedic' and 'kp' systems.
    """
    # Set ayanamsa
    if system.lower() == "kp":
        swe.set_sid_mode(swe.SIDM_USER, 0, 23.85675)  # KP ayanamsa value
    else:
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    chart = {
        "planet_positions": get_planet_positions(jd, latitude, longitude),
        "ascendant": get_ascendant(jd, latitude, longitude)
    }

    if system.lower() == "kp":
        chart["house_cusps"] = get_house_cusps(jd, latitude, longitude)
        chart["sub_lords"] = get_sub_lords(jd, system)

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
            "ayanamsa": round(get_ayanamsa(jd), 6),
            "generated_at": datetime.utcnow().isoformat()
        }
    }
