from utils.chart_extractor import extract_chart
from utils.transit import get_daily_global_transits
from datetime import datetime

def get_daily_forecast(birth_date, birth_time, birth_place, target_date):
    # Get full chart
    chart = extract_chart(birth_date, birth_time, birth_place)

    # Get transit info
    transits = get_daily_global_transits(target_date)

    # ⬇️ Sample logic: enhance this with your KP rules
    lagna = chart.get("ascendant")
    moon_sign = chart.get("moonSign")
    nakshatra = chart.get("nakshatra")
    dasha = chart.get("dasha")
    
    message = f"""
    🌟 Forecast for {target_date}
    🔹 Ascendant (Lagna): {lagna}
    🔹 Moon Sign: {moon_sign}
    🔹 Nakshatra: {nakshatra}
    🔹 Dasha Period: {dasha}
    🔹 Transits: {transits.get('highlights')}

    This day is influenced by the emotional karma of {moon_sign} in {nakshatra}.
    Expect energetic alignment that supports clarity in key life areas like relationships or decisions.

    ✅ Best for: Spiritual work, reflection, legal steps, or bold moves (depending on transits)
    ⚠️ Avoid: Emotional overreaction or rash financial decisions
    """

    return message.strip()
