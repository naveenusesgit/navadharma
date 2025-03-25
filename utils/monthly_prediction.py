# utils/monthly_prediction.py

from datetime import datetime

# Optional: Enhance with real astrological logic in future
def get_monthly_prediction(rashi: str, month: str = None) -> dict:
    # Normalize input
    rashi = rashi.strip().lower()
    month = month.capitalize() if month else datetime.now().strftime("%B")

    # Static monthly prediction map for each Rashi
    predictions = {
        "aries": f"In {month}, Aries natives may experience a boost in confidence and leadership roles. It’s a good time to initiate new ventures, but avoid unnecessary arguments.",
        "taurus": f"{month} brings financial gains and domestic stability for Taurus signs. However, be cautious with overspending and dietary habits.",
        "gemini": f"Communication and travel dominate {month} for Gemini. Short trips may be fruitful, and networking can unlock new opportunities.",
        "cancer": f"{month} urges Cancerians to prioritize emotional wellness. You may feel the need to withdraw and reflect—listen to your instincts.",
        "leo": f"Leo natives shine bright in {month}. Recognition at work is possible. Guard against ego clashes with peers or partners.",
        "virgo": f"{month} supports Virgos in long-term planning. Health matters improve, but focus on routines and time management.",
        "libra": f"For Libras, {month} offers harmony in partnerships and a balanced mental state. Artistic pursuits flourish now.",
        "scorpio": f"{month} brings transformation for Scorpio. Avoid power struggles and focus on introspection. A good month for research or spiritual growth.",
        "sagittarius": f"Sagittarius individuals may see travel or educational success this {month}. Stay committed to personal growth.",
        "capricorn": f"Capricorn sees progress in finances and career during {month}, but should remain grounded and ethical in all dealings.",
        "aquarius": f"{month} helps Aquarians connect with new social circles. Some unexpected opportunities may come from foreign sources.",
        "pisces": f"Pisces may experience increased creativity and emotional depth in {month}. Excellent for writing, art, or meditation.",
    }

    prediction = predictions.get(rashi)
    
    if prediction:
        return {
            "rashi": rashi.capitalize(),
            "month": month,
            "prediction": prediction
        }
    else:
        return {
            "error": f"'{rashi}' is not a recognized Vedic rashi. Please use one of: {', '.join(predictions.keys())}."
        }
