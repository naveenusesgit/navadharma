from .kundli import get_kundli_chart, get_dasha_periods
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

REMEDY_MAP = {
    "Kemadruma Yoga": "Chant Moon mantras (e.g., Om Chandraya Namah), wear a Pearl, and practice emotional grounding through meditation.",
    "Neecha Bhanga Raja Yoga": "Strengthen the cancelled planet through donations on its weekday, and wear its gemstone with guidance.",
    "Debilitated Planet": "Avoid important decisions during its dasha. Chant the planet's mantra or do fasts (vrat)."
}

def parse_degree(planet_str):
    match = re.search(r"\((.*?)°\)", planet_str)
    return float(match.group(1)) if match else 0.0

def get_yogas(datetime_str, latitude, longitude, timezone_offset):
    chart_data = get_kundli_chart(datetime_str, latitude, longitude, timezone_offset)
    dasha_data = get_dasha_periods(datetime_str, latitude, longitude, timezone_offset)
    active_dasha = dasha_data["dashas"][0]["mahadasha"]

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
                "active": "Jupiter" in active_dasha or "Moon" in active_dasha,
                "summary": "Gajakesari Yoga brings fame, wisdom, and leadership."
            })

    # Panch Mahapurusha Yogas
    for planet in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        hnum = planet_house_map.get(planet)
        if hnum and hnum in kendra_houses:
            sign = planet_sign_map.get(planet)
            if sign in OWN_SIGNS[planet] or sign == EXALTED_SIGNS[planet]:
                yogas.append({
                    "name": f"{planet} Mahapurusha Yoga",
                    "description": f"{planet} in Kendra in own/exalted sign.",
                    "score": 9,
                    "active": planet in active_dasha,
                    "summary": f"{planet} gives success and strength through Mahapurusha Yoga."
                })

    # Budhaditya Yoga
    if planet_house_map.get("Sun") == planet_house_map.get("Mercury"):
        yogas.append({
            "name": "Budhaditya Yoga",
            "description": "Sun and Mercury are conjunct.",
            "score": 7,
            "active": "Sun" in active_dasha or "Mercury" in active_dasha,
            "summary": "Excellent for intelligence, speech, teaching, and writing."
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
                "active": "Moon" in active_dasha,
                "summary": "May bring isolation or emotional fluctuation.",
                "remedy": REMEDY_MAP["Kemadruma Yoga"]
            })

    # Vipreet Raj Yogas
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
                        "description": f"Lord of {house_num}th in dusthana.",
                        "score": 7,
                        "active": planet in active_dasha,
                        "summary": f"{name} Yoga gives rise through adversity and karmic protection."
                    })

    # Neecha Bhanga
    for planet, deb_sign in DEBILITATED_SIGNS.items():
        if planet_sign_map.get(planet) == deb_sign:
            for other, exalted_sign in EXALTED_SIGNS.items():
                if other != planet and planet_sign_map.get(other) == deb_sign:
                    yogas.append({
                        "name": "Neecha Bhanga Raja Yoga",
                        "description": f"{planet} is debilitated in {deb_sign} but cancellation occurs due to exalted {other}.",
                        "score": 6,
                        "active": planet in active_dasha or other in active_dasha,
                        "summary": f"Neecha Bhanga restores the dignity of {planet} and empowers you through humility.",
                        "remedy": REMEDY_MAP["Neecha Bhanga Raja Yoga"]
                    })
            # If no cancellation, suggest remedy
            else:
                yogas.append({
                    "name": f"{planet} Debilitated",
                    "description": f"{planet} is in its debilitation sign ({deb_sign}).",
                    "score": 2,
                    "active": planet in active_dasha,
                    "summary": f"Debilitated {planet} can reduce effectiveness unless strengthened.",
                    "remedy": REMEDY_MAP["Debilitated Planet"]
                })

    return yogas
