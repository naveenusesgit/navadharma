from datetime import datetime
from utils.astro_logic import calculate_dasha

def calculate_ashtakoot_score(name1, dob1, name2, dob2):
    """
    Dummy Ashtakoot matching logic — you can replace this with real calculations.
    For now, returns random-like but structured score based on name length and dob digits.
    """
    score = (len(name1) + len(name2)) % 9 + (int(dob1[-2:]) + int(dob2[-2:])) % 10
    return min(score, 36)

def compare_dashas(dasha1, dasha2):
    if dasha1.get("mahadasha") == dasha2.get("mahadasha"):
        return "✅ Both partners are under the same Mahadasha — karmic alignment is strong."
    else:
        return "⚠️ Partners are in different Mahadashas — understanding and patience will be key."

def get_match_remedies(score, dasha_msg):
    remedies = []

    if score < 18:
        remedies.append("🪔 Perform Navagraha Shanti or Graha Shanti puja to balance cosmic energies.")
        remedies.append("🌸 Offer white flowers to the Moon and chant 'Om Chandraya Namah' on Mondays.")

    if "Different" in dasha_msg:
        remedies.append("📿 Meditate together during sunrise to harmonize emotional cycles.")
        remedies.append("🕉️ Recite Vishnu Sahasranama for mutual understanding.")

    if not remedies:
        remedies.append("💖 Your stars align well! Keep communication open and spiritual practices strong.")

    return remedies

def match_compatibility(p1, p2):
    name1 = p1.get("name", "Partner 1")
    name2 = p2.get("name", "Partner 2")
    dob1 = p1.get("date")
    dob2 = p2.get("date")

    ashta_score = calculate_ashtakoot_score(name1, dob1, name2, dob2)

    # Calculate Dasha
    dasha1 = calculate_dasha(p1.get("date"), p1.get("time"), p1.get("place"))
    dasha2 = calculate_dasha(p2.get("date"), p2.get("time"), p2.get("place"))
    dasha_msg = compare_dashas(dasha1, dasha2)

    remedies = get_match_remedies(ashta_score, dasha_msg)

    return {
        "ashtakootScore": ashta_score,
        "ashtakootOutOf": 36,
        "dashaCompatibility": dasha_msg,
        "partner1": {"name": name1, "dasha": dasha1},
        "partner2": {"name": name2, "dasha": dasha2},
        "remedies": remedies
    }
