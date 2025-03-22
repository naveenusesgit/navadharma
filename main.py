from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from geopy.geocoders import Nominatim
from utils.pdf_generator import generate_pdf
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
    date: str
    time: str
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
    "Ketu": swe.TRUE_NODE
}

DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Helper functions
def get_coordinates(place):
    geolocator = Nominatim(user_agent="navadharma")
    loc = geolocator.geocode(place)
    return (loc.latitude, loc.longitude) if loc else (None, None)

def get_lagna(jd, lat, lon):
    houses = swe.houses(jd, lat, lon)
    asc_deg = houses[0][0]
    sign = SIGNS[int(asc_deg // 30)]
    return sign, asc_deg

def get_planet_positions(jd):
    swe.set_ephe_path(".")
    positions = {}
    for name, pid in PLANETS.items():
        lon, _, _, _ = swe.calc_ut(jd, pid)
        if name == "Ketu":
            lon = (lon + 180) % 360
        positions[name] = round(lon, 2)
    return positions

def get_current_dasha(jd, moon_lon, date):
    nak_index = int(moon_lon // (360 / 27))
    dasha_lord = DASHA_SEQUENCE[nak_index % 9]
    sub_index = int((moon_lon % (360 / 27)) // ((360 / 27) / 9))
    antardasha = DASHA_SEQUENCE[sub_index % 9]
    years = DASHA_YEARS[dasha_lord]
    start = datetime.strptime(date, "%Y-%m-%d").year
    return {
        "mahadasha": dasha_lord,
        "antardasha": antardasha,
        "period": f"{start}-01-01 to {start+years}-01-01"
    }

def get_nakshatra(moon_lon):
    index = int(moon_lon // (360 / 27))
    return NAKSHATRAS[index]

def detect_yogas(pos):
    yogas = []
    if abs(((pos["Moon"] - pos["Jupiter"] + 360) % 360) % 90) < 15:
        yogas.append("Gaja Kesari Yoga")
    if abs(((pos["Venus"] - pos["Jupiter"] + 360) % 360) % 90) < 15:
        yogas.append("Raja Yoga")
    return yogas

def get_navamsa_sign(lon):
    sign_index = int(lon // 30)
    pada = int((lon % 30) // (30 / 9))
    if sign_index % 2 == 0:
        navamsa_index = (sign_index * 9 + pada) % 12
    else:
        navamsa_index = (sign_index * 9 + (8 - pada)) % 12
    return SIGNS[navamsa_index]

def get_planet_houses(positions, asc_deg):
    houses = {}
    for planet, lon in positions.items():
        diff = (lon - asc_deg + 360) % 360
        house = int(diff // 30) + 1
        houses[planet] = house
    return houses

@app.post("/predict-kp")
async def predict_kp(req: PredictionRequest):
    try:
        datetime.strptime(req.date, "%Y-%m-%d")
        datetime.strptime(req.time, "%H:%M")
        if not req.place: return JSONResponse(status_code=400, content={"error": "Place required"})
        
        lat, lon = get_coordinates(req.place)
        if lat is None: return JSONResponse(status_code=400, content={"error": "Place not found"})

        dt = datetime.strptime(f"{req.date} {req.time}", "%Y-%m-%d %H:%M")
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
        lagna, asc_deg = get_lagna(jd, lat, lon)
        positions = get_planet_positions(jd)
        moon_lon = positions["Moon"]
        dasha = get_current_dasha(jd, moon_lon, req.date)
        nakshatra = get_nakshatra(moon_lon)
        yogas = detect_yogas(positions)
        navamsa_chart = {planet: get_navamsa_sign(lon) for planet, lon in positions.items()}
        houses = get_planet_houses(positions, asc_deg)

        report_data = {
            "date": req.date,
            "time": req.time,
            "place": req.place,
            "lagna": lagna,
            "nakshatra": nakshatra,
            "yogas": yogas,
            "planetaryPositions": positions,
            "navamsaChart": navamsa_chart,
            "planetHouses": houses,
            "currentDasha": dasha,
            "predictions": {
                "marriage": {
                    "likely": True,
                    "window": "2024–2025",
                    "explanation": "Venus rules 7th and is active in Dasha",
                    "hidden": True
                },
                "career": {
                    "change": False,
                    "explanation": "10th house stable with no malefic influence"
                }
            }
        }

        if req.pdf:
            path = generate_pdf(report_data, filename="Navadharma_Report.pdf")
            return FileResponse(path, filename="Navadharma_Report.pdf", media_type="application/pdf")
        return JSONResponse(content=report_data)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
