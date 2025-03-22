from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY", "kp-demo-secret-key-123456")

class KPInput(BaseModel):
    date: str
    time: str
    place: str
    pdf: Optional[bool] = False  # Optional flag to trigger PDF output

@app.get("/")
def read_root():
    return {
        "message": "👋 Welcome to the KP Predictor API (Navadharma Pro)! Use POST /predict-kp to get detailed KP-based Vedic astrology predictions."
    }

@app.post("/predict-kp")
def predict_kp(request: Request, data: KPInput):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer ") or auth.split(" ")[1] != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Mock KP logic – replace with real astrology engine later
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

    # PDF generation coming in part 2
    if data.pdf:
        return {
            "message": "PDF generation in progress",
            "pdf": False,
            "note": "PDF output feature is under construction."
        }

    return predictions
