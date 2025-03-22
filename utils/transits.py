import swisseph as swe
import datetime
import pytz
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.TRUE_NODE  # Ketu will be handled separately as opposite of Rahu
}

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_sign(degree):
    sign = int(degree / 30)
    return ZODIAC_SIGNS[sign]

def get_today_transits():
    today = datetime.datetime.now(pytz.utc)
    jd = swe.julday(today.year, today.month, today.day, today.hour + today.minute / 60.0)
    swe.set_ephe_path(os.getcwd())  # or set to "/usr/share/ephe" if on Linux

    transits = {}
    for planet_name, planet_id in PLANETS.items():
        lon, _lat, _ = swe.calc_ut(jd, planet_id)[0:3]
        if planet_name == "Ketu":
            lon = (swe.calc_ut(jd, swe.MEAN_NODE)[0] + 180) % 360
        transits[planet_name] = {
            "longitude": round(lon, 2),
            "sign": get_sign(lon)
        }

    transits["date"] = today.strftime("%Y-%m-%d %H:%M:%S UTC")
    return transits

def get_gpt_transit_summary(transits, lang="en"):
    prompt = f"""
    Generate a natural-language astrology summary of today’s planetary transits based on the following:

    {transits}

    The tone should be insightful, spiritual, and reader-friendly. Translate to: {lang.upper()}.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Vedic astrologer and spiritual guide."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating GPT summary: {str(e)}"
