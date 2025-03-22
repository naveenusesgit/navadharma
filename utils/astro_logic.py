import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
import math

swe.set_ephe_path("/usr/share/ephe")  # Adjust if using local ephemeris files

nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="navadharma-astro")
    location = geolocator.geocode(place_name)
    return (location.latitude, location.longitude) if location else (None, None)

def get_timezone_offset(lat, lon, dt_obj):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(timezone_str)
    offset_sec = tz.utcoffset(dt_obj).total_seconds()
    return offset_sec / 3600

def get_planet_positions(jd, lat, lon):
    planets = {}
    for p in range(swe.SUN, swe.PLUTO + 1):
        pos, _ = swe.calc_ut(jd, p)
        name = swe.get_planet_name(p)
        planets[name] = pos[0]
    return planets

def get_nakshatra(degree):
    index = int(degree / (360 / 27))
    return nakshatras[index % 27]

def get_dasha_periods(moon_deg):
    nak_idx = int(moon_deg // (360 / 27))
    dasha_lords = [
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
        "Jupiter", "Saturn", "Mercury"
    ]
    order = dasha_lords[nak_idx % 9:] + dasha_lords[:nak_idx % 9]
    return {
        "mahadasha": order[0],
        "antardasha": order[1],
        "period": f"{order[0]} → {order[1]}"
    }

def detect_yogas(planets):
    yogas = []

    if "Moon" in planets and "Jupiter" in planets:
        moon_sign = int(planets["Moon"] / 30)
        jup_sign = int(planets["Jupiter"] / 30)
        if abs(moon_sign - jup_sign) in [4, 10]:  # Kendra from Moon
            yogas.append("Gajakesari Yoga")

    if "Sun" in planets and "Mercury" in planets:
        if abs(planets["Sun"] - planets["Mercury"]) < 15:
            yogas.append("Budha-Aditya Yoga")

    if "Moon" in planets:
        moon_sign = int(planets["Moon"] / 30)
        alone = all(int(pos / 30) != moon_sign for k, pos in planets.items() if k != "Moon")
        if alone:
            yogas.append("Kemadruma Yoga")

    return yogas

def suggest_remedies(yogas, language="en"):
    remedies = {
        "Gajakesari Yoga": {
            "en": "You have Gajakesari Yoga. It brings fame and wisdom. Worship Lord Vishnu.",
            "hi": "आपके कुंडली में गजकेसरी योग है। यह यश और ज्ञान देता है। भगवान विष्णु की पूजा करें।"
        },
        "Budha-Aditya Yoga": {
            "en": "Budha-Aditya Yoga grants intelligence. Strengthen Sun and Mercury.",
            "ta": "புத அதித்ய யோகம் உங்களுக்கு புத்திசாலித்தனத்தை தரும். சூரியன் மற்றும் புதனை வலுப்படுத்துங்கள்."
        },
        "Kemadruma Yoga": {
            "en": "Kemadruma Yoga may cause loneliness. Chant Moon mantras.",
            "te": "కేమద్రుమ యోగం ఒంటరితనాన్ని కలిగించవచ్చు. చంద్రుని మంత్రాలను జపించండి."
        }
    }

    response = []
    for y in yogas:
        if y in remedies:
            lang_text = remedies[y].get(language, remedies[y]["en"])
            response.append(f"{y}: {lang_text}")
    return response

def analyze_chart(date_str, time_str, place, language="en"):
    dt_obj = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    lat, lon = get_coordinates(place)
    if lat is None or lon is None:
        return {"error": "Invalid location"}

    offset = get_timezone_offset(lat, lon, dt_obj)
    jd = swe.julday(dt_obj.year, dt_obj.month, dt_obj.day, dt_obj.hour + dt_obj.minute / 60 - offset)
    planets = get_planet_positions(jd, lat, lon)
    moon_deg = planets.get("Moon", 0.0)
    
    nakshatra = get_nakshatra(moon_deg)
    dasha_info = get_dasha_periods(moon_deg)
    yogas = detect_yogas(planets)
    remedies = suggest_remedies(yogas, language=language)

    return {
        "nakshatra": nakshatra,
        "currentDasha": dasha_info,
        "yogas": yogas,
        "remedies": remedies,
        "planets": planets,
        "lat": lat,
        "lon": lon
    }

