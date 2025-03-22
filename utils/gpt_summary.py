from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_summary(astro_data, language="English"):
    prompt = f"""
You are a Vedic astrologer. Based on the following astrological data, write a short prediction summary in {language}.
Make it spiritual, compassionate, and insightful. End with a blessing.

Astrological Data:
{astro_data}

Respond only in {language}.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a wise Vedic astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
