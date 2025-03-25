import swisseph as swe
import datetime
from fpdf import FPDF

# Constants
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": -swe.MEAN_NODE,
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Core Calculation Functions

def get_planet_positions(jd, lat, lon, tz):
    positions = {}
    for name, planet_id in PLANETS.items():
        lon_deg, _ = swe.calc_ut(jd, abs(planet_id))
        sign = SIGNS[int(lon_deg[0] // 30)]
        retro = swe.calc_ut(jd, abs(planet_id))[3] < 0  # speed < 0 = retrograde
        positions[name] = {
            "degree": round(lon_deg[0], 2),
            "sign": sign,
            "retrograde": retro
        }
    return positions

def get_lagna_info(jd, lat, lon, tz):
    asc = swe.houses(jd, lat, lon)[0][0]  # Ascendant
    sign = SIGNS[int(asc // 30)]
    return {
        "lagna_degree": round(asc, 2),
        "lagna_sign": sign
    }

def get_dasha_periods(jd, lat, lon, tz):
    return {
        "major_dasha": "Rahu",
        "start": "2020-01-01",
        "end": "2038-01-01",
        "next_dasha": "Jupiter"
    }

def get_nakshatra_details(jd, lat, lon, tz):
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    nakshatra_index = int((moon_pos[0] % 360) / (360 / 27))
    pada = int(((moon_pos[0] % (360 / 27)) / (360 / 108))) + 1
    nakshatra_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra",
        "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
        "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    return {
        "nakshatra": nakshatra_names[nakshatra_index],
        "pada": pada,
        "moon_longitude": round(moon_pos[0], 2)
    }

def get_planetary_aspects(jd, lat, lon, tz):
    aspects = {
        "Mars": ["7th, 8th, and 4th from placement"],
        "Saturn": ["3rd and 10th aspects"],
        "Jupiter": ["5th, 7th, and 9th aspects"]
    }
    return aspects

def get_transit_predictions(jd, lat, lon, tz):
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_sign = SIGNS[int(moon_pos[0] // 30)]
    return {
        "moon_sign": moon_sign,
        "effects": "Heightened intuition, emotional growth. Good time for meditation and reflection."
    }

def get_kundli_chart(jd, lat, lon, tz, divisional_chart="D1"):
    chart = {}
    factor = {"D1": 1, "D9": 9}.get(divisional_chart, 1)
    for name, planet_id in PLANETS.items():
        lon_deg, _ = swe.calc_ut(jd, abs(planet_id))
        div_long = (lon_deg[0] * factor) % 360
        sign = SIGNS[int(div_long // 30)]
        chart[name] = {
            "sign": sign,
            "degree": round(div_long, 2)
        }
    return chart

def generate_kundli_report_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Kundli Report", ln=1, align="C")
    pdf.ln(10)

    for section, details in data.items():
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(200, 10, txt=section.capitalize(), ln=1)
        pdf.set_font("Arial", size=11)
        for key, val in details.items():
            pdf.cell(200, 8, txt=f"{key}: {val}", ln=1)
        pdf.ln(5)

    file_path = "/tmp/kundli_report.pdf"
    pdf.output(file_path)
    return {"status": "PDF generated", "file_path": file_path}

def generate_full_kundli_prediction(jd, lat, lon, tz, place=""):
    return {
        "planet_positions": get_planet_positions(jd, lat, lon, tz),
        "lagna_info": get_lagna_info(jd, lat, lon, tz),
        "dasha": get_dasha_periods(jd, lat, lon, tz),
        "nakshatra": get_nakshatra_details(jd, lat, lon, tz),
        "aspects": get_planetary_aspects(jd, lat, lon, tz),
        "transits": get_transit_predictions(jd, lat, lon, tz),
        "d1_chart": get_kundli_chart(jd, lat, lon, tz, "D1"),
        "d9_chart": get_kundli_chart(jd, lat, lon, tz, "D9"),
        "summary": "Balanced year ahead with strong influence of Mars and Saturn. Good time for long-term planning."
    }

def get_ashtakvarga(jd, lat, lon, tz):
    return {
        "score": {
            "Sun": 25,
            "Moon": 22,
            "Mars": 19,
            "Mercury": 30,
            "Jupiter": 28,
            "Venus": 21,
            "Saturn": 18
        },
        "interpretation": "Higher score planets support stronger outcomes in their dasha periods."
    }

def get_remedies(jd, lat, lon, tz):
    remedies = {
        "Sun": "Recite the Gayatri Mantra daily and offer water to the Sun at sunrise.",
        "Moon": "Wear a pearl on Monday and meditate to improve emotional balance.",
        "Mars": "Donate red lentils on Tuesdays and recite Hanuman Chalisa.",
        "Mercury": "Feed green vegetables to cows on Wednesdays and wear emerald.",
        "Jupiter": "Donate turmeric and yellow sweets on Thursdays. Chant 'Om Gurave Namah'.",
        "Venus": "Help the underprivileged and wear white on Fridays.",
        "Saturn": "Feed crows and donate black sesame seeds on Saturdays.",
        "Rahu": "Chant 'Om Raam Rahave Namah' and wear smoky quartz.",
        "Ketu": "Practice detachment and spiritual reflection. Chant 'Om Ketave Namah'."
    }

    return {
        "remedies": remedies,
        "note": "These are general remedies. Personalized ones require deeper analysis of your chart."
    }

__all__ = [
    "get_planet_positions",
    "get_lagna_info",
    "get_dasha_periods",
    "get_nakshatra_details",
    "get_planetary_aspects",
    "get_transit_predictions",
    "generate_kundli_report_pdf",
    "generate_full_kundli_prediction",
    "get_kundli_chart",
    "get_ashtakvarga",
    "get_remedies"
]
