import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz


def get_julian_day(date_str, time_str, place):
    geolocator = Nominatim(user_agent="kundli_app")
    location = geolocator.geocode(place)
    if not location:
        raise ValueError("Invalid place name")
    
    timezone_str = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude)
    if not timezone_str:
        raise ValueError("Could not determine timezone")

    tz = pytz.timezone(timezone_str)
    local_dt = tz.localize(datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))
    utc_dt = local_dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)

    return jd, location.latitude, location.longitude


def get_planet_positions(jd, flags=swe.FLG_SWIEPH | swe.FLG_SPEED):
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": swe.TRUE_NODE,  # We'll reverse Ketu below
    }
    positions = {}

    for name, planet in planets.items():
        lon, lat, dist, speed = swe.calc_ut(jd, planet, flags)
        if name == "Ketu":
            lon = (lon + 180) % 360  # Ketu is always opposite Rahu
        positions[name] = round(lon, 2)
    
    return positions


def get_d1_chart(jd):
    return get_planet_positions(jd)


def get_d9_chart(jd):
    # Navamsa is calculated from D1 planetary longitudes
    d1_chart = get_planet_positions(jd)
    d9_chart = {}

    for planet, lon in d1_chart.items():
        sign = int(lon // 30)
        navamsa = int(((lon % 30) * 9) // 30)
        new_sign = (sign * 9 + navamsa) % 12
        d9_chart[planet] = new_sign * 30 + ((lon % 30) * 9) % 30

    return {k: round(v, 2) for k, v in d9_chart.items()}


def get_lagna(jd, lat, lon):
    cusps, ascmc = swe.houses(jd, lat, lon)
    return round(ascmc[0], 2)  # Ascendant


def get_nakshatra_info(jd):
    moon_long, _, _, _ = swe.calc_ut(jd, swe.MOON)
    nakshatra = int(moon_long / (360 / 27)) + 1
    pada = int(((moon_long % (360 / 27)) / (360 / 108))) + 1
    return {
        "nakshatra_number": nakshatra,
        "pada": pada
    }


def get_dasha_periods(jd):
    moon_long, _, _, _ = swe.calc_ut(jd, swe.MOON)
    nakshatra_num = int(moon_long / (360 / 27)) % 27
    dasha_lords = [
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
    ]
    dasha_years = {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17
    }

    start_index = nakshatra_num % 9
    start_lord = dasha_lords[start_index]
    start_year = int(datetime.datetime.utcnow().year)

    dasha_sequence = []
    for i in range(9):
        lord = dasha_lords[(start_index + i) % 9]
        dasha_sequence.append({
            "lord": lord,
            "start_year": start_year,
            "end_year": start_year + dasha_years[lord]
        })
        start_year += dasha_years[lord]

    return dasha_sequence


def get_kundli_chart(date, time, place):
    jd, lat, lon = get_julian_day(date, time, place)
    d1 = get_d1_chart(jd)
    d9 = get_d9_chart(jd)
    lagna = get_lagna(jd, lat, lon)
    return {
        "D1": d1,
        "D9": d9,
        "Lagna": lagna
    }


def generate_kundli_report(date, time, place):
    jd, lat, lon = get_julian_day(date, time, place)
    return {
        "chart": get_kundli_chart(date, time, place),
        "nakshatra": get_nakshatra_info(jd),
        "dasha": get_dasha_periods(jd)
    }
