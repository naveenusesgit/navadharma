import swisseph as swe
from datetime import datetime
from utils.dasha_logic import get_dasha_periods
from utils.nakshatra import get_nakshatra
from utils.yogas import detect_yogas
from utils.remedies import suggest_remedies
from utils.chart_utils import get_coordinates, get_timezone_offset


def analyze_chart(birth_details: dict) -> dict:
    date_str = birth_details.get("date")
    time_str = birth_details.get("time")
    place = birth_details.get("place")
    language = birth_details.get("language", "en")

    # Parse datetime
    birth_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

    # Get coordinates and timezone
    lat, lon = get_coordinates(place)
    tz_offset = get_timezone_offset(lat, lon, birth_datetime)

    # Adjust datetime to UTC for swisseph
    utc_datetime = birth_datetime - tz_offset

    jd_ut = swe.julday(utc_datetime.year, utc_datetime.month, utc_datetime.day,
                       utc_datetime.hour + utc_datetime.minute / 60.0)

    # Get planetary positions
    planet_positions = {}
    planet_names = {
        swe.SUN: "Sun", swe.MOON: "Moon", swe.MERCURY: "Mercury", swe.VENUS: "Venus",
        swe.MARS: "Mars", swe.JUPITER: "Jupiter", swe.SATURN: "Saturn",
        swe.RAHU: "Rahu", swe.KETU: "Ketu"
    }

    for planet, name in planet_names.items():
        lon, _, _, _, _, _ = swe.calc_ut(jd_ut, planet)
        nakshatra_info = get_nakshatra(lon)
        planet_positions[name] = {
            "longitude": lon,
            "nakshatra": nakshatra_info.get("name"),
            "pada": nakshatra_info.get("pada")
        }

    # Dasha logic (Vimshottari)
    dashas = get_dasha_periods(jd_ut, planet_positions["Moon"]["longitude"])

    # Yogas
    yogas = detect_yogas(planet_positions)

    # Remedies
    remedies = suggest_remedies(yogas, dashas)

    return {
        "planets": planet_positions,
        "nakshatras": {k: v["nakshatra"] for k, v in planet_positions.items()},
        "yogas": yogas,
        "dashas": dashas,
        "remedies": remedies,
        "language": language
    }
