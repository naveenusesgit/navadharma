# utils/weekly_prediction.py

def get_weekly_prediction(rashi: str) -> dict:
    predictions = {
        "aries": "This week, Aries natives may feel energized and motivated to tackle pending tasks. Focus on career and avoid unnecessary arguments.",
        "taurus": "A good week for financial planning. Avoid impulsive spending and focus on long-term goals.",
        "gemini": "Communication is your strength this week. Great time to resolve conflicts and strengthen relationships.",
        "cancer": "You may feel emotional highs and lows. Try to stay grounded and spend time with family.",
        "leo": "Leadership opportunities may arise. Stay humble and let your work speak for itself.",
        "virgo": "Perfect time to declutter and organize. Health matters might need attention.",
        "libra": "Love life takes center stage. Singles may find new connections, couples deepen bonds.",
        "scorpio": "Professional life picks up pace. Stay focused and avoid office politics.",
        "sagittarius": "Travel or learning opportunities could appear. Explore new avenues.",
        "capricorn": "Be cautious in financial dealings. Investments should be made after proper analysis.",
        "aquarius": "Teamwork will bring success. Trust your instincts but remain flexible.",
        "pisces": "Creativity and intuition are heightened. Express yourself and trust your inner voice."
    }

    result = predictions.get(rashi.lower())
    if result:
        return {"rashi": rashi, "weekly_prediction": result}
    else:
        return {"error": f"Unknown rashi: {rashi}. Please provide a valid zodiac sign."}
