import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
import math

# Set KP (Krishnamurti) Ayanamsa
swe.set_ephe_path('.')  # or set to the path containing ephemeris files if needed
swe.set_ayanamsa(3)     # 3 = KP Ayanamsa

# Nakshatras mapping
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_timezone(lat, lon, date_time):
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=lat, lng=lon)
    tz = pytz.timezone(tz_str)
    return tz

def to_julian_day(dt_utc):
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                      dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600)

def get_ascendant(jd, lat, lon):
    """Calculate Lagna (Ascendant) using Swiss Ephemeris house cusp."""
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'A', flag=swe.FLG_SIDEREAL)
    asc_deg = ascmc[0]
    sign = int(asc_deg // 30) + 1
    return {"ascendant_degree": asc_deg, "ascendant_sign": sign}

def get_rasi_and_nakshatra(jd, lat, lon):
    """Calculate Moon's Rasi and Nakshatra"""
    moon_pos, _ = swe.calc_ut(jd, swe.MOON, flag=swe.FLG_SIDEREAL)
    moon_long = moon_pos[0]
    rasi = int(moon_long // 30) + 1

    nakshatra_index = int(moon_long / (360 / 27))
    pada = int(((moon_long % (360 / 27)) / (360 / 108)) + 1)

    nakshatra_name = NAKSHATRAS[nakshatra_index]
    return {
        "moon_longitude": moon_long,
        "rasi": rasi,
        "nakshatra": nakshatra_name,
        "pada": pada
    }

def generate_kundli_chart(name, birth_date, birth_time, place):
    # Combine date and time
    birth_dt_str = f"{birth_date} {birth_time}"
    birth_dt = datetime.strptime(birth_dt_str, "%Y-%m-%d %H:%M")

    # Resolve coordinates
    geolocator = Nominatim(user_agent="kundli_generator")
    location = geolocator.geocode(place)
    if not location:
        raise ValueError(f"Could not find coordinates for {place}")
    lat, lon = location.latitude, location.longitude

    # Get timezone and convert to UTC
    tz = get_timezone(lat, lon, birth_dt)
    birth_dt_local = tz.localize(birth_dt)
    birth_dt_utc = birth_dt_local.astimezone(pytz.utc)

    # Julian Day
    jd = to_julian_day(birth_dt_utc)

    # Calculate core chart data
    asc = get_ascendant(jd, lat, lon)
    moon_data = get_rasi_and_nakshatra(jd, lat, lon)

    return {
        "name": name,
        "birth_details": {
            "date": birth_date,
            "time": birth_time,
            "place": place,
            "latitude": lat,
            "longitude": lon,
            "timezone": str(tz)
        },
        "lagna": asc,
        "moon": moon_data
    }
