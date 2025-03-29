import swisseph as swe
from datetime import datetime

# Set ephemeris path if needed
swe.set_ephe_path('/usr/share/ephe')  # Modify or remove as per your setup

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
    ("Ashwini", "Ketu"), ("Bharani", "Venus"), ("Krittika", "Sun"), ("Rohini", "Moon"),
    ("Mrigashira", "Mars"), ("Ardra", "Rahu"), ("Punarvasu", "Jupiter"), ("Pushya", "Saturn"),
    ("Ashlesha", "Mercury"), ("Magha", "Ketu"), ("Purva Phalguni", "Venus"), ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"), ("Chitra", "Mars"), ("Swati", "Rahu"), ("Vishakha", "Jupiter"),
    ("Anuradha", "Saturn"), ("Jyeshtha", "Mercury"), ("Mula", "Ketu"), ("Purva Ashadha", "Venus"),
    ("Uttara Ashadha", "Sun"), ("Shravana", "Moon"), ("Dhanishta", "Mars"), ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"), ("Uttara Bhadrapada", "Saturn"), ("Revati", "Mercury")
]

NAK_LENGTH = 13 + (20 / 60)  # 13° 20'

def get_nakshatra_info(degree):
    index = int(degree / NAK_LENGTH) % 27
    nakshatra, dasha_lord = NAKSHATRAS[index]
    pada = int(((degree % NAK_LENGTH) / (NAK_LENGTH / 4))) + 1
    return nakshatra, pada, dasha_lord

def get_planet_positions(jd, latitude, longitude):
    planet_positions = {}
    for name, planet_id in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, planet_id)
        planet_positions[name] = round(lon, 2)
    return planet_positions

def get_kp_planet_details(jd, latitude, longitude):
    kp_data = {}
    for name, planet_id in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, planet_id)
        nakshatra, pada, dasha_lord = get_nakshatra_info(lon)
        kp_data[name] = {
            "degree": round(lon, 2),
            "nakshatra": nakshatra,
            "pada": pada,
            "dasha_lord": dasha_lord,
            "sub_lord": "To be calculated"  # Placeholder for future enhancement
        }
    return kp_data

def get_house_cusps(jd, latitude, longitude):
    """Return house cusps using Placidus (used in KP)."""
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')  # Placidus = 'P'
    house_data = {f"House_{i+1}": round(cusp, 2) for i, cusp in enumerate(cusps)}
    house_data["Ascendant"] = round(ascmc[0], 2)
    return house_data

def generate_kundli_chart(jd, latitude, longitude, tz=5.5, system="vedic"):
    """
    Generate a Kundli chart based on system: 'vedic' or 'kp'.
    """
    if system.lower() == "kp":
        chart = {
            "planet_positions": get_kp_planet_details(jd, latitude, longitude),
            "house_cusps": get_house_cusps(jd, latitude, longitude)
        }
    else:
        chart = {
            "planet_positions": get_planet_positions(jd, latitude, longitude)
        }

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
