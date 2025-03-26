from utils.language_utils import translate_output
from datetime import datetime
import os
import logging

# Optional: DB
try:
    from models import RemedyLog
    from database import db_session
    USE_DB = True
except ImportError:
    USE_DB = False

# ✅ OpenAI Setup
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    use_gpt = True
except ImportError:
    use_gpt = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ------------------ Remedies Data (trimmed for brevity) ------------------

PLANETARY_REMEDIES = {
    "Sun": {
        "weak": {"remedy": "Offer water to the Sun at sunrise and chant Aditya Hridaya Stotra.", "type": "spiritual", "intensity": 7},
        "combust": {"remedy": "Avoid ego conflicts. Perform Surya Namaskar at sunrise.", "type": "lifestyle", "intensity": 5}
    },
    # ... others
}

HOUSE_REMEDIES = {
    1: ("Take care of your health. Focus on self-discipline and daily routine.", "lifestyle", 5),
    # ...
}

DASHA_NAKSHATRA_REMEDIES = {
    "Shani": {
        "remedy": "Worship Lord Hanuman on Saturdays and donate black sesame seeds.",
        "type": "spiritual",
        "intensity": 8
    },
    # ...
}

# ------------------ GPT Explanation Helper ------------------

def generate_gpt_explanation(reason, remedy, lang="en"):
    if not use_gpt:
        return None
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4
            messages=[
                {
                    "role": "system",
                    "content": f"You are a Vedic astrologer. Explain remedies to a user in {lang} in a simple and devotional tone."
                },
                {
                    "role": "user",
                    "content": f"Reason: {reason}\nRemedy: {remedy}\n\nExplain why this remedy is helpful."
                }
            ],
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"GPT explanation error: {e}")
        return None

# ------------------ Remedy Generator ------------------

def get_remedies(
    afflictions: dict,
    houses: dict,
    lang: str = "en",
    current_dasha: str = None,
    current_nakshatra: str = None,
    priority_by: str = "intensity",  # or "type"
    save_to_db: bool = False,
    explain_with_gpt: bool = False
) -> dict:
    remedy_list = []

    # --- Planetary Afflictions ---
    for planet, issues in afflictions.items():
        for issue in issues:
            details = PLANETARY_REMEDIES.get(planet, {}).get(issue)
            if details:
                reason = translate_output(f"{planet} is {issue}", lang)
                remedy = translate_output(details["remedy"], lang)
                explanation = generate_gpt_explanation(reason, remedy, lang) if explain_with_gpt else None

                remedy_list.append({
                    "reason": reason,
                    "remedy": remedy,
                    "type": details["type"],
                    "intensity": details["intensity"],
                    "timestamp": datetime.utcnow().isoformat(),
                    "gpt_summary": explanation
                })

    # --- House Remedies ---
    for planet, house in houses.items():
        if house in HOUSE_REMEDIES:
            desc, r_type, intensity = HOUSE_REMEDIES[house]
            reason = translate_output(f"{planet} is in House {house}", lang)
            remedy = translate_output(desc, lang)
            explanation = generate_gpt_explanation(reason, remedy, lang) if explain_with_gpt else None

            remedy_list.append({
                "reason": reason,
                "remedy": remedy,
                "type": r_type,
                "intensity": intensity,
                "timestamp": datetime.utcnow().isoformat(),
                "gpt_summary": explanation
            })

    # --- Dasha/Nakshatra ---
    for key, label in [(current_dasha, "Mahadasha"), (current_nakshatra, "Nakshatra")]:
        if key and key in DASHA_NAKSHATRA_REMEDIES:
            d = DASHA_NAKSHATRA_REMEDIES[key]
            reason = translate_output(f"In {key} {label}", lang)
            remedy = translate_output(d["remedy"], lang)
            explanation = generate_gpt_explanation(reason, remedy, lang) if explain_with_gpt else None

            remedy_list.append({
                "reason": reason,
                "remedy": remedy,
                "type": d["type"],
                "intensity": d["intensity"],
                "timestamp": datetime.utcnow().isoformat(),
                "gpt_summary": explanation
            })

    # --- Sort & Group ---
    if priority_by == "intensity":
        remedy_list.sort(key=lambda x: x["intensity"], reverse=True)
    elif priority_by == "type":
        remedy_list.sort(key=lambda x: x["type"])

    grouped = {}
    for r in remedy_list:
        grouped.setdefault(r["type"], []).append(r)

    # --- Save to DB if configured ---
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
