# utils/language_utils.py

import os
import logging

try:
    from openai import OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key) if openai_api_key else None
except ImportError:
    client = None

# Set up logging for errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Optional: File logging
# handler = logging.FileHandler("translation_errors.log")
# logger.addHandler(handler)

# --- Local Phrase Dictionary ---
TRANSLATION_DICT = {
    "en": {
        "Tithi": "Tithi",
        "Nakshatra": "Nakshatra",
        "Yoga": "Yoga",
        "Karana": "Karana",
        "Sunrise": "Sunrise",
        "Sunset": "Sunset",
        "Rahu Kaal": "Rahu Kaal",
        "Abhijit Muhurat": "Abhijit Muhurat",
        "Moon Phase": "Moon Phase",
        "Vedic Month": "Vedic Month",
        "Choghadiya": "Choghadiya",
        "Festivals": "Festivals",
        "Ekadashi Vrat": "Ekadashi Vrat",
        "Chaturthi Vrat": "Chaturthi Vrat",
        "Amavasya": "Amavasya",
        "Purnima": "Purnima",
        "Sankashti": "Sankashti",
        "Pradosham": "Pradosham",
    },
    "hi": {
        "Tithi": "तिथि",
        "Nakshatra": "नक्षत्र",
        "Yoga": "योग",
        "Karana": "करण",
        "Sunrise": "सूर्योदय",
        "Sunset": "सूर्यास्त",
        "Rahu Kaal": "राहु काल",
        "Abhijit Muhurat": "अभिजीत मुहूर्त",
        "Moon Phase": "चंद्रमा की स्थिति",
        "Vedic Month": "वैदिक महीना",
        "Choghadiya": "चौघड़िया",
        "Festivals": "त्योहार",
        "Ekadashi Vrat": "एकादशी व्रत",
        "Chaturthi Vrat": "चतुर्थी व्रत",
        "Amavasya": "अमावस्या",
        "Purnima": "पूर्णिमा",
        "Sankashti": "संकष्टी",
        "Pradosham": "प्रदोष व्रत",
    },
    "ta": {
        "Tithi": "திதி",
        "Nakshatra": "நட்சத்திரம்",
        "Yoga": "யோகா",
        "Karana": "கரணம்",
        "Sunrise": "சூரிய உதயம்",
        "Sunset": "சூரிய அஸ்தமனம்",
        "Rahu Kaal": "ராகு காலம்",
        "Abhijit Muhurat": "அபிஜித் முஹூர்த்தம்",
        "Moon Phase": "சந்திர நிலை",
        "Vedic Month": "வேத மாதம்",
        "Choghadiya": "சோகவாதியா",
        "Festivals": "பண்டிகைகள்",
        "Ekadashi Vrat": "ஏகாதசி விரதம்",
        "Chaturthi Vrat": "சதுர்த்தி விரதம்",
        "Amavasya": "அமாவாசை",
        "Purnima": "பௌர்ணமி",
        "Sankashti": "சங்கடஹர சதுர்த்தி",
        "Pradosham": "பிரதோஷம்",
    },
    # Add "te", "kn", "bn", "mr", etc. as needed
}

# --- Main Translation Function ---
def translate_output(text: str, target_language: str = "en") -> str:
    """
    Translate a known or unknown phrase into the target language using
    local dictionary or OpenAI API if enabled.
    """
    if not text or not isinstance(text, str):
        return text

    # Dictionary translation
    if target_language in TRANSLATION_DICT:
        base_dict = TRANSLATION_DICT.get("en", {})
        if text in base_dict:
            return TRANSLATION_DICT[target_language].get(text, text)

    # OpenAI fallback
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Translate to {target_language}"},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"OpenAI translation error for '{text}' → {target_language}: {e}")
            return text

    # Final fallback
    return text
