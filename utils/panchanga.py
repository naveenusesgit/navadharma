# utils/panchanga.py

import swisseph as swe
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
from pytz import timezone, utc

swe.set_ephe_path('.')  # Set ephemeris path to current directory

# --- Constants ---
TITHI_NAMES = [
    "Shukla Pratipada", "Shukla Dvitiya", "Shukla Tritiya", "Shukla Chaturthi",
    "Shukla Panchami", "Shukla Shashti", "Shukla Saptami", "Shukla Ashtami",
    "Shukla Navami", "Shukla Dashami", "Shukla Ekadashi", "Shukla Dwadashi",
    "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dvitiya", "Krishna Tritiya", "Krishna Chaturthi",
    "Krishna Panchami", "Krishna Shashti", "Krishna Saptami", "Krishna Ashtami",
    "Krishna Navami", "Krishna Dashami", "Krishna Ekadashi", "Krishna Dwadashi",
    "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
    "Shoola", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
    "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti",  # repeating 8
    "Shakuni", "Chatushpada", "Naga", "Kimstughna"  # fixed 4
]

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# --- Core Panchanga Logic ---
def get_panchanga(date_str, lat, lon, tz_offset):
    date = datetime.fromisoformat(date_str)

    # Convert to UTC
    tz = timezone(get_timezone_name(lat, lon))
    local_dt = tz.localize(date)
    utc_dt = local_dt.astimezone(utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60)

    # Sunrise and Sunset (approx)
    sunrise_utc, _ = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=1)  # 1 = sunrise
    sunset_utc, _ = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=2)   # 2 = sunset

    # Moon & Sun Longitudes
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    sun_long, _ = swe.calc_ut(jd, swe.SUN)

    # Tithi
    diff = (moon_long[0] - sun_long[0]) % 360
    tithi_index = int(diff / 12)
    tithi = TITHI_NAMES[tithi_index]

    # Nakshatra
    nakshatra_index = int(moon_long[0] / (360 / 27))
    nakshatra = NAKSHATRA_NAMES[nakshatra_index]

    # Yoga
    yoga_index = int(((sun_long[0] + moon_long[0]) % 360) / (360 / 27))
    yoga = YOGA_NAMES[yoga_index]

    # Karana
    karana_index = int((diff % 60) / 6)
    if tithi_index == 14 or tithi_index == 29:
        karana = KARANA_NAMES[karana_index + 7]
    else:
        karana = KARANA_NAMES[karana_index % 7]

    # Final Panchanga
    return {
        "date": date_str,
        "weekday": WEEKDAYS[date.weekday()],
        "sunrise": jd_to_time(sunrise_utc, tz),
        "sunset": jd_to_time(sunset_utc, tz),
        "tithi": tithi,
        "nakshatra": nakshatra,
        "yoga": yoga,
        "karana": karana,
    }

# --- Helper Functions ---
def jd_to_time(jd_val, tz):
    if not jd_val:
        return "N/A"
    y, m, d, h = swe.revjul(jd_val)
    utc_dt = datetime(y, m, d) + timedelta(days=h)
    local_dt = utc_dt.astimezone(tz)
    return local_dt.strftime("%I:%M %p")

def get_timezone_name(lat, lon):
    tf = TimezoneFinder()
    return tf.timezone_at(lat=lat, lng=lon) or "UTC"
