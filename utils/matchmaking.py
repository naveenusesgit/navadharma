# utils/match.py


from typing import Dict
from utils.astro_logic import get_nakshatra
import swisseph as swe

# Simplified Guna points for demo
GUNA_POINTS = {
    "Varna": 1,
    "Vashya": 2,
    "Tara": 3,
    "Yoni": 4,
    "Grah Maitri": 5,
    "Gana": 6,
    "Bhakoot": 7,
    "Nadi": 8,
}

def is_manglik(mars_longitude: float, ascendant_house: int) -> bool:
    # Manglik if Mars in 1, 4, 7, 8, 12 from ascendant
    manglik_houses = [(ascendant_house + i - 1) % 12 + 1 for i in [1, 4, 7, 8, 12]]
    mars_house = int((mars_longitude // 30) + 1)
    return mars_house in manglik_houses

def calculate_guna_match(nakshatra1: str, nakshatra2: str) -> Dict:
    # Placeholder match logic - replace with real nakshatra pair checks
    total_score = 24  # Assume partial match
    return {
        "total": 36,
        "scored": total_score,
        "percentage": round((total_score / 36) * 100, 2),
        "remarks": "Good match with scope for deeper compatibility"
    }

def check_match_making(boy_data: Dict, girl_data: Dict) -> Dict:
    # Assume each has longitude for Mars and Ascendant house
    boy_manglik = is_manglik(boy_data["mars"], boy_data["asc_house"])
    girl_manglik = is_manglik(girl_data["mars"], girl_data["asc_house"])

    nak1 = get_nakshatra(boy_data["moon"])
    nak2 = get_nakshatra(girl_data["moon"])

    guna_match = calculate_guna_match(nak1, nak2)

    return {
        "boy": {
            "nakshatra": nak1,
            "manglik": boy_manglik
        },
        "girl": {
            "nakshatra": nak2,
            "manglik": girl_manglik
        },
        "guna": guna_match
    }
