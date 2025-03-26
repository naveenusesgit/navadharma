from .kundli import get_dasha_periods
from .interpretations import get_yogas
from .flatlib_strength import get_planetary_strength_flatlib as get_planetary_strength
from .muhurat_finder import find_muhurats
from .deity_map import get_deity_recommendation
from utils.remedies import get_remedies


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

    # 🏠 House Mapping — placeholder until real chart integration
    house_mapping = {
        planet: details.get("house") for planet, details in strengths.items()
        if isinstance(details, dict) and details.get("house") is not None
    }

    # 🪬 Remedies — Localized and contextual
    remedies = get_remedies(planetary_status, house_mapping, lang=lang)

    # 🕉️ Vedic Summary Builder
    summary = f"🕉️ You are currently in **{active_dasha} Mahadasha** (Strength: {dasha_score}/40).\n\n"

    # ✨ Active Yogas
    active_yogas = [y for y in yogas if y.get("active")]
    if active_yogas:
        summary += "✨ Active Yogas:\n"
        for y in active_yogas:
            summary += f"- **{y['name']}**: {y['summary']}\n"
    else:
        summary += "No yogas are currently active in this Dasha.\n"

    # ⚠️ Difficult Yogas
    difficult_yogas = [y for y in yogas if y.get("score", 5) <= 4]
    if difficult_yogas:
        summary += "\n⚠️ Challenges:\n"
        for y in difficult_yogas:
            summary += f"- {y['name']}: {y['summary']}\n"

    # 🪬 Remedies
    if remedies:
        summary += "\n🪬 Recommended Remedies:\n"
        for r in remedies:
            summary += f"- **{r['reason']}**: {r['remedy']}\n"

    # ⏰ Muhurat
    muhurat_result = find_muhurats(datetime_str, latitude, longitude, timezone_offset, muhurat_type)
    muhurat_summary = muhurat_result.get("gpt_summary", "")
    if muhurat_summary:
        summary += f"\n\n🕐 **Today's Muhurat Recommendation**\n{muhurat_summary}"

    # 🙏 Deity Guidance
    deity_info = get_deity_recommendation(muhurat_type)
    if deity_info:
        summary += (
            f"\n\n🙏 **Recommended Deity**: {deity_info['deity']}"
            f"\n📿 **Mantra**: {deity_info['mantra']}"
            f"\n🕉️ {deity_info['reason']}"
        )

    # 🧠 GPT Prompt
    gpt_prompt = f"""
You are a traditional Vedic astrologer. Interpret the following chart summary:

- Active Mahadasha: {active_dasha} (Strength: {dasha_score}/40)
- Active Yogas: {', '.join([y['name'] for y in active_yogas]) or 'None'}
- Difficult Yogas: {', '.join([y['name'] for y in difficult_yogas]) or 'None'}
- Remedies: {', '.join([r['remedy'] for r in remedies]) or 'None'}
- Recommended Deity: {deity_info['deity']} | Mantra: {deity_info['mantra']}
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
        "summary": summary.strip(),
        "gpt_prompt": gpt_prompt.strip(),
        "dasha_score": dasha_score,
        "context": context
    }
