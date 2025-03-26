from .kundli import get_dasha_periods
from .interpretations import get_yogas
from .remedies import get_remedies
from .flatlib_strength import get_planetary_strength_flatlib as get_planetary_strength

def generate_summary(datetime_str, latitude, longitude, timezone_offset):
    dasha = get_dasha_periods(datetime_str, latitude, longitude, timezone_offset)
    yogas = get_yogas(datetime_str, latitude, longitude, timezone_offset)
    remedies = get_remedies(datetime_str, latitude, longitude, timezone_offset)
    strengths = get_planetary_strength(datetime_str, latitude, longitude, timezone_offset)

    active_dasha = dasha["dashas"][0]["mahadasha"]
    dasha_score = strengths.get(active_dasha, 20.0)

    # Human-readable narrative
    summary = f"🕉️ You are currently in **{active_dasha} Mahadasha** (Strength: {dasha_score}/40).\n\n"

    active_yogas = [y for y in yogas if y.get("active")]
    if active_yogas:
        summary += "✨ Active Yogas:\n"
        for y in active_yogas:
            summary += f"- **{y['name']}**: {y['summary']}\n"
    else:
        summary += "No yogas are currently active in this Dasha.\n"

    difficult_yogas = [y for y in yogas if y.get("score", 5) <= 4]
    if difficult_yogas:
        summary += "\n⚠️ Challenges:\n"
        for y in difficult_yogas:
            summary += f"- {y['name']}: {y['summary']}\n"

    if remedies:
        summary += "\n🪬 Recommended Remedies:\n"
        for r in remedies:
            summary += f"- **{r['reason']}**: {r['remedy']}\n"

    # ✨ GPT prompt (copy-paste into ChatGPT or use in Action)
    gpt_prompt = f"""
You are a traditional Vedic astrologer. Interpret the following:

- Active Mahadasha: {active_dasha} (Strength: {dasha_score}/40)
- Active Yogas: {', '.join([y['name'] for y in active_yogas]) or 'None'}
- Difficult Yogas: {', '.join([y['name'] for y in difficult_yogas]) or 'None'}
- Remedies: {', '.join([r['remedy'] for r in remedies]) or 'None'}

Generate a 3–5 sentence prediction. Speak in a calm, devotional tone.
"""

    # 🔍 Structured context (for agents / LangChain / UI display)
    context = {
        "activeMahadasha": active_dasha,
        "dashaStrength": dasha_score,
        "activeYogas": active_yogas,
        "difficultYogas": difficult_yogas,
        "remedies": remedies
    }

    return {
        "summary": summary.strip(),
        "gpt_prompt": gpt_prompt.strip(),
        "dasha_score": dasha_score,
        "context": context
    }
