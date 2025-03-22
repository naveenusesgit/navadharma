import swisseph as swe
from datetime import datetime
import pytz

# Nakshatra Names (27 segments of 13°20')
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Graha list for convenience
planets = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN
}

# Set Ephemeris
swe.set_ephe_path('.')


def get_julian_day(date_str, time_str, timezone_str='Asia/Kolkata'):
    """Convert birth date and time into Julian Day"""
    tz = pytz.timezone(timezone_str)
    dt = tz.localize(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)


def get_nakshatra(longitude):
    """Get Nakshatra from ecliptic longitude"""
    segment = int((longitude % 360) / (360 / 27))
    return nakshatras[segment]


def get_planet_positions(jd, lat, lon):
    """Calculate positions and nakshatras for all planets"""
    positions = {}
    nakshatra_info = {}

    for name, planet_id in planets.items():
        lonlat, _ = swe.calc_ut(jd, planet_id)
        positions[name] = lonlat[0]
        nakshatra_info[name] = get_nakshatra(lonlat[0])

    return positions, nakshatra_info

