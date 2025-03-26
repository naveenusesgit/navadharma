from .kundli import PLANET_IDS, parse_datetime
import swisseph as swe

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

def get_yogas(chart_data):
    yogas = []

    asc_house = chart_data["houses"][0]  # 1st house
    kendra_houses = [1, 4, 7, 10]
    house_lookup = {house["house"]: house for house in chart_data["houses"]}
    planet_house_map = {}

    for house in chart_data["houses"]:
        for planet in house["planets"]:
            name = planet.split(" ")[0]
            planet_house_map[name] = house["house"]

    # 🧠 Gajakesari Yoga: Moon + Jupiter in Kendra from Lagna
    moon_house = planet_house_map.get("Moon")
    jup_house = planet_house_map.get("Jupiter")
    if moon_house in kendra_houses and jup_house in kendra_houses:
        yogas.append({
            "name": "Gajakesari Yoga",
            "description": "Moon and Jupiter are in Kendra (1, 4, 7, or 10 houses) from the Lagna. Brings wisdom, fame, and leadership."
        })

    # 🧠 Panch Mahapurusha Yogas
    for planet in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        house_num = planet_house_map.get(planet)
        if not house_num:
            continue
        house_data = house_lookup[house_num]
        if house_num in kendra_houses and (house_data["sign"] in OWN_SIGNS[planet] or house_data["sign"] == EXALTED_SIGNS[planet]):
            yogas.append({
                "name": f"{planet} Mahapurusha Yoga",
                "description": f"{planet} is in a Kendra and in own/exalted sign. Grants power, charisma, and success."
            })

    # 🧠 Budhaditya Yoga
    if "Sun" in planet_house_map and "Mercury" in planet_house_map:
        if planet_house_map["Sun"] == planet_house_map["Mercury"]:
            yogas.append({
                "name": "Budhaditya Yoga",
                "description": "Sun and Mercury are in conjunction. Enhances intelligence, communication, and success in writing/speaking."
            })

    # 🧠 Kemadruma Yoga
    moon_house_num = planet_house_map.get("Moon")
    if moon_house_num:
        before = house_lookup.get(((moon_house_num - 2) % 12) or 12)
        after = house_lookup.get((moon_house_num % 12) + 1)
        if before and after:
            if not before["planets"] and not after["planets"]:
                yogas.append({
                    "name": "Kemadruma Yoga",
                    "description": "No planets in 2nd or 12th from Moon. Indicates loneliness or lack of support unless canceled."
                })

    return yogas
