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
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti",
    "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

RAHU_KAAL_INDEX = {
    "Sunday": 8, "Monday": 2, "Tuesday": 7, "Wednesday": 5,
    "Thursday": 6, "Friday": 4, "Saturday": 3
}

# --- Main Panchanga Logic ---
def get_panchanga(date_str, lat, lon, tz_offset):
    date = datetime.fromisoformat(date_str)

    # Timezone
    tz = timezone(get_timezone_name(lat, lon))
    local_dt = tz.localize(date)
    utc_dt = local_dt.astimezone(utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60)

    # Sunrise & Sunset
    sunrise_jd, _ = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=1)
    sunset_jd, _ = swe.rise_trans(jd, swe.SUN, lon, lat, rsmi=2)

    sunrise_dt = jd_to_datetime(sunrise_jd, tz)
    sunset_dt = jd_to_datetime(sunset_jd, tz)

    # Planetary Positions
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
    karana = KARANA_NAMES[karana_index + 7] if tithi_index in [14, 29] else KARANA_NAMES[karana_index % 7]

    # Rahu Kaal
    rahu_start, rahu_end = get_rahu_kaal(sunrise_dt, sunset_dt, WEEKDAYS[date.weekday()])

    # Abhijit Muhurat
    abhijit_start, abhijit_end = get_abhijit_muhurat(sunrise_dt, sunset_dt)

    # Choghadiya
    choghadiya = get_choghadiya(sunrise_dt, sunset_dt)

    # Festivals
    festivals = get_festivals(tithi, nakshatra, WEEKDAYS[date.weekday()], date)

    return {
        "date": date_str,
        "weekday": WEEKDAYS[date.weekday()],
        "sunrise": sunrise_dt.strftime("%I:%M %p"),
        "sunset": sunset_dt.strftime("%I:%M %p"),
        "tithi": tithi,
        "nakshatra": nakshatra,
        "yoga": yoga,
        "karana": karana,
        "festivals": festivals,
        "rahu_kaal": {
            "start": rahu_start.strftime("%I:%M %p"),
            "end": rahu_end.strftime("%I:%M %p")
        },
        "abhijit_muhurat": {
            "start": abhijit_start.strftime("%I:%M %p") if abhijit_start else "N/A",
            "end": abhijit_end.strftime("%I:%M %p") if abhijit_end else "N/A"
        },
        "choghadiya": choghadiya
    }

# --- Helpers ---
def jd_to_datetime(jd_val, tz):
    y, m, d, h = swe.revjul(jd_val)
    utc_dt = datetime(y, m, d) + timedelta(days=h)
    return utc_dt.replace(tzinfo=utc).astimezone(tz)

def get_timezone_name(lat, lon):
    tf = TimezoneFinder()
    return tf.timezone_at(lat=lat, lng=lon) or "UTC"

def get_rahu_kaal(sunrise, sunset, weekday):
    index = RAHU_KAAL_INDEX[weekday]
    total_seconds = (sunset - sunrise).total_seconds()
    slot = total_seconds / 8
    start = sunrise + timedelta(seconds=(index - 1) * slot)
    end = start + timedelta(seconds=slot)
    return start, end

def get_abhijit_muhurat(sunrise, sunset):
    """Approx. 24 mins before & after solar noon."""
    duration = (sunset - sunrise)
    solar_noon = sunrise + (duration / 2)
    return solar_noon - timedelta(minutes=24), solar_noon + timedelta(minutes=24)

def get_choghadiya(sunrise, sunset):
    choghadiya = {"day": [], "night": []}

    day_duration = (sunset - sunrise).total_seconds() / 8
    for i in range(8):
        start = sunrise + timedelta(seconds=i * day_duration)
        end = start + timedelta(seconds=day_duration)
        choghadiya["day"].append(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}")

    night_start = sunset
    night_end = sunrise + timedelta(days=1)
    night_duration = (night_end - night_start).total_seconds() / 8
    for i in range(8):
        start = night_start + timedelta(seconds=i * night_duration)
        end = start + timedelta(seconds=night_duration)
        choghadiya["night"].append(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}")

    return choghadiya

def get_festivals(tithi, nakshatra, weekday, date):
    mmdd = date.strftime("%m-%d")
    festivals = []

    fixed = {
        "01-14": "Makar Sankranti",
        "08-15": "Independence Day",
        "10-02": "Gandhi Jayanti"
    }
    if mmdd in fixed:
        festivals.append(fixed[mmdd])

    if tithi == "Krishna Ashtami" and nakshatra == "Rohini":
        festivals.append("Krishna Janmashtami")
    if tithi == "Shukla Chaturdashi" and nakshatra == "Rohini":
        festivals.append("Narasimha Jayanti")

    return festivals
