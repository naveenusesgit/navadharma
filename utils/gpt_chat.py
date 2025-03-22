import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chat_sessions = {}

def chat_with_gpt(message: str, session_id: str, lang: str = "en", persona: str = "astrologer"):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    system_prompts = {
        "astrologer": {
            "en": "You are a wise Vedic astrologer...",
            "hi": "आप एक अनुभवी वैदिक ज्योतिषी हैं...",
            "ta": "நீங்கள் ஒரு ஞானமிக்க வேத ஜோதிடர்...",
            "te": "మీరు జ్ఞానమయిన జ్యోతిష్యుడు...",
            "kn": "ನೀವು ಜ್ಞಾನಿಯಾದ ಜ್ಯೋತಿಷ್ಯ...",
            "ml": "നീങ്ങെ ഒരു പ്രഗത്ഭനായ ജ്യോതിഷിയാണ്..."
        }
    }

    system = {
        "role": "system",
        "content": system_prompts.get(persona, {}).get(lang, system_prompts["astrologer"]["en"])
    }

    chat_sessions[session_id].append({"role": "user", "content": message})
    messages = [system] + chat_sessions[session_id][-10:]

    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = chat.choices[0].message.content.strip()
    chat_sessions[session_id].append({"role": "assistant", "content": reply})
    return reply
