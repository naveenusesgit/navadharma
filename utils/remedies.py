# utils/remedies.py

from utils.language_utils import translate_output

# -------------------- Remedy Dictionaries --------------------

PLANETARY_REMEDIES = {
    "Sun": {
        "weak": "Offer water to the Sun at sunrise and chant Aditya Hridaya Stotra.",
        "combust": "Avoid ego conflicts. Perform Surya Namaskar at sunrise regularly."
    },
    "Moon": {
        "weak": "Chant Chandra Beej Mantra and wear white on Mondays.",
        "afflicted": "Meditate and spend time near water bodies. Donate white items."
    },
    "Mars": {
        "weak": "Chant Hanuman Chalisa daily and avoid anger.",
        "afflicted": "Donate red lentils on Tuesdays. Worship Lord Hanuman."
    },
    "Mercury": {
        "weak": "Recite Vishnu Sahasranama. Wear green clothes on Wednesdays.",
        "afflicted": "Avoid arguments. Offer green moong daal to the needy."
    },
    "Jupiter": {
        "weak": "Chant Guru Beej Mantra and offer yellow sweets on Thursdays.",
        "afflicted": "Help teachers or elders. Donate yellow items like turmeric."
    },
    "Venus": {
        "weak": "Chant Shukra Mantra and offer white flowers to Goddess Lakshmi.",
        "afflicted": "Avoid overindulgence. Donate white clothes on Fridays."
    },
    "Saturn": {
        "weak": "Chant Shani Chalisa and visit Shani temple on Saturdays.",
        "afflicted": "Donate black items, mustard oil, or sesame seeds."
    },
    "Rahu": {
        "afflicted": "Chant Rahu Beej Mantra. Feed birds and avoid deception.",
    },
    "Ketu": {
        "afflicted": "Chant Ketu Beej Mantra. Light a camphor lamp daily."
    }
}

HOUSE_REMEDIES = {
    1: "Take care of your health. Focus on self-discipline and daily routine.",
    2: "Watch your speech. Avoid unnecessary expenses and eat sattvic food.",
    3: "Engage in courageous action. Support siblings and short travel planning.",
    4: "Take care of your mother. Avoid stress at home. Do regular meditation.",
    5: "Be disciplined in love and studies. Worship Lord Ganesha.",
    6: "Control debts and enemies. Serve the poor. Avoid overworking.",
    7: "Be mindful in relationships. Avoid legal entanglements.",
    8: "Practice spiritual sadhana. Avoid secrets or manipulative behavior.",
    9: "Seek blessings of gurus. Donate regularly.",
    10: "Be ethical in career. Avoid shortcuts.",
    11: "Keep your goals realistic. Avoid greed.",
    12: "Do charity, mantra japa, and spiritual work."
}

# -------------------- Main Remedy Generator --------------------

def get_remedies(afflictions: dict, houses: dict, lang: str = "en") -> list:
    """
    Generate contextual remedies based on planetary afflictions and house placements.
    Localizes remedies using utils.language_utils.translate_output()
    """
    remedies = []

    for planet, issues in afflictions.items():
        for issue in issues:
            remedy = PLANETARY_REMEDIES.get(planet, {}).get(issue)
            if remedy:
                remedies.append({
                    "reason": translate_output(f"{planet} is {issue}", lang),
                    "remedy": translate_output(remedy, lang)
                })

    for planet, house in houses.items():
        if house in HOUSE_REMEDIES:
            remedies.append({
                "reason": translate_output(f"{planet} is in House {house}", lang),
                "remedy": translate_output(HOUSE_REMEDIES[house], lang)
            })

    return remedies
