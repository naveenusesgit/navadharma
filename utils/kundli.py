import swisseph as swe
from datetime import datetime

# Set Swiss Ephemeris path (update as needed)
swe.set_ephe_path('/usr/share/ephe')

# Always use KP ayanamsa
swe.set_sid_mode(swe.SIDM_USER, 0, 23.85675)  # KP Ayanamsa approx

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

def get_julian_day(year, month, day, hour, minute):
    return swe.julday(year, month, day, hour + (minute / 60.0))

def get_planet_positions(jd):
    positions = {}
    for name, pid in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, pid)[0]
        positions[name] = round(lon % 360, 4)
    return positions

def get_house_cusps(jd, lat, lon):
    """KP style: Placidus house system"""
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    house_data = {f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)}
    house_data["Ascendant"] = round(ascmc[0], 4)
    return house_data

def get_nakshatra_and_pada(moon_long):
    segment = 13.333333
    total = moon_long % 360
    nak_index = int(total // segment)
    pada = int((total % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada
    }

def get_sub_lords(jd):
    sublords = {}
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
        lon, _, _ = swe.calc_ut(jd, pid)[0]
        deg = lon % 360
        pos = deg
        idx = 0
        while pos > sublord_degrees[idx][1]:
            pos -= sublord_degrees[idx][1]
            idx = (idx + 1) % len(sublord_degrees)
        sublords[name] = sublord_degrees[idx][0]

    return sublords

def generate_kundli_chart(jd, lat, lon, tz=5.5):
    planet_positions = get_planet_positions(jd)
    moon_long = planet_positions.get("Moon", 0.0)
    
    chart = {
        "planet_positions": planet_positions,
        "ascendant": get_house_cusps(jd, lat, lon)["Ascendant"],
        "nakshatra_details": get_nakshatra_and_pada(moon_long),
        "house_cusps": get_house_cusps(jd, lat, lon),
        "sub_lords": get_sub_lords(jd)
    }

    return {
        "chart": chart,
        "meta": {
            "system": "kp",
            "julian_day": jd,
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "timezone": tz,
            "ayanamsa": round(swe.get_ayanamsa(jd), 6),
            "generated_at": datetime.utcnow().isoformat()
        }
    }
