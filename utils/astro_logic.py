import swisseph as swe
from utils.location_utils import get_timezone_offset
from datetime import datetime
from timezonefinder import TimezoneFinder

def get_julian_day(date_str, time_str):
    """
    Converts a date and time string to Julian Day.
    """
    dt = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

def get_moon_longitude(jd):
    """
    Returns the moon longitude for a given Julian day.
    """
    moon_pos = swe.calc_ut(jd, swe.MOON)[0]
    return moon_pos[0]

def get_nakshatra(moon_longitude):
    """
    Returns nakshatra name and index (0-based).
    Each nakshatra spans 13°20′ = 13.333... degrees.
    """
    nakshatra_index = int(moon_longitude / (360 / 27))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
        "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[nakshatra_index], nakshatra_index

def get_rashi(moon_longitude):
    """
    Returns the moon sign (Rashi) based on 30° spans.
    """
    rashi_index = int(moon_longitude / 30)
    rashis = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return rashis[rashi_index], rashi_index
