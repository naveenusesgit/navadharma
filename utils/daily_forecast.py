# utils/daily_forecast.py

from datetime import datetime
import swisseph as swe
from utils.chart_extractor import extract_chart_details
from utils.dasha_calculator import get_current_dasha_periods

def get_panchang_elements(date_obj):
    jd = swe.julday(date_obj.year, date_obj.month, date_obj.day)
    moon_long = swe.lun(jd)[0]
    tithi = int((moon_long % 360) // 12) + 1
    weekday = date_obj.strftime('%A')
    return tithi, weekday

def get_daily_forecast(name, dob, tob, pob, target_date=None):
    chart = extract_chart_details(name, dob, tob, pob)
    dasha_info = get_current_dasha_periods(dob, tob, pob)

    if not target_date:
        target_date = datetime.today().strftime("%Y-%m-%d")

    date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    tithi, weekday = get_panchang_elements(date_obj)

    moon_sign = chart.get("moon_sign", "Unknown Rasi")
    nakshatra = chart.get("nakshatra", "Unknown Nakshatra")
    pada = chart.get("pada", "?")
    lagna = chart.get("lagna", "Unknown")
    dasha = dasha_info.get("current_dasha", "Unknown")
    antar_dasha = dasha_info.get("antar_dasha", "Unknown")

    # 🌙 Transit-Based Trigger (Mock)
    moon_transit_in = moon_sign  # Replace with actual logic later

    forecast_text = (
        f"🗓️ **{target_date} Forecast for {name}**\n"
        f"- **Lagna (Ascendant):** {lagna}\n"
        f"- **Moon Sign (Rasi):** {moon_sign}\n"
        f"- **Nakshatra:** {nakshatra} (Pada {pada})\n"
        f"- **Dasha:** {dasha}\n"
        f"- **Antar Dasha:** {antar_dasha}\n"
        f"- **Panchang:** {weekday}, Tithi #{tithi}\n\n"

        f"✨ **Interpretation:**\n"
        f"Today the Moon transits your **{moon_transit_in}**, which aligns with your natal Moon in {moon_sign}. "
        f"This can bring heightened emotional clarity. The influence of **{antar_dasha} antar-dasha** within "
        f"**{dasha} Mahadasha** supports inner healing and confident communication.\n\n"

        f"💡 **Life Guidance:**\n"
        f"- 🧠 *Mental Focus:* High — good for study or planning.\n"
        f"- ❤️ *Emotional Window:* Open — allow self-expression.\n"
        f"- ⚖️ *Legal/Work:* Consult before decisions, esp. post-noon.\n"
        f"- 👫 *Relationship:* Good day to resolve lingering tensions.\n"
        f"- 🧘 *Spiritual:* Meditation recommended around dusk.\n"
    )

    return {
        "forecast": forecast_text.strip()
    }
