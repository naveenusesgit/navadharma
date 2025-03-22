from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

from utils.pdf_generator import generate_pdf  # 🔗 PDF module

app = FastAPI()

API_KEY = os.getenv("API_KEY", "kp-demo-secret-key-123456")


class KPInput(BaseModel):
    date: str
    time: str
    place: str
    pdf: Optional[bool] = False


@app.get("/")
def read_root():
    return {
        "message": "👋 Welcome to the Navadharma KP Predictor API (Pro)! Use POST /predict-kp to get full predictions or request a downloadable PDF."
    }


@app.post("/predict-kp")
def predict_kp(request: Request, data: KPInput):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer ") or auth.split(" ")[1] != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 🔮 Mock KP logic – replace with real KP calculations
    predictions = {
        "lagna": "Aries",
        "currentDasha": {
            "mahadasha": "Venus",
            "antardasha": "Saturn",
            "period": "2023-08-01 to 2026-05-15"
        },
        "predictions": {
            "marriage": {
                "likely": True,
                "window": "2024–2025",
                "explanation": "Venus is sub-lord of 7th house and active in Dasha"
            },
            "career": {
                "change": False,
                "explanation": "10th lord is stable and unaffected by transits"
            },
            "childbirth": {
                "likely": True,
                "window": "2025–2026",
                "explanation": "Jupiter's transit over 5th house supports conception"
            },
            "health": {
                "risk": "Minor",
                "explanation": "Saturn aspecting lagna may bring fatigue or joint issues"
            },
            "wealth": {
                "gain": True,
                "explanation": "Strong 2nd house lord in own sign"
            },
            "foreignTravel": {
                "possible": True,
                "window": "Late 2024",
                "explanation": "Rahu transit favors foreign movement"
            },
            "spirituality": {
                "active": True,
                "explanation": "Ketu transit over 12th house indicates inner journey"
            },
            "litigation": {
                "chance": False,
                "explanation": "No affliction to 6th or 8th house lords"
            }
        }
    }

    if data.pdf:
        report_data = {
            "date": data.date,
            "time": data.time,
            "place": data.place,
            "predictions": predictions["predictions"]
        }
        filepath = generate_pdf(report_data, filename="Navadharma_Report.pdf")
        return FileResponse(filepath, media_type='application/pdf', filename="Navadharma_Report.pdf")

    return predictions
