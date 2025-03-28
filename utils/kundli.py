from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import PLANETS, SIGNS, HOUSES, MOON
from flatlib import const
import swisseph as swe

# Use KP Ayanamsa (Krishnamurti)
swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

# ===============================
# 🪐 Planetary Positions
# ===============================

def get_planet_positions(datetime_str, latitude, longitude, timezone):
    dt = Datetime(datetime_str, timezone)
    pos = GeoPos(latitude, longitude)
    chart = Chart(dt, pos, hsys=const.HOUSES_PLACIDUS)

    planets = {}
    for body in PLANETS:
        obj = chart.get(body)
        planets[obj.id] = {
            'sign': obj.sign,
            'lon': round(obj.lon, 2),
            'deg': obj.signlon,
            'house': obj.house
        }
    return planets

# ===============================
# 🧭 Ascendant (Lagna)
# ===============================

def get_ascendant_info(datetime_str, latitude, longitude, timezone):
    dt = Datetime(datetime_str, timezone)
    pos = GeoPos(latitude, longitude)
    chart = Chart(dt, pos)
    asc = chart.get(const.ASC)
    return {
        'sign': asc.sign,
        'degree': round(asc.signlon, 2)
    }

# ===============================
# 🌙 Moon Rāśi + Nakṣatra + Pada
# ===============================

def get_moon_info(datetime_str, latitude, longitude, timezone):
    from flatlib.ephem import Ephem
    dt = Datetime(datetime_str, timezone)
    pos = GeoPos(latitude, longitude)
    chart = Chart(dt, pos)

    moon = chart.get(MOON)
    moon_lon = moon.lon

    nakshatra_list = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
        "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
        "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
        "Revati"
    ]

    # Each nakshatra is 13°20' (13.3333 degrees)
    nakshatra_index = int(moon_lon / (360 / 27))
    nakshatra_name = nakshatra_list[nakshatra_index % 27]

    pada = int((moon_lon % (360 / 27)) / (360 / 108)) + 1  # 4 padas per nakshatra

    return {
        'rashi': moon.sign,
        'nakshatra': nakshatra_name,
        'padam': pada
    }

# ===============================
# 🏠 House to Sign Mapping
# ===============================

def get_house_mapping(datetime_str, latitude, longitude, timezone):
    dt = Datetime(datetime_str, timezone)
    pos = GeoPos(latitude, longitude)
    chart = Chart(dt, pos, hsys=const.HOUSES_PLACIDUS)

    houses = {}
    for house_num in range(1, 13):
        house = chart.get(str(house_num))
        houses[f"H{house_num}"] = house.sign
    return houses

# ===============================
# 🧠 Kundli Chart (Houses + Planets)
# ===============================

def get_kundli_chart(datetime_str, latitude, longitude, timezone):
    dt = Datetime(datetime_str, timezone)
    pos = GeoPos(latitude, longitude)
    chart = Chart(dt, pos)

    houses_data = []
    for h_num in range(1, 13):
        house = chart.get(str(h_num))
        sign = house.sign
        planets_in_house = []
        for planet in PLANETS:
            p = chart.get(planet)
            if p.house == str(h_num):
                planets_in_house.append(p.id)
        houses_data.append({
            'house': int(h_num),
            'sign': sign,
            'planets': planets_in_house
        })

    return {
        'ascendant': get_ascendant_info(datetime_str, latitude, longitude, timezone),
        'houses': houses_data
    }

# ===============================
# ♓️ Lagna Info
# ===============================

def get_lagna_info(datetime_str, latitude, longitude, timezone):
    asc = get_ascendant_info(datetime_str, latitude, longitude, timezone)
    return {
        'lagna': asc['sign'],
        'description': f"Lagna (Ascendant) is in {asc['sign']} at {asc['degree']} degrees"
    }

# ===============================
# 🌌 Nakshatra Info (only)
# ===============================

def get_nakshatra_details(datetime_str, latitude, longitude, timezone):
    info = get_moon_info(datetime_str, latitude, longitude, timezone)
    return {
        'nakshatra': info['nakshatra'],
        'padam': str(info['padam'])
    }

# Optional: Add get_yogas(), get_remedies(), get_dasha_periods(), get_transits() if needed

