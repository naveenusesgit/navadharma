from .kundli import get_kundli_chart
import re

EXALTED_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra"
}

OWN_SIGNS = {
    "Sun": ["Leo"],
    "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"]
}

DEBILITATED_SIGNS = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries"
}

def parse_degree(planet_str):
    match = re.search(r"\((.*?)°\)", planet_str)
    return float(match.group(1)) if match else 0.0

def get_yogas(datetime_str, latitude, longitude, timezone_offset):
    chart_data = get_kundli_chart(datetime_str, latitude, longitude, timezone_offset)

    yogas = []

    kendra_houses = [1, 4, 7, 10]
    dusthana_houses = [6, 8, 12]

    house_lookup = {house["house"]: house for house in chart_data["houses"]}
    planet_house_map = {}
    planet_sign_map = {}

    for house in chart_data["houses"]:
        for planet in house["planets"]:
            name = planet.split(" ")[0]
            planet_house_map[name] = house["house"]
            planet_sign_map[name] = house["sign"]

    # Gajakesari Yoga
    if "Moon" in planet_house_map and "Jupiter" in planet_house_map:
        if planet_house_map["Moon"] in kendra_houses and planet_house_map["Jupiter"] in kendra_houses:
            yogas.append({
                "name": "Gajakesari Yoga",
                "description": "Moon and Jupiter are in Kendra from Lagna.",
                "score": 8,
                "summary": "You possess strong intelligence and wisdom due to Gajakesari Yoga."
            })

    # Panch Mahapurusha
    for planet in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        hnum = planet_house_map.get(planet)
        if hnum and hnum in kendra_houses:
            sign = planet_sign_map.get(planet)
            if sign in OWN_SIGNS[planet] or sign == EXALTED_SIGNS[planet]:
                yogas.append({
                    "name": f"{planet} Mahapurusha Yoga",
                    "description": f"{planet} is in a Kendra and in own or exalted sign.",
                    "score": 9,
                    "summary": f"{planet} gives strength, charisma, and high success."
                })

    # Budhaditya Yoga
    if planet_house_map.get("Sun") == planet_house_map.get("Mercury"):
        yogas.append({
            "name": "Budhaditya Yoga",
            "description": "Sun and Mercury conjunct in the same house.",
            "score": 7,
            "summary": "You have sharp intellect and communication skills due to Budhaditya Yoga."
        })

    # Kemadruma Yoga
    moon_house = planet_house_map.get("Moon")
    if moon_house:
        before = ((moon_house - 2) % 12) or 12
        after = (moon_house % 12) + 1
        if not house_lookup[before]["planets"] and not house_lookup[after]["planets"]:
            yogas.append({
                "name": "Kemadruma Yoga",
                "description": "No planets in 2nd or 12th from Moon.",
                "score": 3,
                "summary": "Kemadruma Yoga may cause emotional ups and downs or loneliness."
            })

    # Vipreet Raj Yogas: Harsha (6th lord in 6/8/12), Sarala (8th lord), Vimala (12th lord)
    lords = {
        "Harsha": 6,
        "Sarala": 8,
        "Vimala": 12
    }
    for name, house_num in lords.items():
        sign = house_lookup[house_num]["sign"]
        for planet, signs in OWN_SIGNS.items():
            if sign in signs:
                pl_house = planet_house_map.get(planet)
                if pl_house in dusthana_houses:
                    yogas.append({
                        "name": f"{name} Vipreet Raj Yoga",
                        "description": f"Lord of {house_num}th (sign: {sign}) is in a dusthana.",
                        "score": 7,
                        "summary": f"You have {name} Yoga, indicating rise from difficulties and karmic blessings."
                    })

    # Neecha Bhanga Raja Yoga: Debilitated planet gets cancellation
    for planet, deb_sign in DEBILITATED_SIGNS.items():
        if planet_sign_map.get(planet) == deb_sign:
            # Check if another planet in same sign is exalted (e.g. Mars in Cancer, Jupiter in Cancer)
            for other, ex_sign in EXALTED_SIGNS.items():
                if other != planet and planet_sign_map.get(other) == deb_sign:
                    yogas.append({
                        "name": "Neecha Bhanga Raja Yoga",
                        "description": f"{planet} is debilitated in {deb_sign}, but Neecha Bhanga occurs due to {other} being exalted there.",
                        "score": 6,
                        "summary": f"Your debilitated {planet} is cancelled by Neecha Bhanga, giving hidden strength."
                    })

    return yogas
