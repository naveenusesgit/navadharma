import swisseph as swe
from datetime import datetime
from typing import Dict, Any, List

swe.set_ephe_path('.')
swe.set_ayanamsa_mode(swe.AYANAMSA_KRISHNAMURTI)  # KP Ayanamsa

PLANETS = [
    swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
    swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
    swe.MEAN_NODE  # Rahu
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]


def get_planet_positions(dt_str: str, lat: float, lon: float, tz: float) -> Dict[str, Any]:
    utc_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                    utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600 - tz)

    positions = {}
    for p in PLANETS:
        lon_deg, _ = swe.calc_ut(jd, p)[0:2]
        planet_name = swe.get_planet_name(p)
        positions[planet_name] = round(lon_deg % 360, 4)
    return positions


def get_nakshatra_and_pada(moon_longitude: float) -> Dict[str, Any]:
    nak_idx = int(moon_longitude // (360 / 27))
    pada = int((moon_longitude % (360 / 27)) // (360 / 108)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_idx],
        "padam": str(pada)
    }


def get_lagna(jd: float, lat: float, lon: float) -> Dict[str, Any]:
    asc = swe.houses_ex(jd, lat, lon, b'A')[0][0]  # Ascendant degree
    return {
        "lagna_degree": round(asc, 2),
        "lagna_sign": get_zodiac_sign(asc)
    }


def get_zodiac_sign(lon_deg: float) -> str:
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    index = int((lon_deg % 360) // 30)
    return signs[index]


def generate_kundli_chart(dt_str: str, lat: float, lon: float, tz: float) -> Dict[str, Any]:
    utc_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                    utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600 - tz)

    asc_data = get_lagna(jd, lat, lon)
    planet_pos = get_planet_positions(dt_str, lat, lon, tz)
    moon_lon = planet_pos.get("Moon", 0)
    nak_pada = get_nakshatra_and_pada(moon_lon)

    return {
        "ascendant": asc_data,
        "planet_positions": planet_pos,
        "nakshatra_details": nak_pada
    }
