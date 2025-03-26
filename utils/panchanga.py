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

YOGA_NAMES = [ ... ]  # (Same as before)
KARANA_NAMES = [ ... ]  # (Same as before)
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

RAHU_KAAL_INDEX = {
    "Sunday": 8, "Monday": 2, "Tuesday": 7, "Wednesday": 5,
    "Thursday": 6, "Friday": 4, "Saturday": 3
}

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

    # Panchanga Calculations
    diff = (moon_long[0] - sun_long[0]) % 360
    tithi_index = int(diff / 12)
    tithi = TITHI_NAMES[tithi_index]
    nakshatra_index = int(moon_long[0] / (360 / 27))
    nakshatra = NAKSHATRA_NAMES[nakshatra_index]
    yoga_index = int(((sun_long[0] + moon_long[0]) % 360) / (360 / 27))
    yoga = YOGA_NAMES[yoga_index]
    karana_index = int((diff % 60) / 6)
    karana = KARANA_NAMES[karana_index + 7] if tithi_index in [14, 29] else KARANA_NAMES[karana_index % 7]

    weekday = WEEKDAYS[date.weekday()]
    rahu_start, rahu_end = get_rahu_kaal(sunrise_dt, sunset_dt, weekday)
    abhijit_start, abhijit_end = get_abhijit_muhurat(sunrise_dt, sunset_dt)
    abhijit_in_rahu = time_ranges_overlap(abhijit_start, abhijit_end, rahu_start, rahu_end)

    # Yogas
    ravi_yoga = is_ravi_yoga(weekday, nakshatra)
    amrit_siddhi = is_amrit_siddhi_yoga(weekday, nakshatra)
    moon_phase = get_moon_phase(sun_long[0], moon_long[0])
    vedic_month = get_vedic_month(sun_long[0])

    # Vrat & Festivals
    festivals = get_festivals(tithi, nakshatra, weekday, date)
    if "Chaturthi" in tithi:
        festivals.append("Chaturthi Vrat")
    if "Ekadashi" in tithi:
        festivals.append("Ekadashi Vrat")
    if "Trayodashi" in tithi and "Krishna" in tithi:
        festivals.append("Pradosham Vrat")
    if "Chaturthi" in tithi and "Krishna" in tithi:
        festivals.append("Sankashti Chaturthi")

    moon_event = None
    if tithi == "Purnima":
        moon_event = "Purnima"
    elif tithi == "Amavasya":
        moon_event = "Amavasya"

    return {
        "date": date_str,
        "weekday": weekday,
        "sunrise": sunrise_dt.strftime("%I:%M %p"),
        "sunset": sunset_dt.strftime("%I:%M %p"),
        "tithi": tithi,
        "nakshatra": nakshatra,
        "yoga": yoga,
        "karana": karana,
        "festivals": festivals,
        "moon_event": moon_event,
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

# --- Monthly Ekadashi/Chaturthi/Purnima Listing ---
def get_monthly_utsav_list(start_date_str, lat, lon, days=30, tz_offset=5.5):
    start_date = datetime.fromisoformat(start_date_str)
    events = []
    for i in range(days):
        day = start_date + timedelta(days=i)
        panchanga = get_panchanga(day.isoformat(), lat, lon, tz_offset)
        if any(f for f in panchanga["festivals"] if "Vrat" in f or "Jayanti" in f or "Ekadashi" in f):
            events.append({
                "date": panchanga["date"],
                "weekday": panchanga["weekday"],
                "festivals": panchanga["festivals"]
            })
    return events

# --- Monthly Full Moon / New Moon Dates ---
def get_purnima_amavasya_list(start_date_str, lat, lon, days=30, tz_offset=5.5):
    start_date = datetime.fromisoformat(start_date_str)
    results = []
    for i in range(days):
        day = start_date + timedelta(days=i)
        p = get_panchanga(day.isoformat(), lat, lon, tz_offset)
        if p.get("moon_event") in ["Purnima", "Amavasya"]:
            results.append({
                "date": p["date"],
                "event": p["moon_event"],
                "weekday": p["weekday"]
            })
    return results

# --- Helpers ---
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
    noon = sunrise + (sunset - sunrise) / 2
    return noon - timedelta(minutes=24), noon + timedelta(minutes=24)

def time_ranges_overlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1

def get_choghadiya(sunrise, sunset):
    choghadiya = {"day": [], "night": []}
    slot = (sunset - sunrise).total_seconds() / 8
    for i in range(8):
        s = sunrise + timedelta(seconds=i * slot)
        e = s + timedelta(seconds=slot)
        choghadiya["day"].append(f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}")
    night_start = sunset
    night_end = sunrise + timedelta(days=1)
    slot = (night_end - night_start).total_seconds() / 8
    for i in range(8):
        s = night_start + timedelta(seconds=i * slot)
        e = s + timedelta(seconds=slot)
        choghadiya["night"].append(f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}")
    return choghadiya

def is_ravi_yoga(weekday, nakshatra):
    return nakshatra in RAVI_YOGA_PAIRS.get(weekday, [])

def is_amrit_siddhi_yoga(weekday, nakshatra):
    return (weekday == "Monday" and nakshatra == "Rohini") or (weekday == "Wednesday" and nakshatra == "Hasta")

def get_moon_phase(sun_long, moon_long):
    angle = (moon_long - sun_long) % 360
    if angle < 90:
        return "Waxing Crescent"
    elif angle < 180:
        return "Waxing Gibbous"
    elif angle < 270:
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
