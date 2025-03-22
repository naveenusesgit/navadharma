from datetime import datetime
import swisseph as swe

def get_daily_global_transits(date_str=None):
    """
    Returns planetary transits for the current date or a given date (YYYY-MM-DD)
    based on 0° Aries (universal/global).
    """
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.utcnow()

    jd = swe.julday(date.year, date.month, date.day)
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": swe.MEAN_NODE  # Ketu is opposite Rahu
    }

    transits = {}

    for name, planet in planets.items():
        lon, _ = swe.calc_ut(jd, planet)
        sign_index = int(lon // 30)
        sign_names = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        sign = sign_names[sign_index]
        position = round(lon % 30, 2)

        if name == "Ketu":
            # Ketu is 180° from Rahu
            rahu_lon, _ = swe.calc_ut(jd, swe.MEAN_NODE)
            ketu_lon = (rahu_lon + 180) % 360
            sign_index = int(ketu_lon // 30)
            sign = sign_names[sign_index]
            position = round(ketu_lon % 30, 2)

        transits[name] = {
            "sign": sign,
            "degree": position
        }

    return {
        "date": date.strftime("%Y-%m-%d"),
        "transits": transits
    }
