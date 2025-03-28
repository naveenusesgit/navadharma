import swisseph as swe
import math
from datetime import datetime
import pytz

# Set path to ephemeris data (adjust as needed or use default)
swe.set_ephe_path(".")
swe.set_ayanamsa(swe.AYAN_KRISHNAMURTI)  # ✅ Set KP Ayanamsa

ZODIAC_SIGNS = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_julian_day(dt: datetime) -> float:
    utc_dt = dt.astimezone(pytz.utc)
    return swe.julday(
        utc_dt.year, utc_dt.month, utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600
    )

def normalize_angle(degree):
    return degree % 360

def get_rasi(degree):
    return ZODIAC_SIGNS[int(degree // 30)]

def get_nakshatra_info(moon_longitude):
    nak_index = int(moon_longitude // (360 / 27))
    pada = int((moon_longitude % (360 / 27)) // (3.3333)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": f"Pada {pada}"
    }

def get_lagna(jd, latitude, longitude):
    asc = swe.houses_ex(jd, latitude, longitude, b'A')[0][0]
    return {
        "lagna_degree": round(asc, 4),
        "lagna_rasi": get_rasi(asc)
    }

def get_planet_positions(jd):
    planets = [
        swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
        swe.JUPITER, swe.SATURN, swe.TRUE_NODE  # Rahu
    ]
    planet_names = [
        "Sun", "Moon", "Mercury", "Venus", "Mars",
        "Jupiter", "Saturn", "Rahu"
    ]

    positions = {}
    for idx, planet in enumerate(planets):
        lon, _ = swe.calc_ut(jd, planet)[0:2]
        lon = normalize_angle(lon)
        positions[planet_names[idx]] = {
            "degree": round(lon, 4),
            "rasi": get_rasi(lon)
        }
    return positions

def generate_kundli_chart(data):
    """
    data: {
        "datetime": "YYYY-MM-DDTHH:MM:SS",
        "latitude": float,
        "longitude": float,
        "timezone": float
    }
    """
    dt = datetime.fromisoformat(data["datetime"])
    jd = get_julian_day(dt)

    latitude = data["latitude"]
    longitude = data["longitude"]

    # Lagna
    lagna_data = get_lagna(jd, latitude, longitude)

    # Moon
    moon_long = swe.calc_ut(jd, swe.MOON)[0]
    moon_long = normalize_angle(moon_long)
    nak_info = get_nakshatra_info(moon_long)

    # Planetary positions
    planets = get_planet_positions(jd)

    return {
        "datetime": dt.isoformat(),
        "lagna": lagna_data["lagna_rasi"],
        "lagna_degree": lagna_data["lagna_degree"],
        "nakshatra": nak_info["nakshatra"],
        "pada": nak_info["pada"],
        "planet_positions": planets
    }
