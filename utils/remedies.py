import os
from utils.gpt_summary import generate_gpt_summary

def get_remedies_from_gpt(astro_context: dict, lang="en"):
    prompt = f"""
    Based on this person's astrological profile:
    - Lagna: {astro_context.get("lagna")}
    - Current Dasha: {astro_context.get("currentDasha", {}).get("mahadasha", "")}
    - Notable Yogas: {', '.join(astro_context.get("yogas", []))}
    - Nakshatras: {', '.join([p.get('nakshatra', '') for p in astro_context.get('planets', []) if 'nakshatra' in p])}

    Suggest 2–3 spiritual or practical remedies they can follow to improve their well-being.

    Write in {lang}. Keep it concise and culturally appropriate.
    """

    return generate_gpt_summary(prompt, lang=lang)
