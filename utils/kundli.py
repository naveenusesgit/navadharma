import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz

swe.set_ephe_path('.')  # Assumes ephemeris files are in root or shipped

geolocator = Nominatim(user_agent="navadharma-app")
tf = TimezoneFinder()

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.TRUE_NODE,
}


def get_coordinates(place):
    location = geolocator.geocode(place)
    if not location:
        raise ValueError("Place not found.")
    return location.latitude, location.longitude


def get_timezone_offset(lat, lon, date, time):
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        raise ValueError("Could not determine timezone.")
    dt_naive = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    tz = pytz.timezone(tz_name)
    dt_local = tz.localize(dt_naive)
    utc_offset = dt_local.utcoffset().total_seconds() / 3600
    return dt_local, utc_offset


def get_planet_positions(jd, lat, lon):
    swe.set_topo(lon, lat, 0)
    positions = {}
    for name, planet_id in PLANETS.items():
        lon, _lat, _speed = swe.calc_ut(jd, planet_id)
        positions[name] = round(lon % 360, 2)
    return positions


def get_lagna(jd, lat, lon):
    ascendant = swe.houses_ex(jd, lat, lon, b'A')[0][0]
    return round(ascendant, 2)


def get_kundli_data(name, date, time, place):
    lat, lon = get_coordinates(place)
    dt_local, offset = get_timezone_offset(lat, lon, date, time)
    jd = swe.julday(dt_local.year, dt_local.month, dt_local.day, dt_local.hour + dt_local.minute / 60)

    planets = get_planet_positions(jd, lat, lon)
    lagna = get_lagna(jd, lat, lon)

    return {
        "name": name,
        "date": date,
        "time": time,
        "place": place,
        "lagna_degree": lagna,
        "planet_positions": planets,
    }


def get_chart_data(name, date, time, place):
    return get_kundli_data(name, date, time, place)  # Simplified; same logic


def get_nakshatra_info(name, date, time, place):
    lat, lon = get_coordinates(place)
    dt_local, offset = get_timezone_offset(lat, lon, date, time)
    jd = swe.julday(dt_local.year, dt_local.month, dt_local.day, dt_local.hour + dt_local.minute / 60)

    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    moon_deg = moon_long % 360

    nak_num = int(moon_deg / (360 / 27)) + 1
    pada = int((moon_deg % (360 / 27)) / (360 / 108)) + 1

    return {
        "moon_longitude": round(moon_deg, 2),
        "nakshatra_number": nak_num,
        "nakshatra_pada": pada
    }


def get_dasha_report(name, date, time, place):
    # Placeholder: real dasha needs more logic (e.g., Lahiri ayanamsa, moon deg, etc.)
    return {
        "name": name,
        "dasha": [
            {"period": "2023-2039", "planet": "Venus"},
            {"period": "2039-2045", "planet": "Sun"},
            {"period": "2045-2062", "planet": "Moon"},
        ]
    }


def get_matchmaking_report(data):
    # Placeholder logic
    return {
        "boy": data.boy_name,
        "girl": data.girl_name,
        "compatibility_score": 28,
        "verdict": "Good match. Traditional compatibility score is above 25."
    }


def get_panchang_data(date, time, place):
    lat, lon = get_coordinates(place)
    dt_local, offset = get_timezone_offset(lat, lon, date, time)
    jd = swe.julday(dt_local.year, dt_local.month, dt_local.day, dt_local.hour + dt_local.minute / 60)

    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    sun_long, _ = swe.calc_ut(jd, swe.SUN)

    tithi = int(((moon_long - sun_long) % 360) / 12) + 1
    nakshatra = int(moon_long / (360 / 27)) + 1

    return {
        "tithi_number": tithi,
        "nakshatra_number": nakshatra,
        "sun_long": round(sun_long, 2),
        "moon_long": round(moon_long, 2)
    }
