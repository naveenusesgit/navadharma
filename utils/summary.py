from .kundli import get_dasha_periods
from .interpretations import get_yogas
from utils.swiss_strength import get_planetary_strength_swiss as get_planetary_strength
from .muhurat_finder import find_muhurats
from .deity_map import get_deity_recommendation
from utils.remedies import get_remedies
from utils.language_utils import translate_output


def generate_summary(datetime_str, latitude, longitude, timezone_offset, muhurat_type="business", lang="en"):
    # 🔮 Core Calculations
    dasha = get_dasha_periods(datetime_str, latitude, longitude, timezone_offset)
    yogas = get_yogas(datetime_str, latitude, longitude, timezone_offset)
    strengths = get_planetary_strength(datetime_str, latitude, longitude, timezone_offset)

    # 👁️‍🗨️ Extract active Mahadasha
    active_dasha = dasha["dashas"][0]["mahadasha"]
    dasha_score = strengths.get(active_dasha, 20.0)

    # 🧠 Build planetary weakness/affliction map
    planetary_status = {
        planet: details.get("afflictions", [])
        for planet, details in strengths.items()
        if isinstance(details, dict) and details.get("afflictions")
    }

    # 🏠 House Mapping — fallback-safe
    house_mapping = {
        planet: details.get("house", None)
        for planet, details in strengths.items()
        if isinstance(details, dict)
    }

    # 🪬 Remedies — Localized and contextual
    remedies = get_remedies(planetary_status, house_mapping, lang=lang) or []

    # ✨ Yogas
    active_yogas = [y for y in yogas if y.get("active")]
    difficult_yogas = [y for y in yogas if y.get("score", 5) <= 4]

    # ⏰ Muhurat
    muhurat_result = find_muhurats(datetime_str, latitude, longitude, timezone_offset, muhurat_type)
    muhurat_summary = muhurat_result.get("gpt_summary", "")

    # 🙏 Deity
    deity_info = get_deity_recommendation(muhurat_type) or {}
    deity_name = deity_info.get("deity", "Your Ishta Devata")
    deity_mantra = deity_info.get("mantra", "Om Namah Shivaya")
    deity_reason = deity_info.get("reason", "Connect spiritually with this guiding deity.")

    # 📝 Build the English summary
    summary = f"🕉️ You are currently in **{active_dasha} Mahadasha** (Strength: {dasha_score}/40).\n\n"

    if active_yogas:
        summary += "✨ Active Yogas:\n"
        for y in active_yogas:
            summary += f"- **{y['name']}**: {y['summary']}\n"
    else:
        summary += "No yogas are currently active in this Dasha.\n"

    if difficult_yogas:
        summary += "\n⚠️ Challenges:\n"
        for y in difficult_yogas:
            summary += f"- {y['name']}: {y['summary']}\n"

    if remedies:
        summary += "\n🪬 Recommended Remedies:\n"
        for r in remedies:
            summary += f"- **{r['reason']}**: {r['remedy']}\n"

    if muhurat_summary:
        summary += f"\n\n🕐 **Today's Muhurat Recommendation**\n{muhurat_summary}"

    summary += (
        f"\n\n🙏 **Recommended Deity**: {deity_name}"
        f"\n📿 **Mantra**: {deity_mantra}"
        f"\n🕉️ {deity_reason}"
    )

    # 🔠 Translate summary if not in English
    translated_summary = translate_output(summary, target_language=lang)

    # 🧠 GPT Prompt
    gpt_prompt = f"""
You are a traditional Vedic astrologer. Interpret the following chart summary in {lang.upper()}:

- Active Mahadasha: {active_dasha} (Strength: {dasha_score}/40)
- Active Yogas: {', '.join([y['name'] for y in active_yogas]) or 'None'}
- Difficult Yogas: {', '.join([y['name'] for y in difficult_yogas]) or 'None'}
- Remedies: {', '.join([r['remedy'] for r in remedies]) or 'None'}
- Recommended Deity: {deity_name} | Mantra: {deity_mantra}
- Muhurat: {muhurat_summary or 'None'}

Respond in 3–5 sentences using a calm, spiritual, and devotional tone.
""".strip()

    # 🧠 Context for chaining to GPT/PDF/UI
    context = {
        "activeMahadasha": active_dasha,
        "dashaStrength": dasha_score,
        "activeYogas": active_yogas,
        "difficultYogas": difficult_yogas,
        "remedies": remedies,
        "shadbala": strengths,
        "muhurat": muhurat_result,
        "deity": deity_info
    }

    return {
        "summary": translated_summary.strip(),
        "gpt_prompt": gpt_prompt.strip(),
        "dasha_score": dasha_score,
        "context": context
    }
