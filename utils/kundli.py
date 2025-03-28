from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.astro import moon
import math


def get_chart(datetime_str, latitude, longitude, tz_offset):
    """Create a Flatlib chart with Lahiri Ayanamsa"""
    date, time = datetime_str.split('T')
    chart_datetime = Datetime(date, time, tz_offset)
    pos = GeoPos(str(latitude), str(longitude))
    chart = Chart(chart_datetime, pos, IDs=const.LAHIRI)
    return chart


def get_planet_positions(datetime_str, latitude, longitude, tz_offset):
    chart = get_chart(datetime_str, latitude, longitude, tz_offset)
    planet_data = {}

    for body in const.LIST_OBJECTS:
        obj = chart.get(body)
        planet_data[body] = {
            'sign': obj.sign,
            'lon': round(obj.lon, 2),
            'deg': obj.signlon,
            'speed': obj.speed,
            'house': obj.house
        }

    return planet_data


def get_ascendant_info(datetime_str, latitude, longitude, tz_offset):
    chart = get_chart(datetime_str, latitude, longitude, tz_offset)
    asc = chart.get(const.ASC)
    return {
        'sign': asc.sign,
        'degree': asc.signlon
    }


def get_house_mapping(datetime_str, latitude, longitude, tz_offset):
    chart = get_chart(datetime_str, latitude, longitude, tz_offset)
    house_list = []

    for i in range(1, 13):
        house = chart.houses.get(str(i))
        planets = chart.houses.planets_in_house(str(i))
        house_list.append({
            'house': i,
            'sign': house.sign,
            'degree': house.signlon,
            'planets': planets
        })

    return house_list


def get_moon_info(datetime_str, latitude, longitude, tz_offset):
    """Return moon-based info like Rasi (sign), Nakshatra, and Pada"""
    chart = get_chart(datetime_str, latitude, longitude, tz_offset)
    moon_obj = chart.get(const.MOON)
    moon_sign = moon_obj.sign
    nakshatra_deg = moon_obj.lon % 360

    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]

    index = int(nakshatra_deg // (360 / 27))
    nakshatra = nakshatras[index]
    pada = int((nakshatra_deg % (360 / 27)) // (360 / 108)) + 1

    return {
        'moon_sign': moon_sign,
        'nakshatra': nakshatra,
        'padam': pada
    }
