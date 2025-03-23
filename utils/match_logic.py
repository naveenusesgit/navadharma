from utils.astro_logic import get_planet_positions, calculate_dasha, get_nakshatra
import swisseph as swe
import datetime

def analyze_compatibility(jd1, jd2):
    planets1 = get_planet_positions(jd1)
    planets2 = get_planet_positions(jd2)

    dasha1 = calculate_dasha(jd1)
    dasha2 = calculate_dasha(jd2)

    nakshatra1 = get_nakshatra(jd1)
    nakshatra2 = get_nakshatra(jd2)

    return {
        "person1": {
            "planets": planets1,
            "nakshatra": nakshatra1,
            "dasha": dasha1
        },
        "person2": {
            "planets": planets2,
            "nakshatra": nakshatra2,
            "dasha": dasha2
        },
        "compatibility_score": "Moderate (sample score)"
    }
