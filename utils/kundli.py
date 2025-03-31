import swisseph as swe
from datetime import datetime

# Set Swiss Ephemeris path (optional)
swe.set_ephe_path('/usr/share/ephe')

# Set KP Ayanamsa (23.8668° approx)
swe.set_sid_mode(swe.SIDM_USER, 0, 23.8668)

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

def get_planet_positions(jd):
    positions = {}
    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)
        positions[name] = round(lon % 360, 4)
    return positions

def get_lagna(jd, latitude, longitude):
    _, ascmc = swe.houses(jd, latitude, longitude, b'P')  # Placidus
    return round(ascmc[0], 4)

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
    cusps, _ = swe.houses(jd, latitude, longitude, b'P')  # Placidus
    return {f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)}

def get_ayanamsa(jd):
    return round(swe.get_ayanamsa(jd), 6)

def generate_kundli_chart(jd, latitude, longitude, tz=5.5, system="kp"):
    planet_positions = get_planet_positions(jd)
    moon_long = planet_positions.get("Moon", 0.0)

    chart = {
        "planet_positions": planet_positions,
        "ascendant": get_lagna(jd, latitude, longitude),
        "nakshatra_details": get_nakshatra_and_pada(moon_long),
        "house_cusps": get_house_cusps(jd, latitude, longitude),
    }

    return {
        "chart": chart,
        "meta": {
            "system": system,
            "julian_day": jd,
            "ayanamsa": get_ayanamsa(jd),
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "timezone": tz,
            "generated_at": datetime.utcnow().isoformat()
        }
    }
