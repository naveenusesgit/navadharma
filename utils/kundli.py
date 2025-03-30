import swisseph as swe
from datetime import datetime

swe.set_ephe_path('/usr/share/ephe')  # Use your server path

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

KP_AYANAMSA_OFFSET = 23.85675  # Accurate KP ayanamsa offset as of 1987

def get_planet_positions(jd):
    positions = {}
    for name, pid in PLANETS.items():
        lon, _lat, _ = swe.calc_ut(jd, pid)[0]
        positions[name] = round(lon, 4)
    return positions

def get_house_cusps(jd, latitude, longitude):
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return {f"House_{i+1}": round(c, 4) for i, c in enumerate(cusps)}, round(ascmc[0], 4)

def get_nakshatra_and_pada(moon_long):
    segment = 13.333333
    total = moon_long % 360
    nak_index = int(total // segment)
    pada = int((total % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada
    }

def get_ayanamsa(jd):
    return round(swe.get_ayanamsa(jd), 6)

def generate_kundli_chart(year, month, day, hour, minute, latitude, longitude, tz=5.5):
    # Convert local time to UTC
    utc_hour = hour - tz
    utc_decimal = utc_hour + (minute / 60.0)
    jd = swe.julday(year, month, day, utc_decimal)

    # Set KP Ayanamsa manually
    swe.set_sid_mode(swe.SIDM_USER, 0, KP_AYANAMSA_OFFSET)

    # Compute positions
    planet_positions = get_planet_positions(jd)
    houses, ascendant = get_house_cusps(jd, latitude, longitude)
    moon_long = planet_positions.get("Moon", 0.0)
    nak_pada = get_nakshatra_and_pada(moon_long)

    return {
        "chart": {
            "planet_positions": planet_positions,
            "house_cusps": houses,
            "ascendant": ascendant,
            "nakshatra_details": nak_pada
        },
        "meta": {
            "julian_day": jd,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "timezone": tz,
            "ayanamsa": KP_AYANAMSA_OFFSET,
            "generated_at": datetime.utcnow().isoformat()
        }
    }
