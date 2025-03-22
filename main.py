from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
from utils.pdf_generator import generate_pdf
from utils.astro_logic import (
    get_julian_day, get_planet_positions,
    get_lagna, get_nakshatra, detect_yogas, get_timezone
)
from datetime import datetime
import os

app = FastAPI()


class BirthData(BaseModel):
    date: str  # e.g., '1990-03-21'
    time: str  # e.g., '05:45'
    place: str  # e.g., 'Mumbai, India'
    lat: float
    lon: float
    pdf: Optional[bool] = False


@app.post("/predict-kp")
async def predict_kp(req: BirthData):
    try:
        dt_str = f"{req.date} {req.time}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

        tz = get_timezone(req.place, req.lat, req.lon)
        jd = get_julian_day(dt, tz)

        planets = get_planet_positions(jd, req.lat, req.lon)
        moon_long = planets.get("Moon", 0)
        lagna = get_lagna(jd, req.lat, req.lon)
        nakshatra = get_nakshatra(moon_long)
        yogas = detect_yogas(planets)

        # Stub Dasha logic (to be replaced with real logic soon)
        dasha = {
            "mahadasha": "Venus",
            "antardasha": "Saturn",
            "period": "2023-08-01 to 2026-05-15"
        }

        predictions = {
            "marriage": {
                "likely": True,
                "window": "2024–2025",
                "explanation": f"Moon in {nakshatra}, Yogas: {', '.join(yogas)}",
                "hidden": True
            },
            "career": {
                "change": False,
                "explanation": "10th lord stable",
                "hidden": True
            },
            "health": {
                "summary": "Normal vitality, avoid stress during Mars periods",
                "hidden": True
            }
        }

        data = {
            "date": req.date,
            "time": req.time,
            "place": req.place,
            "lagna": f"Lagna Sign {lagna}",
            "nakshatra": nakshatra,
            "currentDasha": dasha,
            "predictions": predictions,
            "yogas": yogas,
            "remedies": [
                "Recite Vishnu Sahasranama on Fridays",
                "Donate white items on Fridays"
            ]
        }

        # If PDF requested
        if req.pdf:
            pdf_path = generate_pdf(data, filename="Navadharma_Report.pdf")
            return FileResponse(pdf_path, media_type="application/pdf", filename="Navadharma_Report.pdf")

        return JSONResponse(content=data)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
