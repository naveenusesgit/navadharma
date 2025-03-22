import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(message: str, lang: str = "en", persona: str = "astrologer"):
    system_prompt = {
        "astrologer": {
            "en": "You are a helpful astrologer giving accurate Vedic insights in simple terms.",
            "hi": "आप एक अनुभवी ज्योतिषी हैं जो सरल हिंदी में सटीक वेदिक ज्योतिष उत्तर देते हैं।",
            "ta": "நீங்கள் ஒரு வேத ஜோதிடர், தமிழில் எளிமையான பதில்கள் அளிக்கிறீர்கள்.",
            "te": "మీరు అనుభవజ్ఞుడైన జ్యోతిష్కుడు, తెలుగు లో సులభంగా వివరించండి.",
            "ml": "നിങ്ങൾ ഒരു പ്രായോഗിക ജ്യോതിഷൻ ആണ്, മലയാളത്തിൽ ലളിതമായ ഉത്തരങ്ങൾ നൽകുക.",
            "kn": "ನೀವು ಅನುಭವಜ್ಞ ಜ್ಯೋತಿಷಿ, ಕನ್ನಡದಲ್ಲಿ ಸರಳ ಉತ್ತರಗಳನ್ನು ನೀಡುತ್ತೀರಿ."
        }
    }

    prompt = system_prompt.get(persona, {}).get(lang, system_prompt["astrologer"]["en"])

    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    )
    return chat.choices[0].message.content.strip()
