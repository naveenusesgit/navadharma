# utils/kundli.py

import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
import math

# ✅ Set Swiss Ephemeris to use KP Ayanamsa
swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

# === Constants ===
PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
PLANET_IDS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Ketu': swe.MEAN_NODE  # Ketu will be 180° from Rahu
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_timezone_offset(lat, lon, dt):
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_str)
    return tz.utcoffset(dt).total_seconds() / 3600.0, tz_str

def calculate_julian_day(dt_utc):
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute / 60.0)

def get_lagna(jd, lat, lon):
    ascendant = swe.houses_ex(jd, lat, lon, b'A')[0][0]
    sign_index = int(ascendant / 30)
    return SIGNS[sign_index]

def get_nakshatra(moon_longitude):
    nakshatra_index = int(moon_longitude / (360 / 27))
    pada = int((moon_longitude % (360 / 27)) / (360 / 27 / 4)) + 1
    return NAKSHATRAS[nakshatra_index], pada

def get_planet_positions(jd, lat, lon):
    positions = {}
    for planet in PLANETS:
        if planet == 'Ketu':
            rahu_long, _ = swe.calc_ut(jd, PLANET_IDS['Rahu'])
            ketu_long = (rahu_long[0] + 180.0) % 360.0
            planet_long = ketu_long
        else:
            planet_long, _ = swe.calc_ut(jd, PLANET_IDS[planet])

        sign = SIGNS[int(planet_long[0] / 30)]
        nakshatra, pada = get_nakshatra(planet_long[0])
        positions[planet] = {
            'degree': round(planet_long[0], 4),
            'sign': sign,
            'nakshatra': nakshatra,
            'pada': pada
        }
    return positions

def generate_kundli_chart(name, date, time, place):
    geolocator = Nominatim(user_agent="kundli-api")
    location = geolocator.geocode(place)
    if not location:
        raise Exception("Location not found")

    lat, lon = location.latitude, location.longitude
    dt_naive = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    offset_hours, tz_name = get_timezone_offset(lat, lon, dt_naive)
    dt_utc = dt_naive - datetime.timedelta(hours=offset_hours)

    jd = calculate_julian_day(dt_utc)

    lagna = get_lagna(jd, lat, lon)
    planet_positions = get_planet_positions(jd, lat, lon)

    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    moon_nakshatra, moon_pada = get_nakshatra(moon_long[0])
    rasi = SIGNS[int(moon_long[0] / 30)]

    return {
        "name": name,
        "birth_datetime": dt_naive.isoformat(),
        "timezone": tz_name,
        "lagna": lagna,
        "rasi": rasi,
        "nakshatra": moon_nakshatra,
        "pada": moon_pada,
        "planet_positions": planet_positions
    }
