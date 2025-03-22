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

# Pydantic Input Schema
class PredictionRequest(BaseModel):
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str
    pdf: Optional[bool] = False

# Get lat/lon from place
def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="navadharma")
    location = geolocator.geocode(place_name)
    if not location:
        return None, None
    return location.latitude, location.longitude

# Calculate Lagna (Ascendant)
def get_lagna(date_str, time_str, lat, lon):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd_ut = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
    swe.set_ephe_path('.')  # Path to ephemeris files if needed
    houses = swe.houses(jd_ut, lat, lon)
    asc_degree = houses[0][0]  # Lagna in degrees

    # Get sign (0=Aries, ..., 11=Pisces)
    sign_index = int(asc_degree / 30)
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return signs[sign_index]

# Main Endpoint
@app.post("/predict-kp")
async def predict_kp(request: PredictionRequest):
    try:
        # ✅ Validate Date
        try:
            datetime.strptime(request.date, "%Y-%m-%d")
        except ValueError:
            return JSONResponse(status_code=400, content={"error": "Invalid date format. Use YYYY-MM-DD"})

        # ✅ Validate Time
        try:
            datetime.strptime(request.time, "%H:%M")
        except ValueError:
            return JSONResponse(status_code=400, content={"error": "Invalid time format. Use HH:MM (24-hour)"})

        # ✅ Validate Place
        if not request.place or len(request.place.strip()) < 2:
            return JSONResponse(status_code=400, content={"error": "Place must be a valid name"})

        # 🔍 Get coordinates
        lat, lon = get_coordinates(request.place)
        if lat is None or lon is None:
            return JSONResponse(status_code=400, content={"error": "Unable to geolocate place"})

        # 🔮 Compute Lagna using swisseph
        lagna_sign = get_lagna(request.date, request.time, lat, lon)

        # ✅ Simulated Prediction Output
        report_data = {
            "date": request.date,
            "time": request.time,
            "place": request.place,
            "lagna": lagna_sign,
            "currentDasha": {
                "mahadasha": "Venus",
                "antardasha": "Saturn",
                "period": "2023-08-01 to 2026-05-15"
            },
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

        # 📄 Return PDF or JSON
        if request.pdf:
            filepath = generate_pdf(report_data, filename="Navadharma_Report.pdf")
            return FileResponse(filepath, filename="Navadharma_Report.pdf", media_type="application/pdf")

        return JSONResponse(content=report_data)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
