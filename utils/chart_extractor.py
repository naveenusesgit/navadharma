# utils/chart_extractor.py

import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from utils.dasha_calculator import get_current_dasha_periods

swe.set_ephe_path('/usr/share/ephe')  # Or wherever your ephemeris files are installed

def get_julian_day(date_str, time_str):
    date_parts = [int(x) for x in date_str.split("-")]
    time_parts = [int(x) for x in time_str.split(":")]
    dt = datetime.datetime(*date_parts, *time_parts)
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

def get_timezone_and_coordinates(place_name):
    geolocator = Nominatim(user_agent="chart_extractor")
    location = geolocator.geocode(place_name)
    if not location:
        raise ValueError("Could not find location: " + place_name)
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    return location.latitude, location.longitude, timezone_str

def get_moon_sign_and_nakshatra(jd):
    flags = swe.FLG_SWIEPH
    moon_pos, _ = swe.calc_ut(jd, swe.MOON, flags)
    sign = int(moon_pos[0] // 30)
    sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    moon_sign = sign_names[sign]

    nakshatra = int(moon_pos[0] // (13.3333))
    pada = int(((moon_pos[0] % 13.3333) / 3.3333)) + 1
    nakshatra_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
        "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
        "Vishakha", "Anuradha", "Jyeshta", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
        "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    return moon_sign, nakshatra_names[nakshatra], pada

def get_ascendant(jd, latitude, longitude):
    # House calculation
    cusps, ascmc = swe.houses(jd, latitude, longitude.decode() if isinstance(longitude, bytes) else longitude, b'P')
    asc_deg = ascmc[0]
    asc_sign = int(asc_deg // 30)
    sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return sign_names[asc_sign]

def extract_chart_details(name, date_of_birth, time_of_birth, place_of_birth):
    try:
        latitude, longitude, tz_str = get_timezone_and_coordinates(place_of_birth)

        jd = get_julian_day(date_of_birth, time_of_birth)
        moon_sign, nakshatra, pada = get_moon_sign_and_nakshatra(jd)
        lagna = get_ascendant(jd, latitude, longitude)

        dasha_info = get_current_dasha_periods(date_of_birth, time_of_birth, latitude, longitude)

        return {
            "name": name,
            "moon_sign": moon_sign,
            "nakshatra": nakshatra,
            "pada": str(pada),
            "lagna": lagna,
            "dasha": dasha_info
        }

    except Exception as e:
        return {
            "error": str(e)
        }
