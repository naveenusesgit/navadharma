from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

from typing import Dict, Any
import math

# Define list of planets (as flatlib has no PLANETS constant)
PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS,
    const.MARS, const.JUPITER, const.SATURN,
    const.NORTH_NODE, const.SOUTH_NODE
]


def get_kundli_details(datetime_str: str, latitude: float, longitude: float, timezone: float) -> Dict[str, Any]:
    dt = Datetime(datetime_str, tz=timezone)
    pos = GeoPos(latitude, longitude)
    chart = Chart(dt, pos, hsys=const.HOUSES_WHOLE_SIGN)

    kundli = {}

    # Ascendant (Lagna)
    asc = chart.get(const.ASC)
    kundli["ascendant"] = {
        "sign": asc.sign,
        "degree": round(asc.lon, 2)
    }

    # Moon Rasi and Nakshatra
    moon = chart.get(const.MOON)
    kundli["moon"] = {
        "sign": moon.sign,
        "degree": round(moon.lon, 2),
        "nakshatra": get_nakshatra(moon.lon),
        "padam": get_padam(moon.lon)
    }

    # All planetary positions
    kundli["planet_positions"] = {}
    for planet in PLANETS:
        obj = chart.get(planet)
        kundli["planet_positions"][planet] = {
            "sign": obj.sign,
            "degree": round(obj.lon, 2),
            "house": obj.house
        }

    # House mapping
    kundli["houses"] = []
    for i in range(1, 13):
        house = chart.houses[i - 1]
        kundli["houses"].append({
            "house": i,
            "sign": house.sign,
            "start_degree": round(house.start, 2)
        })

    return kundli


# Nakshatra Calculation (27 divisions of 13°20')
def get_nakshatra(moon_longitude: float) -> str:
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
        "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    index = int(moon_longitude // (13 + 1 / 3)) % 27
    return nakshatras[index]


# Pada Calculation (Each Nakshatra has 4 padas of 3°20')
def get_padam(moon_longitude: float) -> str:
    pada_num = int((moon_longitude % (13 + 1 / 3)) // (3 + 1 / 3)) + 1
    return str(pada_num)
