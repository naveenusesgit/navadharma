# utils/language_utils.py

import os

try:
    from openai import OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key) if openai_api_key else None
except ImportError:
    client = None

# Basic local dictionary for fast predefined translations (extend as needed)
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
    },
    "te": {
        "Tithi": "తిథి",
        "Nakshatra": "నక్షత్రం",
        "Yoga": "యోగ",
        "Karana": "కరణం",
        "Sunrise": "సూర్యోదయం",
        "Sunset": "సూర్యాస్తమయం",
        "Rahu Kaal": "రాహు కాలం",
        "Abhijit Muhurat": "అభిజిత్ ముహూర్తం",
    },
    "kn": {
        "Tithi": "ತಿಥಿ",
        "Nakshatra": "ನಕ್ಷತ್ರ",
        "Yoga": "ಯೋಗ",
        "Karana": "ಕರಣ",
        "Sunrise": "ಸೂರ್ಯೋದಯ",
        "Sunset": "ಸೂರ್ಯಾಸ್ತ",
        "Rahu Kaal": "ರಾಹು ಕಾಲ",
        "Abhijit Muhurat": "ಅಭಿಜಿತ್ ಮುಹೂರ್ತ",
    }
}


def translate_output(text: str, target_language: str = "en") -> str:
    """
    Translate a given string to the target language using a predefined dictionary,
    or fall back to OpenAI translation if available.
    """
    # Try dictionary translation (for known phrases)
    if target_language in TRANSLATION_DICT and text in TRANSLATION_DICT["en"]:
        return TRANSLATION_DICT[target_language].get(text, text)

    # Fallback: OpenAI translation if key & client is set
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Translate this to {target_language}"},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Translation Error] {e}")
            return text

    # Final fallback - return original text
    return text
