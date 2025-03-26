# utils/deity_map.py

from utils.language_utils import translate_output

GOAL_DEITY_MAP = {
    "marriage": {
        "deity": "Parvati & Shiva",
        "mantra": "ॐ नमः शिवाय। (Om Namah Shivaya)",
        "reason": "For harmony, union, and blessings in love and relationships."
    },
    "business": {
        "deity": "Lord Ganesha",
        "mantra": "ॐ गण गणपतये नमः। (Om Gam Ganapataye Namah)",
        "reason": "To remove obstacles and bring prosperity in new ventures."
    },
    "travel": {
        "deity": "Lord Hanuman",
        "mantra": "ॐ हनुमते नमः। (Om Hanumate Namah)",
        "reason": "For protection, strength and safe journeys."
    },
    "education": {
        "deity": "Goddess Saraswati",
        "mantra": "ॐ ऐं सरस्वत्यै नमः। (Om Aim Saraswatyai Namah)",
        "reason": "To enhance focus, wisdom, and success in studies."
    },
    "default": {
        "deity": "Lord Vishnu",
        "mantra": "ॐ नमो भगवते वासुदेवाय। (Om Namo Bhagavate Vasudevaya)",
        "reason": "For general peace, balance and spiritual growth."
    }
}


def get_deity_recommendation(goal_type: str = "default", lang: str = "en") -> dict:
    """
    Returns a deity recommendation for a specific goal type.
    Localizes reason and deity name using optional language.
    """
    recommendation = GOAL_DEITY_MAP.get(goal_type.lower(), GOAL_DEITY_MAP["default"])

    return {
        "deity": translate_output(recommendation["deity"], lang),
        "mantra": recommendation["mantra"],  # Mantras are kept in Devanagari with transliteration
        "reason": translate_output(recommendation["reason"], lang)
    }
