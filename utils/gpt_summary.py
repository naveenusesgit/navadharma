import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ✅ Load your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_gpt_summary(astro_data: dict) -> str:
    """
    Generates a natural-language summary of the astrology reading using GPT.
    """

    name = astro_data.get("name", "This person")
    lagna = astro_data.get("lagna", "Unknown")
    current_dasha = astro_data.get("currentDasha", {})
    yogas = astro_data.get("yogas", [])
    nakshatras = astro_data.get("nakshatras", {})

    prompt = f"""
You are a learned Vedic astrologer from the Navadharma school of thought.
Provide a 6-8 line summary for the following person based on the data.

Name: {name}
Lagna: {lagna}
Current Mahadasha: {current_dasha.get('mahadasha')}
Antardasha: {current_dasha.get('antardasha')}
Important Yogas: {", ".join(yogas) if yogas else "None"}
Notable Nakshatras: {nakshatras}

Mention health, finance, spiritual growth, and overall energy in this period. Keep it concise and in professional tone.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("GPT Error:", e)
        return "Unable to generate AI summary at this time."
