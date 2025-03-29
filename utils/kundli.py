import swisseph as swe
from datetime import datetime

# Set ephemeris path if needed (optional)
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

def get_ayanamsa(jd):
    """Get Lahiri ayanamsa for metadata"""
    return swe.get_ayanamsa(jd)

def get_planet_positions(jd, latitude, longitude):
    """Get planetary positions with longitudes."""
    positions = {}
    for name, pid in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, pid)
        positions[name] = round(lon, 4)
    return positions

def get_house_cusps(jd, latitude, longitude):
    """Return house cusps using Placidus system (used in KP)."""
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')  # Placidus = 'P'
    house_data = {f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)}
    house_data["Ascendant"] = round(ascmc[0], 4)
    return house_data

def get_sub_lords(jd, system='vedic'):
    """Determine sub-lords using KP Ayanamsa."""
    sublords = {}
    # Vimshottari Dasha sequence
    dasha_years = {
        'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
        'Mars': 7, 'Rahu': 18, 'Jupiter': 16,
        'Saturn': 19, 'Mercury': 17
    }
    dasha_lords = list(dasha_years.keys())

    total_span = 360
    sublord_degrees = []
    for lord in dasha_lords:
        deg = (dasha_years[lord] / 120) * total_span
        sublord_degrees.append((lord, deg))

    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)

        # Adjust for ayanamsa if KP
        if system.lower() == "kp":
            lon -= 23.999
            if lon < 0:
                lon += 360

        # Find sub-lord
        deg = lon % 360
        pos = deg
        idx = 0
        while pos > sublord_degrees[idx][1]:
            pos -= sublord_degrees[idx][1]
            idx = (idx + 1) % len(sublord_degrees)
        sublords[name] = sublord_degrees[idx][0]

    return sublords

def generate_kundli_chart(jd, latitude, longitude, tz=5.5, system="vedic"):
    """
    Generate a Kundli chart. Supports 'vedic' and 'kp'.
    """
    # Apply correct ayanamsa
    if system.lower() == "kp":
        swe.set_sid_mode(swe.SIDM_USER, 0, 23.999)  # KP Ayanamsa
    else:
        swe.set_sid_mode(swe.SIDM_LAHIRI)  # Default to Lahiri

    planet_positions = get_planet_positions(jd, latitude, longitude)
    chart = {
        "planet_positions": planet_positions
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
