import swisseph as swe
from datetime import datetime

# Set ephemeris path
swe.set_ephe_path('/usr/share/ephe')  # Optional

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

def get_ayanamsa(jd):
    return swe.get_ayanamsa(jd)

def get_planet_positions(jd, latitude, longitude):
    positions = {}
    for name, pid in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, pid)[0]
        positions[name] = round(lon % 360, 4)
    return positions

def get_house_cusps(jd, latitude, longitude):
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')  # Placidus for KP
    return {
        f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)
    }, round(ascmc[0], 4)  # ascendant degree

def get_nakshatra_and_pada(moon_longitude):
    segment = 13.333333
    nak_index = int(moon_longitude // segment)
    pada = int((moon_longitude % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada
    }

def get_sub_lords(jd, system='vedic'):
    sublords = {}
    dasha_years = {
        'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
        'Mars': 7, 'Rahu': 18, 'Jupiter': 16,
        'Saturn': 19, 'Mercury': 17
    }
    dasha_lords = list(dasha_years.keys())
    total_span = 360
    sublord_degrees = [(lord, (dasha_years[lord] / 120) * total_span) for lord in dasha_lords]

    for name, pid in PLANETS.items():
        lon = swe.calc_ut(jd, pid)[0][0]
        if system.lower() == "kp":
            lon -= get_ayanamsa(jd)
        deg = lon % 360
        idx = 0
        pos = deg
        while pos > sublord_degrees[idx][1]:
            pos -= sublord_degrees[idx][1]
            idx = (idx + 1) % len(sublord_degrees)
        sublords[name] = sublord_degrees[idx][0]

    return sublords

def generate_kundli_chart(jd, latitude, longitude, tz=5.5, system="vedic"):
    # 🔁 Use correct Ayanamsa based on system
    if system.lower() == "kp":
        swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    else:
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    planet_positions = get_planet_positions(jd, latitude, longitude)
    moon_long = planet_positions.get("Moon", 0.0)
    nakshatra = get_nakshatra_and_pada(moon_long)

    chart = {
        "planet_positions": planet_positions,
        "nakshatra_details": nakshatra
    }

    if system.lower() == "kp":
        house_cusps, asc = get_house_cusps(jd, latitude, longitude)
        chart["house_cusps"] = house_cusps
        chart["ascendant"] = asc
        chart["sub_lords"] = get_sub_lords(jd, system)
    else:
        _, asc = get_house_cusps(jd, latitude, longitude)
        chart["ascendant"] = asc

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
            "moon_degree": round(moon_long, 4),
            "ascendant_degree": chart["ascendant"],
            "generated_at": datetime.utcnow().isoformat()
        }
    }
