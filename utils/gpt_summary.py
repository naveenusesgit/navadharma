import openai
import os
from dotenv import load_dotenv
from utils.language_utils import translate_output

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_summary(data, lang="en"):
    # Compose summary from structured chart data
    chart_part = ""
    if "planets" in data:
        chart_part += "Here are the planetary positions:\n"
        for planet, details in data["planets"].items():
            chart_part += f"{planet} in sign {details.get('sign', '?')} at degree {details.get('degree', '?')}\n"

    # Add Yoga summaries
    yoga_part = ""
    if "yogas" in data and data["yogas"]:
        yoga_part += "\nImportant Yogas:\n"
        for yoga in data["yogas"]:
            yoga_part += f"- {yoga.get('name', '')}: {yoga.get('summary', '')}\n"

    # Add Remedy summaries
    remedy_part = ""
    if "remedies" in data and data["remedies"]:
        remedy_part += "\nSuggested Remedies:\n"
        for remedy in data["remedies"]:
            remedy_part += f"- {remedy.get('planet', '')}: {remedy.get('summary', '')}\n"

    # Add Transit interpretation (if provided)
    if "transits" in data:
        chart_part += "\nTransit Overview:\n"
        for planet, transit in data["transits"].items():
            chart_part += f"{planet} transiting {transit.get('sign')} in house {transit.get('house')}.\n"

    prompt = f"""
    Provide a short summary interpretation of this chart for the user, covering yogas and remedies if available.
    Keep the tone uplifting and simple to understand for general audience.

    ---
    {chart_part}
    {yoga_part}
    {remedy_part}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a Vedic Astrology assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        english_summary = response.choices[0].message.content.strip()

        # Translate if needed
        translated = translate_output(english_summary, lang)
        return translated

    except Exception as e:
        return f"Error generating summary: {str(e)}"
