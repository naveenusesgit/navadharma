# utils/daily_forecast.py

from datetime import datetime
from utils.chart_extractor import extract_chart_details
from utils.dasha_calculator import get_current_dasha_periods

def get_daily_forecast(name, dob, tob, pob, target_date=None):
    """
    Generates a personalized daily forecast based on chart and dasha logic.
    """
    chart = extract_chart_details(name, dob, tob, pob)
    dasha_info = get_current_dasha_periods(dob, tob, pob)

    if not target_date:
        target_date = datetime.today().strftime("%Y-%m-%d")

    # Simple mock logic for now – expand as needed
    forecast = f"Dear {name}, on {target_date}, you are under the influence of {dasha_info.get('current_dasha', 'unknown')}." \
               f" With the Moon in {chart.get('moon_sign', '...')}, this is a good day for introspection and emotional clarity."

    return {
        "forecast": forecast
    }
