from utils.language_utils import translate_output
from datetime import datetime

# Optional: SQLAlchemy or custom save function
try:
    from models import RemedyLog  # Example model
    from database import db_session
    USE_DB = True
except ImportError:
    USE_DB = False

# ------------------ Remedies Data ------------------

PLANETARY_REMEDIES = {
    "Sun": {
        "weak": {"remedy": "Offer water to the Sun at sunrise and chant Aditya Hridaya Stotra.", "type": "spiritual", "intensity": 7},
        "combust": {"remedy": "Avoid ego conflicts. Perform Surya Namaskar at sunrise.", "type": "lifestyle", "intensity": 5}
    },
    # ... (same as before for Moon, Mars, etc.)
}

HOUSE_REMEDIES = {
    1: ("Take care of your health. Focus on self-discipline and daily routine.", "lifestyle", 5),
    2: ("Watch your speech. Avoid unnecessary expenses and eat sattvic food.", "lifestyle", 4),
    # ... (same as before)
}

DASHA_NAKSHATRA_REMEDIES = {
    "Shani": {
        "remedy": "Worship Lord Hanuman on Saturdays and donate black sesame seeds.",
        "type": "spiritual",
        "intensity": 8
    },
    "Ashlesha": {
        "remedy": "Practice deep breathing and detox regularly.",
        "type": "lifestyle",
        "intensity": 5
    }
}

# ------------------ Remedy Generator ------------------

def get_remedies(
    afflictions: dict,
    houses: dict,
    lang: str = "en",
    current_dasha: str = None,
    current_nakshatra: str = None,
    priority_by: str = "intensity",  # or "type"
    save_to_db: bool = False
) -> dict:
    """
    Generate, prioritize, group, and optionally store remedies.
    """
    remedy_list = []

    # --- Planetary Afflictions ---
    for planet, issues in afflictions.items():
        for issue in issues:
            details = PLANETARY_REMEDIES.get(planet, {}).get(issue)
            if details:
                entry = {
                    "reason": translate_output(f"{planet} is {issue}", lang),
                    "remedy": translate_output(details["remedy"], lang),
                    "type": details["type"],
                    "intensity": details["intensity"],
                    "timestamp": datetime.utcnow().isoformat()
                }
                remedy_list.append(entry)

    # --- House-based Remedies ---
    for planet, house in houses.items():
        if house in HOUSE_REMEDIES:
            desc, r_type, intensity = HOUSE_REMEDIES[house]
            entry = {
                "reason": translate_output(f"{planet} is in House {house}", lang),
                "remedy": translate_output(desc, lang),
                "type": r_type,
                "intensity": intensity,
                "timestamp": datetime.utcnow().isoformat()
            }
            remedy_list.append(entry)

    # --- Dasha & Nakshatra Remedies ---
    if current_dasha and current_dasha in DASHA_NAKSHATRA_REMEDIES:
        d = DASHA_NAKSHATRA_REMEDIES[current_dasha]
        remedy_list.append({
            "reason": translate_output(f"In {current_dasha} Mahadasha", lang),
            "remedy": translate_output(d["remedy"], lang),
            "type": d["type"],
            "intensity": d["intensity"],
            "timestamp": datetime.utcnow().isoformat()
        })

    if current_nakshatra and current_nakshatra in DASHA_NAKSHATRA_REMEDIES:
        d = DASHA_NAKSHATRA_REMEDIES[current_nakshatra]
        remedy_list.append({
            "reason": translate_output(f"Born in {current_nakshatra} Nakshatra", lang),
            "remedy": translate_output(d["remedy"], lang),
            "type": d["type"],
            "intensity": d["intensity"],
            "timestamp": datetime.utcnow().isoformat()
        })

    # --- Sort Remedies ---
    if priority_by == "intensity":
        remedy_list.sort(key=lambda x: x["intensity"], reverse=True)
    elif priority_by == "type":
        remedy_list.sort(key=lambda x: x["type"])

    # --- Group by Type ---
    grouped = {}
    for r in remedy_list:
        grouped.setdefault(r["type"], []).append(r)

    # --- Optional Save to DB ---
    if save_to_db and USE_DB:
        for r in remedy_list:
            log = RemedyLog(
                reason=r["reason"],
                remedy=r["remedy"],
                remedy_type=r["type"],
                intensity=r["intensity"],
                timestamp=datetime.utcnow()
            )
            db_session.add(log)
        db_session.commit()

    return {
        "all": remedy_list,
        "grouped": grouped
    }
