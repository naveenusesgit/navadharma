import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# Set Swiss Ephemeris path
swe.set_ephe_path("/usr/share/ephe")  # Update this path if needed

# Helper: get Julian Day
def get_julian_day(date, time, place):
    dt = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    geolocator = Nominatim(user_agent="kundli-generator")
    location = geolocator.geocode(place)
    if not location:
        raise ValueError("Invalid location")
    
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    tz_offset = datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset().total_seconds() / 3600

    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60 - tz_offset)
    return jd, location.latitude, location.longitude

# Nakshatra and Lord
def get_nakshatra_info(moon_long):
    nakshatra_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
        "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    lords = [
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
    ]
    index = int(moon_long / (13 + 1/3))
    nak = nakshatra_names[index % 27]
    lord = lords[index % 9]
    return {"nakshatra": nak, "lord": lord}

# Lagna calculation
def get_lagna(jd, lat, lon):
    asc = swe.houses(jd, lat, lon)[0][0]
    return round(asc, 2)

# Generate D1 Chart
def get_d1_chart(jd):
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    planet_positions = {}
    for i, planet in enumerate(planets, start=0):
        lon, _ = swe.calc_ut(jd, i)
        planet_positions[planet] = round(lon[0], 2)
    return planet_positions

# Generate D9 (Navamsa) Chart
def get_d9_chart(jd):
    d9_chart = {}
    for planet_id in range(7):  # Sun to Saturn
        lon, _ = swe.calc_ut(jd, planet_id)
        sign = int(lon[0] / 30)
        navamsa = int((lon[0] % 30) / 3.3333)
        d9_chart[swe.get_planet_name(planet_id)] = f"Sign: {sign+1}, Navamsa: {navamsa+1}"
    return d9_chart

# Expanded Vimshottari Dasha
def get_dasha_periods(date, time, place):
    jd, lat, lon = get_julian_day(date, time, place)
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_long = moon_pos[0]

    nakshatra_size = 13 + (20 / 60)
    nakshatra_index = int(moon_long // nakshatra_size)
    degrees_into_nakshatra = moon_long % nakshatra_size

    dasha_lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    dasha_years = {
        "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10,
        "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
    }

    current_lord = dasha_lords[nakshatra_index % 9]
    total_dasha_years = dasha_years[current_lord]
    proportion_passed = degrees_into_nakshatra / nakshatra_size
    days_passed = total_dasha_years * proportion_passed * 365.25

    start_date = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    dasha_start = start_date - datetime.timedelta(days=days_passed)
    dasha_end = dasha_start + datetime.timedelta(days=total_dasha_years * 365.25)

    antardasha_list = []
    for lord in dasha_lords:
        sub_years = total_dasha_years * (dasha_years[lord] / 120)
        sub_days = sub_years * 365.25
        antardasha_list.append({
            "lord": lord,
            "duration_days": round(sub_days, 1)
        })

    return {
        "current_mahadasha": current_lord,
        "start_date": dasha_start.strftime("%Y-%m-%d"),
        "end_date": dasha_end.strftime("%Y-%m-%d"),
        "antardasha_sequence": antardasha_list
    }

# Remedy suggestion (stub)
def suggest_remedies(nakshatra_lord):
    remedies = {
        "Sun": "Worship Surya, chant Aditya Hridayam",
        "Moon": "Chant Chandra mantra, wear white",
        "Mars": "Hanuman Chalisa, wear red coral",
        "Mercury": "Budh mantra, green clothes",
        "Jupiter": "Guru mantra, yellow clothing",
        "Venus": "Shukra mantra, offer sweets",
        "Saturn": "Shani mantra, offer mustard oil",
        "Rahu": "Durga mantra, coconut donation",
        "Ketu": "Ganesha worship, feed dogs"
    }
    return remedies.get(nakshatra_lord, "Meditate and follow your dharma")

# Full Kundli report
def generate_kundli_report(name, date, time, place):
    jd, lat, lon = get_julian_day(date, time, place)
    d1 = get_d1_chart(jd)
    d9 = get_d9_chart(jd)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nakshatra_info = get_nakshatra_info(moon_long[0])
    lagna = get_lagna(jd, lat, lon)
    dasha = get_dasha_periods(date, time, place)
    remedies = suggest_remedies(nakshatra_info["lord"])

    return {
        "name": name,
        "lagna": lagna,
        "nakshatra": nakshatra_info,
        "d1_chart": d1,
        "d9_chart": d9,
        "dasha": dasha,
        "remedies": remedies
    }
