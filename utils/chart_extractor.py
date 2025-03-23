import swisseph as swe
import pytz
from datetime import datetime
from utils.geolocation import get_lat_lon_timezone
from utils.dasha_calculator import get_current_dasha

def extract_chart(birth_date, birth_time, birth_place):
    # Get coordinates and timezone
    lat, lon, tz_str = get_lat_lon_timezone(birth_place)
    tz = pytz.timezone(tz_str)

    # Combine date and time to local datetime
    birth_dt_str = f"{birth_date} {birth_time}"
    local_dt = tz.localize(datetime.strptime(birth_dt_str, "%Y-%m-%d %H:%M"))

    # Convert to UTC and Julian day
    utc_dt = local_dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60)

    # Set ephemeris path
    swe.set_ephe_path("/usr/share/ephe")  # or your local ephemeris path

    # Moon position for Rasi & Nakshatra
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_long = moon_pos[0]

    # Determine Rasi (Moon Sign)
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    rasi = signs[int(moon_long // 30)]

    # Determine Nakshatra & Pada
    nakshatra_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    nak_index = int((moon_long % 360) / (13 + 1/3))
    nak_pada = int(((moon_long % (13 + 1/3)) / ((13 + 1/3)/4)) + 1)
    nakshatra = nakshatra_names[nak_index]

    # Ascendant (Lagna)
    ascmc = swe.houses_ex(jd, lat, lon, b'A')[0]
    ascendant_long = ascmc[0]
    lagna = signs[int(ascendant_long // 30)]

    # Dasha info
    dasha_info = get_current_dasha(jd, moon_long)

    return {
        "moon_sign": rasi,
        "nakshatra": nakshatra,
        "pada": nak_pada,
        "ascendant": lagna,
        "current_dasha": dasha_info
    }
