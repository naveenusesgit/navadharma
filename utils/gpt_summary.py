import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_gpt_summary(astro_summary: str, language: str = "English") -> str:
    if not astro_summary:
        return "No astrological data provided."

    prompt = f"""
    Based on the following astrological interpretation:

    \"\"\"
    {astro_summary}
    \"\"\"

    Write a personalized summary in {language}. 
    Keep it warm, insightful, and professional.
    Limit to 8-10 sentences. Do not repeat text.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a wise and warm Indian astrologer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating GPT summary: {e}"
