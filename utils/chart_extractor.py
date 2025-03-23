from utils.astro_logic import get_planet_positions, get_nakshatra
from utils.geolocation import get_lat_lon_timezone

def extract_chart(birth_date: str, birth_time: str, birth_place: str):
    lat, lon, timezone = get_lat_lon_timezone(birth_place)

    chart = get_planet_positions(birth_date, birth_time, lat, lon, timezone)

    moon_sign = chart.get("Moon", {}).get("sign", "Unknown")
    moon_deg = chart.get("Moon", {}).get("degree", 0)
    nakshatra_info = get_nakshatra(moon_sign, moon_deg)

    return {
        "moonSign": moon_sign,
        "nakshatra": nakshatra_info.get("nakshatra"),
        "pada": nakshatra_info.get("pada"),
        "ascendant": chart.get("Ascendant", {}).get("sign", "Unknown"),
        "planets": {k: v.get("sign", "Unknown") for k, v in chart.items()}
    }
