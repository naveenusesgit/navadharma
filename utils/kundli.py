import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz

# Constants
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.MEAN_NODE  # will adjust 180 deg later
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_nakshatra(degree):
    segment = 13 + 1/3  # 13°20' = 13.333...
    nak_num = int(degree // segment)
    pada = int((degree % segment) // (segment / 4)) + 1
    nakshatra = NAKSHATRAS[nak_num % 27]
    return nakshatra, pada

def get_rasi_chart(positions):
    rasi = {i: [] for i in range(1, 13)}  # Houses 1-12
    for planet, lon in positions.items():
        sign = int(lon // 30) + 1
        rasi[sign].append(planet)
    return rasi

def get_d9_chart(positions):
    d9 = {i: [] for i in range(1, 13)}
    for planet, lon in positions.items():
        navamsa_pos = (lon % 30) * 12
        navamsa_sign = int(navamsa_pos // 30) + 1
        sign = int(lon // 30) + 1
        if sign in [1, 4, 7, 10]:
            final_sign = ((sign - 1) * 3 + navamsa_sign - 1) % 12 + 1
        elif sign in [2, 5, 8, 11]:
            final_sign = ((sign - 2) * 3 + navamsa_sign + 3 - 1) % 12 + 1
        else:
            final_sign = ((sign - 3) * 3 + navamsa_sign + 6 - 1) % 12 + 1
        d9[final_sign].append(planet)
    return d9

def get_lagna(jd_ut, lat, lon):
    # Calculate the ascendant (Lagna)
    flags = swe.FLG_SIDEREAL
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'A', flags)
    lagna_deg = ascmc[0]
    return lagna_deg, int(lagna_deg // 30) + 1

def get_kundli_data(name: str, date: str, time: str, place: str):
    try:
        # Parse input datetime
        dt = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Geocode place
        geolocator = Nominatim(user_agent="kundli-generator")
        location = geolocator.geocode(place)
        if not location:
            return {"error": "Place not found"}
        lat, lon = location.latitude, location.longitude

        # Get timezone info
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=lon, lat=lat)
        local_tz = pytz.timezone(timezone_str)
        local_dt = local_tz.localize(dt)
        utc_dt = local_dt.astimezone(pytz.utc)

        # Swiss Ephemeris setup
        swe.set_ephe_path(".")
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                           utc_dt.hour + utc_dt.minute / 60.0)

        # Calculate planetary longitudes
        planet_positions = {}
        for planet, pid in PLANETS.items():
            lon_deg = swe.calc_ut(jd_ut, pid)[0]
            if planet == "Ketu":
                lon_deg = (lon_deg + 180) % 360
            planet_positions[planet] = round(lon_deg, 2)

        # Lagna
        lagna_deg, lagna_sign = get_lagna(jd_ut, lat, lon)

        # Moon Nakshatra
        moon_deg = planet_positions["Moon"]
        nakshatra, pada = get_nakshatra(moon_deg)

        # Charts
        d1 = get_rasi_chart(planet_positions)
        d9 = get_d9_chart(planet_positions)

        return {
            "name": name,
            "birth_datetime_utc": utc_dt.isoformat(),
            "birth_place": place,
            "coordinates": {"lat": lat, "lon": lon},
            "lagna": {
                "degree": round(lagna_deg, 2),
                "rasi": lagna_sign
            },
            "moon_nakshatra": {
                "nakshatra": nakshatra,
                "pada": pada
            },
            "planet_positions": planet_positions,
            "d1_chart": d1,
            "d9_chart": d9
        }

    except Exception as e:
        return {"error": str(e)}
