import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import math
from fpdf import FPDF
import os

swe.set_ephe_path(".")
geolocator = Nominatim(user_agent="astro-prediction")
tz_finder = TimezoneFinder()

# Get zodiac sign from longitude
def get_planet_sign(lon):
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return signs[int(lon / 30) % 12]

# Get nakshatra
def get_nakshatra(moon_longitude):
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu", "Pushya",
        "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
        "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    index = int(moon_longitude / (360 / 27))
    return nakshatras[index]

def nakshatra_predictions():
    return {
        "Ashwini": "Great day for new beginnings.",
        "Bharani": "Handle responsibilities with care.",
        "Krittika": "Cut through obstacles with clarity.",
        "Rohini": "Favorable for beauty, love, and prosperity.",
        "Mrigashirsha": "Curiosity rules. A good time to explore.",
        "Ardra": "Expect emotional upheavals. Stay steady.",
        "Punarvasu": "Return to what grounds you.",
        "Pushya": "Nourishment and care are highlighted.",
        "Ashlesha": "Stay alert to manipulation or mind-games.",
        "Magha": "Honoring ancestors and tradition helps.",
        "Purva Phalguni": "Pleasure and creativity will flow.",
        "Uttara Phalguni": "Focus on service and long-term growth.",
        "Hasta": "Work with your hands. Productivity high.",
        "Chitra": "Time to beautify or renovate your space.",
        "Swati": "Adaptability wins. Let go of rigidity.",
        "Vishakha": "Targeted effort yields results.",
        "Anuradha": "Friendships and loyalty are key today.",
        "Jyeshtha": "Leadership calls. Be responsible.",
        "Mula": "Root-level changes. Let go of what's stale.",
        "Purva Ashadha": "Take a stand for your beliefs.",
        "Uttara Ashadha": "Build towards legacy and dharma.",
        "Shravana": "Learning, listening and travel favor you.",
        "Dhanishta": "Auspicious for music, rhythm and teamwork.",
        "Shatabhisha": "Healing and mysticism emerge.",
        "Purva Bhadrapada": "Idealism vs realism theme today.",
        "Uttara Bhadrapada": "Spiritual work gains strength.",
        "Revati": "Compassion, charity and intuition rise."
    }

def is_retrograde(jd, planet):
    lon_today = swe.calc_ut(jd, planet)[0][0]
    lon_yesterday = swe.calc_ut(jd - 1, planet)[0][0]
    return lon_today < lon_yesterday

def check_aspects(lon1, lon2):
    diff = abs(lon1 - lon2) % 360
    aspects = {
        "Conjunction": 0,
        "Opposition": 180,
        "Trine": 120,
        "Square": 90,
        "Sextile": 60
    }
    tolerance = 6
    for name, angle in aspects.items():
        if abs(diff - angle) <= tolerance:
            return name
    return None

transit_effects = {
    "Sun": {"positive": ["Aries", "Leo"], "negative": ["Libra"]},
    "Mars": {"positive": ["Aries", "Scorpio"], "negative": ["Cancer"]},
    "Jupiter": {"positive": ["Sagittarius", "Pisces"], "negative": ["Capricorn"]},
    "Saturn": {"positive": ["Capricorn", "Aquarius"], "negative": ["Aries", "Cancer"]}
}

def get_transit_effects(natal_moon_sign, planets):
    effects = []
    for planet, data in planets.items():
        if planet in transit_effects:
            if data["sign"] in transit_effects[planet]["positive"]:
                effects.append(f"{planet} is positively influencing your Moon sign ({natal_moon_sign}).")
            elif data["sign"] in transit_effects[planet]["negative"]:
                effects.append(f"{planet} is challenging your Moon sign ({natal_moon_sign}).")
    return effects

def generate_prediction_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Daily Vedic Astrology Prediction", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Name: {data['name']} | Date: {data['date']}", ln=True)

    pdf.cell(200, 10, txt=f"Moon Sign: {data['moonSign']}", ln=True)
    pdf.cell(200, 10, txt=f"Nakshatra: {data['nakshatra']} - {data['nakshatraMeaning']}", ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Planetary Positions:", ln=True)
    pdf.set_font("Arial", size=11)

    for planet, details in data["planetaryData"].items():
        retro = " (Retrograde)" if details["retrograde"] else ""
        pdf.cell(200, 8, txt=f"{planet}: {details['sign']}{retro}", ln=True)

    if data["aspects"]:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Moon Aspects:", ln=True)
        pdf.set_font("Arial", size=11)
        for a in data["aspects"]:
            pdf.cell(200, 8, txt=a, ln=True)

    if data["transitEffects"]:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Transit Effects:", ln=True)
        pdf.set_font("Arial", size=11)
        for effect in data["transitEffects"]:
            pdf.multi_cell(0, 8, effect)

    pdf.output(filename)

# Primary prediction function with PDF download link
def get_daily_prediction(name: str, date: str):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        jd = swe.julday(dt.year, dt.month, dt.day)

        planet_ids = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mercury": swe.MERCURY,
            "Venus": swe.VENUS,
            "Mars": swe.MARS,
            "Jupiter": swe.JUPITER,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE,
            "Ketu": swe.MEAN_NODE  # shifted 180 degrees
        }

        planet_data = {}
        for pname, pid in planet_ids.items():
            lon = swe.calc_ut(jd, pid)[0][0]
            if pname == "Ketu":
                lon = (lon + 180) % 360
            planet_data[pname] = {
                "longitude": lon,
                "sign": get_planet_sign(lon),
                "retrograde": is_retrograde(jd, pid) if pname not in ["Sun", "Moon", "Rahu", "Ketu"] else False
            }

        moon_sign = planet_data["Moon"]["sign"]
        moon_lon = planet_data["Moon"]["longitude"]
        nakshatra = get_nakshatra(moon_lon)

        aspects = []
        for pname, pdata in planet_data.items():
            if pname != "Moon":
                asp = check_aspects(moon_lon, pdata["longitude"])
                if asp:
                    aspects.append(f"Moon is in {asp} with {pname}")

        transits = get_transit_effects(moon_sign, planet_data)

        result = {
            "name": name,
            "date": date,
            "moonSign": moon_sign,
            "nakshatra": nakshatra,
            "nakshatraMeaning": nakshatra_predictions().get(nakshatra, "Today has unique energies."),
            "planetaryData": planet_data,
            "aspects": aspects,
            "transitEffects": transits
        }

        # Save PDF in static/predictions folder
        os.makedirs("static/predictions", exist_ok=True)
        filename = f"static/predictions/{name}_{date}.pdf"
        generate_prediction_pdf(result, filename)

        result["pdf_url"] = f"/static/predictions/{name}_{date}.pdf"
        return result

    except Exception as e:
        return {"error": str(e)}
