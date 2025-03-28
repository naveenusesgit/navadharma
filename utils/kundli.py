import re
import hashlib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class RemediesRequest(BaseModel):
    planetaryStatus: Dict[str, List[str]]
    houseMapping: Dict[str, str]
    lang: str = "en"

class RemediesResponse(BaseModel):
    spiritual: List[str]
    mantra: List[str]
    donation: List[str]

@router.post("/remedies", response_model=RemediesResponse)
def get_remedies(req: RemediesRequest):
    planetary_status = req.planetaryStatus
    house_mapping = req.houseMapping
    lang = req.lang

    spiritual = []
    mantras = []
    donations = []

    for planet, afflictions in planetary_status.items():
        if afflictions:
            if planet == "Saturn":
                spiritual.append("Practice patience and seva (selfless service)")
                mantras.append("Om Sham Shanicharaya Namah")
                donations.append("Donate black sesame or black clothes on Saturdays")

            elif planet == "Mars":
                spiritual.append("Engage in discipline and physical fitness")
                mantras.append("Om Mangalaya Namah")
                donations.append("Donate red lentils or jaggery")

            elif planet == "Rahu":
                spiritual.append("Practice detachment and meditation")
                mantras.append("Om Raam Rahave Namah")
                donations.append("Feed lepers or donate dark blue clothes")

            elif planet == "Ketu":
                spiritual.append("Detox and engage in spiritual practices")
                mantras.append("Om Ketave Namah")
                donations.append("Feed dogs or donate blankets")

            elif planet == "Venus":
                spiritual.append("Balance desires and cultivate artistic expression")
                mantras.append("Om Shum Shukraya Namah")
                donations.append("Donate white rice or curd")

    # House-based remedies
    if house_mapping.get("6") in ["Saturn", "Rahu"]:
        donations.append("Donate medicines or volunteer at hospitals")

    if house_mapping.get("8") in ["Ketu", "Mars"]:
        spiritual.append("Practice pranayama and introspection")

    return {
        "spiritual": list(set(spiritual)),
        "mantra": list(set(mantras)),
        "donation": list(set(donations))
    }

def get_yogas(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    positions = {name: swe.calc_ut(jd, pid)[0] for name, pid in PLANET_IDS.items()}
    lagna = swe.houses(jd, latitude, longitude.encode(), b'P')[1][0]
    sun = positions["Sun"]
    moon = positions["Moon"]
    jupiter = positions["Jupiter"]

    yogas = []

    # Sample yoga rules
    if 0 <= abs(sun - moon) <= 12:
        yogas.append({
            "name": "Amavasya Yoga",
            "summary": "Sun and Moon are close together (new moon)",
            "active": True,
            "score": 8.5
        })

    if 180 <= abs(jupiter - moon) <= 200:
        yogas.append({
            "name": "Gajakesari Yoga",
            "summary": "Moon and Jupiter in Kendra from each other",
            "active": True,
            "score": 9.2
        })

    return {
        "yogas": yogas
    }

def get_generate_summary(datetime_str, latitude, longitude, timezone_offset, lang="en", goal="spiritual"):
    nakshatra_data = get_nakshatra_details(datetime_str, latitude, longitude, timezone_offset)
    dasha_data = get_dasha_periods(datetime_str, latitude, longitude, timezone_offset)

    gpt_prompt = (
        f"User is born under Nakshatra {nakshatra_data['nakshatra']} (Pada {nakshatra_data['padam']}), "
        f"and current Mahadasha is {dasha_data['dashas'][0]['mahadasha']}. "
        f"Goal: {goal}. Provide insights and guidance."
    )

    return {
        "summary": f"Nakshatra: {nakshatra_data['nakshatra']}, Dasha: {dasha_data['dashas'][0]['mahadasha']}",
        "gpt_prompt": gpt_prompt,
        "dasha_score": 8.0,
        "context": {
            "nakshatra": nakshatra_data['nakshatra'],
            "padam": nakshatra_data['padam'],
            "mahadasha": dasha_data['dashas'][0]['mahadasha']
        }
    }

def get_numerology(name, dob_str):
    # Calculate basic numbers
    digits = [int(d) for d in re.sub(r'\D', '', dob_str)]
    birth_number = sum(digits[:2]) if len(digits) >= 2 else sum(digits)
    life_path = sum(digits)
    while life_path > 9:
        life_path = sum([int(x) for x in str(life_path)])

    # Name hashing as pseudo numeric encoding
    name_hash = int(hashlib.md5(name.encode()).hexdigest(), 16)
    lucky = name_hash % 9 + 1

    return {
        "life_path_number": life_path,
        "birth_number": birth_number,
        "numerology_message": f"Name vibration aligns with lucky number {lucky}. Life path is {life_path}."
    }

def get_remedies(planetary_status: dict, house_mapping: dict, lang: str = "en"):
    spiritual = []
    mantras = []
    donations = []

    for planet, afflictions in planetary_status.items():
        if afflictions:
            if planet == "Saturn":
                spiritual.append("Practice patience and seva (selfless service)")
                mantras.append("Om Sham Shanicharaya Namah")
                donations.append("Donate black sesame or black clothes on Saturdays")

            elif planet == "Mars":
                spiritual.append("Engage in discipline and physical fitness")
                mantras.append("Om Mangalaya Namah")
                donations.append("Donate red lentils or jaggery")

            elif planet == "Rahu":
                spiritual.append("Practice detachment and meditation")
                mantras.append("Om Raam Rahave Namah")
                donations.append("Feed lepers or donate dark blue clothes")

            elif planet == "Ketu":
                spiritual.append("Detox and engage in spiritual practices")
                mantras.append("Om Ketave Namah")
                donations.append("Feed dogs or donate blankets")

            elif planet == "Venus":
                spiritual.append("Balance desires and cultivate artistic expression")
                mantras.append("Om Shum Shukraya Namah")
                donations.append("Donate white rice or curd")

    # Sample house-based suggestions
    if house_mapping.get("6") in ["Saturn", "Rahu"]:
        donations.append("Donate medicines or volunteer at hospitals")

    if house_mapping.get("8") in ["Ketu", "Mars"]:
        spiritual.append("Practice pranayama and introspection")

    return {
        "spiritual": list(set(spiritual)),
        "mantra": list(set(mantras)),
        "donation": list(set(donations))
    }
