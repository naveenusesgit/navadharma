from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import FileResponse, JSONResponse
from utils.pdf_generator import generate_pdf
from datetime import datetime
from geopy.geocoders import Nominatim
import swisseph as swe

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str
    pdf: Optional[bool] = False

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
    "Ketu": swe.TRUE_NODE  # computed as Rahu + 180°
}

DASHA_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Helpers
def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="navadharma")
    location = geolocator.geocode(place_name)
    if not location:
        return None, None
    return location.latitude, location.longitude

def get_lagna(date_str, time_str, lat, lon):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd_ut = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
    swe.set_ephe_path(".")
    houses = swe.houses(jd_ut, lat, lon)
    asc_degree = houses[0][0]
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sign_index = int(asc_degree / 30)
    return signs[sign_index]

def get_planet_positions(date_str, time_str, lat, lon):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd_ut = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
    swe.set_ephe_path(".")
    positions = {}
    for name, planet_id in PLANETS.items():
        lon, _lat, dist, speed = swe.calc_ut(jd_ut, planet_id)
        if name == "Ketu":
            lon = (lon + 180) % 360
        positions[name] = round(lon, 2)
    return positions

def get_current_dasha(date_str, time_str, lat, lon):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd_ut = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
    moon_lon, _, _, _ = swe.calc_ut(jd_ut, swe.MOON)
    
    nakshatra_index = int(moon_lon // (360 / 27))
    dasha_lord = DASHA_SEQUENCE[nakshatra_index % 9]
    dasha_years = DASHA_YEARS[dasha_lord]

    start_year = dt.year
    end_year = start_year + dasha_years
    mahadasha_period = f"{start_year}-01-01 to {end_year}-01-01"

    sub_index = int((moon_lon % (360 / 27)) / ((360 / 27) / 9))
    antardasha = DASHA_SEQUENCE[sub_index % 9]

    return {
        "mahadasha": dasha_lord,
        "antardasha": antardasha,
        "period": mahadasha_period
    }

def get_nakshatra(moon_longitude):
    index = int(moon_longitude // (360 / 27))
    return NAKSHATRAS[index]

def detect_yogas(positions):
    yogas = []

    # Gaja Kesari Yoga: Moon and Jupiter in Kendra (90° multiple)
    moon = positions["Moon"]
    jupiter = positions["Jupiter"]
    if abs(((moon - jupiter) + 360) % 360) % 90 < 15:
        yogas.append("Gaja Kesari Yoga")

    # Raja Yoga: Venus and Jupiter in Kendra
    venus = positions["Venus"]
    if abs(((venus - jupiter) + 360) % 360) % 90 < 15:
        yogas.append("Raja Yoga")

    return yogas

@app.post("/predict-kp")
async def predict_kp(request: PredictionRequest):
    try:
        datetime.strptime(request.date, "%Y-%m-%d")
        datetime.strptime(request.time, "%H:%M")

        if not request.place or len(request.place.strip()) < 2:
            return JSONResponse(status_code=400, content={"error": "Place is required."})

        lat, lon = get_coordinates(request.place)
        if lat is None:
            return JSONResponse(status_code=400, content={"error": "Could not resolve location."})

        lagna_sign = get_lagna(request.date, request.time, lat, lon)
        planets = get_planet_positions(request.date, request.time, lat, lon)
        dasha_info = get_current_dasha(request.date, request.time, lat, lon)
        moon_lon = planets["Moon"]
        nakshatra_name = get_nakshatra(moon_lon)
        yogas = detect_yogas(planets)

        report_data = {
            "date": request.date,
            "time": request.time,
            "place": request.place,
            "lagna": lagna_sign,
            "nakshatra": nakshatra_name,
            "yogas": yogas,
            "planetaryPositions": planets,
            "currentDasha": dasha_info,
            "predictions": {
                "marriage": {
                    "likely": True,
                    "window": "2024–2025",
                    "explanation": "Venus is sub-lord of 7th house and active in Dasha",
                    "hidden": True
                },
                "career": {
                    "change": False,
                    "explanation": "10th lord is stable and unaffected by transit"
                },
                "health": {
                    "summary": "Stable energy seen through Moon placement",
                    "hidden": True
                },
                "finance": {
                    "summary": "Steady flow expected; Jupiter aspect supports gains",
                    "hidden": True
                }
            }
        }

        if request.pdf:
            filepath = generate_pdf(report_data, filename="Navadharma_Report.pdf")
            return FileResponse(filepath, filename="Navadharma_Report.pdf", media_type="application/pdf")

        return JSONResponse(content=report_data)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
