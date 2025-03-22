import swisseph as swe
import datetime
from utils.helpers import get_planetary_positions, get_house_lords, get_lagna_lord

def analyze_chart(name, dob, tob, pob):
    chart_data = {
        "name": name,
        "dob": dob,
        "tob": tob,
        "pob": pob,
        "planets": get_planetary_positions(dob, tob, pob),
        "house_lords": get_house_lords(dob, tob, pob),
    }
    chart_data["lagna_lord"] = get_lagna_lord(chart_data)
    return chart_data

def calculate_dasha(chart_data):
    return {
        "current": {
            "planet": "Saturn",
            "start": "2020-05-01",
            "end": "2039-05-01",
        },
        "next": {
            "planet": "Mercury",
            "start": "2039-05-01",
            "end": "2056-05-01",
        }
    }

def get_nakshatra_details(chart_data):
    moon = chart_data["planets"].get("Moon", {})
    nakshatra_index = int(moon.get("longitude", 0) // (360 / 27))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    return {
        "nakshatra": nakshatras[nakshatra_index],
        "padam": int(((moon.get("longitude", 0) % (360 / 27)) // 3.33) + 1)
    }

def get_yogas(chart_data):
    yogas = []
    planets = chart_data.get("planets", {})
    lords = chart_data.get("house_lords", {})

    # Gajakesari Yoga
    if 'Moon' in planets and 'Jupiter' in planets:
        if planets['Moon']['house'] in [1, 4, 7, 10] and planets['Jupiter']['house'] in [1, 4, 7, 10]:
            yogas.append({
                "name": "Gajakesari Yoga",
                "description": "Jupiter and Moon in kendra houses. Brings wisdom, respect and leadership.",
                "type": "Raja Yoga",
                "summary": "Gajakesari Yoga gives mental strength and reputation."
            })

    # Chandra-Mangal Yoga
    if planets.get("Moon", {}).get("sign") == planets.get("Mars", {}).get("sign"):
        yogas.append({
            "name": "Chandra-Mangal Yoga",
            "description": "Moon and Mars in same sign. Indicates business success and courage.",
            "type": "Dhana Yoga",
            "summary": "Chandra-Mangal Yoga gives wealth and enterprise."
        })

    # Budha-Aditya Yoga
    if planets.get("Sun", {}).get("sign") == planets.get("Mercury", {}).get("sign"):
        yogas.append({
            "name": "Budha-Aditya Yoga",
            "description": "Sun and Mercury in same sign. Brings intellect, communication power, and leadership.",
            "type": "Raja Yoga",
            "summary": "Budha-Aditya Yoga: intelligence meets leadership."
        })

    # Vipareeta Raja Yoga
    for house in [6, 8, 12]:
        lord = lords.get(house, {}).get("lord")
        if lord:
            lord_house = planets.get(lord, {}).get("house")
            if lord_house in [6, 8, 12]:
                yogas.append({
                    "name": "Vipareeta Raja Yoga",
                    "description": f"Lord of {house} house is placed in a dusthana. Brings unexpected rise after adversity.",
                    "type": "Raja Yoga",
                    "summary": f"Vipareeta Raja Yoga: Triumph through trials. House {house} lord in dusthana."
                })

    return yogas

def get_remedies(chart_data):
    remedies = []
    planets = chart_data.get("planets", {})
    dasha_info = calculate_dasha(chart_data)

    # Afflicted Moon
    moon = planets.get("Moon", {})
    if moon.get("afflicted", False):
        remedies.append({
            "planet": "Moon",
            "issue": "Mental stress or emotional instability",
            "remedy": "Chant Chandra mantra on Mondays, wear white, offer milk to Shiva.",
            "summary": "Balance emotions by chanting Chandra mantra on Mondays and offering milk to Shiva."
        })

    # Weak Lagna Lord
    lagna_lord = chart_data.get("lagna_lord", {})
    if lagna_lord and lagna_lord.get("strength", 100) < 50:
        remedies.append({
            "planet": lagna_lord["name"],
            "issue": "Low confidence or health due to weak Lagna lord",
            "remedy": f"Chant {lagna_lord['name']} mantra daily, practice Surya Namaskar.",
            "summary": f"Boost health and confidence with {lagna_lord['name']} mantra and Surya Namaskar."
        })

    # Dasha remedy
    current_dasha = dasha_info.get("current", {}).get("planet")
    if current_dasha:
        remedies.append({
            "planet": current_dasha,
            "issue": f"Currently in {current_dasha} Mahadasha",
            "remedy": f"Worship {current_dasha}, chant their stotra on their weekday.",
            "summary": f"Pacify effects of {current_dasha} Mahadasha with worship and mantra recitation."
        })

    return remedies
