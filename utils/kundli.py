import swisseph as swe
from datetime import datetime

# Set ephemeris path if needed
swe.set_ephe_path('/usr/share/ephe')

PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
    'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 'Venus': swe.VENUS,
    'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE, 'Ketu': swe.TRUE_NODE
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

def get_planet_positions(jd, debug=False):
    positions = {}
    raw_data = {}
    for name, pid in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, pid)
        sidereal_lon = lon - get_ayanamsa(jd)
        sidereal_lon = sidereal_lon % 360
        positions[name] = round(sidereal_lon, 4)
        if debug:
            raw_data[name] = {
                "tropical": round(lon, 4),
                "sidereal": round(sidereal_lon, 4)
            }
    return (positions, raw_data) if debug else (positions, None)

def get_house_cusps(jd, latitude, longitude):
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return {
        f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)
    }

def get_lagna(jd, latitude, longitude):
    _, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return round(ascmc[0], 4)

def get_nakshatra_and_pada(moon_lon):
    deg = moon_lon % 360
    segment = 13.333333
    nak_index = int(deg // segment)
    pada = int((deg % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada
    }

def generate_kundli_chart(jd, lat, lon, tz=5.5, system="kp", debug=False):
    swe.set_sid_mode(swe.SIDM_USER, 0, 23.999)  # KP Ayanamsa hardcoded

    planet_positions, raw_planets = get_planet_positions(jd, debug)
    lagna = get_lagna(jd, lat, lon)
    moon_deg = planet_positions['Moon']
    nakshatra_info = get_nakshatra_and_pada(moon_deg)

    chart = {
        "planet_positions": planet_positions,
        "ascendant": lagna,
        "nakshatra_details": nakshatra_info
    }

    if system == "kp":
        chart["house_cusps"] = get_house_cusps(jd, lat, lon)

    if debug:
        chart["debug"] = {
            "julian_day": jd,
            "ayanamsa": round(get_ayanamsa(jd), 6),
            "raw_planet_positions": raw_planets,
            "ascendant_deg": lagna,
            "moon_deg": moon_deg
        }

    return {
        "chart": chart,
        "meta": {
            "system": system,
            "julian_day": jd,
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "timezone": tz,
            "generated_at": datetime.utcnow().isoformat()
        }
    }
