from .summary import generate_summary

def generate_full_kundli_prediction(
    datetime_str,
    place,
    latitude,
    longitude,
    timezone_offset,
    goal="business"
):
    """
    🔮 Combines planetary positions, yogas, dasha, muhurat and remedies
    into a GPT-aware unified summary. Ideal for /generate-kundli or GPT tools.
    """

    summary = generate_summary(
        datetime_str,
        latitude,
        longitude,
        timezone_offset,
        muhurat_type=goal
    )

    return {
        "place": place,
        "datetime": datetime_str,
        "goal": goal,
        "summary": summary["summary"],
        "gpt_prompt": summary["gpt_prompt"],
        "context": summary["context"]
    }
