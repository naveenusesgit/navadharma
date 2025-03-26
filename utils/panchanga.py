# utils/panchanga.py

import swisseph as swe
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
from pytz import timezone, utc

swe.set_ephe_path('.')

# --- Constants ---
TITHI_NAMES = [ ... ]  # as before
NAKSHATRA_NAMES = [ ... ]  # as before
YOGA_NAMES = [ ... ]  # as before
KARANA_NAMES = [ ... ]  # as before
WEEKDAYS = [ ... ]  # as before
RAHU_KAAL_INDEX = { ... }  # as before

VEDIC_MONTHS = [
    "Chaitra", "Vaishakha", "Jyeshtha", "Ashadha",
    "Shravana", "Bhadrapada", "Ashwin", "Kartika",
    "Margashirsha", "Pausha", "Magha", "Phalguna"
]

RAVI_YOGA_PAIRS = {
    "Sunday": ["Bharani", "Krittika"],
    "Monday": ["Ashlesha", "Magha"],
    "Tuesday": ["Anuradha", "Jyeshtha"],
    "Wednesday": ["Revati", "Ashwini"],
    "Thursday": ["Pushya", "Punarvasu"],
    "Friday": ["Rohini", "Mrigashirsha"],
    "Saturday": ["Uttara Phalguni", "Hasta"]
}

# --- Main Panchanga Logic ---
def get_panchanga(date_str, lat, lon, tz_offset):
    date = datetime.fromisoformat(date_str)
    tz = timezone(get_timezone_name(lat, lon))
    local_dt = tz.localize(date)
    utc_dt = local_dt.astimezone(utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60)

    # Sunrise & Sunset
    sunrise_jd, _ = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=1)
    sunset_jd, _ = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=2)
    sunrise_dt = jd_to_datetime(sunrise_jd, tz)
    sunset_dt = jd_to_datetime(sunset_jd, tz)

    # Planetary Longitudes
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    sun_long, _ = swe.calc_ut(jd, swe.SUN)

    # Panchanga
    diff = (moon_long[0] - sun_long[0]) % 360
    tithi_index = int(diff / 12)
    tithi = TITHI_NAMES[tithi_index]
    nakshatra_index = int(moon_long[0] / (360 / 27))
    nakshatra = NAKSHATRA_NAMES[nakshatra_index]
    yoga_index = int(((sun_long[0] + moon_long[0]) % 360) / (360 / 27))
    yoga = YOGA_NAMES[yoga_index]
    karana_index = int((diff % 60) / 6)
    karana = KARANA_NAMES[karana_index + 7] if tithi_index in [14, 29] else KARANA_NAMES[karana_index % 7]

    # Rahu Kaal & Abhijit
    weekday = WEEKDAYS[date.weekday()]
    rahu_start, rahu_end = get_rahu_kaal(sunrise_dt, sunset_dt, weekday)
    abhijit_start, abhijit_end = get_abhijit_muhurat(sunrise_dt, sunset_dt)
    abhijit_in_rahu = time_ranges_overlap(abhijit_start, abhijit_end, rahu_start, rahu_end)

    # Yogas
    ravi_yoga = is_ravi_yoga(weekday, nakshatra)
    amrit_siddhi = is_amrit_siddhi_yoga(weekday, nakshatra)

    # Moon Phase & Vedic Month
    moon_phase = get_moon_phase(sun_long[0], moon_long[0])
    vedic_month = get_vedic_month(sun_long[0])

    return {
        "date": date_str,
        "weekday": weekday,
        "sunrise": sunrise_dt.strftime("%I:%M %p"),
        "sunset": sunset_dt.strftime("%I:%M %p"),
        "tithi": tithi,
        "nakshatra": nakshatra,
        "yoga": yoga,
        "karana": karana,
        "festivals": get_festivals(tithi, nakshatra, weekday, date),
        "rahu_kaal": {
            "start": rahu_start.strftime("%I:%M %p"),
            "end": rahu_end.strftime("%I:%M %p")
        },
        "abhijit_muhurat": {
            "start": abhijit_start.strftime("%I:%M %p"),
            "end": abhijit_end.strftime("%I:%M %p"),
            "is_in_rahu_kaal": abhijit_in_rahu
        },
        "yogas": {
            "ravi_yoga": ravi_yoga,
            "amrit_siddhi_yoga": amrit_siddhi
        },
        "moon_phase": moon_phase,
        "vedic_month": vedic_month,
        "choghadiya": get_choghadiya(sunrise_dt, sunset_dt)
    }

# --- Helper Functions ---
def jd_to_datetime(jd_val, tz):
    y, m, d, h = swe.revjul(jd_val)
    utc_dt = datetime(y, m, d) + timedelta(days=h)
    return utc_dt.replace(tzinfo=utc).astimezone(tz)

def get_timezone_name(lat, lon):
    return TimezoneFinder().timezone_at(lat=lat, lng=lon) or "UTC"

def get_rahu_kaal(sunrise, sunset, weekday):
    index = RAHU_KAAL_INDEX[weekday]
    duration = (sunset - sunrise).total_seconds() / 8
    start = sunrise + timedelta(seconds=(index - 1) * duration)
    end = start + timedelta(seconds=duration)
    return start, end

def get_abhijit_muhurat(sunrise, sunset):
    duration = (sunset - sunrise)
    solar_noon = sunrise + (duration / 2)
    return solar_noon - timedelta(minutes=24), solar_noon + timedelta(minutes=24)

def time_ranges_overlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1

def get_choghadiya(sunrise, sunset):
    choghadiya = {"day": [], "night": []}
    # Day
    day_slot = (sunset - sunrise).total_seconds() / 8
    for i in range(8):
        start = sunrise + timedelta(seconds=i * day_slot)
        end = start + timedelta(seconds=day_slot)
        choghadiya["day"].append(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}")
    # Night
    night_start = sunset
    night_end = sunrise + timedelta(days=1)
    night_slot = (night_end - night_start).total_seconds() / 8
    for i in range(8):
        start = night_start + timedelta(seconds=i * night_slot)
        end = start + timedelta(seconds=night_slot)
        choghadiya["night"].append(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}")
    return choghadiya

def is_ravi_yoga(weekday, nakshatra):
    return nakshatra in RAVI_YOGA_PAIRS.get(weekday, [])

def is_amrit_siddhi_yoga(weekday, nakshatra):
    # Simplified rule version
    if weekday == "Monday" and nakshatra == "Rohini":
        return True
    if weekday == "Wednesday" and nakshatra == "Hasta":
        return True
    return False

def get_moon_phase(sun_long, moon_long):
    diff = (moon_long - sun_long) % 360
    if diff < 90:
        return "Waxing Crescent"
    elif diff < 180:
        return "Waxing Gibbous"
    elif diff < 270:
        return "Waning Gibbous"
    else:
        return "Waning Crescent"

def get_vedic_month(sun_long):
    return VEDIC_MONTHS[int(sun_long // 30)]

def get_festivals(tithi, nakshatra, weekday, date):
    mmdd = date.strftime("%m-%d")
    fixed = {
        "01-14": "Makar Sankranti",
        "08-15": "Independence Day",
        "10-02": "Gandhi Jayanti"
    }
    special = []
    if mmdd in fixed:
        special.append(fixed[mmdd])
    if tithi == "Krishna Ashtami" and nakshatra == "Rohini":
        special.append("Krishna Janmashtami")
    if tithi == "Shukla Chaturdashi" and nakshatra == "Rohini":
        special.append("Narasimha Jayanti")
    return special
