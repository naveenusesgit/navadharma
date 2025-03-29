import swisseph as swe
from datetime import datetime

# Set ephemeris path
swe.set_ephe_path('/usr/share/ephe')  # adjust this as needed

# Set KP-compatible mode: Lahiri ayanamsa, sidereal
swe.set_sid_mode(swe.SIDM_LAHIRI)

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

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_planet_positions(jd, latitude, longitude):
    planet_positions = {}
    for name, pid in PLANETS.items():
        lon, _lat, _dist = swe.calc_ut(jd, pid)[0]
        planet_positions[name] = round(lon % 360, 2)
    return planet_positions

def get_lagna(jd, latitude, longitude):
    """Compute the Ascendant (Lagna)"""
    flags = swe.FLG_SIDEREAL
    cusp, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return round(ascmc[0], 2)  # Ascendant is ascmc[0]

def get_nakshatra_and_pada(moon_longitude):
    segment = 13.333333
    total = moon_longitude % 360
    nak_index = int(total // segment)
    pada = int((total % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada
    }

def get_house_cusps(jd, latitude, longitude):
    """KP system: Placidus houses"""
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return {
        f"House_{i+1}": round(cusp, 2)
        for i, cusp in enumerate(cusps)
    }

def generate_kundli_chart(jd, latitude, longitude, tz=5.5, system="vedic"):
    chart = {
        "planet_positions": get_planet_positions(jd, latitude, longitude)
    }

    moon_long = chart["planet_positions"].get("Moon", 0.0)
    chart["nakshatra_details"] = get_nakshatra_and_pada(moon_long)
    chart["ascendant"] = get_lagna(jd, latitude, longitude)

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
