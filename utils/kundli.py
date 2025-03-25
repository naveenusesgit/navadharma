import swisseph as swe
import datetime
from typing import List, Dict

# Set ephemeris path (you can include ephemeris files in your project if needed)
swe.set_ephe_path('/usr/share/ephe')  # You can customize this path if running locally

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Ketu': swe.MEAN_NODE  # Ketu is calculated as opposite of Rahu
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra",
    "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

MAJOR_DASHA_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

MAJOR_DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
}

def get_planet_positions(jd: float) -> List[Dict[str, float]]:
    results = []
    for planet_name, planet_id in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, planet_id)
        if planet_name == "Ketu":
            lon = (lon + 180.0) % 360.0
        results.append({
            "planet": planet_name,
            "degree": round(lon, 4)
        })
    return results


def get_nakshatra_info(jd: float) -> Dict[str, str]:
    moon_lon, _, _ = swe.calc_ut(jd, swe.MOON)
    nak_index = int(moon_lon // (360 / 27))
    nakshatra = NAKSHATRAS[nak_index]
    pada = int(((moon_lon % (360 / 27)) // (360 / 108)) + 1)
    return {
        "nakshatra": nakshatra,
        "pada": f"{pada}"
    }


def get_lagna_info(jd: float, lat: float, lon: float) -> Dict[str, str]:
    # Ascendant or Lagna calculation
    houses = swe.houses(jd, lat, lon)[1]
    ascendant = houses[0]  # First house cusp
    return {
        "lagna_degree": round(ascendant, 4),
        "lagna_sign": zodiac_sign(ascendant)
    }


def zodiac_sign(degree: float) -> str:
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return signs[int(degree // 30)]


def get_dasha_periods(jd: float) -> List[Dict[str, str]]:
    # This is a simplified Vimshottari Dasha mock logic (not accurate)
    # In real-world apps, use full dasha calculation libraries or formulas
    start_year = datetime.datetime.utcnow().year
    dasha_periods = []

    for lord in MAJOR_DASHA_SEQUENCE:
        years = MAJOR_DASHA_YEARS[lord]
        end_year = start_year + years
        dasha_periods.append({
            "dasha_lord": lord,
            "start_year": start_year,
            "end_year": end_year
        })
        start_year = end_year

    return dasha_periods
